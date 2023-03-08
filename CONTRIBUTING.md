# How to contribute

I'm really glad you want to help.

### Here are some important resources:

  * Want to add something from yourself? [Make a PR](https://github.com/CiscoDevNet/vManage-client/compare) - remember to follow code guidelines.
  * Bugs? [Report it here](https://github.com/CiscoDevNet/vManage-client/issues/new?assignees=&labels=needs+review&template=bug_report.yml) - remember to provide as much information as you can.
  * Need some additional feature? [Let us know here](https://github.com/CiscoDevNet/vManage-client/issues/new?assignees=&labels=enhancement&template=feature_request.yml)

## Testing

Test newly implemented features on Cisco SD-WAN, ideally on different versions. If you don't have access to any SD-WAN you can use [Cisco provided sandboxes](https://developer.cisco.com/sdwan/sandbox/).

## Submitting changes

Make clear PR description and include doc strings in your code to make it easily understandable.

Always write a clear log message for your commits.

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

Thanks,\
vmngclient team