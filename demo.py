#!/usr/bin/env python
# encoding=utf-8

'''
    Example fab file for use with ylmfab.

    Usage:
    $ fab -f demo.py deploy
'''

import os

from fabric.api import *
import ylmfab

# dependencies as Dependency objects

bolibana = ylmfab.Dependency()
bolibana.url = 'git://github.com/bolibana/bolibana.git'
bolibana.branch = 'who'
bolibana.lib_path = os.path.join('lib', 'rapidsms')
bolibana.lib_name = 'rapidsms'
bolibana.pip_file = 'pip-requires.txt'
bolibana.revision = 'ac43a836e0de060de2af4dae259f4db6a387999c'

direct_sms = ylmfab.Dependency()
direct_sms.url = 'git://github.com/rgaudin/Direct-SMS.git'
direct_sms.branch = 'new-core'
direct_sms.lib_name = 'direct_sms'

simple_locations = ylmfab.Dependency()
simple_locations.url = 'git://github.com/yeleman/simple_locations.git'

django_eav = ylmfab.Dependency()
django_eav.url = 'git+git://github.com/mvpdev/django-eav.git#egg=django-eav'
django_eav.kind = ylmfab.Dependency.PIP_URL

dependencies = [bolibana, direct_sms, simple_locations, django_eav]

# fabric methods/optioms


def deploy():

    # install dependencies
    for dependency in dependencies:
        ylmfab.install(dependency)
