# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


from BuildSystem.BuildSystemBase import *
from CraftCompiler import CraftCompiler


class MesonBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "meson")

    def __env(self):
        env = {
            "LDFLAGS": self.subinfo.options.configure.ldflags + " " + os.environ.get("LDFLAGS", ""),
            "CFLAGS": self.subinfo.options.configure.cflags + " " + os.environ.get("CFLAGS", ""),
        }
        if CraftCore.compiler.isMSVC():
            env.update(
                {
                    "LIB": f"{os.environ['LIB']};{os.path.join(CraftStandardDirs.craftRoot() , 'lib')}",
                    "INCLUDE": f"{os.environ['INCLUDE']};{os.path.join(CraftStandardDirs.craftRoot() , 'include')}",
                }
            )
        else:
            env["LDFLAGS"] = f"-L{CraftStandardDirs.craftRoot() / 'lib'} {env['LDFLAGS']}"
            env["CFLAGS"] = f"-I{CraftStandardDirs.craftRoot() / 'include'} {env['CFLAGS']}"
        return env

    def configureOptions(self, defines=""):
        buildType = {
            "Release": "release",
            "RelWithDebInfo": "debugoptimized",
            "MinSizeRel": "minsize",
            "Debug": "debug",
        }.get(self.buildType())
        return Arguments(
            [
                defines,
                "--prefix",
                CraftCore.standardDirs.craftRoot(),
                "--libdir",
                "lib",
                "--datadir",
                CraftCore.standardDirs.locations.data,
                "--buildtype",
                buildType,
                "--cmake-prefix-path",
                CraftCore.standardDirs.craftRoot(),
                self.buildDir(),
                self.sourceDir(),
                "-Ddefault_library=shared",
                BuildSystemBase.configureOptions(self),
            ]
        )

    def craftCrossFile(self):
        craftCrossFilePath = CraftStandardDirs.craftRoot() / "etc/craft-cross-file.txt"
        config = "[constants]\n"

        toolchain_path = os.path.join(CraftCore.standardDirs.tmpDir(), f"android-{CraftCore.compiler.architecture}-toolchain")
        config += f"android_ndk = '{toolchain_path}/bin/'\n"
        if CraftCore.compiler.architecture == CraftCompiler.Architecture.arm64:
            config += "toolchain = 'aarch64-linux-android-'\n"
        else:
            config += f"toolchain = '{CraftCore.compiler.androidArchitecture}-linux-android-'\n"

        config = (
            "[binaries]\n"
            "c = android_ndk + toolchain + 'gcc'\n"
            "cpp = android_ndk + toolchain + 'g++'\n"
            "ar = android_ndk + toolchain + 'ar'\n"
            "ld = android_ndk + toolchain + 'ld'\n"
            "objcopy = android_ndk + toolchain + 'objcopy'\n"
            "strip = android_ndk + toolchain + 'strip'\n"
            "pkgconfig = '/usr/bin/pkg-config'\n"
            "[host_machine]\n"
            "system = 'linux'\n"
            f"cpu_family = '{CraftCore.compiler.androidArchitecture}'\n"
            f"cpu = '{CraftCore.compiler.androidArchitecture}'\n"  # according to meson, this value is meaningless (https://github.com/mesonbuild/meson/issues/7037#issuecomment-620137436)
            "endian = 'little'\n"
        )

        with craftCrossFilePath.open("wt", encoding="UTF-8") as f:
            f.write(config)

        return craftCrossFilePath

    def configure(self, defines=""):
        with utils.ScopedEnv(self.__env()):
            print(CraftCore.compiler)

            extra_options = []
            if CraftCore.compiler.isAndroid:
                extra_options = ["--cross-file", self.craftCrossFile()]

            return utils.system(Arguments(["meson", "setup", extra_options, self.configureOptions(defines)]))

    def make(self):
        with utils.ScopedEnv(self.__env()):
            # cwd should not be the build dir as it might confuse the dependencie resolution
            return utils.system(
                Arguments(
                    [
                        "meson",
                        "compile",
                        "-C",
                        self.buildDir(),
                        self.makeOptions(self.subinfo.options.make.args),
                    ]
                ),
                cwd=CraftCore.standardDirs.craftRoot(),
            )

    def install(self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False
        env = self.__env()
        env["DESTDIR"] = self.installDir()
        with utils.ScopedEnv(env):
            return utils.system(["meson", "install"], cwd=self.buildDir()) and self._fixInstallPrefix()

    def unittest(self):
        """running make tests"""
        return utils.system(["meson", "test"], cwd=self.buildDir())

    def makeOptions(self, args):
        defines = Arguments()
        if CraftCore.debug.verbose() > 0:
            defines.append("-v")
        if self.subinfo.options.make.supportsMultijob:
            if ("Compile", "Jobs") in CraftCore.settings:
                defines += [
                    "-j",
                    str(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count())),
                ]
        if args:
            defines.append(args)
        return defines
