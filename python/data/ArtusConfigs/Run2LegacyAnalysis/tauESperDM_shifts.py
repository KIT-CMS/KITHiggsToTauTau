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
      "TauEnergyCorrectionOneProngPtGt100" : {"down" : 0.991 - 0.03, "up" : 0.991 + 0.03},
      "TauEnergyCorrectionOneProngPiZeros" : {"down" : 0.996, "up" : 1.003},
      "TauEnergyCorrectionOneProngPiZerosPtGt100" : {"down" : 1.042 - 0.02, "up" : 1.042 + 0.02},
      "TauEnergyCorrectionThreeProng" : {"down" : 1.004, "up" : 1.015},
      "TauEnergyCorrectionThreeProngPtGt100" : {"down" : 1.004 - 0.012, "up" : 1.004 + 0.012},
      "TauEnergyCorrectionThreeProngPiZeros" : {"down" : 0.991, "up" : 1.011},
      "TauEnergyCorrectionThreeProngPiZerosPtGt100" : {"down" : 0.97 - 0.027, "up" : 0.97 + 0.027},
    },
    2017: {
      "TauEnergyCorrectionOneProng" : {"down" : 0.999, "up" : 1.017},
      "TauEnergyCorrectionOneProngPtGt100" : {"down" : 1.004 - 0.03, "up" : 1.004 + 0.03},
      "TauEnergyCorrectionOneProngPiZeros" : {"down" : 0.998, "up" : 1.007},
      "TauEnergyCorrectionOneProngPiZerosPtGt100" : {"down" : 1.014 - 0.027, "up" : 1.014 + 0.027},
      "TauEnergyCorrectionThreeProng" : {"down" : 0.997, "up" : 1.007},
      "TauEnergyCorrectionThreeProngPtGt100" : { "down" : 0.978 - 0.017, "up" : 0.978 + 0.017},
      "TauEnergyCorrectionThreeProngPiZeros" : {"down" : 0.985, "up" : 1.011},
      "TauEnergyCorrectionThreeProngPiZerosPtGt100" : {"down" : 0.944 - 0.04, "up" : 0.944 + 0.04},
    },
    2018: {
      "TauEnergyCorrectionOneProng" : {"down" : 0.977, "up" : 0.991},
      "TauEnergyCorrectionOneProngPtGt100" : {"down" : 0.984 - 0.03, "up" : 0.984 + 0.03},
      "TauEnergyCorrectionOneProngPiZeros" : {"down" : 0.993, "up" : 1.001},
      "TauEnergyCorrectionOneProngPiZerosPtGt100" : {"down" : 1.004 - 0.02, "up" : 1.004 + 0.02},
      "TauEnergyCorrectionThreeProng" : {"down" : 0.984, "up" : 0.994},
      "TauEnergyCorrectionThreeProngPtGt100" : { "down" : 1.006 - 0.011, "up" : 1.006 + 0.011},
      "TauEnergyCorrectionThreeProngPiZeros" : {"down" : 0.992, "up" : 1.012},
      "TauEnergyCorrectionThreeProngPiZerosPtGt100" : {"down" : 0.955 - 0.039, "up" : 0.955 + 0.039},
    }
  }

  tauES_uncertainties_embedded = {
    2016 : {
      "TauEnergyCorrectionOneProng" : {"down" : 0.9934, "up" : 1.0026},
      "TauEnergyCorrectionOneProngPiZeros" : {"down" : 0.9953, "up" : 1.000},
      "TauEnergyCorrectionThreeProng" : {"down" : 0.9823, "up" : 0.9907},
      "TauEnergyCorrectionThreeProngPiZeros" : {"down" : 0.9823, "up" : 0.9907},
    },
    2017: {
      "TauEnergyCorrectionOneProng" : {"down" : 0.9954, "up" : 1.0038},
      "TauEnergyCorrectionOneProngPiZeros" : {"down" : 0.9859, "up" : 0.9932},
      "TauEnergyCorrectionThreeProng" : { "down" : 0.9879, "up" : 0.9969},
      "TauEnergyCorrectionThreeProngPiZeros" : { "down" : 0.9879, "up" : 0.9969},
    },
    2018: {
      "TauEnergyCorrectionOneProng" : {"down" : 0.9928, "up" : 1.0006},
      "TauEnergyCorrectionOneProngPiZeros" : {"down" : 0.9912, "up" : 0.998},
      "TauEnergyCorrectionThreeProng" : { "down" : 0.9894, "up" : 0.9958},
      "TauEnergyCorrectionThreeProngPiZeros" : {"down" : 0.9894, "up" : 0.9958},
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
    config["tauEsOneProngUp"]["TauEnergyCorrectionOneProng"] = tauES_uncertainties_embedded[year]["TauEnergyCorrectionOneProng"]["up"]

    config["tauEsOneProngDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngDown"]["TauEnergyCorrectionOneProng"] = tauES_uncertainties_embedded[year]["TauEnergyCorrectionOneProng"]["down"]


    config["tauEsOneProngOnePiZeroUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngOnePiZeroUp"]["TauEnergyCorrectionOneProngPiZeros"] = tauES_uncertainties_embedded[year]["TauEnergyCorrectionOneProngPiZeros"]["up"]

    config["tauEsOneProngOnePiZeroDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsOneProngOnePiZeroDown"]["TauEnergyCorrectionOneProngPiZeros"] = tauES_uncertainties_embedded[year]["TauEnergyCorrectionOneProngPiZeros"]["down"]


    config["tauEsThreeProngUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngUp"]["TauEnergyCorrectionThreeProng"] = tauES_uncertainties_embedded[year]["TauEnergyCorrectionThreeProng"]["up"]

    config["tauEsThreeProngDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngDown"]["TauEnergyCorrectionThreeProng"] = tauES_uncertainties_embedded[year]["TauEnergyCorrectionThreeProng"]["down"]


    config["tauEsThreeProngOnePiZeroUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngOnePiZeroUp"]["TauEnergyCorrectionThreeProngPiZeros"] = tauES_uncertainties_embedded[year]["TauEnergyCorrectionThreeProngPiZeros"]["up"]

    config["tauEsThreeProngOnePiZeroDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEsThreeProngOnePiZeroDown"]["TauEnergyCorrectionThreeProngPiZeros"] = tauES_uncertainties_embedded[year]["TauEnergyCorrectionThreeProngPiZeros"]["down"]

  return config
