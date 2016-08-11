# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.dependencies['libs/qt5'] = 'default'
        self.dependencies['qt-libs/quazip'] = 'default'
        self.dependencies['qt-libs/libjreen'] = 'default'
        #self.dependencies['qt-libs/qtsparkle'] = 'default
        self.dependencies['qt-libs/qtkeychain'] = 'default'
        # self.dependencies['qt-libs/qtweetlib'] = 'default'
        self.dependencies['binary/vlc'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['qt-libs/libechonest'] = 'default'
        self.dependencies['frameworks/attica'] = 'default'
        self.dependencies['qt-libs/liblastfm'] = 'default'
        self.dependencies['win32libs/luceneplusplus'] = 'default'
        self.dependencies['win32libs/taglib'] = 'default'
        self.dependencies['win32libs/gnutls'] = 'default'
        self.buildDependencies['win32libs/websocketpp'] = 'default'
        self.dependencies['win32libs/libsparsehash'] = 'default'
        
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/tomahawk-player/tomahawk.git'
        self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = " -DWITH_CRASHREPORTER=OFF -DBUILD_WITH_QT4=OFF -DWITH_KDE4=OFF -DBUILD_HATCHET=ON"

