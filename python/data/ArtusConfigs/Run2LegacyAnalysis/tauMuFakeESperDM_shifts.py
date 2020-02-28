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
  #isDY = re.search("DY.?JetsToLL", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)
  year = datasetsHelper.base_dict[nickname]["year"]

  # TODO measure corrections & uncertainties for all years
  tauMuFakeES_uncertainties = {
    2016 : {
      "TauMuonFakeEnergyCorrectionOneProng" : {"down" : 0.985, "up" : 1.015},
      "TauMuonFakeEnergyCorrectionOneProngPiZeros" : {"down" : 0.985, "up" : 1.015},
    },
    2017: {
      "TauMuonFakeEnergyCorrectionOneProng" : {"down" : 0.985, "up" : 1.015},
      "TauMuonFakeEnergyCorrectionOneProngPiZeros" : {"down" : 0.985, "up" : 1.015},
    },
    2018: {
      "TauMuonFakeEnergyCorrectionOneProng" : {"down" : 0.985, "up" : 1.015},
      "TauMuonFakeEnergyCorrectionOneProngPiZeros" : {"down" : 0.985, "up" : 1.015},
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
    config["tauMuFakeEsOneProngUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauMuFakeEsOneProngUp"]["TauMuonFakeEnergyCorrectionOneProng"] = tauMuFakeES_uncertainties[year]["TauMuonFakeEnergyCorrectionOneProng"]["up"]

    config["tauMuFakeEsOneProngDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauMuFakeEsOneProngDown"]["TauMuonFakeEnergyCorrectionOneProng"] = tauMuFakeES_uncertainties[year]["TauMuonFakeEnergyCorrectionOneProng"]["down"]


    config["tauMuFakeEsOneProngPiZerosUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauMuFakeEsOneProngPiZerosUp"]["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = tauMuFakeES_uncertainties[year]["TauMuonFakeEnergyCorrectionOneProngPiZeros"]["up"]

    config["tauMuFakeEsOneProngPiZerosDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauMuFakeEsOneProngPiZerosDown"]["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = tauMuFakeES_uncertainties[year]["TauMuonFakeEnergyCorrectionOneProngPiZeros"]["down"]

  return config
