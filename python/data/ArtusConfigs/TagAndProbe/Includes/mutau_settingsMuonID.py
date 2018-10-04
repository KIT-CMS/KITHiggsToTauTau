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
  config["MuonID"] = "medium"

  config["MuonIsoTypeUserMode"] = "fromcmsswr04"

  config["MuonIsoType"] = "user"
  config["MuonIso"] = "none"
  config["MuonIsoSignalConeSize"] = 0.4
  config["MuonDeltaBetaCorrectionFactor"] = 0.5
  config["MuonIsoPtSumOverPtUpperThresholdEB"] = 0.1
  config["MuonIsoPtSumOverPtUpperThresholdEE"] = 0.1

  config["MuonLowerPtCuts"] = ["24.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.1"]
  config["MuonTrackDxyCut"] = -1.0
  config["MuonTrackDzCut"] = -1.0
  config["DirectIso"] = True

  ## further settings taken into account by ValidMuonsProducer:
  # - Year (should be 2017), written into the 'base' config

  return config
