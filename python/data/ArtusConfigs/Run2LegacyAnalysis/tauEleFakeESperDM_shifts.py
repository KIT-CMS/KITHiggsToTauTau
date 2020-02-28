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
    'inclusive_eta': {
      2016 : {
      "TauElectronFakeEnergyCorrectionOneProng": {"down": 1.019, "up": 1.029},
      "TauElectronFakeEnergyCorrectionOneProngPiZeros": {"down": 1.066, "up": 1.086},
      },
      2017: {
        "TauElectronFakeEnergyCorrectionOneProng": {"down": 0.996, "up": 1.01},
        "TauElectronFakeEnergyCorrectionOneProngPiZeros": {"down": 1.029, "up": 1.043},
      },
      2018: {
        "TauElectronFakeEnergyCorrectionOneProng": {"down": 0.996, "up": 1.01},
        "TauElectronFakeEnergyCorrectionOneProngPiZeros": {"down": 1.029, "up": 1.043},
      }
    },

    'split_eta': {
      2016 : {
        "TauElectronFakeEnergyCorrectionOneProngBarrel": {"down": 1.0 + (+0.532 - 0.740) / 100.0, "up": 1.0 + (+0.532 + 896) / 100.0},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel": {"down": 1.0 + (+5.818 - 1.203) / 100.0, "up": 1.0 + (+5.818 + 1.172) / 100.0},
        "TauElectronFakeEnergyCorrectionOneProngEndcap": {"down": 1.0 + (+4.922 - 3.088) / 100.0, "up": 1.0 + (+4.9220 + 4.085) / 100.0},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap": {"down": 1.0 + (+1.804 - 4.235) / 100.0, "up": 1.0  (+1.804 + 3.420) / 100.0},
      },
      2017: {
        "TauElectronFakeEnergyCorrectionOneProngBarrel": {"down": 1.0 + (+0.126 - 0.959) / 100.0, "up": 1.0 + (+0.126 + 1.041) / 100.0},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel": {"down": 1.0 + (+3.354 - 0.987) / 100.0, "up": 1.0 + (+3.3543 + 1.005) / 100.0},
        "TauElectronFakeEnergyCorrectionOneProngEndcap": {"down": 1.0 + (-3.440 - 4.048) / 100.0, "up": 1.0 + (-3.440 + 4.055) / 100.0},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap": {"down": 1.0 + (+0.476 - 4.753) / 100.0, "up": 1.0 + (+0.476 + 2.418) / 100.0},
      },
      2018: {
        "TauElectronFakeEnergyCorrectionOneProngBarrel": {"down": 1.0 + (+0.25 - 0.252) / 100.0, "up": 1.0 + (+0.25 + 0.438) / 100.0},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel": {"down": 1.0 + (+3.610 - 0.706) / 100.0, "up": 1.0 + (+3.610 + 0.896) / 100.0},
        "TauElectronFakeEnergyCorrectionOneProngEndcap": {"down": 1.0 + (-1.708 - 1.733) / 100.0, "up": 1.0 + (-1.708 + 2.350) / 100.0},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap": {"down": 1.0 + (-1.8 - 2.3) / 100.0, "up": 1.0 + (-1.8 + 2.3) / 100.0},
      }
    },
  }

 ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  log.info("Fake e->tau Energy Correction Uncertainties shifts split in eta")
  tauEleFakeES_uncertainties = tauEleFakeES_uncertainties['split_eta']
  # explicit configuration
  if re.search("DY.?JetsToLL|EWKZ", nickname):
    config["tauEleFakeEsOneProngBarrelUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngBarrelUp"]["TauElectronFakeEnergyCorrectionOneProngBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngBarrel"]["up"]

    config["tauEleFakeEsOneProngBarrelDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngBarrelDown"]["TauElectronFakeEnergyCorrectionOneProngBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngBarrel"]["down"]


    config["tauEleFakeEsOneProngPiZerosBarrelUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosBarrelUp"]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"]["up"]

    config["tauEleFakeEsOneProngPiZerosBarrelDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosBarrelDown"]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"]["down"]

    config["tauEleFakeEsOneProngEndcapUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngEndcapUp"]["TauElectronFakeEnergyCorrectionOneProngEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngEndcap"]["up"]

    config["tauEleFakeEsOneProngEndcapDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngEndcapDown"]["TauElectronFakeEnergyCorrectionOneProngEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngEndcap"]["down"]


    config["tauEleFakeEsOneProngPiZerosEndcapUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosEndcapUp"]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"]["up"]

    config["tauEleFakeEsOneProngPiZerosEndcapDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosEndcapDown"]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"]["down"]

  #log.info("Fake e->tau Energy Correction Uncertainties shifts inclusive in eta")
  #tauEleFakeES_uncertainties = tauEleFakeES_uncertainties['inclusive_eta']
  # explicit configuration
  #if re.search("DY.?JetsToLL|EWKZ", nickname):
  #  config["tauEleFakeEsOneProngUp"] = {
  #    "JetEnergyCorrectionUncertaintyShift" : [0.0]
  #  }
  #  config["tauEleFakeEsOneProngUp"]["TauElectronFakeEnergyCorrectionOneProng"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProng"]["up"]

  #  config["tauEleFakeEsOneProngDown"] = {
  #    "JetEnergyCorrectionUncertaintyShift" : [0.0]
  #  }
  #  config["tauEleFakeEsOneProngDown"]["TauElectronFakeEnergyCorrectionOneProng"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProng"]["down"]

  #  config["tauEleFakeEsOneProngPiZerosUp"] = {
  #    "JetEnergyCorrectionUncertaintyShift" : [0.0]
  #  }
  #  config["tauEleFakeEsOneProngPiZerosUp"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZeros"]["up"]

  #  config["tauEleFakeEsOneProngPiZerosDown"] = {
  #    "JetEnergyCorrectionUncertaintyShift" : [0.0]
  #  }
  #  config["tauEleFakeEsOneProngPiZerosDown"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZeros"]["down"]

  return config
