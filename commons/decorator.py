# -*- coding: utf-8 -*-

import copy
from django.core.cache import cache

def action(name):
    def decorator(func):
        func.wsgi_action = name
        return func

    return decorator


def generate_key_name(prefix, *args):
    for a in args:
        if isinstance(a, basestring):
            return prefix + str(a)


def _validate_key_id(*args):
    flag = False
    for a in args:
        if isinstance(a, basestring):
            flag = True
            break
    return flag


def cache_get(key):
    def decorator(func):
        def wrapped(*args, **kwargs):
            if _validate_key_id(*args):
                key_name = generate_key_name(key, *args)
                if cache.get(key_name):
                    return cache.get(key_name)
                else:
                    result = func(*args, **kwargs)
                    cache.set(key_name, result)
                    return result
            else:
                return func(*args, **kwargs)

        return wrapped

    return decorator


def cache_delete(key):
    def decorator(func, *args, **kwargs):
        def wrapped(*args, **kwargs):
            if _validate_key_id(args):
                key_name = generate_key_name(key, args)
                if cache.get(key_name):
                    cache.delete(key_name)
                return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapped

    return decorator


def cache_set(key):
    def decorator(func, *args, **kwargs):
        def wrapped(*args, **kwargs):
            if _validate_key_id(args):
                key_name = generate_key_name(key, args)
                result = func(*args, **kwargs)
                cache.set(key_name, result)
                return result
            else:
                return func(*args, **kwargs)

        return wrapped

    return decorator


def permission(perm_class=None, msg=None):
    def wrappered(self, *args, **kwargs):
        self.message = msg

    def wrapper(cls):
        assert perm_class is not None, (
            'perm_class parameter is not None!'
        )
        perm_class.__init__ = wrappered
        origin_permission_classes = copy.deepcopy(cls.permission_classes)
        origin_permission_classes.append(perm_class)
        cls.permission_classes = origin_permission_classes
        return cls

    return wrapper
