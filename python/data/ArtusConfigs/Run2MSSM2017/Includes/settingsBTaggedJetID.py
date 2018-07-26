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

def build_config(nickname):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  
  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["BTaggedJetID_documentation"] = "https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#b_tagging"

  # settings for CSVv2 algorithm 94X recommendation
  #config["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_94XSF_V2_B_F.csv"
  #config["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies_moriond2017.root"
  #config["BTaggedJetCombinedSecondaryVertexName"] = "pfCombinedInclusiveSecondaryVertexV2BJetTags"
  #config["BTaggerWorkingPoints"] = [
  #  "tight:0.9693",
  #  "medium:0.8838",
  #  "loose:0.5803"
  #]

  # settings for DeepCSV algorithm 94X recommendation (stated to perform better than CSVv2)
  config["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepCSV_94XSF_V3_B_F.csv"
  config["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies_moriond2017.root"
  config["BTaggedJetCombinedSecondaryVertexName"] = "pfDeepCSVJetTagsprobbb+pfDeepCSVJetTagsprobb"
  config["BTaggerWorkingPoints"] = [
    "tight:0.8001",
    "medium:0.4941",
    "loose:0.1522"
  ]

  config["BTaggedJetAbsEtaCut"] = 2.5 # 2017 value
  config["ApplyBTagSF"] = True
  config["JetTaggerUpperCuts"] = []
  config["BTagSFMethod"] = "PromotionDemotion"
  config["BTagShift"] = 0
  config["BMistagShift"] = 0

  ## further settings taken into account by ValidBTaggedJetsProducer:
  # - Year (should be 2017), written into the 'base' config
  
  ## further hard-coded settings in the ValidBTaggedJetsProducer:
  # lower pt_cut for the Jet: 20 GeV -> valid for 2016 & 2017
  # upper pt_cut for the Jet: 1000 GeV -> valid for 2016 & 2017
  # parton flavour definition: hadron-based
  # b- and c- jets: combined measurement type, light jets: inclusive measurement type

  return config
