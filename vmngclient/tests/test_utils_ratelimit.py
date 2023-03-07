import unittest
from ipaddress import ip_address
from unittest.mock import patch

from parameterized import parameterized  # type: ignore

from vmngclient.utils.ratelimit import (
    DEFAULT_MAX_REQUESTS_PER_MINUTE,
    max_requests_per_minute_setting,
    on_request_throttle,
    ratelimit,
    ratelimiters,
    throttle,
)


class TestTypedList(unittest.TestCase):
    def setUp(self) -> None:
        global ratelimiter
        ratelimiters.clear()
        ratelimit(DEFAULT_MAX_REQUESTS_PER_MINUTE)
        return super().setUp()

    def test_default_ratelimiter(self):
        ratelimit(max_requests_per_minute=100)
        assert ratelimiters[None].max_requests_per_minute == 100
        assert ratelimiters[None].min_interval == 60.0 / 100.0
        ratelimiters[None].max_requests_per_minute = 700
        assert ratelimiters[None].min_interval == 60.0 / 700.0

    @parameterized.expand(
        [
            (15, ip_address("127.0.0.9")),
            (85, ip_address("127.0.0.9")),
            (11, None),
            (99, ip_address("2001:db8:3333:4444:5555:6666:7777:8888")),
            (32, ip_address("127.0.2.22")),
        ]
    )
    @patch("socket.gethostbyaddr")
    def test_create_per_host_ratelimiters(self, rate, ip, mock_gethostbyaddr):
        mock_gethostbyaddr.return_value = str(ip)
        ratelimit(max_requests_per_minute=rate, host=ip)
        assert ratelimiters[ip].max_requests_per_minute == rate

    @parameterized.expand(
        [
            (ip_address("127.0.0.9"),),
            (ip_address("127.0.0.9"),),
            (None,),
            (ip_address("2001:db8:3333:4444:5555:6666:7777:8888"),),
            (ip_address("127.0.2.22"),),
        ]
    )
    @patch("socket.gethostbyaddr")
    def test_throttle_with_default_rate(self, ip, mock_gethostbyaddr):
        mock_gethostbyaddr.return_value = str(ip)
        throttle(host=ip)
        assert ratelimiters[ip].max_requests_per_minute == max_requests_per_minute_setting

    @parameterized.expand(
        [
            (3333, "http://localhost:333/foo", ip_address("127.0.0.9")),
            (8818, b"127.0.0.9:80/foo", ip_address("127.0.0.9")),
            (8978, "{/?>>}/7897/89-=/57/8", None),
            (9556, "www.google.com", ip_address("2001:db8:3333:4444:5555:6666:7777:8888")),
            (1111, "https://127.0.2.22/#", ip_address("127.0.2.22")),
        ]
    )
    @patch("socket.gethostbyaddr")
    def test_on_request_throttle_preset_rate(self, rate, url, ip, mock_gethostbyaddr):
        mock_gethostbyaddr.return_value = str(ip)
        ratelimit(max_requests_per_minute=rate, host=ip)
        on_request_throttle(method="get", url=url)
        assert ratelimiters[ip].max_requests_per_minute == rate
