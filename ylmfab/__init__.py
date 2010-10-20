#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

VERSION = (0, 1, 0)

def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2] != 0:
        version = "%s.%s" % (version, VERSION[2])
    return version

__version__ = get_version()

from .constants import *
from .models import Dependency
try:
    from .raw_tools import *
    from .tools import *
except ImportError:
    pass
