import os
import unittest
from typing import cast

from catalystwan.session import create_manager_session
from catalystwan.workflows.config_migration import collect_ux1_config, transform


class TestConfigMigration(unittest.TestCase):
    def setUp(self) -> None:
        self.session = create_manager_session(
            url=cast(str, os.environ.get("TEST_VMANAGE_URL")),
            port=cast(int, int(os.environ.get("TEST_VMANAGE_PORT"))),  # type: ignore
            username=cast(str, os.environ.get("TEST_VMANAGE_USERNAME")),
            password=cast(str, os.environ.get("TEST_VMANAGE_PASSWORD")),
        )

    def test_config_migration(self):
        ux1_config = collect_ux1_config(self.session)
        ux2_config = transform(ux1_config)
        # push_ux2_config(self.session, ux2_config)
        # This section will include the Feature profiles creation
        # and pushing the configuration to the vManage
        assert ux2_config

    def tearDown(self) -> None:
        # This section will include the Feature profiles deletion
        self.session.close()
