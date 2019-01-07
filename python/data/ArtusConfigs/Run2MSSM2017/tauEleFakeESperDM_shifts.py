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
  #isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  #isDY = re.search("DY.?JetsToLLM(50|150)", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)


  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  if re.search("DY.?JetsToLL|EWKZ", nickname) or isEmbedded:
    config["tauEleFakeEsOneProngUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngUp"]["TauElectronFakeEnergyCorrectionOneProng"] = 1.01

    config["tauEleFakeEsOneProngDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngDown"]["TauElectronFakeEnergyCorrectionOneProng"] = 0.996


    config["tauEleFakeEsOneProngPiZerosUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosUp"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.043

    config["tauEleFakeEsOneProngPiZerosDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosDown"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.029


  return config
