import unittest
from unittest.mock import MagicMock, patch

from vmngclient.endpoints.configuration_group import (
    ConfigGroup,
    ConfigGroupAssociatePayload,
    ConfigGroupCreationPayload,
    ConfigGroupCreationResponse,
    ConfigGroupDeployPayload,
    ConfigGroupDeployResponse,
    ConfigGroupDisassociateResponse,
    ConfigGroupVariablesCreatePayload,
    ConfigGroupVariablesCreateResponse,
    ConfigGroupVariablesEditPayload,
    DeviceId,
    FeatureProfile,
    ProfileId,
    Solution,
    VariableData,
)


class ConfigurationGroupEndpointTest(unittest.TestCase):
    @patch("vmngclient.session.vManageSession")
    def setUp(self, session_mock):
        self.session = session_mock
        self.session.api_version = None
        self.session.session_type = None

    def test_associate(self):
        associate_payload = ConfigGroupAssociatePayload(
            devices=[DeviceId(id="C8K-1926b264-5e72-43ac-aa39-65b439032976")]
        )

        cg_id = "655d4a92-500f-4256-8e85-0fb518c2d574"
        self.session.endpoints.configuration_group.associate = MagicMock()
        self.session.endpoints.configuration_group.associate(config_group_id=cg_id, payload=associate_payload)
        self.session.endpoints.configuration_group.associate.assert_called_once_with(
            config_group_id=cg_id, payload=associate_payload
        )

    def test_create_config_group(self):
        cg_creation_payload = ConfigGroupCreationPayload(
            name="CLIConfigGroup",
            description="CLIConfigGroup",
            solution="sd-routing",
            profiles=[ProfileId(id="655d4a92-500f-4256-8e85-0fb518c2d574")],
        )
        expected_cg_creation_response = ConfigGroupCreationResponse(id="655d4a92-500f-4256-8e85-0fb518c2d576")

        self.session.endpoints.configuration_group.create_config_group = MagicMock(
            return_value=expected_cg_creation_response
        )
        observed_config_group_creation_response = self.session.endpoints.configuration_group.create_config_group(
            payload=cg_creation_payload
        )
        assert expected_cg_creation_response == observed_config_group_creation_response

    def test_create_variables(self):
        cg_vars_create_payload = ConfigGroupVariablesCreatePayload(
            deviceIds=["C8K-2ff2b97c-aef2-4571-b5c9-33c34edb3fc4", "C8K-2ff2b97c-aef2-4572-b5c9-33c34edb3fc5"],
            suggestions=True,
        )

        dev1_vars = [VariableData(name="hostname", value="branch1"), VariableData(name="system-ip", value="10.0.1.1")]
        dev1_vars_map = {"device-id": "C8K-2ff2b97c-aef2-4571-b5c9-33c34edb3fc4", "variables": dev1_vars}

        dev2_vars = [VariableData(name="hostname", value="branch2"), VariableData(name="system-ip", value="10.0.1.2")]
        dev2_vars_map = {"device-id": "C8K-2ff2b97c-aef2-4572-b5c9-33c34edb3fc5", "variables": dev2_vars}

        group_vars = [VariableData(name="site-id", value=500)]
        groups = {"name": "Group1Vars", "group-variables": group_vars}

        expected_create_vars_response = ConfigGroupVariablesCreateResponse(
            family=Solution.SDROUTING, devices=[dev1_vars_map, dev2_vars_map], groups=[groups]
        )

        self.session.endpoints.configuration_group.create_variables = MagicMock(
            return_value=expected_create_vars_response
        )
        observed_create_vars_response = self.session.endpoints.configuration_group.create_variables(
            payload=cg_vars_create_payload
        )
        assert expected_create_vars_response == observed_create_vars_response

    def test_delete_config_group(self):
        cg_id = "655d4a92-500f-4256-8e85-0fb518c2d574"
        self.session.endpoints.configuration_group.delete_config_group = MagicMock()
        self.session.endpoints.configuration_group.delete_config_group(config_group_id=cg_id)
        self.session.endpoints.configuration_group.delete_config_group.assert_called_once_with(config_group_id=cg_id)

    def test_deploy(self):
        cg_deploy_payload = ConfigGroupDeployPayload(
            devices=[
                DeviceId(id="C8K-2ff2b97c-aef2-4571-b5c9-33c34edb3fc4"),
                DeviceId(id="C8K-2ff2b97c-aef2-4572-b5c9-33c34edb3fc5"),
            ]
        )

        expected_cg_deploy_response = ConfigGroupDeployResponse(
            parentTaskId="deploy_config_group-1a02fa64-0cc3-4ae9-a145-ef5ee4e880d5"
        )

        self.session.endpoints.configuration_group.deploy = MagicMock(return_value=expected_cg_deploy_response)
        observed_cg_deploy_response = self.session.endpoints.configuration_group.deploy(payload=cg_deploy_payload)
        assert expected_cg_deploy_response == observed_cg_deploy_response

    def test_disassociate(self):
        associate_payload = ConfigGroupAssociatePayload(
            devices=[DeviceId(id="C8K-1926b264-5e72-43ac-aa39-65b439032976")]
        )

        cg_id = "655d4a92-500f-4256-8e85-0fb518c2d574"

        expected_cg_disassociate_response = ConfigGroupDisassociateResponse(
            parentTaskId="removed_devices_from_config-group-3ce8b81e-c1ef-4528-95c1-8e267e6ffcd3"
        )

        self.session.endpoints.configuration_group.disassociate = MagicMock(
            return_value=expected_cg_disassociate_response
        )
        observed_cg_disassociate_response = self.session.endpoints.configuration_group.disassociate(
            config_group_id=cg_id, payload=associate_payload
        )
        assert expected_cg_disassociate_response == observed_cg_disassociate_response

    def test_get(self):
        expected_config_groups = [
            ConfigGroup(
                name="CLIConfigGroup",
                description="CLIConfigGroup",
                solution="sd-routing",
                profiles=[
                    FeatureProfile(
                        id="15428072-61b3-455e-80e4-d440605c2506",
                        name="CLIFeatureProfile",
                        description="CLIFeatureProfile",
                        solution="sd-routing",
                        type="cli",
                        createdBy="admin",
                        lastUpdatedBy="admin",
                        createdOn=1695986643498,
                        lastUpdatedOn=1695986643498,
                    )
                ],
            )
        ]

        self.session.endpoints.configuration_group.get = MagicMock(return_value=expected_config_groups)
        observed_config_groups = self.session.endpoints.configuration_group.get()
        assert expected_config_groups == observed_config_groups

    def test_update_variables(self):
        dev1_vars = [VariableData(name="hostname", value="branch1"), VariableData(name="system-ip", value="10.0.1.1")]
        dev1_vars_map = {"device-id": "C8K-2ff2b97c-aef2-4571-b5c9-33c34edb3fc4", "variables": dev1_vars}

        dev2_vars = [VariableData(name="hostname", value="branch2"), VariableData(name="system-ip", value="10.0.1.2")]
        dev2_vars_map = {"device-id": "C8K-2ff2b97c-aef2-4572-b5c9-33c34edb3fc5", "variables": dev2_vars}

        cg_variables_edit_payload = ConfigGroupVariablesEditPayload(
            solution=Solution.SDROUTING, devices=[dev1_vars_map, dev2_vars_map]
        )

        cg_id = "655d4a92-500f-4256-8e85-0fb518c2d574"
        self.session.endpoints.configuration_group.update_variables = MagicMock()
        self.session.endpoints.configuration_group.update_variables(
            config_group_id=cg_id, payload=cg_variables_edit_payload
        )
        self.session.endpoints.configuration_group.update_variables.assert_called_once_with(
            config_group_id=cg_id, payload=cg_variables_edit_payload
        )
