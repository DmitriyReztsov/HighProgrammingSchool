import abc
import json
from copy import copy, deepcopy
from typing_extensions import Self


class General(object, metaclass=abc.ABCMeta):
    """Для последних (3.4+) версий Питона эта запись устаревшая, необходимо просто наследовать
    от abc.ABC класса. Так же нет смысла наследоваться от object, поскольку все классы наследуют
    от этого базового класса. В примере это показано для наглядности - наследуемся от базового
    класса и объявляем класс абстрактным.
    """

    @abc.abstractmethod
    def copy(self, dest_obj: Self) -> Self: ...

    @abc.abstractmethod
    def deepcopy(self, des_obj: Self) -> Self: ...

    @abc.abstractmethod
    def clone(self) -> Self: ...

    @abc.abstractmethod
    def __eq__(self, obj: Self, shallow: bool = True) -> bool: ...

    @abc.abstractmethod
    def to_json(self) -> str: ...

    @abc.abstractmethod
    def from_json(self) -> Self: ...

    @abc.abstractmethod
    def as_str(self) -> str: ...

    @abc.abstractmethod
    def is_type(self, type_to_check: object) -> bool: ...

    @abc.abstractmethod
    def get_type(self) -> str: ...


class Any(General):
    def copy(self, dest_obj):
        attrs_dict = self.__dict__
        for attr_name, attr_value in attrs_dict:
            if isinstance(attr_value, (list, dict, tuple)):
                attr_name = copy(attr_name)
            setattr(dest_obj, attr_name, attr_value)

    def deepcopy(self, dest_obj):
        attrs_dict = self.__dict__
        for attr_name, attr_value in attrs_dict:
            if isinstance(attr_value, Any):
                deepcopy_obj = type(attr_value)()
                attr_value.deepcopy(deepcopy_obj)
            if isinstance(attr_value, (list, dict, tuple)):
                attr_name = deepcopy(attr_name)
            setattr(dest_obj, attr_name, attr_value)

    def clone(self):
        cloned_obj = type(self)()
        self.deepcopy(cloned_obj)
        return cloned_obj

    def equals(self, obj):
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

    def as_str(self):
        return self.__str__()

    def to_json(self):
        attrs_dict: dict = self.__dict__
        json_dict = {}
        for attr_name, attr_value in attrs_dict:
            if isinstance(attr_value, Any):
                json_dict[attr_name] = attr_value.to_json()
            else:
                json_dict[attr_name] = attr_value
        return json.dumps(json_dict)

    def from_json(self, json_data: str):
        attrs_dict = json.loads(json_data)
        respored_obj = Any()
        respored_obj.__dict__ = attrs_dict
        return respored_obj

    def get_type(self):
        return type(self)

    def is_type(self, type_to_check):
        return isinstance(self, type_to_check)
