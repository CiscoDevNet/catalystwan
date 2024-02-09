# Configuration Group - Creation of First and Second Layer

This README document provides guidelines on creating configuration groups within the `Cisco Catalyst WAN SDK` repository.

## Guidelines for Creating Config Groups

### 1. Directory Structure

Place every model in the `models` directory. 

For endpoints, use `endpoints/configuration/feature_profiles/sdwan/*.py`. 

For models, use `models/configuration/feature_profiles/sdwan/*.py`.

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

### 5. Case Sensitivity

When dealing with multiple proper nouns in a class name in Python, it's customary to use CamelCase, where each proper noun is capitalized. If we consider `VANWPN` as an acronym or initialism for multiple proper nouns, you might structure your class name like this:

```python
class VanWpn:
    # Class implementation goes here
```

This adheres to Python's PEP 8 style guide, which recommends using CamelCase for class names. Following this convention makes your code more readable and aligns with the standard practices in the Python community.

https://peps.python.org/pep-0008/#descriptive-naming-styles

### 6. Excluding values

Utilize `model_validator` for two or more excluding values.

### 7. Pipeline and Integration Tests

- Implement a pipeline and integration tests. (TODO: Provide details)


If you have any questions or need further clarification, please reach out to the project maintainers. Thank you for your contribution!
