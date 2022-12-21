import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from vmngclient.dataclasses import AlarmData
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass, flatten_dict

logger = logging.getLogger(__name__)


class AlarmLevel(Enum):
    minor = "Minor"
    medium = "Medium"
    major = "Major"
    critical = "Critical"


class Viewed(Enum):
    yes = "true"
    no = "false"


class AlarmsAPI:

    URL = "/dataservice/alarms"

    def __init__(self, session: vManageSession):
        self.session = session

    def get_alarms(
        self,
        hours: Optional[int] = None,
        level: Optional[str] = None,
        viewed: Optional[bool] = None,
    ) -> List[AlarmData]:
        query: Dict[str, Any] = {"query": {"condition": "AND", "rules": []}}

        if hours:
            query["query"]["rules"].append(
                {
                    "value": [str(hours)],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours",
                }
            )

        if level:
            query["query"]["rules"].append(
                {
                    "value": [level],
                    "field": "severity",
                    "type": "string",
                    "operator": "in",
                }
            )

        if viewed is not None:
            if viewed:
                value = Viewed.yes.value
            else:
                value = Viewed.no.value

            query["query"]["rules"].append(
                {
                    "value": [value],
                    "field": "acknowledged",
                    "type": "bool",
                    "operator": "equal",
                }
            )

        alarms = self.session.post(url=AlarmsAPI.URL, json=query).json()["data"]

        logger.info("Current alarms collected successfully.")

        return [create_dataclass(AlarmData, flatten_dict(alarm)) for alarm in alarms]

    def get_critical_alarms(self, hours: Optional[int] = None, viewed: Optional[bool] = None) -> List[AlarmData]:
        return self.get_alarms(hours, AlarmLevel.critical.value, viewed)

    def get_major_alarms(self, hours: Optional[int] = None, viewed: Optional[bool] = None) -> List[AlarmData]:
        return self.get_alarms(hours, AlarmLevel.major.value, viewed)

    def get_medium_alarms(self, hours: Optional[int] = None, viewed: Optional[bool] = None) -> List[AlarmData]:
        return self.get_alarms(hours, AlarmLevel.medium.value, viewed)

    def get_minor_alarms(self, hours: Optional[int] = None, viewed: Optional[bool] = None) -> List[AlarmData]:
        return self.get_alarms(hours, AlarmLevel.minor.value, viewed)

    def get_not_viewed_alarms(self, hours: Optional[int] = None) -> List[AlarmData]:
        return self.get_alarms(hours=hours, viewed=False)

    def mark_all_as_viewed(self) -> bool:
        """Marks all alarms as viewed.

        Returns:
          True if all alarms are viewed
        """

        self.session.post(f"{AlarmsAPI.URL}/markallasviewed")
        logger.info("Alarms mark as viewed.")

        return not self.get_not_viewed_alarms()

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
        """

        alarms_expected = {create_dataclass(AlarmData, flatten_dict(expected_alarm)) for expected_alarm in expected}

        verification = AlarmVerification(logger, self.get_not_viewed_alarms)
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

    def __init__(self, logger: logging.Logger, alarms_getter: Callable[[], List[AlarmData]]) -> None:
        self.alarms_getter = alarms_getter
        self.logger = logger

    def __check(self, expected: AlarmData) -> bool:
        """The checking if the expected alarm is included in the alarm set.

        Args:
          expected(AlarmData): The expected alarm.

        Returns:
          True if the requested alarm appears in the current alarm set.
        """
        checked = {expected.lowercase().issubset(actual.lowercase()) for actual in self.alarms_getter()}
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
