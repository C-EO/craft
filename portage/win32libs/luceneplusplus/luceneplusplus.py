import info


class subinfo (info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/boost-thread'] = 'default'
        self.dependencies['win32libs/boost-system'] = 'default'
        self.dependencies['win32libs/boost-regex'] = 'default'
        self.dependencies['win32libs/boost-iostreams'] = 'default'
        self.dependencies['win32libs/boost-date-time'] = 'default'
        self.dependencies['win32libs/boost-filesystem'] = 'default'
        self.dependencies['win32libs/boost-atomic'] = 'default'


    def setTargets( self ):
        for ver in [ ]:
            self.targets[ ver ] = "https://github.com/luceneplusplus/LucenePlusPlus/archive/rel_%s.tar.gz" % ver
            self.archiveNames[ ver ] = "luceneplusplus-%s.tar.gz" % ver
            self.targetInstSrc[ ver ] = "LucenePlusPlus-rel_%s" % ver
        self.patchToApply["gitHEAD"] = ("luceneplusplus-20150916.patch", 1)

        self.svnTargets[ "gitHEAD" ] = "https://github.com/luceneplusplus/LucenePlusPlus.git"
        
        self.shortDescription = "Lucene++ is an up to date C++ port of the popular Java Lucene library, a high-performance, full-featured text search engine."
        self.homepage = "https://github.com/luceneplusplus/LucenePlusPlus/"
        self.defaultTarget = "gitHEAD"


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DENABLE_TEST=OFF"
