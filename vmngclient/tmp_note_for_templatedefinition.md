How the example look like:


```python
cs_model = CiscoSystemModel(
    name="test_python",
    description="zzz",
    site_id=2,
    bps=1,
    system_ip="172.168.1.1",
    overlay_id=1
)

cs_model = template_api.get_feature_template(template_name="test_python")
# cs_model = FeatureTemplate.get("test_python", session)
cs_model.bps = 2

template_api.edit(cs_model)
```


Order of tasks:
1.	dataclass for TemplateFieldDefinition
2.	FeatureTemplate is interface -> add there class method for get()
3.	Deserialize response to TemplateFieldDefinition, and create destination FeatureTemplateModel
4.	Upadate object of FeatureTemplateModel with desired value
5.	Try to send new template (meaning use .edit())






Available structures



```json

1. "field_name": empty dict :

"flow-control": {},
"clear-dont-fragment": {},


2. "field_name": TemplateFieldDefinition ==  TemplateField.name: TemplateField.definition

"dhcp-distance": {
    "vipObjectType": "object",
    "vipType": "ignore",
    "vipValue": 1,
    "vipVariableName": "vpn_if_ipv4_dhcp_distance"
},
"description": {
    "vipObjectType": "object",
    "vipType": "ignore",
    "vipVariableName": "vpn_if_description"
},
"secondary-address": {
    "vipType": "ignore",
    "vipValue": [],
    "vipObjectType": "tree",
    "vipPrimaryKey": [
        "address"
    ]
}


3. TemplateField.name: dict{TemplateField.name: TemplateField.definition} :
   "ipv6"              TemplateField.template_dicts
"ipv6": {
    "access-list": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
            "direction"
        ]
    },
    "address": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "",
        "vipVariableName": "vpn_if_ipv6_ipv6_address"
    }
}


4. TemplateField.name: TemplateField.definition

    but

    TemplateField.definition.vip_value = List[Dict{ TemplateField.name: TemplateField.definition   |  "priority-order": List[TemplateField.name]  }]

    "dns": {
        "vipType": "constant",
        "vipValue": [
            {
                "role": {
                    "vipType": "constant",
                    "vipValue": "primary",
                    "vipObjectType": "object"
                },
                "dns-addr": {
                    "vipType": "variableName",
                    "vipValue": "",
                    "vipObjectType": "object",
                    "vipVariableName": "vpn_dns_primary"
                },
                "priority-order": [
                    "dns-addr",
                    "role"
                ]
            }
        ],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
            "dns-addr"
        ]
    }


5. TemplateField.name: dict{TemplateField.name: TemplateField.definition}

"ip": {
    "route": {
        "vipType": "constant",
        "vipValue": [
            {
                "prefix": {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": "0.0.0.0/0",
                    "vipVariableName": "vpn_ipv4_ip_prefix"
                },
                "next-hop": {
                    "vipType": "constant",
                    "vipValue": [
                        {
                            "address": {
                                "vipObjectType": "object",
                                "vipType": "variableName",
                                "vipValue": "",
                                "vipVariableName": "vpn_next_hop_ip_address_0"
                            },
                            "distance": {
                                "vipObjectType": "object",
                                "vipType": "ignore",
                                "vipValue": 1,
                                "vipVariableName": "vpn_next_hop_ip_distance_0"
                            },
                            "priority-order": [
                                "address",
                                "distance"
                            ]
                        }
                    ],
                    "vipObjectType": "tree",
                    "vipPrimaryKey": [
                        "address"
                    ]
                },
                "priority-order": [
                    "prefix",
                    "next-hop",
                    "next-hop-with-track"
                ]
            }
        ],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
            "prefix"
        ]
    }
}
```