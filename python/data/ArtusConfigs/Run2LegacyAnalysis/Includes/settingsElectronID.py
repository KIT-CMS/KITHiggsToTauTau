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
import os

def build_config(nickname, **kwargs):

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  year = datasetsHelper.base_dict[nickname]["year"]

  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  isEmbedded = datasetsHelper.isEmbedded(nickname)

  # explicit configuration
  config["ElectronID_documentation"] = "https://twiki.cern.ch/twiki/bin/view/CMS/EgammaRunIIRecommendations"
  config["ElectronReco"] = "mvanontrig"
  config["ElectronID"] = "user"
  config["ElectronIDType"] = "cutbased2015andlater" # still MVA, using boolean functionality of IsCutBased()

  # signal electron ID
  config["ElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp90" # better S/sqrt(B)

  config["ElectronIDList"] = [
    "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wp80",
    "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wp90",
    "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp80",
    "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp90",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-veto",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-loose",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-medium",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-tight",
  ]

  config["ElectronIsoType"] = "user"
  config["ElectronIso"] = "none"
  config["ElectronIsoSignalConeSize"] = 0.3
  config["ElectronDeltaBetaCorrectionFactor"] = 0.5
  # reference eA values & bins from https://github.com/cms-sw/cmssw/blob/master/RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_94X.txt
  if year in [2016, 2017, 2018]:
    config["ElectronEtaBinnedEAValues"] = [0.1440, 0.1562, 0.1032, 0.0859, 0.1116, 0.1321, 0.1654]
    config["ElectronEtaBinsForEA"] = [0.0, 1.0, 1.479, 2.0, 2.2, 2.3, 2.4, 2.5]
  # reference eA values & bins from https://github.com/cms-sw/cmssw/blob/master/RecoEgamma/ElectronIdentification/data/Summer16/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt
  # values for Summer16 Electron ID, not recommended for legacy
  # elif year == 2016:
  #   config["ElectronEtaBinnedEAValues"] = [0.1703, 0.1715, 0.1213, 0.1230, 0.1635, 0.1937, 0.2393]
  #   config["ElectronEtaBinsForEA"] = [0.0, 1.0, 1.479, 2.0, 2.2, 2.3, 2.4, 5.0]

  config["ElectronTrackDxyCut"] = 0.045
  config["ElectronTrackDzCut"] = 0.2

  if isEmbedded:
    if year==2016:
      config["ElectronEnergyCorrectionShiftEB"] = 0.99757
      config["ElectronEnergyCorrectionShiftEE"] = 0.99300
    elif year==2017:
      config["ElectronEnergyCorrectionShiftEB"] = 0.99933
      config["ElectronEnergyCorrectionShiftEE"] = 0.98867
    elif year==2018:
      config["ElectronEnergyCorrectionShiftEB"] = 0.99672
      config["ElectronEnergyCorrectionShiftEE"] = 0.99443     
  else:
      config["ElectronEnergyCorrectionShiftEB"] = 1.0
      config["ElectronEnergyCorrectionShiftEE"] = 1.0    
  return config
