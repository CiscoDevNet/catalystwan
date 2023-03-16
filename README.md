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
admintech.download(admin_tech_file)
admintech.delete(admin_tech_file)
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
vsmarts = [device for device in DevicesAPI(session).devices
            if device .personality == Personality.VSMART]
software_image = "viptela-20.7.2-x86_64.tar.gz"

# Upload image
session.api.repository.upload_image(software_image)

# Upgrade
software_action = SoftwareActionAPI(session, DeviceCategory.VEDGES)
software_action_id = software_action.upgrade_software(vsmarts,
    InstallSpecHelper.CEDGE.value, reboot = False, sync = True, software_image=software_image)

# Check action status
wait_for_completed(session, software_action_id, 3000)
```

</details>

<details>
    <summary> <b>Get alarms</b> <i>(click to expand)</i></summary>

```python
alarms = session.api.alarms.get()
```

</details>

### Note:
To remove `InsecureRequestWarning`, you can include in your scripts:
```Python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## [Contributing, reporting issues, seeking support](https://github.com/CiscoDevNet/vManage-client/blob/main/CONTRIBUTING.md)
