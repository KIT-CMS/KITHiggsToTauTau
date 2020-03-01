#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
import os

def build_config(nickname, **kwargs):
  etau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "etau-fake-es" else False
  mtau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "mtau-fake-es" else False
  tau_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "tau-es" else False

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  year = datasetsHelper.base_dict[nickname]["year"]


  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["FESetaSplit"] = True
  config["TauEnergyCorrection"] = "smhtt2016"

  config["TauEnergyCorrectionOneProng"] = 1.0
  config["TauEnergyCorrectionOneProngPiZeros"] = 1.0
  config["TauEnergyCorrectionThreeProng"] = 1.0
  config["TauElectronFakeEnergyCorrectionOneProng"] = 1.0
  config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.0

  if not re.search("Run201", nickname):
    if not re.search("Embedding", nickname):
      if not tau_es:
        log.info("Tau Energy Correction applied")
        # preliminary numbers from https://ineuteli.web.cern.ch/ineuteli/TauPOG/slides/Izaak_TauPOG_TauES_20191112.pdf
        if year == 2016:
          config["TauEnergyCorrectionOneProng"] = 0.990 # down: 0.984, central: 0.990, up: 0.997
          config["TauEnergyCorrectionOneProngPtGt100"] = 0.991  # error=0.03
          config["TauEnergyCorrectionOneProngPiZeros"] = 0.999 # down: 0.996, central: 0.999, up: 1.003
          config["TauEnergyCorrectionOneProngPiZerosPtGt100"] = 1.042  # error=0.02
          config["TauEnergyCorrectionThreeProng"] = 1.008 # down: 1.004, central: 1.008, up: 1.015
          config["TauEnergyCorrectionThreeProngPtGt100"] = 1.004  # error=0.012
          config["TauEnergyCorrectionThreeProngPiZeros"] = 1.001 # down: 0.991, central: 1.001, up: 1.011
          config["TauEnergyCorrectionThreeProngPiZerosPtGt100"] = 0.97  # error=0.027
        elif year == 2017:
          config["TauEnergyCorrectionOneProng"] = 1.007 # down: 0.999, central: 1.007, up: 1.017
          config["TauEnergyCorrectionOneProngPtGt100"] = 1.004  # error=0.03
          config["TauEnergyCorrectionOneProngPiZeros"] = 1.002 # down: 0.998, central: 1.002, up: 1.007
          config["TauEnergyCorrectionOneProngPiZerosPtGt100"] = 1.014  # error=0.027
          config["TauEnergyCorrectionThreeProng"] = 1.002 # down: 0.997, central: 1.002, up: 1.007
          config["TauEnergyCorrectionThreeProngPtGt100"] = 0.978  # error=0.017
          config["TauEnergyCorrectionThreeProngPiZeros"] = 0.995 # down: 0.985, central: 0.995, up: 1.011
          config["TauEnergyCorrectionThreeProngPiZerosPtGt100"] = 0.944  # error=0.04
        elif year == 2018:
          config["TauEnergyCorrectionOneProng"] = 0.984 # down: 0.977, central: 0.984, up: 0.991
          config["TauEnergyCorrectionOneProngPtGt100"] = 0.984  # error=0.03
          config["TauEnergyCorrectionOneProngPiZeros"] = 0.997 # down: 0.993, central: 0.997, up: 1.001
          config["TauEnergyCorrectionOneProngPiZerosPtGt100"] = 1.004  # error=0.02
          config["TauEnergyCorrectionThreeProng"] = 0.989 # down: 0.984, central: 0.989, up: 0.994
          config["TauEnergyCorrectionThreeProngPtGt100"] = 1.006  # error=0.011
          config["TauEnergyCorrectionThreeProngPiZeros"] = 1.001 # down: 0.992, central: 1.001, up: 1.012
          config["TauEnergyCorrectionThreeProngPiZerosPtGt100"] = 0.955  # error=0.039

      if not etau_fake_es:
        log.info("Fake e->tau Energy Correction applied split in eta")
        if year == 2016:
          config["TauElectronFakeEnergyCorrectionOneProngBarrel"] = 1.00679
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = 1.03389
          config["TauElectronFakeEnergyCorrectionOneProngEndcap"] = 0.965
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = 1.05

        elif year == 2017:
          config["TauElectronFakeEnergyCorrectionOneProngBarrel"] = 1.00911
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = 1.01154
          config["TauElectronFakeEnergyCorrectionOneProngEndcap"] = 0.97396
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = 1.015

        elif year == 2018:
          config["TauElectronFakeEnergyCorrectionOneProngBarrel"] = 1.01362
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = 1.01945
          config["TauElectronFakeEnergyCorrectionOneProngEndcap"] = 0.96903
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = 0.985

        #log.info("Fake e->tau Energy Correction applied inclusive in eta")
        #if year == 2016:
        #  config["TauElectronFakeEnergyCorrectionOneProng"] = 1.004
        #  config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.030
        #elif year == 2017:
        #  config["TauElectronFakeEnergyCorrectionOneProng"] = 1.000
        #  config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.018
        #elif year == 2018:
        #  config["TauElectronFakeEnergyCorrectionOneProng"] = 1.013
        #  config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.017

      #TODO measure mu->tau fake ES for all years (1prong & 1prong pi0's), current values from AN2019_109_v4
      if not mtau_fake_es:
        log.info("Fake m->tau Energy Correction applied")
        if year == 2016:
          config["TauMuonFakeEnergyCorrectionOneProng"] = 1.0
          config["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 0.995
        elif year == 2017:
          config["TauMuonFakeEnergyCorrectionOneProng"] = 0.998
          config["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 0.992
        elif year == 2018:
          config["TauMuonFakeEnergyCorrectionOneProng"] = 0.998
          config["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 0.990
    else:
      if not tau_es:
        log.info("Tau Energy Correction applied")
        if year == 2016:
          config["TauEnergyCorrectionOneProng"] = 0.998
          config["TauEnergyCorrectionOneProngPiZeros"] = 0.9978
          config["TauEnergyCorrectionThreeProng"] = 0.9874
          config["TauEnergyCorrectionThreeProngPiZeros"] = 0.9874
        elif year == 2017:
          config["TauEnergyCorrectionOneProng"] = 0.9996
          config["TauEnergyCorrectionOneProngPiZeros"] = 0.988
          config["TauEnergyCorrectionThreeProng"] = 0.9925
          config["TauEnergyCorrectionThreeProngPiZeros"] = 0.9925
        elif year == 2018:
          config["TauEnergyCorrectionOneProng"] = 0.9967
          config["TauEnergyCorrectionOneProngPiZeros"] = 0.9943
          config["TauEnergyCorrectionThreeProng"] = 0.9926
          config["TauEnergyCorrectionThreeProngPiZeros"] = 0.9926
  return config
