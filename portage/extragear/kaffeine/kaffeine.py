import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/multimedia/kaffeine'
        self.defaultTarget = 'svnHEAD'

    def setDependencies(self):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
