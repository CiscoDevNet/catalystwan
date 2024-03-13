from typing import List

from catalystwan.api.templates.device_template.device_template import GeneralTemplate


def flatten_general_templates(general_templates: List[GeneralTemplate]) -> List[GeneralTemplate]:
    """
    Recursively flattens a list of GeneralTemplate objects.

    Args:
        general_templates (List[GeneralTemplate]): The list of GeneralTemplate objects to flatten.

    Returns:
        List[GeneralTemplate]: The flattened list of GeneralTemplate objects.
    """
    result = []
    for gt in general_templates:
        sub_templates = gt.subTemplates
        gt.subTemplates = []
        result.append(gt)
        result.extend(flatten_general_templates(sub_templates))
    return result
