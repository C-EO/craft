import info
from CraftCompiler import craftCompiler


class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies['dev-util/cmake'] = 'default'
        self.buildDependencies['dev-util/jom'] = 'default'

        if craftCompiler.isMinGW():
            self.buildDependencies['dev-util/mingw-w64'] = 'default'


from Package.InternalPackageBase import *


class Package(InternalPackageBase):
    def __init__(self):
        InternalPackageBase.__init__(self)
