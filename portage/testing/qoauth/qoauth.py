import os

import info
from Package.QMakePackageBase import *


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'http://github.com/ayoy/qoauth.git'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'

class Package(QMakePackageBase):
    def __init__( self, **args ):
        QMakePackageBase.__init__(self)

    def configure( self ):
        os.putenv("BUILDDIR", os.path.join( self.buildDir(), "lib" ))
        os.putenv("INSTALLDIR", self.installDir())
        return QMakePackageBase.configure(self)

    def install( self ):
        utils.copyDir( os.path.join( self.buildDir(), "bin" ) , os.path.join( self.installDir(), "bin" ) )
        return QMakePackageBase.install(self)

    def setPathes( self ):
        pass

