#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import os

def build_config(nickname, **kwargs):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))


  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  if isEmbedded:
      if "TauTau" in nickname:
          channel = "tt"
      elif "ElTau" in nickname:
          channel = "et"
      elif "MuTau" in nickname:
          channel = "mt"
      elif "ElMu" in nickname:
          channel = "em"
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  #isDY = re.search("DY.?JetsToLLM(50|150)", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)
  year = datasetsHelper.base_dict[nickname]["year"]

  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  if isEmbedded:
    config["scale_metDown"] = {
            "EmbeddingFakeMETCorrectionNumApplies": 2
    }
    config["scale_metUp"] = {
             "EmbeddingFakeMETCorrectionNumApplies": 0
    }

  return config
