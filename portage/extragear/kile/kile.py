import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = '[git]kde:kile'
        self.svnTargets['gitStable-2.1'] = '[git]kde:kile|2.1|'
        for ver in ['2.1.1','2.1b5']:
            self.targets[ver] = 'http://downloads.sourceforge.net/kile/kile-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'kile-' + ver
        self.shortDescription = "a user friendly TeX/LaTeX editor for KDE"
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['qt-libs/poppler'] = 'default' # this is only a dependency for kile > 2.1, but we keep it like that for now
        self.dependencies['kde/okular'] = 'default'         # this is only a dependency for kile > 2.1, but we keep it like that for now
        self.runtimeDependencies['kde/kate'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

