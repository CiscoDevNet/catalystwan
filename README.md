# vManage-client
[![Python3.8](https://img.shields.io/static/v1?label=Python&logo=Python&color=3776AB&message=3.8)](https://www.python.org/)

vManage client is a package for creating simple and parallel automatic requests via official vManageAPI. It is intended to serve as a multiple session handler (provider, provider as a tenant, tenant). The library is not dependent on environment which is being run in, you just need a connection to any vManage.

## Installation
```console
pip install vmngclient
```

## Session usage example
Our session is an extension to `requests.Session` designed to make it easier to communicate via API calls with vManage. We provide ready to use authenticetion, you have to simply provide the vmanage url, username and password as as if you were doing it through a GUI. 
```python
from vmngclient.session import create_vManageSession

url = "example.com"
username = "admin"
password = "password123"
session = create_vManageSession(url=url, username=username, password=password)

session.get("/dataservice/device")
```

## API usage examples

<details>
    <summary> <b>Get devices</b> <i>(click to expand)</i></summary>

```python
devices = session.api.devices.get()
```

</details>

<details>
    <summary> <b>Admin Tech</b> <i>(click to expand)</i></summary>

```Python
admin_tech_file = session.api.admin_tech.generate("172.16.255.11")
session.api.admin_tech.download(admin_tech_file)
session.api.admin_tech.delete(admin_tech_file)
```
</details>

<details>
    <summary> <b>Speed test</b> <i>(click to expand)</i></summary>

```python
devices = session.api.devices.get()
speedtest = session.api.speedtest.speedtest(devices[0], devices[1])
```

</details>

<details>
    <summary> <b>Upgrade device</b> <i>(click to expand)</i></summary>

```python
# Prepare devices list
vsmarts = session.api.devices.get().filter(personality=Personality.VSMART)
image = "viptela-20.7.2-x86_64.tar.gz"

# Upload image
session.api.repository.upload_image(image)

# Install software

install_task = session.api.software.install(devices=vsmarts, image=image)

# Check action status
install_task.wait_for_completed()
```

</details>

<details>
    <summary> <b>Get alarms</b> <i>(click to expand)</i></summary>
To get all alarms:

```python
alarms = session.api.alarms.get()
```

To get all not viewed alarms:

```python
not_viewed_alarms = session.api.alarms.get().filter(viewed=False)
```

To get all alarms from past `n` hours:

```python
n = 24
alarms_from_n_hours = session.api.alarms.get(from_time=n)
```

To get all critical alarms from past `n` hours:

```python
n = 48
critical_alarms = session.api.alarms.get(from_time=n).filter(severity=Severity.CRITICAL)
```

</details>

<details>
    <summary> <b>User operations</b> <i>(click to expand)</i></summary>

```python
from vmngclient.api.administration import User, UsersAPI

# Get all users
all_users = UsersAPI(session).get_all_users()

# Create a user
new_user = User(username="new_user", password="new_user", group=["netadmin"], description="new user")
status = UsersAPI(session).create_user(new_user)

# Delete a user
status = UsersAPI(session).delete_user(username="new_user")
```

</details>

<details>
    <summary> <b>Tenant management</b> <i>(click to expand)</i></summary>

```python
api = session.api.tenant_management
# create tenants
tenants = [
    Tenant(
        name="tenant1",
        orgName="CiscoDevNet",
        subDomain="alpha.bravo.net",
        desc="This is tenant for unit tests",
        edgeConnectorEnable=True,
        edgeConnectorSystemIp="172.16.255.81",
        edgeConnectorTunnelInterfaceName="GigabitEthernet1",
        wanEdgeForecast=1,
    )
]
create_task = api.create(tenants)
create_task.wait_for_completed()
# list all tenants
tenants_data = api.get_all()
# pick tenant from list by name
tenant = tenants_data.filter(name="tenant1").single_or_default()
# get selected tenant id
tenant_id = tenant.tenant_id
# get vsession id of selected tenant
vsessionid = api.vsession_id(tenant_id)
# delete tenant by ids
delete_task = api.delete([tenant_id])
delete_task.wait_for_completed()
# others
api.get_hosting_capacity_on_vsmarts()
api.get_statuses()
api.get_vsmart_mapping()
```
</details>

<details>
    <summary> <b>Tenant migration</b> <i>(click to expand)</i></summary>
Preparation:

```python
from vmngclient.api.tenant_migration_api import TenantMigrationAPI, st_to_mt
from vmngclient.model.tenant import Tenant
from vmngclient.session import create_vManageSession
# create sessions to both systems
st_session = create_vManageSession(**single_tenant_login)
mt_session = create_vManageSession(**multi_tenant_provider_login)
# create api and tenant objects
st_api = TenantMigrationAPI(st_session)
mt_api = TenantMigrationAPI(mt_session)
tenant = Tenant.parse_obj({
    "name": "single-tenant",
    "desc": "Migrated from Single Tenant",
    "orgName": "vIPtela Inc Regression",
    "subDomain": "single-tenant.fruits.com",
    "wanEdgeForecast": 99
})
```

Method below performs multi-step migration procedure according to [Migrate Single-Tenant Cisco SD-WAN Overlay to Multitenant Cisco SD-WAN Deployment](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/system-interface/vedge-20-x/systems-interfaces-book/sdwan-multitenancy.html#concept_sjj_jmm_z4b)

```python
from pathlib import Path
st_to_mt(st_api, mt_api, workdir=Path.cwd(), tenant=tenant)
```

Each step of the procedure can be executed independently using api methods: `export_tenant`, `download`, `import_tenant`, `store_token`, `migrate_network`

```python
tenant_file = Path("~/tenant.tar.gz")
token_file = Path("~/tenant-token.txt")
# export
export_task = st_api.export_tenant(tenant=tenant)
export_result = export_task.wait_for_completed()
# download
st_api.download(tenant_file)
# import
import_task = mt_api.import_tenant(tenant_file)
import_task.wait_for_completed()
# get token
migration_id = import_task.import_info.migration_token_query_params.migration_id
mt_api.store_token(migration_id, token_file)
# migrate network
migrate_task = st_api.migrate_network(token_file)
migrate_task.wait_for_completed()
```
</details>

### Note:
To remove `InsecureRequestWarning`, you can include in your scripts (warning is suppressed when `VMNGCLIENT_DEVEL` environment variable is set):
```Python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## Catching Exceptions
```python
try:
	session.api.users.delete_user("XYZ")
except vManageBadRequestError as error:
	# Process an error.
	logger.error(error.info.details)

# message = 'Delete users request failed' 
# details = 'No user with name XYZ was found' 
# code = 'USER0006'
```

## [Contributing, bug reporting and feature requests](https://github.com/CiscoDevNet/vManage-client/blob/main/CONTRIBUTING.md)

## Seeking support

You can contact us by submitting [issues](https://github.com/CiscoDevNet/vManage-client/issues), or directly via mail on vmngclient@cisco.com.
