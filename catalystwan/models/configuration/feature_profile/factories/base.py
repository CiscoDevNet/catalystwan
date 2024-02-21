class BaseFactory:
    DELETE_PROPERTIES: tuple = tuple()

    def __init__(self, name, description, template_values):
        self.template_values = template_values
        self.template_values["name"] = name
        self.template_values["description"] = description

        if self.DELETE_PROPERTIES:
            for del_key in self.DELETE_PROPERTIES:
                if del_key in self.template_values:
                    del self.template_values[del_key]

    def create_parcel(self):
        raise NotImplementedError()
