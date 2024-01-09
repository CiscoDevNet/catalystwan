# Configuration Group - Creation of First and Second Layer

This README document provides guidelines on creating configuration groups within the `vManage-client` repository.

## Guidelines for Creating Config Groups

### 1. Directory Structure

Place every model in the `models` directory. 

For endpoints, use `endpoints/configuration/feature_profiles/sdwan/*.py`. 

For models, use `model/configuration/feature_profiles/sdwan/*.py`.

### 2. Default Values

Use `Default[None]` for `Defaults` without values.

Example:
```python
auto_sim: Union[Variable, Global[bool], Default[None]]
```

`auto_sim` can be set as `Default` but without the value.

### 3. Literals vs Enums

Use `Enums` over the `Literals`. Justification:
- `Enum` provides IntelliSense.
- Both provides static typing safety.
- `Enum` can be treated as a `str`.

### 4. Naming Conventions

- Avoid explicit naming `MyAwesomeEntityParcel`. Use `MyAwesomeEntity` instead.

