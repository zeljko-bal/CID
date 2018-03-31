from functools import wraps, reduce
from inspect import getfullargspec
from types import MethodType, BuiltinMethodType
from contextlib import contextmanager
from cid.utils.common import *


class ModelProcessor:
    def __init__(self, callbacks, allow_revisiting=False):
        self.callbacks = callbacks
        self.allow_revisiting = allow_revisiting
        self.parent_stack = []
        self.visited = []

    @contextmanager
    def parent(self, model):
        self.parent_stack.append(model)
        yield
        self.parent_stack.pop()

    def invoke(self, element):
        if not self.allow_revisiting and element in self.visited:
            return

        callback = self.callbacks.get(element_type(element))
        if callback:
            args_count = len(getfullargspec(callback).args)
            if isinstance(callback, (MethodType, BuiltinMethodType)):
                args_count -= 1
            if args_count == 1:
                callback(element)
            else:
                callback(element, self.parent_stack)

            self.visited.append(element)

    @staticmethod
    def depth_first(func):
        return ModelProcessor.process_self_last(ModelProcessor.with_parent(func))

    @staticmethod
    def breadth_first(func):
        return ModelProcessor.process_self_first(ModelProcessor.with_parent(func))

    @staticmethod
    def with_parent(func):
        @wraps(func)
        def wrapper(self, node):
            with self.parent(node):
                func(self, node)

        return wrapper

    @staticmethod
    def process_self_first(func):
        @wraps(func)
        def wrapper(self, node):
            self.invoke(node)
            func(self, node)

        return wrapper

    @staticmethod
    def process_self_last(func):
        @wraps(func)
        def wrapper(self, node):
            func(self, node)
            self.invoke(node)

        return wrapper
