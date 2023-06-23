# vManage-client v0.9.0

📈 Enhancements:
- Dashboard - add new additional endpoints
- Add primitive `edit()` Feature Template
- Refresh closed session
- Add schema for L2/L3 layer separation (more info soon)
- Add View decorator
```python
# API calls can now be tagged from within 
# the vmngclient on which view they function
@View({ProviderView})
def create_tenant(self, tenant: Tenant) -> Tenant:
	...
```
- Add tenant management API primitives
- Add `DeviceModel` support in Feature Templates
- Custom Exception Tree was created. Now every Exception inherits from `vManageClientError`. Every Exception regarding Already existing entity was removed, and vManage response message is now being used.
- Add possibility to catch Exception error from the response
```python
try:
    session.api.users.delete_user("ABC")
except vManageBadRequestError as error:
    response = error.response.text
    print(response)
>>> {"error":{"message":"Delete users request failed","code":"USER0006","details":"No user with name ABC was found"}}
```

🔨 Fixes:

- Fixed Tasks status (`get_all_tasks()`  has been removed, because not every user is able to request API call)
- Fixed `ProviderAsTenant` usage
- Fixed not logged Exception messages
  
📖 Documentation:
- Fix docstrings in multiple packages
- Add new contributing API guideline
- Clarify README



# vManage-client v0.10.2.post
I encourage everyone to use and contribute to vManage-client https://github.com/CiscoDevNet/vManage-client.

⭐ Help us to shine brighter by starring our repository. 
## 💦🔥Hotfix relogin

Currently, when `JSESSIONID` was detected in response we raised `CookieNotValidError` and handled exception internally to conditionally relogin when `enable_relogin` attribute was set for given session.
It is more adequate to do relogin attempt only when `JSESSIONID` contains different id (eg. it was found that PUT `/admin/user/password` can sometimes return `JSESSIONID` for exisiting session) 
Removed `CookieNotValidError` - we can inspect response cookies and act using normal flow.
Removed `AuthenticationError` as it was superficial with new flow (we will rely on `vManageAuth` for authentication and if it fails it should raise `UnauthorizedAccessError`)

https://pypi.org/project/vmngclient/0.10.2.post0/

PRs related:
- https://github.com/CiscoDevNet/vManage-client/pull/296