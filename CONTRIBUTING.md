# How to contribute

We're really glad you want to help.

## Here are some important resources:

  * Want to add something from yourself? [Make a PR](https://github.com/CiscoDevNet/vManage-client/pulls) - remember to follow code guidelines.
    ### Contributors from CiscoDevNet organization:
    To make a PR - pull the repository, create branch for your changes, make said changes and make the pull request. Now just wait for the review and feedback from our developers.  
    ### Contributors outside CiscoDevNet organization
    To make a PR - fork our repository, make your changes and make the pull request. Now just wait for the review and feedback from our developers.
  * Feel free to review existing [PR](https://github.com/CiscoDevNet/vManage-client/pulls)s, any suggestion is welcome.
  * Want to help but you don't have any new ideas for improvement or feature? Take any [issue](https://github.com/CiscoDevNet/vManage-client/issues) and fix it.
  * Bugs? [Report it here](https://github.com/CiscoDevNet/vManage-client/issues/new?assignees=&labels=needs+review&template=bug_report.yml) - remember to provide as much information as you can.
  * Need some additional feature? [Let us know here](https://github.com/CiscoDevNet/vManage-client/issues/new?assignees=&labels=enhancement&template=feature_request.yml)

## Testing

Test newly implemented features on Cisco SD-WAN, ideally on different versions. If you don't have access to any SD-WAN you can use [Cisco provided sandboxes](https://developer.cisco.com/sdwan/sandbox/).

- **Building package for tests**\
  To make a `.whl` file run
  ```
  poetry build
  ```
  Then in `/vManage-client/dist/` directory there is a `.whl` file named `vmngclient-<version>-py3-none-any.whl`, which can be installed by running
  ```
  pip install vmngclient-<version>-py3-none-any.whl
  ```

## Submitting changes

Make clear PR description and include doc strings in your code to make it easily understandable.

Always write a clear log message for your commits.

## Enviroment setup
1. Download Python3.8 or higher.
2. Download repository
    ```
    git clone https://github.com/CiscoDevNet/vManage-client.git
    ```
3. Install and configure poetry (v1.3.1 or higher)
    https://python-poetry.org/docs/#installation

    On linux/mac this usually means:
    ```
    curl -sSL https://install.python-poetry.org | python3 -
    poetry config virtualenvs.in-project true
    ```
4. Install dependecies 
    ```
    poetry install
    ```
5. Activate `pre-commit`
    ```
    pre-commit install
    ```
### Environment Variables
- `VMNGCLIENT_DEVEL` when set: loggers will be configured according to `./logging.conf` and `urllib3.exceptions.InsecureRequestWarning` will be suppressed

## Code guidelines

Start reading our code, and you'll get the hang of it.

  * Make sure you run pre-commit on your code before submitting it, it will make sure you follow rules we use:
    * line length below 120
    * double quotes
    * [isort](https://pypi.org/project/isort/)
    * [black](https://pypi.org/project/black/)
    * [mypy](https://pypi.org/project/mypy/)
    * [flake8](https://pypi.org/project/flake8/)
  * Use clear naming and add description with examples.
  * Use [Google Style Python Docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
  * Add unit tests to your code.

## Introducing new API

  ### API Endpoints:
  vManage-client APIs should make requests only through API Endpoints layer. This layer defines:
  * http method
  * endpoint url
  * payload data-model (subtyping `vmngclient.dataclasses.DataclassBase` or `pydantic.BaseModel` and others)
  * return type (subtyping `vmngclient.dataclasses.DataclassBase` or `pydantic.BaseModel` and others)
  * allowed sessions/views
  * supported versions

  Example:

  ```python
  from pydantic.v1 import BaseModel, Field
  from typing import List
  from vmngclient.endpoints import APIEndpoints, request, versions, view
  from vmngclient.utils.session_type import ProviderView

  class TenantBulkDeleteRequest(BaseModel):
      password: str
      tenant_id_list: List[str] = Field(alias="tenantIdList")

  class TenantTaskId(BaseModel):
      id: str

  class TenantManagement(APIEndpoints):

      @versions(">=20.4")
      @view({ProviderView})
      @request("DELETE", "/tenant/bulk/async")
      def delete_tenant_async_bulk(self, payload: TenantBulkDeleteRequest) -> TenantTaskId:
          ...
  ```

  Please note that when using `@request` decorator method must have no body. Request will be built automatically and return value based on defined type will be provided.

  API endpoints Definitions can be found in: `vmngclient/endpoints` directory.

  The organization of items **strictly** follows an OpenAPI spec: https://developer.cisco.com/docs/sdwan/#!sd-wan-vmanage-v20-9

  Auto generated python methods names can be found in: https://github.com/sbasan/vmanage-python-open-api/blob/main/README.md

  If common data-model is being reused by more than one `APIEndpoints` class it should be moved to `vmngclient/model` folder with appropriate module name.

  Dedicated pre-commit step will automatically check corectness and add documentation for endpoints with `@request` decorator.

  Custom payload types are allowed (eg. for sending various types of files) please check example: [**SoftwarePackageUpdatePayload**](vmngclient/utils/upgrades_helper.py#L68)

1. Check that endpoints you want to utilize in your API already defined in `vmngclient/endpoints`.
2. If endpoint not present, create new file with endpoint including data-model and methods with `@request`, `@view` and `@versions` decorators when needed.
3. Implement higher level API in `vmngclient/api` using created endpoints.

Thanks,\
vmngclient team
