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
  config["ElectronID_documentation"] = "https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#Electrons"
  config["ElectronReco"] = "mvanontrig"
  config["ElectronID"] = "none"
  config["ElectronIDType"] = "cutbased2015andlater" # still MVA, using boolean functionality of IsCutBased()

  # signal electron ID
  config["ElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90" # better S/sqrt(B)
  #config["ElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90" # already has something like a iso cut ---> not good for side-band regions

  config["ElectronIDList"] = [
    "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp80",
    "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90",
    "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp80",
    "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-veto",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-loose",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-medium",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-tight",
  ]

  config["ElectronIsoType"] = "user"
  config["ElectronIso"] = "none"
  config["ElectronIsoSignalConeSize"] = 0.3
  config["ElectronDeltaBetaCorrectionFactor"] = 0.5
  # reference eA values & bins from https://github.com/cms-sw/cmssw/blob/master/RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_94X.txt
 # config["ElectronEtaBinnedEAValues"] = [0.1440, 0.1562, 0.1032, 0.0859, 0.1116, 0.1321, 0.1654]
 # config["ElectronEtaBinsForEA"] = [0.0, 1.0, 1.479, 2.0, 2.2, 2.3, 2.4, 5.0]
  config["ElectronTrackDxyCut"] = 0.0
  config["ElectronTrackDzCut"] = 0.0
  
  #config["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values" if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"
  
  config["ElectronMvaIDCutEB1"] = 0.967083 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.940962684155
  config["ElectronMvaIDCutEB2"] = 0.929117 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.899208843708
  config["ElectronMvaIDCutEE"] = 0.726311 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.758484721184

  return config