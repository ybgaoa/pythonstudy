# -*- coding: utf-8 -*-

'''
@author: wfliu
'''

import logging

from inspect import isclass
from abc import abstractmethod
from importlib import import_module
from commons.action_view import ACTIONS
from commons.action_view import ActionView

logger = logging.getLogger('popcorn')


class Listener():
    @abstractmethod
    def init(self, app):
        pass


def get_view_model(view):
    try:
        return import_module(view + '.views')
    except:
        return None


class ViewListener(Listener):
    def init(self, app):
        actions = {}

        obj = get_view_model(app)
        if obj:
            for v in dir(obj):
                cv = getattr(obj, v)
                if type(cv) is type and issubclass(cv, ActionView):
                    for key, value in cv.__dict__.items():
                        if not callable(value):
                            continue
                        if getattr(value, 'wsgi_action', None):
                            actions[value.wsgi_action] = value
                    ACTIONS[cv] = actions


class DependencyListener(Listener):
    def init(self, app):
        if app.__contains__('study.'):
            scan_m = ['.sql', '.core']
            for package in scan_m:
                try:
                    mod_name = app + package
                    module = import_module(mod_name)
                    if module:
                        for obj in dir(module):
                            if obj.endswith('Driver') or obj.endswith('Manager'):
                                cls = getattr(module, obj, None)
                                if cls and isclass(cls):
                                    try:
                                        cls()
                                    except Exception as e:
                                        # logger.warning(msg=msg)
                                        pass
                except ImportError as e:
                    msg = 'loading module "' + (app + package) + '" failure. the reason is [' + e.message + ']'
                    logger.warning(msg=msg)
