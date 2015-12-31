import os

import EmergeDebug
import info
import compiler


class subinfo(info.infoclass):
    def setDependencies( self ):
        EmergeDebug.debug("emergebuildsystem:subinfo.setDependencies not implemented yet", 1)
        # we need at least qmake
        #self.dependencies['libs/qt'] = 'default'
        self.buildDependencies['dev-util/jom'] = 'default'

        if compiler.isMinGW():
            self.buildDependencies['dev-util/mingw-w64']    = 'default'

from Package.InternalPackageBase import *

class Package(InternalPackageBase):
    def __init__( self ):
        InternalPackageBase.__init__(self)

