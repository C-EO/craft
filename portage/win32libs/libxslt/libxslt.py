import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.1.26', '1.1.28']:
            self.targets[ver] = 'ftp://xmlsoft.org/libxslt/libxslt-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libxslt-' + ver
        self.patchToApply['1.1.26'] = ("libxslt-1.1.26-20101102.diff", 1)
        self.patchToApply['1.1.28'] = ("libxslt-1.1.26-20101102.diff", 1)
        self.targetDigests['1.1.26'] = '69f74df8228b504a87e2b257c2d5238281c65154'
        self.targetDigests['1.1.28'] = '4df177de629b2653db322bfb891afa3c0d1fa221'

        self.description = "The GNOME XSLT C library and tools"
        self.defaultTarget = '1.1.28'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/libxml2"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.package.packageName = 'libxslt'
