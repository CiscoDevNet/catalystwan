# from typing import Dict, Generic, Type, TypeVar

# from vmngclient.api.configuration_groups.parcel import Parcel

# ParcelModel = TypeVar("ParcelModel", bound=Parcel)


# class Builder(Generic[ParcelModel]):
#     model: Type[ParcelModel]
#     values: Dict[str, object]

#     def __init__(self, model: Type[ParcelModel]) -> None:
#         super().__setattr__("model", model)
#         super().__setattr__("values", {})

#     def __setattr__(self, name: str, value: object) -> None:
#         self.values[name] = value

#     def build(self) -> ParcelModel:
#         return self.model(**self.values)
