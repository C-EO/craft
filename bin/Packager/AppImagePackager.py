from Packager.CollectionPackagerBase import *


class AppImagePackager(CollectionPackagerBase):
    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)
        self.linuxdeployExe = None
        self._isInstalled = False

    def setDefaults(self, defines: {str: str}) -> {str: str}:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}.AppImage"
        defines.setdefault(
            "runenv",
            [
                # XDG_DATA_DIRS: to make QStandardPaths::GenericDataLocation look in the AppImage paths too.
                # necessary, e.g., to make switching languages for KDE (with KConfigWidgets) applications work.
                # we need to append the default value in any case, since it may not be defined (looking at you, Debian!)
                # in case it is not set by default, UI frameworks won't be able to find files anymore
                # this has caused problems in the past when, e.g., trying to open a browser using QDesktopServices
                'XDG_DATA_DIRS="$this_dir/usr/share/:$XDG_DATA_DIRS:/usr/local/share:/usr/share"',
                'FONTCONFIG_PATH="$(if [ -d /etc/fonts ]; then echo "/etc/fonts"; else echo "$this_dir/etc/fonts"; fi)"',
                'PATH="$this_dir/usr/bin:$this_dir/usr/lib:$PATH"',
            ],
        )
        return defines

    def isLinuxdeployInstalled(self):
        if not self._isInstalled:
            self._isInstalled = self.__isInstalled()
            if not self._isInstalled:
                CraftCore.log.critical("Craft requires linuxdeploy to create an AppImage, please install linuxdeploy\n" "\t'craft linuxdeploy'")
                return False
        return True

    def __isInstalled(self):
        """check if linuxdeploy is installed somewhere"""
        self.linuxdeployExe = CraftCore.cache.findApplication("linuxdeploy-x86_64.AppImage")
        if not self.linuxdeployExe:
            return False
        return True

    def createPackage(self):
        """create a package"""
        if not self.isLinuxdeployInstalled():
            return False

        CraftCore.log.debug("packaging using the AppImagePackager")

        archiveDir = Path(self.archiveDir())
        defines = self.setDefaults(self.defines)
        if not self.internalCreatePackage(defines):
            return False
        if not utils.mergeTree(archiveDir, archiveDir / "usr"):
            return False
        etc = archiveDir / "usr/etc"
        if etc.exists():
            if not utils.createSymlink(etc, archiveDir / "etc", useAbsolutePath=False, targetIsDirectory=True):
                return False
        if "runenv" in defines:
            if not utils.createDir(archiveDir / "apprun-hooks"):
                return False
            with (archiveDir / "apprun-hooks/craft-runenv-hook.sh").open("wt") as hook:
                hook.write("# generated by craft based on the runenv define\n\n")
                hook.writelines([f"{i}\nexport {i.split('=')[0]}\n" for i in defines["runenv"]])
        if not utils.createDir(self.packageDestinationDir()):
            return False
        desktopFiles = glob.glob(f"{archiveDir}/usr/share/applications/*{defines['appname']}.desktop")
        if len(desktopFiles) != 1:
            CraftCore.log.error("Failed to find the .desktop file")
            return False

        env = {
            "ARCH": CraftCore.compiler.appImageArchitecture,
            "LD_LIBRARY_PATH": f"{archiveDir}/usr/lib:{archiveDir}/usr/lib/x86_64-linux-gnu",
            "LINUXDEPLOY_OUTPUT_VERSION": defines["version"],
            "LDAI_OUTPUT": defines["setupname"],
            "LDNP_META_PACKAGE_NAME": defines.get("appimage_native_package_name", defines["appname"]),
            "LDNP_META_DEB_ARCHITECTURE": CraftCore.compiler.debArchitecture,
            "LDNP_META_RPM_BUILD_ARCH": CraftCore.compiler.rpmArchitecture,
            "NO_STRIP": "1",  # our binaries are already stripped
        }

        if "website" in defines:
            env.update(
                {
                    "LDNP_META_DEB_HOMEPAGE": defines["website"],
                    "LDNP_META_RPM_URL": defines["website"],
                }
            )

        if OsUtils.detectDocker():
            env["APPIMAGE_EXTRACT_AND_RUN"] = "1"
        args = [
            "--appdir",
            self.archiveDir(),
            "--desktop-file",
            desktopFiles[0],
        ]
        for output in ["appimage"] + defines.get("appimage_extra_output", []):
            args += [f"--output={output}"]
        for plugin in ["qt"] + defines.get("appimage_extra_plugins", []):
            args += [f"--plugin={plugin}"]
        if "appimage_apprun" in defines:
            args += ["--custom-apprun", defines["appimage_apprun"]]
        if CraftCore.debug.verbose() > 0:
            args += ["-v0"]
        with utils.ScopedEnv(env):
            return utils.system([self.linuxdeployExe] + args, cwd=self.packageDestinationDir())
