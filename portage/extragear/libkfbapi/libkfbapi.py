import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:libkfbapi'

        for ver in ['1.0']:
            self.targets[ver] = "http://download.kde.org/stable/libkfbapi/" + ver + "/src/libkfbapi-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "libkfbapi-" + ver
            self.patchToApply[ver] = [("libkfbapi-1.0-fix-build-on-msvc.diff", 1)]  # TODO: commit upstream

        self.targetDigests['1.0'] = 'a04dbca49b3ade2f015ce8d32c9024a5383f4abc'

        self.defaultTarget = '1.0'

    def setDependencies(self):
        self.runtimeDependencies['kde/kdepimlibs'] = 'default'
        self.runtimeDependencies["kdesupport/qjson"] = "default"
        self.buildDependencies["dev-util/gettext-tools"] = "default"
        self.description = "KDE library for accessing Facebook services"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
