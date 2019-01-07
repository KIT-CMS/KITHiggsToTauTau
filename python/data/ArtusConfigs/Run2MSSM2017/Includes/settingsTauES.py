#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
#import os

def build_config(nickname, **kwargs):
  etau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "etau-fake-es" else False
  tau_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "tau-es" else False
  config = jsonTools.JsonDict()
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))


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
      # recent numbers for Tau ES: Slide 14, m_vis fit: https://indico.cern.ch/event/763206/contributions/3170631/attachments/1730040/2795667/Izaak_TauPOG_TauES_20181008_v0.pdf
      config["TauEnergyCorrectionOneProng"] = 1.007 # down: 0.999, central: 1.007, up: 1.015
      config["TauEnergyCorrectionOneProngPiZeros"] = 0.998 # down: 0.990, central: 0.998, up: 1.006
      config["TauEnergyCorrectionThreeProng"] = 1.001 # down: 0.992, central: 1.001, up: 1.010

    if not etau_fake_es:
      config["TauElectronFakeEnergyCorrectionOneProng"] = 1.003 # values for 2017 measured by RWTH/KIT; uncertainties down: 0.996, central: 1.003, up: 1.01
      config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.036 # values for 2017 measured by RWTH/KIT; uncertainties down: 1.029, central 1.036, up: 1.043

  return config
