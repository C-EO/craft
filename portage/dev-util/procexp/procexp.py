import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['15.3'] = 'http://download.sysinternals.com/files/ProcessExplorer.zip'
        self.defaultTarget = '15.3'
        #self.targetDigests['15.3'] = '4a1c3964e624254cc301f7c014f9d211d97e37f3'
        # the zip file does not have a bin dir, so we have to create it
        # This attribute is in prelimary state
        self.targetInstallPath['15.3'] = os.path.join("dev-util", "bin")

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
