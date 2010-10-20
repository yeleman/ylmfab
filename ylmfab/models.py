#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


class Dependency(object):

    GIT_REPO = 0
    PIP_PACKAGE = 1
    PIP_URL = 2
    KINDS = ((GIT_REPO, 'Git repository'),
             (PIP_PACKAGE, 'PIP package'),
             (PIP_URL, 'PIP URL'))

    def __init__(self, url=None, branch=None, revision=None, \
                 lib_path=None, lib_name=None, pip_file=None, \
                 clone_name=None, run_tests=False, symlink=True, \
                 install=False, kind=GIT_REPO, *args, **kwargs):

        self.url = url
        self.branch = branch
        self.revision = revision
        self.lib_path = lib_path
        self.lib_name = lib_name
        self.pip_file = pip_file
        self.clone_name = clone_name
        self.run_tests = run_tests
        self.symlink = symlink
        self.install = install
        self.kind = kind

    # url
    def set_url(self, value):
        self._url = value

    def get_url(self):
        return self._url
    url = property(get_url, set_url)

    # branch
    def set_branch(self, value):
        self._branch = value

    def get_branch(self):
        return self._branch
    branch = property(get_branch, set_branch)

    # revision
    def set_revision(self, value):
        self._revision = value

    def get_revision(self):
        return self._revision
    revision = property(get_revision, set_revision)

    # lib_path
    def set_lib_path(self, value):
        self._lib_path = value

    def get_lib_path(self):
        return self._lib_path
    lib_path = property(get_lib_path, set_lib_path)

    # lib_name
    def set_lib_name(self, value):
        self._lib_name = value

    def get_lib_name(self):
        return self._lib_name
    lib_name = property(get_lib_name, set_lib_name)

    # pip_file
    def set_pip_file(self, value):
        self._pip_file = value

    def get_pip_file(self):
        return self._pip_file
    pip_file = property(get_pip_file, set_pip_file)

    # clone_name
    def set_clone_name(self, value):
        self._clone_name = value

    def get_clone_name(self):
        return self._clone_name or self._get_name_from_git()
    clone_name = property(get_clone_name, set_clone_name)

    # run_tests
    def set_run_tests(self, value):
        self._run_tests = bool(value)

    def get_run_tests(self):
        return bool(self._run_tests)
    run_tests = property(get_run_tests, set_run_tests)

    # symlink
    def set_symlink(self, value):
        self._symlink = bool(value)

    def get_symlink(self):
        return bool(self._symlink)
    symlink = property(get_symlink, set_symlink)

    # install
    def set_install(self, value):
        self._install = bool(value)

    def get_install(self):
        return bool(self._install)
    install = property(get_install, set_install)

    # kind
    def set_kind(self, value):
        if not [kind[0] for kind in self.KINDS].count(value):
            raise ValueError
        self._kind = value

    def get_kind(self):
        return self._kind
    kind = property(get_kind, set_kind)

    def _get_name_from_git(self):
        h, s, t = self.url.rpartition('/')
        return t.rstrip('.git')

    def __str__(self):
        return u"%(name)s" % {'name': self.lib_name}
