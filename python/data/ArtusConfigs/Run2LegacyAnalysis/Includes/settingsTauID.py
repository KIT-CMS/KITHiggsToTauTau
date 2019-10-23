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
  #config["TauID_documentation"] = []
  config["TauDiscriminatorIsolationName"] = "byDeepTau2017v2p1VSjetraw" # Fall17 trainings
  config["TauDiscriminators"] = ["byVVVLooseDeepTau2017v2p1VSjet"]
  config["TauElectronLowerDeltaRCut"] = -1.0
  config["TauMuonLowerDeltaRCut"] = -1.0


  return config
