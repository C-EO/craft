import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("http://downloads.sourceforge.net/boost/boost_${VERSION}.7z",
                                          tarballInstallSrc="boost_${VERSION}")

        self.targetDigests['1_55_0'] = '09203c60118442561d0ee196772058d80226762d'
        self.targetDigests['1_56_0'] = '3a65d31ad443a46ce6bb5011a5d5a0750765f157'
        self.targetDigests['1_57_0'] = 'cc08224035b6aa642599bbf28c76ee5ec8061c10'

        self.patchToApply['1_55_0'] = [('boost_1_54_0-spirit-20131114.diff', 1)]
        self.patchToApply['1_56_0'] = [
            ('boost_1_56_0-spirit-20131114.diff', 1)]  # TODO: also include in future releases!
        self.patchToApply['1_57_0'] = [('boost_1_56_0-spirit-20131114.diff', 1)]

        self.webpage = 'http://www.boost.org/'

        self.description = 'portable C++ libraries'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.BoostPackageBase import *


class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)
        self.subinfo.options.package.packSources = True

    def make(self):
        return True

    def install(self):
        shutil.copytree(os.path.join(self.sourceDir(), 'boost'),
                        os.path.join(self.imageDir(), 'include', 'boost'))  # disable autolinking
        f = open(os.path.join(self.imageDir(), 'include', 'boost', 'config', 'user.hpp'), 'a')
        f.write('#define BOOST_ALL_NO_LIB\n')
        f.close()
        return True
