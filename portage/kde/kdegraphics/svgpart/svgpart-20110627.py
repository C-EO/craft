import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['4.7']:
            self.svnTargets[ ver ] = '[git]kde:svgpart|%s|' % ver
            
        self.svnTargets['gitHEAD'] = '[git]kde:svgpart'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
