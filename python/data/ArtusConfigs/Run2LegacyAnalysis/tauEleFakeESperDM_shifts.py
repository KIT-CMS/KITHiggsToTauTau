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
  #isEmbedded = datasetsHelper.isEmbedded(nickname)
  #isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  #isDY = re.search("DY.?JetsToLLM(50|150)", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)
  year = datasetsHelper.base_dict[nickname]["year"]

  tauEleFakeES_uncertainties = {
    2016 : {
      "TauElectronFakeEnergyCorrectionOneProng" : {"down" : 0.992, "up" : 1.016},
      "TauElectronFakeEnergyCorrectionOneProngPiZeros" : {"down" : 1.015, "up" : 1.048},
    },
    2017: {
      "TauElectronFakeEnergyCorrectionOneProng" : {"down" : 0.993, "up" : 1.012},
      "TauElectronFakeEnergyCorrectionOneProngPiZeros" : {"down" : 1.006, "up" : 1.036},
    },
    # TODO measure correcction & uncertainties for 2018; until now taking 2017 measurement
    2018: {
      "TauElectronFakeEnergyCorrectionOneProng" : {"down" : 1.008, "up" : 1.020},
      "TauElectronFakeEnergyCorrectionOneProngPiZeros" : {"down" : 0.999, "up" : 1.029},
    }
  }

  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  if re.search("DY.?JetsToLL|EWKZ", nickname):
    config["tauEleFakeEsOneProngUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngUp"]["TauElectronFakeEnergyCorrectionOneProng"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProng"]["up"]

    config["tauEleFakeEsOneProngDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngDown"]["TauElectronFakeEnergyCorrectionOneProng"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProng"]["down"]


    config["tauEleFakeEsOneProngPiZerosUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosUp"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZeros"]["up"]

    config["tauEleFakeEsOneProngPiZerosDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosDown"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZeros"]["down"]


  return config
