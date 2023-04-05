"""
This is utility module which can be used to limit requests rate globally (from multiple sessions, threads and processes)
To enable ratelimiting for all requests sent from vmanage-client in your application:
>>> from vmngclient.utils.ratelimit import ratelimit, on_request_throttle
>>> ratelimit(max_requests_per_second=100)
>>> vManageSession.on_request_hook = on_request_throttle
>>> vManageAuth.on_request_hook = on_request_throttle
Each unique host ip will have its own RateLimiter (host ip is obtained automatically from request url)

According to SD-WAN documentation responses are being rate-limited:
https://developer.cisco.com/docs/sdwan/#!browsing-returned-results-sorting-results-filtering-results-and-rate-limits/rate-limits-on-results
https://developer.cisco.com/docs/sdwan/#!bulk-api
This does not mean that rate-limiting in client is required,
but application can benefit from increased stability when implemented (not overloading vManage)
"""

import logging
import pickle
import time
from ipaddress import IPv4Address, IPv6Address, ip_address
from math import ceil
from multiprocessing import current_process
from multiprocessing.shared_memory import SharedMemory
from pathlib import Path
from socket import gaierror, gethostbyaddr, herror
from typing import Dict, Union

from oslo_concurrency import lockutils
from urllib3.exceptions import LocationParseError, LocationValueError
from urllib3.util import parse_url

SHARED_MEM_DSIZE = 2**16
SHARED_MEM_DBLEN = ceil(SHARED_MEM_DSIZE.bit_length() / 8.0)
SHARED_MEM_BUFLEN = SHARED_MEM_DSIZE + SHARED_MEM_DBLEN
DEFAULT_MAX_REQUESTS_PER_SECOND = 100.0
DEFAULT_BULK_MAX_REQUESTS_PER_SECOND = 0.8

logger = logging.getLogger(__name__)
synchronized = lockutils.synchronized_with_prefix(__package__)
lockutils.set_defaults(str(Path.home() / __package__))
HostSpecifier = Union[IPv4Address, IPv6Address, None]


class RateLimiter:
    def __init__(self, max_requests_per_second: float, host: HostSpecifier):
        self.host = host
        self.last_request_timestamp = 0.0
        self.max_requests_per_second = max_requests_per_second
        self.hostinfo = str(host) if host else "unknown"

    @property
    def lock(self):
        return lockutils.external_lock(name=self.hostinfo, lock_file_prefix=__package__)

    @property
    def max_requests_per_second(self):
        return self._max_requests_per_second

    @max_requests_per_second.setter
    def max_requests_per_second(self, rps: float):
        self._max_requests_per_second = rps
        self.min_interval = 1.0 / float(rps)
        if self.host is None:
            logger.info(f"Default ratelimiter set to {rps} requests per second")
        else:
            logger.info(f"Host: {self.host} limited to {rps} requests per second")

    def block(self, **kwargs):
        # ensures that each call is separated with min_interval in seconds
        elapsed = time.monotonic() - self.last_request_timestamp
        left_to_wait = self.min_interval - elapsed
        if left_to_wait > 0:
            time.sleep(left_to_wait)
            # logger.debug(f"Delayed request to host: {self.hostinfo} {kwargs} by: {left_to_wait:.2f}s")
            logger.debug(f"Delayed request to host: {self.hostinfo} {kwargs} by: {left_to_wait:.2f}s")
        self.last_request_timestamp = time.monotonic()
        # logger.info(f"{self} timestamp: {self.last_request_timestamp}")


class RateLimiters:
    def __init__(self, default_requests_per_second: int):
        self.default_rps = default_requests_per_second
        self.dict: Dict[HostSpecifier, RateLimiter] = {}

    def __getitem__(self, host: HostSpecifier) -> RateLimiter:
        return self.dict[host]

    def __setitem__(self, host: HostSpecifier, ratelimiter: RateLimiter):
        self.dict[host] = ratelimiter

    def ratelimit(self, max_requests_per_second: int, host: HostSpecifier = None):
        if host is None:
            self.default_rps = max_requests_per_second
        if ratelimiter := self.dict.get(host):
            ratelimiter.max_requests_per_second = max_requests_per_second
        else:
            self.dict[host] = RateLimiter(max_requests_per_second, host)


@synchronized("data", external=True)
def _store_ratelimit_data(ratelimiters: RateLimiters, create: bool = False) -> bool:
    data = pickle.dumps(ratelimiters)
    dlen = len(data)
    if dlen >= SHARED_MEM_DSIZE:
        logger.error(
            f"Cannot create shared memory object, ratelimiters object grown too big: {dlen} > {SHARED_MEM_DSIZE}"
        )
        return False
    if create:
        try:
            shmem = SharedMemory(name="ratelimiters")
            shmem.close()
            shmem.unlink()
        except FileNotFoundError:
            pass
        shmem = SharedMemory(name="ratelimiters", create=True, size=SHARED_MEM_BUFLEN)
    else:
        shmem = SharedMemory(name="ratelimiters")
    shmem.buf[0:SHARED_MEM_DBLEN] = len(data).to_bytes(SHARED_MEM_DBLEN, "big")
    shmem.buf[SHARED_MEM_DBLEN : SHARED_MEM_DBLEN + dlen] = data
    # logger.debug(f"stored to shared memory: {ratelimiters.dict}")
    logger.info(f"stored to shared memory: {ratelimiters.dict.keys()}")
    shmem.close()
    return True


@synchronized("data", external=True)
def _load_ratelimit_data() -> RateLimiters:
    shmem = SharedMemory(name="ratelimiters")
    dlen = int.from_bytes(shmem.buf[0:SHARED_MEM_DBLEN], "big")
    ratelimiters: RateLimiters = pickle.loads(shmem.buf[SHARED_MEM_DBLEN : SHARED_MEM_DBLEN + dlen])
    # logger.debug(f"read from shared memory: {ratelimiters.dict}")
    logger.info(f"loaded from shared memory: {ratelimiters.dict.keys()}")
    shmem.close()
    return ratelimiters


def url_to_host(url: Union[str, bytes]) -> HostSpecifier:
    """
    Takes url like "https://tenant1.domain.com:3333/dataservice/foo"
    Return primary host IP responding to the given url, returns None when host ip cannot be determined
    """
    if isinstance(url, bytes):
        _url = url.decode()
    else:
        _url = url
    try:
        host = str(parse_url(_url).host)
        adressess = gethostbyaddr(host)[2]
        return ip_address(adressess[0])
    except (LocationValueError, LocationParseError, gaierror, herror):
        logger.warning(f"Cannot obtain host ip from url: {_url}")
        return None


def ratelimit(max_requests_per_second: int, host: HostSpecifier = None):
    """
    Sets or changes ratelimit for given host IP
    If host not provided it changes default ratelimit setting for all new ratelimiters
    RateLimiters are also created automatically by throttle function
    """
    ratelimiters = _load_ratelimit_data()
    ratelimiters.ratelimit(max_requests_per_second, host)
    _store_ratelimit_data(ratelimiters)

    # global ratelimiters
    # global max_requests_per_second_setting
    # if host is None:
    #     max_requests_per_second_setting = max_requests_per_second
    # if not ratelimiters.get(host):
    #     ratelimiters[host] = RateLimiter(max_requests_per_second, host)
    # else:
    #     ratelimiters[host].max_requests_per_second = max_requests_per_second


def clear():
    # clears/initializes ratelimiters to defaults
    _store_ratelimit_data(ratelimiters=RateLimiters(DEFAULT_MAX_REQUESTS_PER_SECOND), create=True)


def throttle(host: HostSpecifier, **kwargs):
    """
    Ensures that each call is separated with min_interval for given Host
    Creates new Ratelimiter for given host if it does not exist
    One shared RateLimiter is used for all throttle calls for which host ip cannot be determined from url
    """
    ratelimiters = _load_ratelimit_data()
    if not ratelimiters.dict.get(host):
        ratelimiters[host] = RateLimiter(ratelimiters.default_rps, host)
    ratelimiter = ratelimiters[host]
    ratelimiter.lock.acquire()
    ratelimiter.block(**kwargs)
    _store_ratelimit_data(ratelimiters)
    ratelimiter.lock.release()

    # global ratelimiters
    # if not ratelimiters.get(host):
    #     ratelimiters[host] = RateLimiter(max_requests_per_second_setting, host)
    # ratelimiters[host].block(**kwargs)


def on_request_throttle(method: str, url: Union[bytes, str], *args, **kwargs):
    """
    Example of function performing throttle with matching signature of vmngclient.session.OnRequestHook
    """
    throttle(url_to_host(url), url=url)


if current_process().name == "MainProcess":
    clear()
