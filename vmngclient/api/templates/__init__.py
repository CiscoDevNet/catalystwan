"""Contains a list of feature templates.

These feature template models are used to create and modify the templates
on the vManage server.

In addition, they are used to convert CLI config into separate feature
templates in vManage.
"""

# Basic FeatureTemplate class
from vmngclient.api.templates.feature_template import FeatureTemplate

# CEdge Templates
from vmngclient.api.templates.payloads.tenant.tenant_model import TenantModel

__all__ = [
    "FeatureTemplate",
    "TenantModel",
]
