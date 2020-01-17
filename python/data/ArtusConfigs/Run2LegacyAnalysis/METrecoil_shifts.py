#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
#import os

def build_config(nickname, **kwargs):
  config = jsonTools.JsonDict()
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))


  # define frequently used conditions
  #isEmbedded = datasetsHelper.isEmbedded(nickname)
  #isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLL", nickname)
  isWjets = re.search("(W.?Jets|WG|WGstar)ToLNu", nickname)
  isSignal = re.search("HToTauTau|NMSSM|ttHJetToTT",nickname)
  isHWW = re.search("HToWW",nickname)
  isEWK = re.search("EWK",nickname)


  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  if isDY or isWjets or isSignal or isHWW or isEWK:
    config["metRecoilResponseUp"] = {
      "MetSysType" : 0,
      "MetSysShift" : 1,
      "SvfitCacheFileFolder" : "metRecoilResponseUp"
    }
    config["metRecoilResponseDown"] = {
      "MetSysType" : 0,
      "MetSysShift" : -1,
      "SvfitCacheFileFolder" : "metRecoilResponseDown"
    }
    config["metRecoilResolutionUp"] = {
      "MetSysType" : 1,
      "MetSysShift" : 1,
      "SvfitCacheFileFolder" : "metRecoilResolutionUp"
    }
    config["metRecoilResolutionDown"] = {
      "MetSysType" : 1,
      "MetSysShift" : -1,
      "SvfitCacheFileFolder" : "metRecoilResolutionDown"
    }

  return config
