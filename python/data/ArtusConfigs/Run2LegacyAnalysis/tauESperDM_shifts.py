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
  #isDY = re.search("DY.?JetsToLLM(50|150)", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)
  year = datasetsHelper.base_dict[nickname]["year"]

  tauES_uncertainties = {
    2016 : {
      "TauEnergyCorrectionOneProng" : {"down" : 0.984, "up" : 0.997},
      "TauEnergyCorrectionOneProngPiZeros" : {"down" : 0.994, "up" : 1.002},
      "TauEnergyCorrectionThreeProng" : {"down" : 1.001, "up" : 1.015},
      "TauEnergyCorrectionThreeProngPiZeros" : {"down" : 0.992, "up" : 1.012},
    },
    2017: {
      "TauEnergyCorrectionOneProng" : {"down" : 0.990, "up" : 1.009},
      "TauEnergyCorrectionOneProngPiZeros" : {"down" : 0.996, "up" : 1.006},
      "TauEnergyCorrectionThreeProng" : { "down" : 0.995, "up" : 1.007},
      "TauEnergyCorrectionThreeProngPiZeros" : {"down" : 0.985, "up" : 1.011},
    },
    2018: {
      "TauEnergyCorrectionOneProng" : {"down" : 0.976, "up" : 0.990},
      "TauEnergyCorrectionOneProngPiZeros" : {"down" : 0.992, "up" : 1.000},
      "TauEnergyCorrectionThreeProng" : { "down" : 0.982, "up" : 0.993},
      "TauEnergyCorrectionThreeProngPiZeros" : {"down" : 0.988, "up" : 1.011},
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
  if not isData and not isEmbedded:
    config["tauEsOneProngUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngUp"]["TauEnergyCorrectionOneProng"] = tauES_uncertainties[year]["TauEnergyCorrectionOneProng"]["up"]

    config["tauEsOneProngDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngDown"]["TauEnergyCorrectionOneProng"] = tauES_uncertainties[year]["TauEnergyCorrectionOneProng"]["down"]


    config["tauEsOneProngOnePiZeroUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngOnePiZeroUp"]["TauEnergyCorrectionOneProngPiZeros"] = tauES_uncertainties[year]["TauEnergyCorrectionOneProngPiZeros"]["up"]

    config["tauEsOneProngOnePiZeroDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngOnePiZeroDown"]["TauEnergyCorrectionOneProngPiZeros"] = tauES_uncertainties[year]["TauEnergyCorrectionOneProngPiZeros"]["down"]


    config["tauEsThreeProngUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngUp"]["TauEnergyCorrectionThreeProng"] = tauES_uncertainties[year]["TauEnergyCorrectionThreeProng"]["up"]

    config["tauEsThreeProngDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngDown"]["TauEnergyCorrectionThreeProng"] = tauES_uncertainties[year]["TauEnergyCorrectionThreeProng"]["down"]

    
    config["tauEsThreeProngOnePiZeroUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngOnePiZeroUp"]["TauEnergyCorrectionThreeProngPiZeros"] = tauES_uncertainties[year]["TauEnergyCorrectionThreeProngPiZeros"]["up"]

    config["tauEsThreeProngOnePiZeroDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngOnePiZeroDown"]["TauEnergyCorrectionThreeProngPiZeros"] = tauES_uncertainties[year]["TauEnergyCorrectionThreeProngPiZeros"]["down"]
  elif isEmbedded:
    config["tauEsOneProngUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngUp"]["TauEnergyCorrectionOneProng"] = 1.015

    config["tauEsOneProngDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngDown"]["TauEnergyCorrectionOneProng"] = 0.985


    config["tauEsOneProngOnePiZeroUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngOnePiZeroUp"]["TauEnergyCorrectionOneProngPiZeros"] = 1.015

    config["tauEsOneProngOnePiZeroDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngOnePiZeroDown"]["TauEnergyCorrectionOneProngPiZeros"] = 0.985


    config["tauEsThreeProngUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngUp"]["TauEnergyCorrectionThreeProng"] = 1.015

    config["tauEsThreeProngDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngDown"]["TauEnergyCorrectionThreeProng"] = 0.985

 
     config["tauEsThreeProngOnePiZeroUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngOnePiZeroUp"]["TauEnergyCorrectionThreeProngPiZeros"] = 1.015

    config["tauEsThreeProngOnePiZeroDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngOnePiZeroDown"]["TauEnergyCorrectionThreeProngPiZeros"] = 0.985

  return config
