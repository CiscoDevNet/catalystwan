# How to use

## Feature Template Creation

```python
omp_vsmart = OMPvSmart(
    name="my_first_template",
    description="NA",
    device_models=[DeviceModel.VSMART]
    
)

session.api.templates.create(omp_vsmart)
```

## Add new Feature Template in Cisco Catalyst WAN SDK
These steps will help you to automate feature template creation. We'll explain what to do and why, so everyone will have deep understanding how our templates work. In the example we will try to create `OMP` Feature Template for vSmart. 

1. Get your template type name and version. 
    >Note: display name is not template type name!
- For example, you could extract it from response body. Go to your Manager and create any template which you would like to automate in catalystwan. Send template creation request and check for `templateType` and `templateMinVersion` variable names. `OMP` (display name) for vSmart has `omp-vsmart` template type name.

2. With corresponding `templateType` we are able to create new class which implements `FeatureTemplate` interface. Create new file in `catalystwan\api\templates\models\` and copy-paste the code and change name of the class with its type attribute.

	```python
	from pathlib import Path
	from typing import ClassVar
	from pydantic import ConfigDict
	from catalystwan.api.templates.feature_template import FeatureTemplate


	class OMPvSmart(FeatureTemplate):
		model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
			
		payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
		type: ClassVar[str] = "omp-vsmart"
	```
3. (This step is temporary) Find `is_created_by_generator` method in `template_api` and add your new template class.

	```python
	ported_templates = (..., OMPvSmart)
	```
	NOTE: This step will be removed once all template payloads will be generated automatically.
4. (This step is temporary) Find `available_models` definition in 'supported' and add your new template class.
	```python
	available_models = {
		(...)
		'omp_vsmart': OMPvSmart
	}
	```
	NOTE: This step will be removed once all template payloads will be generated dynamically.
5. We can try to create our first template with default values.
   ```python
	omp_vsmart = OMPvSmart(
		name="my_first_template",
		description="NA",
		device_models=[DeviceModel.VSMART]
	)

	session.api.templates.create(omp_vsmart)
	```
	If everything went successfuly, we will get similar message 

	`Template my_first_template (FeatureTemplate) was created successfully (7e56acdd-640e-45dc-9335-87abc697995f).`

6. We can check whether our template is created sucessfully in Manager manually. If there is an error, please create an issue with error and try go to the 7th step.
   
### Customize Feature Template fields.
7. Run below code with already created session and changed corresponding variables.

    ```python
    # TODO: Use 2nd layer.
    import json


    template_type = "omp-vsmart" # Change this value
    template_version = "15.0.0" # Change this value
    endpoint = f"/dataservice/template/feature/types/definition/{template_type}/{template_version}"

    schema = session.get(url=endpoint).json()

    with open(f"response_{template_type}.json", "w") as f:
        f.write(json.dumps(schema, indent=4))
    ```

8. Open `response_{template_type}.json` file.
9. Find `fields` key. The value should be list of dictionaries. Get every possible key in the dictionary and fill our class with every possible key. You can find the code in `catalystwan\api\templates\models\omp_vsmart_model.py` file.
