# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:nepomukshell'
        self.defaultTarget = 'master'
        self.shortDescription =(
                "NepomukShell is a maintenance and debugging "
                "tool intended for developers. It allows to browse, "
                "query, and edit Nepomuk resources.")

    def setDependencies(self):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/soprano'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

