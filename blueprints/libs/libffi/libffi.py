import info
from CraftCompiler import CraftCompiler
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.3", "3.4.6"]:
            self.targets[ver] = f"https://github.com/libffi/libffi/releases/download/v{ver}/libffi-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libffi-{ver}"
        self.targetDigests["3.3"] = (["72fba7922703ddfa7a028d513ac15a85c8d54c8d67f55fa5a4802885dc652056"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.4.6"] = (["b0dea9df23c863a7a50e825440f3ebffabd65df1497108e5d437747843895a4e"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["3.3"] = [("libffi-3.3-20210126.diff", 1)]
        self.patchLevel["3.3"] = 2
        self.defaultTarget = "3.4.6"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
        if CraftCore.compiler.isMSVC():
            wrapper = self.shell.toNativePath(self.sourceDir() / "msvcc.sh")
            arch = ""
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
                arch = " -m64"
            self.subinfo.options.configure.args += [f"CC={wrapper}{arch}", f"CXX={wrapper}{arch}"]
            self.subinfo.options.configure.args += ["--enable-static", "--disable-shared"]
        else:
            self.subinfo.options.configure.args += ["--enable-shared", "--disable-static", "--disable-multi-os-directory"]
