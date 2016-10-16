import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:kdev-php|5.0|'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies[ 'extragear/kdevelop-pg-qt' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )

