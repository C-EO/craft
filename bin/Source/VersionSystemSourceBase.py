#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import EmergeDebug
from Source.SourceBase import *

class VersionSystemSourceBase (SourceBase):
    """abstract base class for version system support"""

    def __init__(self):
        EmergeDebug.trace("VersionSystemSourceBase __init__", 2)
        SourceBase.__init__(self)

    def getUrl( self, index ):
        """get the url at position 'index' from a ';' separated list of urls"""
        EmergeDebug.trace("VersionSystemSourceBase getUrl", 2)
        u = self.subinfo.svnTarget()
        if u.find(';') == -1:
            if index == 0:
                return u
            else:
                return None
        # urls are a list
        urls = u.split(';')
        if index >= len(urls):
            return None

        u = urls[index]
        return u

    def splitUrl( self, url ):
        """ split url into real url and url option. the delimiter is '#'"""
        EmergeDebug.trace("VersionSystemSourceBase splitUrl", 2)
        if url.find('#') != -1:
            return url.split('#')
        return [url, ""]

    def __repositoryBaseUrl( self ):
        """ this function return the base url to the KDE repository """
        EmergeDebug.trace("VersionSystemSourceBase __repositoryBaseUrl", 2)
        # @todo move to SvnSource
        server = emergeSettings.get("General", "KDESVNSERVER", "svn://anonsvn.kde.org")


        return server + '/home/kde/'

    def unpack(self):
        EmergeDebug.trace("VersionSystemSourceBase unpack", 2)
        self.enterBuildDir()

        if not self.noClean:
            if EmergeDebug.verbose() > 0:
                print("cleaning %s" % self.buildDir())
            utils.cleanDirectory( self.buildDir() )
        if not self.noCopy:
            sourceDir = self.checkoutDir()
            if EmergeDebug.verbose() > 0:
                print("copying %s to %s" % (sourceDir, self.buildDir()))
            utils.copyDir(sourceDir, self.buildDir())
        ret = self.applyPatches()
        if emergeSettings.getboolean("General","EMERGE_HOLD_ON_PATCH_FAIL", False):
            return ret
        return True

    def repositoryUrlCount( self ):
        """return the number of provided repository url's. Multiple repository urls' are delimited by ';'"""
        EmergeDebug.trace("VersionSystemSourceBase repositoryUrlCount", 2)
        if not self.subinfo.hasSvnTarget():
            return 0
        u = self.subinfo.svnTarget()
        if u.find(';') == -1:
            return 1
        urls = u.split(';')
        return len(urls)

    def repositoryUrl( self, index=0 ):
        """this function returns the full url into a version system based repository at position 'index'.
        See @ref repositoryUrlCount how to define multiple repository urls."""
        EmergeDebug.trace("VersionSystemSourceBase repositoryUrl", 2)
        if self.subinfo.hasSvnTarget():
            u1 = self.getUrl(index)
            (u, dummy) = self.splitUrl(u1)
            # check relative kde url
            # @todo this is svn specific - move to SvnSource
            if u.find("://") == -1 and utils.getVCSType( u ) == "svn":
                url = self.__repositoryBaseUrl() + u
            else:
                url = u
            return url
        else:
            return False

    def repositoryUrlOptions( self, index=0 ):
        """this function return options for the repository url at position 'index'.
        Options for a repository url are defined by adding '#' followed by the specific option.
        """
        EmergeDebug.trace("VersionSystemSourceBase repositoryUrlOptions", 2)
        if self.subinfo.hasSvnTarget():
            u = self.getUrl(index)
            (dummy, option) = self.splitUrl(u)
            return option
        return None

    def checkoutDir( self, dummyIndex=0 ):
        EmergeDebug.trace("VersionSystemSourceBase checkoutDir", 2)
        if self.subinfo.hasSvnTarget():
            sourcedir = os.path.join(  EmergeStandardDirs.gitDir(), self.package )
        else:
            EmergeDebug.die("svnTarget property not set for this target")

        if self.subinfo.targetSourceSuffix() != None:
            sourcedir = "%s-%s" % (sourcedir, self.subinfo.targetSourceSuffix())

        return os.path.abspath(sourcedir)

    def sourceDir(self, index=0 ):
        EmergeDebug.trace("VersionSystemSourceBase sourceDir", 2)
        if not self.noCopy:
            # need to check index ?
            sourcedir = self.workDir()

            if self.subinfo.targetSourceSuffix() != None:
                sourcedir = "%s-%s" % (sourcedir, self.subinfo.targetSourceSuffix())

            return sourcedir
        else:
            sourcedir = self.checkoutDir( index )

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())

        EmergeDebug.debug("using sourcedir: %s" % sourcedir, 2)
        return os.path.abspath(sourcedir)

    def sourceRevision(self):
        EmergeDebug.trace("VersionSystemSourceBase sourceRevision", 2)
        return self.sourceVersion()



