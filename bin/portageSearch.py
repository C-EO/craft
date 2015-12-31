import re

import EmergeDebug
import portage
import utils
import InstallDB


def printSearch(search_category, search_package,maxDist = 2):
        installable = portage.PortageInstance.getInstallables()
        similar = []
        match = None
        package_re = re.compile(".*%s.*" % search_package, re.IGNORECASE)
        for _p in installable:
            if search_category == "" or search_category == _p.category:
                package = portage.PortageInstance.getPackageInstance( _p.category, _p.package)
                if not package:
                    continue
                levDist = utils.levenshtein(search_package.lower(),package.package.lower())
                if levDist == 0 :
                    match = (levDist,package)
                    break
                elif package_re.match(package.package):
                    similar.append((levDist-maxDist,package))
                elif len(package.package)>maxDist and levDist <= maxDist:
                    similar.append((levDist,package))
                else:
                    if package_re.match(package.subinfo.shortDescription):
                        similar.append((100,package))

        if match == None:
            if len(similar)>0:
                print("Emerge was unable to find %s, similar packages are:" % search_package) 
                similar.sort( key = lambda x: x[0])
            else:
                print("Emerge was unable to find %s" % search_package)
        else:
            print("Package %s found:" % search_package)
            similar = [match]
        
        for levDist,package in similar:
            EmergeDebug.debug((package, levDist), 1)
            print(package)
            print("\t Homepage: %s" % package.subinfo.homepage)
            print("\t Description: %s" % package.subinfo.shortDescription)
            print("\t Latest version: %s" % package.subinfo.defaultTarget)
            installed = False
            for pack in InstallDB.installdb.getInstalledPackages(package.category,package.package):
                if pack.getVersion():
                    installed = True
                    print("\t Installed versions: %s" % pack.getVersion())
                if pack.getRevision():
                    print("\t Installed revision: %s" % pack.getRevision())
            if not installed:
                print("\t Installed versions: None")
    