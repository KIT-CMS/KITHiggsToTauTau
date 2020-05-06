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
  nmssm = True if ("nmssm" in kwargs and kwargs["nmssm"]) else False
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  config["PlotlevelFilterExpressionQuantities"] = [
    "flagMETFilter",
    "extraelec_veto",
    "extramuon_veto",
    "nBJets20",
  ]
  config["PlotlevelFilterExpression"] = "(flagMETFilter > 0.5)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"

  # remove events with no b jets for nmssm analysis
  if nmssm:
    config["PlotlevelFilterExpressionQuantities"].append('nBJets20')
    config["PlotlevelFilterExpression"] += '*(nBJets20 > 0.5)'


  return config
