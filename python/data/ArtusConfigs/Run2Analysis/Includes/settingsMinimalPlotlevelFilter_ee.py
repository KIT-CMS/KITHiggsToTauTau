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

def build_config(nickname):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json")
  
  config["PlotlevelFilterExpressionQuantities"] = [
    "extraelec_veto",
    "extramuon_veto"
  ]
  config["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
  
  return config