#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os

from fabric.api import *

from .constants import *
from .raw_tools import *


def install(dep, working_dir=DEFAULT_WD):

    if dep.kind in (dep.PIP_URL, dep.PIP_PACKAGE):
        if dep.kind == dep.PIP_URL:
            pip_install_url(dep.url)
        elif dep.kind == dep.PIP_PACKAGE:
            pip_install_package(dep.url)
        return JOB_DONE

    with cd(working_dir):
        # clone or pull
        if os.path.exists(dep.clone_name):
            with cd(dep.clone_name):
                update(dep)
        else:
            clone(dep, working_dir)

        # now we'll be working on the new folder
        with cd(dep.clone_name):
            # switch branch
            switch_branch(dep)

            # get revision
            get_revision(dep)        

            # install
            setup_install(dep)

            # symlink site packages
            create_symlink(dep)

            # install pip-req
            install_pip_req(dep)

def clone(dep, working_dir=DEFAULT_WD):

    # git clone the repository
    git_clone(url=dep.url, at=working_dir, to=dep.clone_name)

def update(dep, working_dir=DEFAULT_WD):

    # git pull the repository
    git_pull(at=working_dir)

def switch_branch(dep, working_dir=DEFAULT_WD):

    if not dep.branch:
        return NOTHING_TO_DO

    with cd(working_dir):
        if not git_branch_exists(dep.branch, at=working_dir):
            switch_remote_branch(branch=dep.branch, local_branch=dep.branch, \
                                 at=working_dir)
        else:
            switch_local_branch(branch=dep.branch, at=working_dir)

def get_revision(dep, working_dir=DEFAULT_WD):

    if not dep.revision:
        return NOTHING_TO_DO

    git_get_revision(revision=dep.revision, at=working_dir)

def create_symlink(dep, working_dir=DEFAULT_WD):

    if not dep.symlink:
        return NOTHING_TO_DO

    # create lib symlink on site-packages
    symlink_lib(lib_name=dep.lib_name, to=working_dir, lib_path=dep.lib_path)

def setup_install(dep, working_dir=DEFAULT_WD):

    if not dep.install:
        return NOTHING_TO_DO

    python_install(at=working_dir)

def install_pip_req(dep, working_dir=DEFAULT_WD):

    if not dep.pip_file:
        return NOTHING_TO_DO

    req_file = absolute_path(dep.pip_file, at=working_dir)
    pip_install_req(req_file)
