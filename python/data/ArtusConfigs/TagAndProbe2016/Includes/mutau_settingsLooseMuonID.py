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
  config["LooseMuonID"] = "looseHIPsafe2016" if re.search("(Run|Embedding)2016(B|C|D|E|F)|Spring16", nickname) else "loose"

  config["LooseMuonIsoTypeUserMode"] = "fromcmsswr04"

  config["LooseMuonIsoType"] = "user"
  config["LooseMuonIso"] = "none"
  config["LooseMuonDeltaBetaCorrectionFactor"] = 0.5
  config["LooseMuonIsoPtSumOverPtUpperThresholdEB"] = 0.3
  config["LooseMuonIsoPtSumOverPtUpperThresholdEE"] = 0.3

  config["LooseMuonLowerPtCuts"] = ["10.0"]
  config["LooseMuonUpperAbsEtaCuts"] = ["2.4"]
  config["LooseMuonTrackDxyCut"] = -1.0
  config["LooseMuonTrackDzCut"] = -1.0
  config["DirectIso"] = True

  ## further settings taken into account by ValidLooseMuonsProducer:
  # - Year (should be 2017), written into the 'base' config

  return config
