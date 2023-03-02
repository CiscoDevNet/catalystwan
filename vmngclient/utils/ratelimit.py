"""
This is utility module which can be help to limit requests rate globally (from multiple sessions, threads and processes)
To enable ratelimiting for all requests sent from vmanage-client in your application:
>>> from vmngclient.utils.ratelimit import ratelimit, on_request_throttle
>>> ratelimit(100)
>>> vManageSession.on_request_hook = on_request_throttle
>>> vManageAuth.on_request_hook = on_request_throttle
"""

import multiprocessing
import threading
import time
from ipaddress import IPv4Address, IPv6Address, ip_address
from socket import getaddrinfo
from typing import Dict, Union
from urllib.parse import urlparse

DEFAULT_MAX_REQUESTS_PER_MINUTE = 1000
max_requests_per_minute_setting = DEFAULT_MAX_REQUESTS_PER_MINUTE


class RateLimiter:
    def __init__(self, max_requests_per_minute: int):
        self.tlock = threading.Lock()
        self.mplock = multiprocessing.Lock()
        self.last_request_timestamp = 0.0
        self.max_requests_per_minute = max_requests_per_minute

    @property
    def max_requests_per_minute(self):
        return self._max_requests_per_minute

    @max_requests_per_minute.setter
    def max_requests_per_minute(self, rpm: int):
        self._max_requests_per_minute = rpm
        self.min_interval = 60.0 / float(rpm)

    def block(self):
        # ensures that each call is separated with min_interval
        with self.tlock:
            with self.mplock:
                elapsed = time.monotonic() - self.last_request_timestamp
                left_to_wait = self.min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                self.last_request_timestamp = time.monotonic()


ratelimiters: Dict[Union[IPv4Address, IPv6Address, None], RateLimiter] = {}


def url_to_host(url: str) -> Union[IPv4Address, IPv6Address, None]:
    """
    Takes url like "http://apple.fruits.com:3333/dataservice/foo"
    And returns host IP Address
    """
    host, _, port = urlparse(url).netloc.partition(":")
    addrinfos = getaddrinfo(host, port)
    return ip_address(addrinfos[0][4][0])


def ratelimit(max_requests_per_minute: int, host: Union[IPv4Address, IPv6Address, None] = None):
    """
    Sets or changes ratelimit for given IP host
    If host not provided it changes default ratelimit setting for new ratelimiters
    (ratelimiters can be created automatically on traffic by throttle function)
    """
    global ratelimiters
    global max_requests_per_minute_setting
    if not host:
        max_requests_per_minute_setting = max_requests_per_minute
    if not ratelimiters.get(host):
        ratelimiters[host] = RateLimiter(max_requests_per_minute)
    else:
        ratelimiters[host].max_requests_per_minute = max_requests_per_minute


def throttle(host: Union[IPv4Address, IPv6Address, None] = None):
    """
    Ensures that each call is separated with min_interval for given Host
    One ratelimiter is shared for all throttle calls when host is not provided
    """
    global ratelimiters
    if not ratelimiters.get(host):
        ratelimiters[host] = RateLimiter(max_requests_per_minute_setting)
    ratelimiters[host].block()


def on_request_throttle(method: str, url: str, *args, **kwargs):
    """
    Example of function performing throttle with matching signature of vmngclient.session.OnRequestHook
    """
    throttle(url_to_host(url))
