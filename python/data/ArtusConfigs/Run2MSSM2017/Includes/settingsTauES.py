#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
#import os

def build_config(nickname):
  config = jsonTools.JsonDict()
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  
  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["TauEnergyCorrection"] = "mssmhtt2016"
  
  if re.search("Run201|Embedding", nickname):
    config["TauEnergyCorrectionOneProng"] = 1.0
    config["TauEnergyCorrectionOneProngPiZeros"] = 1.0
    config["TauEnergyCorrectionThreeProng"] = 1.0
    config["TauElectronFakeEnergyCorrectionOneProng"] = 1.0
    config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.0
  else:
    config["TauEnergyCorrectionOneProng"] = 0.97
    config["TauEnergyCorrectionOneProngPiZeros"] = 0.98
    config["TauEnergyCorrectionThreeProng"] = 0.99
    config["TauElectronFakeEnergyCorrectionOneProng"] = 1.0
    config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.0
  

  return config
