import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'

    def setDependencies( self ):
        if not utils.varAsBool(emergeSettings.get("General",'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES',"False")):
            self.buildDependencies['gnuwin32/wget'] = 'default'
            self.buildDependencies['dev-util/7zip'] = 'default'
            self.buildDependencies['gnuwin32/patch'] = 'default'

from Package.VirtualPackageBase import *
from Source.SourceBase import *

class Package(VirtualPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
