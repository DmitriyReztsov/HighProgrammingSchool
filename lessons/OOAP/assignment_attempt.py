import json
from copy import copy, deepcopy
from typing import Any, final
from typing_extensions import Self


class General(object):
    @final
    def copy(self, dest_obj: Self) -> Self:
        attrs_dict = self.__dict__
        for attr_name, attr_value in attrs_dict:
            if isinstance(attr_value, (list, dict, tuple)):
                attr_name = copy(attr_name)
            setattr(dest_obj, attr_name, attr_value)

    @final
    def deepcopy(self, dest_obj: Self) -> Self:
        attrs_dict = self.__dict__
        for attr_name, attr_value in attrs_dict:
            if isinstance(attr_value, Any):
                deepcopy_obj = type(attr_value)()
                attr_value.deepcopy(deepcopy_obj)
            if isinstance(attr_value, (list, dict, tuple)):
                attr_name = deepcopy(attr_name)
            setattr(dest_obj, attr_name, attr_value)

    @final
    def clone(self) -> Self:
        cloned_obj = type(self)()
        self.deepcopy(cloned_obj)
        return cloned_obj

    @final
    def equals(self, obj: Self) -> bool:
        attrs_dict_self: dict = self.__dict__
        attrs_dict_obj: dict = obj.__dict__

        if set(attrs_dict_obj.keys()) != set(attrs_dict_self.keys()):
            return False

        attrs_names = attrs_dict_self.keys()
        for attr in attrs_names:
            self_value = getattr(self, attr)
            obj_value = getattr(obj, attr)
            if not type(self_value) is type(obj_value):
                return False
            if isinstance(self_value, Any):
                self_value.equals(obj_value)
            elif self_value != obj_value:
                return False
        return True

    @final
    def as_str(self) -> str:
        return self.__str__()

    @final
    def to_json(self) -> str:
        attrs_dict: dict = self.__dict__
        json_dict = {}
        for attr_name, attr_value in attrs_dict:
            if isinstance(attr_value, Any):
                json_dict[attr_name] = attr_value.to_json()
            else:
                json_dict[attr_name] = attr_value
        return json.dumps(json_dict)

    @final
    def from_json(self, json_data: str) -> Self:
        attrs_dict = json.loads(json_data)
        respored_obj = Any()
        respored_obj.__dict__ = attrs_dict
        return respored_obj

    @final
    def get_type(self) -> str:
        return type(self)

    @final
    def is_type(self, type_to_check: object) -> bool:
        return isinstance(self, type_to_check)

    @staticmethod
    def assignment_attempt(target: Any, source: Any) -> None:
        if isinstance(source, type(target)):
            target = source
            return
        target = Void


class AnyCustom(General):
    pass


@final
class Void(AnyCustom):
    """None не может быть именем класса"""

    pass
