"""
This is utility module which can be used to limit requests rate globally (from multiple sessions, threads and processes)
To enable ratelimiting for all requests sent from vmanage-client in your application:
>>> from vmngclient.utils.ratelimit import ratelimit, on_request_throttle
>>> ratelimit(max_requests_per_minute=100)
>>> vManageSession.on_request_hook = on_request_throttle
>>> vManageAuth.on_request_hook = on_request_throttle
Each unique host ip has own RateLimiter (host ip is obtained automatically from request url)
"""

import logging
import multiprocessing
import threading
import time
from ipaddress import IPv4Address, IPv6Address, ip_address
from socket import gaierror, gethostbyaddr
from typing import Dict, Union

from urllib3.exceptions import LocationParseError, LocationValueError
from urllib3.util import parse_url

DEFAULT_MAX_REQUESTS_PER_MINUTE = 1000
max_requests_per_minute_setting = DEFAULT_MAX_REQUESTS_PER_MINUTE
logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, max_requests_per_minute: int, host: Union[IPv4Address, IPv6Address, None]):
        self.host = host
        self.tlock = threading.Lock()
        self.mplock = multiprocessing.Lock()
        self.last_request_timestamp = 0.0
        self.max_requests_per_minute = max_requests_per_minute
        self.hostinfo = str(host) if host else "unknown"

    @property
    def max_requests_per_minute(self):
        return self._max_requests_per_minute

    @max_requests_per_minute.setter
    def max_requests_per_minute(self, rpm: int):
        self._max_requests_per_minute = rpm
        self.min_interval = 60.0 / float(rpm)
        if self.host is None:
            logger.info(f"Default ratelimiter set to {rpm} requests per minute")
        else:
            logger.info(f"Host: {self.host} limited to {rpm} requests per minute")

    def block(self, **kwargs):
        # ensures that each call is separated with min_interval
        with self.tlock:
            with self.mplock:
                elapsed = time.monotonic() - self.last_request_timestamp
                left_to_wait = self.min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                    logger.debug(f"Delayed request to host: {self.hostinfo} {kwargs} by: {left_to_wait:.2f}s")
                self.last_request_timestamp = time.monotonic()


ratelimiters: Dict[Union[IPv4Address, IPv6Address, None], RateLimiter] = {}


def url_to_host(url: Union[str, bytes]) -> Union[IPv4Address, IPv6Address, None]:
    """
    Takes url like "https://tenant1.domain.com:3333/dataservice/foo"
    Return primary host IP responding to the given url, returns None when host ip cannot be determined
    """
    if isinstance(url, bytes):
        _url = url.decode()
    else:
        _url = url
    try:
        adressess = gethostbyaddr(str(parse_url(_url).host))[2]
        return ip_address(adressess[0])
    except (LocationValueError, LocationParseError, gaierror):
        logger.warning(f"Cannot obtain host ip from url: {_url}")
        return None


def ratelimit(max_requests_per_minute: int, host: Union[IPv4Address, IPv6Address, None] = None):
    """
    Sets or changes ratelimit for given IP host
    If host not provided it changes default ratelimit setting for new ratelimiters
    (ratelimiters can be created automatically on traffic by throttle function)
    """
    global ratelimiters
    global max_requests_per_minute_setting
    if host is None:
        max_requests_per_minute_setting = max_requests_per_minute
    if not ratelimiters.get(host):
        ratelimiters[host] = RateLimiter(max_requests_per_minute, host)
    else:
        ratelimiters[host].max_requests_per_minute = max_requests_per_minute


def throttle(host: Union[IPv4Address, IPv6Address, None], **kwargs):
    """
    Ensures that each call is separated with min_interval for given Host
    One ratelimiter is shared for all throttle calls when host is not provided
    """
    global ratelimiters
    if not ratelimiters.get(host):
        ratelimiters[host] = RateLimiter(max_requests_per_minute_setting, host)
    ratelimiters[host].block(**kwargs)


def on_request_throttle(method: str, url: Union[bytes, str], *args, **kwargs):
    """
    Example of function performing throttle with matching signature of vmngclient.session.OnRequestHook
    """
    throttle(url_to_host(url), url=url)
