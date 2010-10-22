#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import weakref


class Dependency(object):

    __instances__ = []

    DEBIAN_PACKAGE = 0
    PIP_PACKAGE = 1
    PIP_URL = 2
    GIT_REPO = 3
    KINDS = ((DEBIAN_PACKAGE, 'Debian package(s)'),
             (PIP_PACKAGE, 'PIP package(s)'),
             (PIP_URL, 'PIP URL(s)'),
             (GIT_REPO, 'Git repositor(y|ies)'))

    def __init__(self, source=None, branch=None, revision=None, \
                 lib_path=None, lib_name=None, pip_file=None, \
                 clone_name=None, run_tests=False, symlink=True, \
                 install=False, kind=GIT_REPO, *args, **kwargs):

        # keep track of instances
        self.__instances__.append(weakref.ref(self))

        self.source = source
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

    # source/url
    def set_source(self, value):
        self._source = value

    def get_source(self):
        return unicode(self._source)
    source = property(get_source, set_source)

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
        h, s, t = self.source.rpartition('/')
        return t.rsplit('.git')[0]

    def is_git(self):
        return self.kind in (self.GIT_REPO,)

    def is_pip_package(self):
        return self.kind == self.PIP_PACKAGE

    def is_pip_url(self):
        return self.kind == self.PIP_URL

    def is_pip(self):
        return self.kind in (self.PIP_PACKAGE, self.PIP_URL)

    def is_deb(self):
        return self.kind == self.DEBIAN_PACKAGE

    def is_package(self):
        return self.kind in (self.PIP_PACKAGE, self.DEBIAN_PACKAGE)

    @classmethod
    def canonical_name_from(cls, url=''):
        xpart = url.rpartition('/')[2].rpartition('.')
        index = 0 if xpart[0] else 2
        return xpart[index]

    def github_public(self):
        return self.source.replace('git@github.com:', 'git://github.com/')

    def github_private(self):
        return self.source.replace('git://github.com/', 'git@github.com:')

    @property
    def module_name(self):
        if self.is_package():
            return self.source
        if self.lib_name:
            return self.lib_name
        return Dependency.canonical_name_from(url=self.source)

    @classmethod
    def instances(cls):
        return [inst.__call__() for inst in cls.__instances__]

    @classmethod
    def all_by_kind(cls, kind):
        results = []
        for inst in cls.instances():
            if inst.kind == kind:
                results.append(inst)
        return results

    def __str__(self):

        return u"<%(name)s>" % {'name': self.module_name()}

    def __rst__(self):
        if self.is_deb():
            return u"**%(name)s**\n\n" \
                    "    ``sudo aptitude install %(name)s``" \
                   % {'name': self.module_name}
        if self.is_pip_package():
            return u"**%(name)s**\n\n" \
                    "    ``pip install %(name)s``" \
                   % {'name': self.module_name}
        if self.is_pip_url():
            return u"**%(name)s**\n\n" \
                    "    ``pip install -e %(source)s``" \
                   % {'name': self.module_name, 'source': self.source}
        if self.is_git():
            rst = u"**%(name)s**\n\n" \
                    "    ``git clone %(source)s``" \
                   % {'name': self.module_name, 'source': self.source}
            if self.branch:
                rst += u"\n    ``git checkout %(branch)s``" \
                       % {'branch': self.branch}
            if self.revision:
                rst += u"\n    ``git reset --hard %(revision)s``" \
                       % {'revision': self.revision}
            return rst

    @classmethod
    def kind_name(cls, kind):
        for kind_id, kind_name in cls.KINDS:
            if kind == kind_id:
                return kind_name
        return None

    @classmethod
    def kind_rst(cls, kind):
        kind_name = cls.kind_name(kind)
        line = u"".zfill(kind_name.__len__()).replace('0', '~')
        return u"%(name)s\n%(line)s" % {'name': kind_name, 'line': line}

    @classmethod
    def __rst_all__(cls):

        rst = u""
        # store dependencies in a hash indexed by type
        deps = {}
        for kind, kind_name in Dependency.KINDS:
            deps[kind] = Dependency.all_by_kind(kind)

        for kind, kind_deps in deps.items():
            if kind_deps:
                deps_rst = u"- " + u"\n\n- ".join([k.__rst__() \
                                                for k in kind_deps])
                rst += "%(kind)s\n\n%(deps)s\n\n" \
                       % {'kind': cls.kind_rst(kind), \
                          'deps': deps_rst}
        return rst
