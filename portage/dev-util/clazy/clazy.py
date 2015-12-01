# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.buildDependencies['virtual/base'] = 'default'
      self.dependencies['testing/clang'] = 'default'

        
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = '[git]kde:clazy'
      self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

