from functools import wraps
from inspect import getfullargspec
from types import MethodType, BuiltinMethodType
from contextlib import contextmanager


class ModelProcessor:
    def __init__(self, callbacks, allow_revisiting=False):
        self.callbacks = callbacks
        self.allow_revisiting = allow_revisiting
        self.parent_stack = []
        self.visited = []

    def element_type_name(self, element):
        raise NotImplementedError('ModelProcessor.element_type_name not implemented in derived class.')

    @contextmanager
    def parent(self, model):
        self.parent_stack.append(model)
        yield
        self.parent_stack.pop()

    def invoke(self, element):
        if not self.allow_revisiting and element in self.visited:
            return

        callback = self.callbacks.get(self.element_type_name(element))
        if callback:
            args_count = len(getfullargspec(callback).args)
            if isinstance(callback, (MethodType, BuiltinMethodType)):
                args_count -= 1
            if args_count == 1:
                callback(element)
            else:
                callback(element, self.parent_stack)

            self.visited.append(element)


def self_first_with_parent(func):
    return self_first(with_parent(func))


def self_last_with_parent(func):
    return self_last(with_parent(func))


def with_parent(func):
    @wraps(func)
    def wrapper(self: ModelProcessor, node):
        with self.parent(node):
            func(self, node)

    return wrapper


def self_first(func):
    @wraps(func)
    def wrapper(self: ModelProcessor, node):
        self.invoke(node)
        func(self, node)

    return wrapper


def self_last(func):
    @wraps(func)
    def wrapper(self: ModelProcessor, node):
        func(self, node)
        self.invoke(node)

    return wrapper
