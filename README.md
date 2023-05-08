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
vsmarts = session.api.devices.get().filter(personality = Personality.VSMART)
image = "viptela-20.7.2-x86_64.tar.gz"

# Upload image
session.api.repository.upload_image(software_image)

# Install software

install_task = session.api.software.install(devices = vsmarts,
    image= image)

# Check action status
install_task.wait_for_completed()
```

</details>

<details>
    <summary> <b>Get alarms</b> <i>(click to expand)</i></summary>

```python
alarms = session.api.alarms.get()
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

### Note:
To remove `InsecureRequestWarning`, you can include in your scripts (warning is supressed when `VMNGCLIENT_DEVEL` environment variable is set):
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
