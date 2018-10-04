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
  config["JetID"] = "tight"
  config["JetIDVersion"] = "2017"
  config["PuJetIDs"] = []
  config["PuJetIDFullDiscrName"] = "pileupJetIdfullDiscriminant"
  config["JetTaggerLowerCuts"] = []
  config["JetTaggerUpperCuts"] = []
  config["JetLowerPtCuts"] = ["20.0"]
  config["JetUpperAbsEtaCuts"] = ["4.7"]
  config["JetLeptonLowerDeltaRCut"] = 0.5


  return config
