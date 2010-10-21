#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
import os

from fabric.api import local, cd, settings, hide

from .constants import *


def python_version():
    return  '.'.join(str(p) for p in sys.version_info[:2])


def site_packages_path():
    return '%(prefix)s/lib/python%(version)s/site-packages' \
            % {'prefix': path_prefix(), 'version': python_version()}


def path_prefix():
    if is_virtual():
        return os.environ['VIRTUAL_ENV']
    else:
        return '%s/local/' % sys.prefix


def is_virtual():
    return 'VIRTUAL_ENV' in os.environ


def absolute_path(path, at=DEFAULT_WD):

    with cd(at):
        root = get_pwd()
    return os.path.join(root, path)


def get_pwd():
     with settings(
        hide('warnings', 'running', 'stdout', 'stderr'), \
        warn_only=True):
        return local('pwd')


def git_clone(url, at=DEFAULT_WD, to=None):

    """ clone a git repository

    Keyword arguments:
    url -- repository url
    at -- clone's parent folder (where command will be initiated)
    to -- name of the clone's folder

    """

    path = ' %s' % to if to else ''
    with cd(at):
        local('git clone %(url)s%(path)s' % {'url': url, 'path': path}, \
               capture=False)


def git_pull(at=DEFAULT_WD):

    """ pulls a git repository

    Keyword arguments:
    at -- repository's folder

    """

    with cd(at):
        local('git pull', capture=False)


def switch_local_branch(branch, at=DEFAULT_WD):

    with cd(at):
        local('git checkout %(branch)s' % {'branch': branch}, capture=False)


def switch_remote_branch(branch, local_branch=None, at=DEFAULT_WD):

    if not local_branch:
        local_branch = branch

    with cd(at):
        local('git checkout -b %(local_branch)s %(branch)s' \
              % {'branch': branch, 'local_branch': local_branch}, \
              capture=False)


def git_branch_exists(branch, at=DEFAULT_WD):

    with cd(at):
        with settings(
            hide('warnings', 'running', 'stdout', 'stderr'), \
            warn_only=True):
            return bool(local('git branch -a |grep %(branch)s | wc -l' \
                              % {'branch': branch}))


def git_get_revision(revision, at=DEFAULT_WD):

    with cd(at):
        local('git reset --hard %(rev)s' % {'rev': revision}, capture=False)


def symlink_lib(lib_name=None, to=DEFAULT_WD, lib_path=None, destination=None):

    with cd(to):
        dep_dir = get_pwd()

    if not destination:
        destination = site_packages_path()

    if lib_path:
        dep_lib = os.path.join(dep_dir, lib_path)
    else:
        dep_lib = dep_dir

    if not lib_name:
        lib_name = '.'

    lib_name = absolute_path(path=lib_name, at=destination)
    #with cd(destination):
    local('ln -fs %(dep_lib)s %(dep_name)s' % \
          {'dep_lib': dep_lib, 'dep_name': lib_name}, capture=False)


def python_install(at):

    # sudo the install if not on virtualenv
    launcher = local if is_virtual() else sudo

    with cd(at):
        launcher('./setup.py install', capture=False)


def pip_install_package(package):

    # sudo the install if not on virtualenv
    launcher = local if is_virtual() else sudo

    launcher('pip install %(package)s' % {'package': package}, capture=False)


def pip_install_url(url):

    # sudo the install if not on virtualenv
    launcher = local if is_virtual() else sudo

    launcher('pip install -e %(url)s' % {'url': url}, capture=False)


def pip_install_req(req_file):

    # sudo the install if not on virtualenv
    launcher = local if is_virtual() else sudo

    launcher('pip install -r %(pip_file)s' \
             % {'pip_file': req_file}, capture=False)

def deb_install_package(package):

    sudo('aptitude install %(package)s' % {'package': package}, capture=False)
