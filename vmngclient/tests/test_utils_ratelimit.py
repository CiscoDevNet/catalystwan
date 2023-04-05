import logging
import time
import unittest
from ipaddress import ip_address
from multiprocessing.pool import Pool, ThreadPool
from unittest.mock import patch

from parameterized import parameterized  # type: ignore

from vmngclient.utils.ratelimit import (
    DEFAULT_MAX_REQUESTS_PER_SECOND,
    _load_ratelimit_data,
    clear,
    on_request_throttle,
    ratelimit,
    throttle,
)

logger = logging.getLogger(__name__)


class TestUtilsRateLimit(unittest.TestCase):
    def setUp(self) -> None:
        global ratelimiter
        clear()
        ratelimit(DEFAULT_MAX_REQUESTS_PER_SECOND)
        return super().setUp()

    def test_default_ratelimiter(self):
        ratelimit(max_requests_per_second=100)
        ratelimiters = _load_ratelimit_data()
        assert ratelimiters[None].max_requests_per_second == 100
        assert ratelimiters[None].min_interval == 1 / 100.0
        ratelimiters[None].max_requests_per_second = 700
        assert ratelimiters[None].min_interval == 1 / 700.0

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
        ratelimit(max_requests_per_second=rate, host=ip)
        ratelimiters = _load_ratelimit_data()
        assert ratelimiters[ip].max_requests_per_second == rate

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
        ratelimiters = _load_ratelimit_data()
        assert ratelimiters[ip].max_requests_per_second == ratelimiters.default_rps

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
        ratelimit(max_requests_per_second=rate, host=ip)
        on_request_throttle(method="get", url=url)
        ratelimiters = _load_ratelimit_data()
        assert ratelimiters[ip].max_requests_per_second == rate

    @patch("socket.gethostbyaddr")
    def test_throttle_multiple_threads_and_processes(self, mock_gethostbyaddr):
        # Given
        ip = ip_address("127.0.0.2")
        mock_gethostbyaddr.return_value = str(ip)
        mp_items = [ip] * 33
        t_items = [ip] * 31
        item_count = len(mp_items) + len(t_items)
        max_rps = 3
        ratelimit(max_requests_per_second=max_rps)
        min_expected_time_to_finish_tasks = item_count * 1.0 / max_rps
        # Act
        start = time.monotonic()
        mp_results = Pool(len(mp_items)).map_async(throttle, mp_items)
        t_results = ThreadPool(len(t_items)).map_async(throttle, t_items)
        mp_results.wait()
        t_results.wait()
        finish = time.monotonic()
        delta = finish - start
        assert finish - start > min_expected_time_to_finish_tasks, (
            f"{item_count} tasks finished in {delta:.2f}s, "
            f"but expected no earlier than: {min_expected_time_to_finish_tasks:.2f}s for given rate {max_rps}/s"
        )
