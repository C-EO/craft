import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['frameworks'] = '[git]kde:kmymoney|frameworks'
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.dependencies['frameworks/kcmutils'] = 'default'
        self.dependencies['frameworks/kdelibs4support'] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'
        self.dependencies['testing/kdiagram'] = 'default'
        self.dependencies['testing/gpgmepp'] = 'default'
        self.dependencies['binary/mysql-pkg'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        #self.dependencies['win32libs/libofx'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
        self.dependencies['extragear/libalkimia'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'
        self.shortDescription = "a personal finance manager for KDE"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)

