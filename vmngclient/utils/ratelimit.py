"""
This is utility module which can be used to limit requests rate globally (from multiple sessions, threads and processes)
To enable ratelimiting for all requests sent from vmanage-client in your application:
>>> from vmngclient.utils.ratelimit import ratelimit, on_request_throttle
>>> ratelimit(max_requests_per_second=100)
>>> vManageSession.on_request_hook = on_request_throttle
>>> vManageAuth.on_request_hook = on_request_throttle
Each unique host ip has own RateLimiter (host ip is obtained automatically from request url)
"""

import logging
import multiprocessing
import threading
import time
from ipaddress import IPv4Address, IPv6Address, ip_address
from socket import gaierror, gethostbyaddr, herror
from typing import Dict, Union

from urllib3.exceptions import LocationParseError, LocationValueError
from urllib3.util import parse_url

DEFAULT_MAX_REQUESTS_PER_SECOND = 100  # according to:
max_requests_per_second_setting = DEFAULT_MAX_REQUESTS_PER_SECOND
logger = logging.getLogger(__name__)

HostSpecifier = Union[IPv4Address, IPv6Address, None]


class RateLimiter:
    def __init__(self, max_requests_per_second: int, host: HostSpecifier):
        self.host = host
        self.tlock = threading.Lock()
        self.mplock = multiprocessing.Lock()
        self.last_request_timestamp = 0.0
        self.max_requests_per_second = max_requests_per_second
        self.hostinfo = str(host) if host else "unknown"

    @property
    def max_requests_per_second(self):
        return self._max_requests_per_second

    @max_requests_per_second.setter
    def max_requests_per_second(self, rps: int):
        self._max_requests_per_second = rps
        self.min_interval = 1.0 / float(rps)
        if self.host is None:
            logger.info(f"Default ratelimiter set to {rps} requests per second")
        else:
            logger.info(f"Host: {self.host} limited to {rps} requests per second")

    def block(self, **kwargs):
        # ensures that each call is separated with min_interval in seconds
        with self.tlock:
            with self.mplock:
                elapsed = time.monotonic() - self.last_request_timestamp
                left_to_wait = self.min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                    logger.debug(f"Delayed request to host: {self.hostinfo} {kwargs} by: {left_to_wait:.2f}s")
                self.last_request_timestamp = time.monotonic()


ratelimiters: Dict[HostSpecifier, RateLimiter] = {}


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
    Sets or changes ratelimit for given IP host
    If host not provided it changes default ratelimit setting for new ratelimiters
    RateLimiters are also created automatically by throttle function
    """
    global ratelimiters
    global max_requests_per_second_setting
    if host is None:
        max_requests_per_second_setting = max_requests_per_second
    if not ratelimiters.get(host):
        ratelimiters[host] = RateLimiter(max_requests_per_second, host)
    else:
        ratelimiters[host].max_requests_per_second = max_requests_per_second


def throttle(host: HostSpecifier, **kwargs):
    """
    Ensures that each call is separated with min_interval for given Host
    Creates new Ratelimiter for given host if it does not exist
    One shared RateLimiter is used for all throttle calls for which host ip cannot be determined from url
    """
    global ratelimiters
    if not ratelimiters.get(host):
        ratelimiters[host] = RateLimiter(max_requests_per_second_setting, host)
    ratelimiters[host].block(**kwargs)


def on_request_throttle(method: str, url: Union[bytes, str], *args, **kwargs):
    """
    Example of function performing throttle with matching signature of vmngclient.session.OnRequestHook
    """
    throttle(url_to_host(url), url=url)
