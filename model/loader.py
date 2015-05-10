# -*- encoding:utf8 -*-

import sys
import pkgutil

from metaclass.singleton import Singleton
from plugins.base.responsebase import IResponseBase


class PluginLoader(object):

    __metaclass__ = Singleton
    plugins = []

    def __init__(self):
        self.plugins = []
        self._load_modules()

    def _load_modules(self):
        pkg = 'model.plugins'
        prefix = pkg + '.'
        package = sys.modules[pkg]
        reload(package)
        for importer, m, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            if m.endswith("base") or m.endswith("IResponseBase"):
                continue
            t = __import__(m, {}, {}, ['*'])
            for l in (l for l in dir(t) if not l.startswith('_')):
                if l == IResponseBase.__name__:
                    continue
                c = getattr(t, l)
                try:
                    if not c.__module__.startswith(pkg):
                        continue
                except:
                    continue
                self.plugins.append(getattr(t, l))

    def get_plugins(self):
        print("Plugin size : %r" % len(self.plugins))
        return self.plugins
