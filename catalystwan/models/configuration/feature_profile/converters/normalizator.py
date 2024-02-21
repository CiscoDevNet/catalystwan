import json
from typing import cast

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.utils.feature_template import find_template_values


def template_definition_normalization(template_definition):
    """
    Normalizes a template definition by changing keys to snake_case and casting all leafs values to global types.

    Args:
        template_definition (str): The template definition in JSON format.

    Returns:
        dict: The normalized template values.

    """

    print(f"TEMPLATE DEF :{template_definition}")

    def to_snake_case(s: str):
        """
        Converts a string from kebab-case to snake_case.

        Args:
            s (str): The string to be converted.

        Returns:
            str: The converted string.

        """
        if "-" in s:
            temp = s.split("-")
            return "_".join(ele for ele in temp)
        return s

    def transform_dict(d):
        """
        Transforms a nested dictionary into a normalized form.

        Args:
            d (dict): The nested dictionary to be transformed.

        Returns:
            dict: The transformed dictionary.

        """
        if isinstance(d, list):
            return [transform_dict(i) if isinstance(i, (dict, list)) else i for i in d]
        return {to_snake_case(a): transform_dict(b) if isinstance(b, (dict, list)) else b for a, b in d.items()}

    def cast_leafs_to_global(node: dict):
        """
        Recursively casts all leaf values in a nested dictionary or list to the global configuration type.

        Args:
            node (dict): The nested dictionary or list to be processed.

        Returns:
            None

        """
        for key, item in node.items():
            if isinstance(item, dict):
                cast_leafs_to_global(item)
            elif isinstance(item, list):
                for i in item:
                    if isinstance(i, dict):
                        cast_leafs_to_global(i)
            else:
                node[key] = as_global(item)

    template_definition_as_dict = json.loads(cast(str, template_definition))
    print(f"template_definition_as_dict : {template_definition_as_dict}")
    template_values = find_template_values(template_definition_as_dict)
    print(f"find_template_values:{template_values}")
    template_values = transform_dict(template_values)
    print(f"ID OF DICT :{id(template_values)}")
    cast_leafs_to_global(template_values)
    print(f"cast_leafs_to_global:{template_values}")
    return template_values
