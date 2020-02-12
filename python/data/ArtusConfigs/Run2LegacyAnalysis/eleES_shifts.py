#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import os

def build_config(nickname, **kwargs):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))


  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  #isDY = re.search("DY.?JetsToLL", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)
  year = datasetsHelper.base_dict[nickname]["year"]
  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  if isEmbedded:
    eleEs_shift_EB = 1.0
    eleEs_shift_EE = 1.0
    if year==2016:
      eleEs_shift_EB = 0.99757
      eleEs_shift_EE = 0.99300
    elif year==2017:
      eleEs_shift_EB = 0.99933
      eleEs_shift_EE = 0.98867    
    elif year==2018:
      eleEs_shift_EB = 0.99672
      eleEs_shift_EE = 0.99443 
    config["eleEsUp"] = {
      "ElectronEnergyCorrectionShiftEB" : 1.005*eleEs_shift_EB,
      "ElectronEnergyCorrectionShiftEE" : 1.0125*eleEs_shift_EE,
      "SvfitCacheFileFolder" : "eleEsUp"
    }
    config["eleEsDown"] = {
      "ElectronEnergyCorrectionShiftEB" : 0.995*eleEs_shift_EB,
      "ElectronEnergyCorrectionShiftEE" : 0.9875*eleEs_shift_EE,
      "SvfitCacheFileFolder" : "eleEsDown"
    }
  if (not isData) and (not isEmbedded):
    config["eleScaleUp"] = {
      "ElectronScaleAndSmearTag" : "energyScaleUp"
    }
    config["eleScaleDown"] = {
      "ElectronScaleAndSmearTag" : "energyScaleDown"
    }
    config["eleSmearUp"] = {
      "ElectronScaleAndSmearTag" : "energySigmaUp"
    }
    config["eleSmearDown"] = {
      "ElectronScaleAndSmearTag" : "energySigmaDown"
    }

  return config
