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
  includes = ["HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe2016.Includes.mutau_settingsElectronID",
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["LooseElectronReco"] = "none"
  config["LooseElectronID"] = "none"
  config["LooseElectronIDType"] = "cutbased2015andlater" # still MVA, using boolean functionality of IsCutBased()
  #config["LooseElectronIDType"] = "mvabased2015andlater"

  # signal electron ID
  config["LooseElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wpLoose"
  #config["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values" if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"

  #config["LooseElectronMvaIDCutEB1"] = 0.967083 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.940962684155
  #config["ElectronMvaIDCutEB2"] = 0.929117 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.899208843708
  #config["ElectronMvaIDCutEE"] = 0.726311 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.758484721184


  config["LooseElectronIsoType"] = "user"
  config["LooseElectronIso"] = "none"
  config["LooseElectronLowerPtCut"] = ["10.0"]
  config["LooseElectronUpperAbsEtaCut"] = ["2.5"]

  return config
