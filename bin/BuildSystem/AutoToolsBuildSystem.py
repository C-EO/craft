# -*- coding: utf-8 -*-
# definitions for the autotools build system

import os

import utils
from shells import *
from BuildSystem.BuildSystemBase import *


class AutoToolsBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "autotools")
        self._shell = MSysShell()
        if craftCompiler.isX86():
            self.platform = "--host=i686-w64-mingw32 --build=i686-w64-mingw32 --target=i686-w64-mingw32 "
        else:
            self.platform = "--host=x86_64-w64-mingw32 --build=x86_64-w64-mingw32 --target=x86_64-w64-mingw32 "

    @property
    def makeProgram(self):
        make = "make "
        if self.subinfo.options.make.supportsMultijob and not craftCompiler.isMSVC():
            make += " -j%s" % os.getenv("NUMBER_OF_PROCESSORS")
        return make

    # make sure shell cant be overwritten
    @property
    def shell(self):
        return self._shell

    def configureDefaultDefines(self):

        """defining the default cmake cmd line"""
        return ""

    def configure(self):
        """configure the target"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        configure = os.path.join(self.sourceDir(), "configure")
        self.shell.environment["CFLAGS"] = self.subinfo.options.configure.cflags + self.shell.environment["CFLAGS"]
        self.shell.environment["CXXFLAGS"] = self.subinfo.options.configure.cxxflags + self.shell.environment[
            "CXXFLAGS"]
        self.shell.environment["LDFLAGS"] = self.subinfo.options.configure.ldflags + self.shell.environment["LDFLAGS"]
        if craftCompiler.isMSVC() or self.subinfo.options.configure.bootstrap == True:
            autogen = os.path.join(self.sourceDir(), "autogen.sh")
            if os.path.exists(autogen):
                self.shell.execute(self.sourceDir(), autogen)
            else:
                self.shell.execute(self.sourceDir(), "autoreconf -f -i")

        if not self.subinfo.options.useShadowBuild:
            ret = self.shell.execute(self.sourceDir(), configure, self.configureOptions(self))
        else:
            ret = self.shell.execute(self.buildDir(), configure, self.configureOptions(self))
        return ret

    def make(self, dummyBuildType=None):
        """Using the *make program"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        command = self.makeProgram
        args = self.makeOptions()

        # adding Targets later
        if not self.subinfo.options.useShadowBuild:
            if not self.shell.execute(self.sourceDir(), self.makeProgram, "clean"):
                print("while Make'ing. cmd: %s clean" % self.makeProgram)
                return False
            if not self.shell.execute(self.sourceDir(), command, args):
                print("while Make'ing. cmd: %s" % command)
                return False
        else:
            if not self.shell.execute(self.buildDir(), command, args):
                print("while Make'ing. cmd: %s" % command)
                return False
        return True

    def install(self):
        """Using *make install"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        command = self.makeProgram
        args = "install"

        if self.subinfo.options.install.useDestDir == True:
            args += " DESTDIR=%s prefix=" % self.shell.toNativePath(self.installDir())

        if self.subinfo.options.make.ignoreErrors:
            args += " -i"

        if self.subinfo.options.make.makeOptions:
            args += " %s" % self.subinfo.options.make.makeOptions
        if not self.subinfo.options.useShadowBuild:
            if not self.shell.execute(self.sourceDir(), command, args):
                print("while installing. cmd: %s %s" % (command, args))
                return False
        else:
            if not self.shell.execute(self.buildDir(), command, args):
                print("while installing. cmd: %s %s" % (command, args))
                return False
        if os.path.exists(os.path.join(self.imageDir(), "lib")):
            return self.shell.execute(os.path.join(self.imageDir(), "lib"), "rm", " -Rf *.la")
        else:
            return True

    def runTest(self):
        """running unittests"""
        return True

    def configureOptions(self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)
        if self.subinfo.options.configure.noDefaultOptions == False:
            if self.subinfo.options.install.useDestDir == False:
                options += " --prefix=%s " % self.shell.toNativePath(self.imageDir())
            else:
                options += " --prefix=%s " % self.shell.toNativePath(self.mergeDestinationDir())
        options += self.platform

        return options;

    def ccacheOptions(self):
        return " CC='ccache gcc' CXX='ccache g++' "
