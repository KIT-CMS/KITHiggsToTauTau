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

        config["TauEnergyCorrectionOneProngPtDependantUncShift"] = [0.0, 0.0]
        config["TauEnergyCorrectionOneProngPiZerosPtDependantUncShift"] = [0.0, 0.0]
        config["TauEnergyCorrectionThreeProngPtDependantUncShift"] = [0.0, 0.0]
        config["TauEnergyCorrectionThreeProngPiZerosPtDependantUncShift"] = [0.0, 0.0]

        # preliminary numbers from https://ineuteli.web.cern.ch/ineuteli/TauPOG/slides/Izaak_TauPOG_TauES_20191112.pdf
        if year == 2016:
          config["TauEnergyCorrectionOneProngPtDependant"] = [0.994, 0.991]  # error=0.03
          config["TauEnergyCorrectionOneProngPiZerosPtDependant"] = [0.995, 0.995]  # error=0.03
          config["TauEnergyCorrectionThreeProngPtDependant"] = [1.0, 1.0]  # error=0.03
          # config["TauEnergyCorrectionThreeProngPiZeros"] = 1  # error=0.011  #  1.001 down: 0.991, central: 1.001, up: 1.011
          # config["TauEnergyCorrectionThreeProngPiZerosPtDependant"] = [1.0, 1.0]  # error=0.011  #  1.001 down: 0.991, central: 1.001, up: 1.011
        elif year == 2017:
          config["TauEnergyCorrectionOneProngPtDependant"] = [1.007, 1.004]  # error=0.03
          config["TauEnergyCorrectionOneProngPiZerosPtDependant"] = [0.998, 0.998]  # error=0.03
          config["TauEnergyCorrectionThreeProngPtDependant"] = [1.001, 1.001]  # error=0.03
          # config["TauEnergyCorrectionThreeProngPiZeros"] = 0.999, x=11.5, error=0.01 #  0.995 down: 0.985, central: 0.995, up: 1.011
          # config["TauEnergyCorrectionThreeProngPiZerosPtDependant"] = [0.999, 0.999], x=11.5, error=0.01 #  0.995 down: 0.985, central: 0.995, up: 1.011
        elif year == 2018:
          config["TauEnergyCorrectionOneProngPtDependant"] = [0.987, 0.984]  # error=0.03
          config["TauEnergyCorrectionOneProngPiZerosPtDependant"] = [0.995, 0.995]  # error=0.03
          config["TauEnergyCorrectionThreeProngPtDependant"] = [0.988, 0.988]  # error=0.03
          # config["TauEnergyCorrectionThreeProngPiZeros"] = 0.988  # error=0.008 # 1.001 # down: 0.992, central: 1.001, up: 1.012
          # config["TauEnergyCorrectionThreeProngPiZerosPtDependant"] = [0.988, 0.988]  # error=0.008 # 1.001 # down: 0.992, central: 1.001, up: 1.012

      if not etau_fake_es:
        log.info("Fake e->tau Energy Correction applied split in eta")
        if year == 2016:
          config["TauElectronFakeEnergyCorrectionOneProngBarrel"] = 1.0 + (0.532) / 100.0
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = 1.0 + (5.8) / 100.0
          config["TauElectronFakeEnergyCorrectionOneProngEndcap"] = 1.0 + (+4.922) / 100.0
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = 1.0 + (+1.804) / 100.0

        elif year == 2017:
          config["TauElectronFakeEnergyCorrectionOneProngBarrel"] = 1.0 + (0.126) / 100.0
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = 1.0 + (+3.354) / 100.0
          config["TauElectronFakeEnergyCorrectionOneProngEndcap"] = 1.0 + (-3.440) / 100.0
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = 1.0 + (+0.476) / 100.0

        elif year == 2018:
          config["TauElectronFakeEnergyCorrectionOneProngBarrel"] = 1.0 + (+0.25) / 100.0
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = 1.0 + (+3.610) / 100.0
          config["TauElectronFakeEnergyCorrectionOneProngEndcap"] = 1.0 + (-1.708) / 100.0
          config["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = 1.0 + (-1.8) / 100.0

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

      #TODO measure mu->tau fake ES for all years (1prong & 1prong pi0's)
      if not mtau_fake_es:
        log.info("Fake m->tau Energy Correction applied")
        if year == 2016:
          config["TauMuonFakeEnergyCorrectionOneProng"] = 1.0 # using only 1.5% uncertainty for the time-being
          config["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 1.0 # using only 1.5% uncertainty for the time-being
        elif year == 2017:
          config["TauMuonFakeEnergyCorrectionOneProng"] = 1.0 # using only 2% uncertainty for the time-being
          config["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 1.0 # using only 2% uncertainty for the time-being
        elif year == 2018:
          config["TauMuonFakeEnergyCorrectionOneProng"] = 1.0 # using only 2% uncertainty for the time-being
          config["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 1.0 # using only 2% uncertainty for the time-being

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
