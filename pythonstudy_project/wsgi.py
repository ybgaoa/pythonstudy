"""
WSGI config for Popcorn project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from pythonstudy_project.settings import INSTALLED_APPS
from pythonstudy_project.settings import APP_LISTENERS

from django.utils import six
from importlib import import_module


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pythonstudy_project.settings")

app_listeners = []
for listener in APP_LISTENERS:
    try:
        module_path, class_name = listener.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % listener
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])
    module = import_module(module_path)
    cls = getattr(module, class_name)
    app_listeners.append(cls())

for app in INSTALLED_APPS:
    for l in app_listeners:
        l.init(app)

application = get_wsgi_application()