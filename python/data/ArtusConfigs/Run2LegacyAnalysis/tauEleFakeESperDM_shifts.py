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
        "TauElectronFakeEnergyCorrectionOneProng" : {"down" : 0.992, "up" : 1.016},
        "TauElectronFakeEnergyCorrectionOneProngPiZeros" : {"down" : 1.015, "up" : 1.048},
      },
      2017: {
        "TauElectronFakeEnergyCorrectionOneProng" : {"down" : 0.993, "up" : 1.012},
        "TauElectronFakeEnergyCorrectionOneProngPiZeros" : {"down" : 1.006, "up" : 1.036},
      },
      2018: {
        "TauElectronFakeEnergyCorrectionOneProng" : {"down" : 1.008, "up" : 1.020},
        "TauElectronFakeEnergyCorrectionOneProngPiZeros" : {"down" : 0.999, "up" : 1.029},
      }
    },
    'split_eta': {
      2016 : {
        "TauElectronFakeEnergyCorrectionOneProngBarrel" : {"down" : 1.0 + (0.679 - 0.982) / 100, "up" : 1.0 + (0.679 + 0.806) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel" : {"down" : 1.0 + (3.389 - 2.475) / 100, "up" : 1.0 + (3.389 +1.168) / 100},
        "TauElectronFakeEnergyCorrectionOneProngEndcap" : {"down" : 1.0 + (-3.5 - 1.102) / 100, "up" : 1.0 + (-3.5 + 1.808) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap" : {"down" : 1.0 + (5.0 - 5.694) / 100, "up" : 1.0 + (5.0 +6.57) / 100},
      },
      2017: {
        "TauElectronFakeEnergyCorrectionOneProngBarrel" : {"down" : 1.0 + (0.911 - 0.882) / 100, "up" : 1.0 + (0.911 + 1.343) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel" : {"down" : 1.0 + (1.154 - 0.973) / 100, "up" : 1.0 + (1.154 + 2.162) / 100},
        "TauElectronFakeEnergyCorrectionOneProngEndcap" : {"down" : 1.0 + (-2.604 - 1.43) / 100, "up" : 1.0 + (-2.604 + 2.249) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap" : {"down" : 1.0 + (1.5 - 4.969) / 100, "up" : 1.0 + (1.5 + 6.461) / 100},
      },
      2018: {
        "TauElectronFakeEnergyCorrectionOneProngBarrel" : {"down" : 1.0 + (1.362 - 0.474) / 100, "up" : 1.0 + (1.362 + 0.904) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel" : {"down" : 1.0 + (1.945 - 1.598) / 100, "up" : 1.0 + (1.945 + 1.226) / 100},
        "TauElectronFakeEnergyCorrectionOneProngEndcap" : {"down" : 1.0 + (-3.097 - 1.25) / 100, "up" : 1.0 + (-3.097 + 3.404) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap" : {"down" : 1.0 + (-1.5 - 4.309) / 100, "up" : 1.0 + (-1.5 + 5.499) / 100},
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
    config["tauEleFakeEsOneProngUpBarrel"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngUpBarrel"]["TauElectronFakeEnergyCorrectionOneProngBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngBarrel"]["up"]

    config["tauEleFakeEsOneProngDownBarrel"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngDownBarrel"]["TauElectronFakeEnergyCorrectionOneProngBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngBarrel"]["down"]


    config["tauEleFakeEsOneProngPiZerosUpBarrel"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosUpBarrel"]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"]["up"]

    config["tauEleFakeEsOneProngPiZerosDownBarrel"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosDownBarrel"]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"]["down"]

    config["tauEleFakeEsOneProngUpEndcap"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngUpEndcap"]["TauElectronFakeEnergyCorrectionOneProngEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngEndcap"]["up"]

    config["tauEleFakeEsOneProngDownEndcap"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngDownEndcap"]["TauElectronFakeEnergyCorrectionOneProngEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngEndcap"]["down"]


    config["tauEleFakeEsOneProngPiZerosUpEndcap"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosUpEndcap"]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"]["up"]

    config["tauEleFakeEsOneProngPiZerosDownEndcap"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["tauEleFakeEsOneProngPiZerosDownEndcap"]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"]["down"]

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
