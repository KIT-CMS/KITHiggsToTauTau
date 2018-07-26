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

def build_config(nickname):
  config = jsonTools.JsonDict()
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  
  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsElectronID"
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["LooseElectronReco"] = "mvanontrig"
  config["LooseElectronID"] = "user"
  config["LooseElectronIDType"] = "cutbased2015andlater" # still MVA, using boolean functionality of IsCutBased()
  # extra lepton veto electron ID
  config["LooseElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90" # better S/sqrt(B)
  #config["LooseElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90" # already has something like a iso cut ---> not good for side-band regions

  config["LooseElectronIsoType"] = "user"
  config["LooseElectronIso"] = "none"
  config["LooseElectronIsoPtSumOverPtUpperThresholdEB"] = 0.3
  config["LooseElectronIsoPtSumOverPtUpperThresholdEE"] = 0.3
  config["LooseElectronLowerPtCuts"] = ["10.0"]
  config["LooseElectronUpperAbsEtaCuts"] = ["2.5"]
  config["LooseElectronTrackDxyCut"] = 0.045
  config["LooseElectronTrackDzCut"] = 0.2
  config["DirectIso"] = True

  config["ElectronIDList"] = [
  ]
  config["ElectronEtaBinnedEAValues"] = []
  config["ElectronEtaBinsForEA"] = []


  return config
