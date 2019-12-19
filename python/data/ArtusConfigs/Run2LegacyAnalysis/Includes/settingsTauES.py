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
  fes_eta_split = True if "fes_eta_split" in kwargs and kwargs["fes_eta_split"] else False

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
  config["TauEnergyCorrection"] = "smhtt2016"

  config["TauEnergyCorrectionOneProng"] = 1.0
  config["TauEnergyCorrectionOneProngPiZeros"] = 1.0
  config["TauEnergyCorrectionThreeProng"] = 1.0
  config["TauElectronFakeEnergyCorrectionOneProng"] = 1.0
  config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.0

  if not re.search("Run201|Embedding", nickname):
    if not tau_es:
      log.info("Tau Energy Correction applied")
      # recent numbers for Tau ES: m_vis fit: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV#Tau_energy_scale
      if year == 2016:
        config["TauEnergyCorrectionOneProng"] = 0.994 # down: 0.984, central: 0.994, up: 1.004
        config["TauEnergyCorrectionOneProngPiZeros"] = 0.995 # down: 0.986, central: 0.995, up: 1.004
        config["TauEnergyCorrectionThreeProng"] = 1.000 # down: 0.989, central: 1.000, up: 1.011
      elif year == 2017:
        config["TauEnergyCorrectionOneProng"] = 1.007 # down: 0.999, central: 1.007, up: 1.015
        config["TauEnergyCorrectionOneProngPiZeros"] = 0.998 # down: 0.990, central: 0.998, up: 1.006
        config["TauEnergyCorrectionThreeProng"] = 1.001 # down: 0.992, central: 1.001, up: 1.010
      elif year == 2018:
        config["TauEnergyCorrectionOneProng"] = 0.987 # down: 0.976, central: 0.987, up: 0.998
        config["TauEnergyCorrectionOneProngPiZeros"] = 0.995 # down: 0.986, central: 0.995, up: 1.004
        config["TauEnergyCorrectionThreeProng"] = 0.988 # down: 0.980, central: 0.988, up: 0.996

    if not etau_fake_es:
      if fes_eta_split:
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

      else:
        log.info("Fake e->tau Energy Correction applied inclusive in eta")
        if year == 2016:
          config["TauElectronFakeEnergyCorrectionOneProng"] = 1.024 # values for 2016 measured by IC; down: 1.019, central: 1.024, up: 1.029
          config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.076 # values for 2016 measured by IC; down: 1.066, central 1.076, up: 1.086
        elif year == 2017:
          config["TauElectronFakeEnergyCorrectionOneProng"] = 1.003 # values for 2017 measured by RWTH/KIT; down: 0.996, central: 1.003, up: 1.01
          config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.036 # values for 2017 measured by RWTH/KIT; down: 1.029, central 1.036, up: 1.043
        elif year == 2018:
          config["TauElectronFakeEnergyCorrectionOneProng"] = 1.003 # values for 2017 measured by RWTH/KIT; down: 0.996, central: 1.003, up: 1.01 #TODO measure for 2018
          config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.036 # values for 2017 measured by RWTH/KIT; down: 1.029, central 1.036, up: 1.043 #TODO measure for 2018

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

  return config
