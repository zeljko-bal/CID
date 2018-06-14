from functools import wraps
from typing import List


class ModelSpecs:
    def __init__(self):
        specs = [callback for callback in [getattr(self, attr_name) for attr_name in dir(self)] if hasattr(callback, 'spec_type_name')]
        if not specs:
            raise Exception("No spec methods specified.")
        self.visitor = {spec_func.spec_type_name: spec_func for spec_func in specs}


class SpecModelNode:
    def __init__(self, model_value: any, path='...'):
        self.value = model_value
        self.path = path
        self.type_name = type(self.value).__name__ if self.value is not None else 'None'

    def _get_value(self, attr_name: str):
        return getattr(self.value, attr_name)

    def _get_child_path(self, child_relative_path):
        return self.path + '/' + child_relative_path

    def get(self, attr_name: str) -> 'SpecModelNode':
        self.should_exist()
        attr_value = self._get_value(attr_name) if self.has(attr_name) else None
        attr_path = self._get_child_path(attr_name)
        return SpecModelNode(attr_value, attr_path)

    def map(self, func, path='...') -> 'SpecModelNode':
        self.should_exist()
        mapped_value = func(self.value)
        mapped_path = self._get_child_path(path)
        return SpecModelNode(mapped_value, mapped_path)

    def is_equal_to(self, other_value: any) -> bool:
        return self.value == other_value

    def has(self, attr_name: str) -> bool:
        return hasattr(self.value, attr_name)

    def has_true(self, attr_name: str) -> bool:
        return self.get(attr_name).is_true()

    def has_filled(self, attr_name: str) -> bool:
        return self.has_true(attr_name)

    def is_true(self) -> bool:
        return self.value

    def is_filled(self) -> bool:
        return self.is_true()

    def exists(self) -> bool:
        return self.value is not None

    def is_of_type(self, type_name: str) -> bool:
        return self.type_name == type_name

    def should_be(self, other_value: any) -> 'SpecModelNode':
        if not self.is_equal_to(other_value):
            self._raise("An instance of type [{type_name}] should be [{other_value}]",
                        other_value=other_value)
        else:
            return self

    def shouldnt_be(self, other_value: any) -> 'SpecModelNode':
        if self.is_equal_to(other_value):
            self._raise("An instance of type [{type_name}] shouldn't be [{other_value}]",
                        other_value=other_value)
        else:
            return self

    def should_have(self, attr_name: str) -> 'SpecModelNode':
        self.should_exist()
        if not self.has(attr_name):
            self._raise("An instance of type [{type_name}] should have [{attr_name}] attribute.",
                        attr_name=attr_name)
        else:
            return self.get(attr_name)

    def shouldnt_have(self, attr_name: str) -> 'SpecModelNode':
        self.should_exist()
        if self.has(attr_name):
            self._raise("An instance of type [{type_name}] should not have [{attr_name}] attribute.",
                        attr_name=attr_name)
        else:
            return self

    def should_have_filled(self, attr_name: str) -> 'SpecModelNode':
        return self.should_have(attr_name).should_be_filled()

    def should_have_true(self, attr_name: str) -> 'SpecModelNode':
        return self.should_have(attr_name).should_be_true()

    def should_have_false(self, attr_name: str) -> 'SpecModelNode':
        return self.should_have(attr_name).should_be_false()

    def should_have_empty(self, attr_name: str) -> 'SpecModelNode':
        return self.should_have(attr_name).should_be_empty()

    def should_be_filled(self) -> 'SpecModelNode':
        self.should_exist()
        if not self.is_filled():
            self._raise("An instance of type [{type_name}] should be filled.")
        else:
            return self

    def should_be_true(self) -> 'SpecModelNode':
        self.should_exist()
        if not self.is_true():
            self._raise("An instance of type [{type_name}] should be true.")
        else:
            return self

    def should_be_empty(self) -> 'SpecModelNode':
        self.should_exist()
        if self.is_filled():
            self._raise("An instance of type [{type_name}] should be empty.")
        else:
            return self

    def should_be_false(self) -> 'SpecModelNode':
        self.should_exist()
        if self.is_true():
            self._raise("An instance of type [{type_name}] should be false.")
        else:
            return self

    def should_exist(self) -> 'SpecModelNode':
        if not self.exists():
            self._raise("An instance of type [{type_name}] shouldn't be None.")
        else:
            return self

    def shouldnt_exist(self):
        if self.exists():
            self._raise("An instance of type [{type_name}] shouldn't exist.")

    def of_type(self, type_name: str) -> 'SpecModelNode':
        self.should_exist()
        if not self.is_of_type(type_name):
            self._raise("An instance of type [{type_name}] should be of type [{required_type}]",
                        required_type=type_name)
        else:
            return self

    def each(self, attr_name: str = '') -> List['SpecModelNode']:
        list_node = self.should_have(attr_name) if attr_name else self
        list_attr_value = list_node.of_type('list').value
        return [SpecModelNode(element, self._get_child_path('{name}[{idx}]'.format(name=attr_name, idx=idx))) for idx, element in enumerate(list_attr_value)]

    def _format_message(self, message: str, **kwargs: str) -> str:
        return (message + "\n[path={path}]")\
            .format(type_name=self.type_name, path=self.path, **kwargs)

    def _raise(self, message: str, **kwargs: str):
        raise AssertionError(self._format_message(message, **kwargs))


def spec(type_name):
    def decorator(spec_func):
        spec_func.spec_type_name = type_name

        @wraps(spec_func)
        def wrapper(self, model):
            spec_func(self, SpecModelNode(model, type_name))

        return wrapper

    return decorator
