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
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsElectronID"
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["LooseElectronReco"] = "none"
  config["LooseElectronID"] = "user"
  config["LooseElectronIDType"] = "cutbased2015andlater" # still MVA, using boolean functionality of IsCutBased()
  # extra lepton veto electron ID
  config["LooseElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wpLoose" # better S/sqrt(B)

  config["LooseElectronIsoType"] = "none"
  config["LooseElectronIso"] = "none"
  config["LooseElectronLowerPtCuts"] = ["10.0"]
  config["LooseElectronUpperAbsEtaCuts"] = ["2.5"]

  return config
