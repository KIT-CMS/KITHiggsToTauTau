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
  config["VetoElectronReco"] = "none"
  config["VetoElectronID"] = "user"
  config["VetoElectronIDType"] = "cutbased2015andlater"
  # dilepton veto electron ID
  config["VetoElectronIDName"] = "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-veto"
  
  config["VetoElectronIsoType"] = "user"
  config["VetoElectronIso"] = "none"
  config["VetoElectronIsoPtSumOverPtUpperThresholdEB"] = 0.3
  config["VetoElectronIsoPtSumOverPtUpperThresholdEE"] = 0.3
  
  config["VetoElectronLowerPtCuts"] = ["15.0"]
  config["VetoElectronUpperAbsEtaCuts"] = ["2.5"]
  config["DiVetoElectronMinDeltaRCut"] = "0.15"
  config["DiVetoElectronVetoMode"] = "veto_os_keep_ss"
  config["DirectIso"] = True
  
  config["ElectronIDList"] = [
  ]
  config["ElectronEtaBinnedEAValues"] = []
  config["ElectronEtaBinsForEA"] = []
  
  return config
