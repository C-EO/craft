import os
import subprocess

from CraftCore import CraftCore
from Notifier.NotificationInterface import NotificationInterface


class SnoreToast(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self, "SnoreToast")
        self.icon = os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craft.ico")

    def notify(self, title, message, alertClass):
        try:
            snore = CraftCore.cache.findApplication("snoretoast")
            if not snore:
                return
            command = [snore, "-t", title, "-m", message, "-p", self.icon]
            CraftCore.log.debug(command)
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=CraftCore.standardDirs.craftRoot(),
            )  # make sure that nothing is spawned in a build dir
        except Exception as e:
            CraftCore.log.debug(e)
            return
