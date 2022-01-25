from functools import partial
from inspect import isroutine
from numbers import Number
import inspect
from apretty import apretty
import sys

import itertools
from types import FunctionType

base_types = tuple([list, tuple, set, dict, int, float,
                   complex, str, bytes, bool, set, frozenset])
def whatis(obj: object):
    objis = set()

    if inspect.ismodule(obj):
        objis.add("module")
    if inspect.isclass(obj):
        objis.add("class")
    if inspect.ismethod(obj):
        objis.add("method")
    if inspect.isfunction(obj):
        objis.add("function")
    if inspect.isgeneratorfunction(obj):
        objis.add("generatorfunction")
    if inspect.isgenerator(obj):
        objis.add("generator")
    if inspect.iscoroutinefunction(obj):
        objis.add("coroutinefunction")
    if inspect.iscoroutine(obj):
        objis.add("coroutine")
    if inspect.isawaitable(obj):
        objis.add("awaitable")
    if inspect.isasyncgenfunction(obj):
        objis.add("asyncgenfunction")
    if inspect.isasyncgen(obj):
        objis.add("asyncgen")
    if inspect.istraceback(obj):
        objis.add("traceback")
    if inspect.isframe(obj):
        objis.add("frame")
    if inspect.iscode(obj):
        objis.add("code")
    if inspect.isbuiltin(obj):
        objis.add("builtin")
    if inspect.isroutine(obj):
        objis.add("routine")
    if inspect.isabstract(obj):
        objis.add("abstract")
    if inspect.ismethoddescriptor(obj):
        objis.add("methoddescriptor")
    if inspect.isdatadescriptor(obj):
        objis.add("datadescriptor")
    if inspect.isgetsetdescriptor(obj):
        objis.add("getsetdescriptor")
    if inspect.ismemberdescriptor(obj):
        objis.add("memberdescriptor")
    if isinstance(obj, base_types):
        objis.add("base")

    return objis


def is_method(obj):
    w = whatis(obj)
    if w and "routine" in w:
        return True

    return False

def _list_members(cls):
    return set(x for x, y in inspect.getmembers(cls))

def _list_methods(cls):
    # return set(x for x, y in cls.__dict__.items()
    #            if "routine" in whatis(y))
    return set(x for x, y in inspect.getmembers(cls, is_method))

def _list_parent_methods(cls):
    if not isinstance(cls, type):
        bases = [type(cls)]
    else:
        bases = getattr(cls, "__bases__", [])

    return set(itertools.chain.from_iterable(
        _list_members(c).union(_list_parent_methods(c)) for c in bases))

def subclass_methods(cls):
    methods = _list_methods(cls)
    parent_methods = _list_parent_methods(cls)
    return methods.difference(parent_methods)
    # return set(cls for cls in methods if not (cls in parent_methods))


# list attributes (by listing non-methods) -- is there a better way?
# def _list_attrs(cls):
#     return set(x for x, y in cls.__dict__.items()
#                if "routine" not in whatis(y))

# def _list_parent_attrs(cls):
#     return set(itertools.chain.from_iterable(
#         _list_attrs(c).union(_list_parent_attrs(c)) for c in cls.__bases__))

# def subclass_attrs(cls):
#     attrs = _list_attrs(cls)

#     parent_attrs = _list_parent_attrs(cls)
#     return set(cls for cls in attrs if not (cls in parent_attrs))


# list data (stuff that's not an attribute or method)
def is_not_method(obj):
    return not is_method(obj)

def _list_data(cls):
    if type(cls) is type:
        return set()

    # return set(x for x in dir(cls) if x not in getattr(cls, "__dict__", []))
    return set(x for x, y in inspect.getmembers(cls, is_not_method))

def _list_parent_data(cls):
    if not isinstance(cls, type):
        bases = [type(cls)]
    else:
        bases = getattr(cls, "__bases__", [])
    return set(itertools.chain.from_iterable(
        _list_members(c).union(_list_parent_data(c)) for c in bases))

def subclass_data(cls):
    datas = _list_data(cls)
    parent_datas = _list_parent_data(cls)

    return datas.difference(parent_datas)
    # return set(x for x in datas if not (x in parent_data))


def print_class_hierarchy(cls):
    seen = set()
    for t in reversed(type(cls).__mro__):
        seen.add(t)
        print(f"\n===== {str(t)} =====")
        print("  Methods:")
        meth = subclass_methods(t)
        if meth:
            print("    " + str(sorted(meth)))
        else:
            print("    --None--")

        print("\n  Attrs:")
        att = subclass_attrs(t)
        if att:
            print("    " + str(sorted(att)))
        else:
            print("  Attributes: --None--")


def print_thing(name, mro, meth, data):
    print(f"\n===== {name} =====")
    print(f"  MRO: {mro}")

    print("  Methods:")
    if meth:
        print("    " + str(sorted(meth)))
    else:
        print("    --None--")

    print("\n  Attrs and data:")
    if data:
        print("    " + str(sorted(data)))
    else:
        print("    --None--")


def print_class_hierarchy_r(cls, seen=None):
    if seen is None:
        seen = set()

    if not isinstance(cls, type):
        print_class_hierarchy_r(type(cls), seen)

    if getattr(type(cls), "__mro__", None) is not None:
        for t in reversed(type(cls).__mro__):
            if t in seen:
                continue

            seen.add(t)

            mro = [str(x) for x in t.__mro__]
            meth = subclass_methods(t)
            data = subclass_data(t)

            print_thing(str(t), mro, meth, data)

            print_class_hierarchy_r(t, seen)

    # if getattr(cls, "__mro__", None) is None:
    if not isinstance(cls, type):
        meth = subclass_methods(cls)
        data = subclass_data(cls)

        print_thing("<instance>", "--None--", meth, data)
