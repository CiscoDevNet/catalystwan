# Copyright 2022 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Set

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from catalystwan.dataclasses import AlarmData
from catalystwan.typed_list import DataSequence
from catalystwan.utils.creation_tools import create_dataclass, flatten_dict

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


class AlarmsAPI:
    """API methods of vManage for Alarms.

    Attributes:
        session: logged in API client session
    """

    URL = "/dataservice/alarms"

    def __init__(self, session: ManagerSession):
        self.session = session

    def get(self, from_time: Optional[int] = None) -> DataSequence[AlarmData]:
        """Data sequence of alarms.

        Args:
            from_time: Gets alarms from time in hour. Defaults to None - gets all alrams.

        Returns:
            DataSequence[AlarmData] of getted alarms.

        Examples:
            Get all alarms:
            >>> alarms = AlarmsAPI(session).get()

            Get all alarms from 3 hours:
            >>> alarms = AlarmsAPI(session).get(from_time=3)

            Get all not viewed alarms:
            >>> alarms = AlarmsAPI(session).get()
            >>> not_viewed_alarms = alarms.filter(viewed=False)

            Get all critical alarms:
            >>> alarms = AlarmsAPI(session).get()
            >>> critical_alarms = alarms.filter(severity=Severity.CRITICAL)
        """
        query: Dict[str, Any] = {"query": {"condition": "AND", "rules": []}}
        if from_time:
            query["query"]["rules"].append(
                {
                    "value": [str(from_time)],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours",
                }
            )

        response = self.session.post(url=AlarmsAPI.URL, json=query).json()["data"]
        alarms = [create_dataclass(AlarmData, flatten_dict(alarm)) for alarm in response]
        logger.info("Current alarms collected successfully.")

        return DataSequence(AlarmData, alarms)

    def mark_all_as_viewed(self) -> None:
        """Marks all alarms as viewed."""

        self.session.post(f"{AlarmsAPI.URL}/markallasviewed")
        logger.info("Alarms mark as viewed.")

    def check_alarms(
        self,
        expected: List[Dict[str, str]],
        timeout_seconds: int = 240,
        sleep_seconds: int = 5,
    ) -> Dict[str, set]:
        """Checks if alarms have occurred.

        For a specified period of time, the method queries the API about unread alarms and
        checks if they occur in the expected ones. If all alarms occur before the time expires,
        it will not poll any further.

        Args:
          expected(list): The list of expected alarms.
          timeout_seconds (int): Failure timeout.
          sleep_seconds (int): Sleep time.

        Returns:
          The dictionary with alarms that occurred (key 'found') and did not (key 'no-found')

        Examples:
            >>> expected_alarms = [{
                "type": "memory-usage",
                "rulename": "memory-usage",
                "component": "System",
                "severity": "Medium",
                "system_ip": "192.168.1.2",
                "acknowledged": true,
                "active": true,
                }]
            >>> result = AlarmsAPI(session).check_alarms(expected = expected_alarms)
        """

        alarms_expected = {create_dataclass(AlarmData, flatten_dict(expected_alarm)) for expected_alarm in expected}

        verification = AlarmVerification(logger, self.get)
        verification.verify(alarms_expected, timeout_seconds, sleep_seconds)

        logger.info(f"found alarms: {verification.found}")
        logger.info(f"not-found alarms: {verification.not_found}")

        return {"found": verification.found, "not-found": verification.not_found}


class AlarmVerification:
    """The Alarms verification class

    Attributes:
        alarms_getter (Callable): The function that returns a set of current alarms.
        logger (Logger): Logger.
    """

    def __init__(self, logger: logging.Logger, alarms_getter: Callable[[], DataSequence[AlarmData]]) -> None:
        self.alarms_getter = alarms_getter
        self.logger = logger

    def __check(self, expected: AlarmData) -> bool:
        """The checking if the expected alarm is included in the alarm set.

        Args:
          expected(AlarmData): The expected alarm.

        Returns:
          True if the requested alarm appears in the current alarm set.
        """
        not_viewed_alarms = self.alarms_getter().filter(viewed=False)
        checked = {expected.lowercase().issubset(actual.lowercase()) for actual in not_viewed_alarms}
        return any(checked)

    def verify(self, expected: Set[AlarmData], timeout_seconds: int, sleep_seconds: int):
        """The verifying if the expected alarms is included in the actual alarms set.

        Args:
          expected(Set[AlarmData]): The set expected alarms.
          timeout_seconds (int): Failure timeout.
          sleep_seconds (int): Sleep time.

        """
        self.found: Set[AlarmData] = set()
        self.not_found: Set[AlarmData] = set()

        def _log_exception(retry_state):
            self.logger.error(f"Cannot found alarms in {timeout_seconds}.")
            self.logger.error(f"Original exception: {retry_state.outcome.exception()}.")

        def check(founds):
            return expected != founds

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check),
            retry_error_callback=_log_exception,
        )
        def wait_for_alarms():
            self.logger.info(f"waiting for alarms: {expected ^ self.found}")
            for expected_alarm in expected ^ self.found:
                if self.__check(expected_alarm):
                    self.found.add(expected_alarm)
            self.not_found = expected ^ self.found
            return self.found

        wait_for_alarms()
