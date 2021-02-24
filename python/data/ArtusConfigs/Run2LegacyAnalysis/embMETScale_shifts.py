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

  fakeMetScale_uncertainties = {
    2016 : {
        "tt": {"down" : 0.949*0.949, "up" : 1.0},
        "et": {"down" : 0.958*0.958, "up" : 1.0},
        "mt": {"down" : 0.962*0.962, "up" : 1.0},
        "em": {"down" : 0.992*0.992, "up" : 1.0},
    },
    2017 : {
        "tt": {"down" : 0.918*0.918, "up" : 1.0},
        "et": {"down" : 0.960*0.960, "up" : 1.0},
        "mt": {"down" : 0.952*0.952, "up" : 1.0},
        "em": {"down" : 0.955*0.955, "up" : 1.0},
    },
    2018 : {
        "tt": {"down" : 0.900*0.900, "up" : 1.0},
        "et": {"down" : 0.935*0.935, "up" : 1.0},
        "mt": {"down" : 0.931*0.931, "up" : 1.0},
        "em": {"down" : 0.957*0.957, "up" : 1.0},
    },
  }

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
            "EmbedddingFakeMETCorrection" : fakeMetScale_uncertainties[year][channel]["up"]
    }
    config["scale_metUp"] = {
            "EmbedddingFakeMETCorrection" : fakeMetScale_uncertainties[year][channel]["down"]
    }

  return config
