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
  #isEmbedded = datasetsHelper.isEmbedded(nickname)
  #isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  #isDY = re.search("DY.?JetsToLL", nickname)
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
  if not re.search("Run201|Embedding", nickname):
    # grouped JEC uncs documented in https://docs.google.com/spreadsheets/d/1Feuj1n0MdotcPq19Mht7SUIgvkXkA4hiB0BxEuBShLw/edit#gid=1345121349
    
    config["jecUncAbsoluteUp"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : 1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "SinglePionECAL",
            "SinglePionHCAL",
            "AbsoluteMPFBias",
            "AbsoluteScale",
            "Fragmentation",
            "PileUpDataMC",
            "RelativeFSR",
            "PileUpPtRef"
        ]
    }
    config["jecUncAbsoluteDown"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : -1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "SinglePionECAL",
            "SinglePionHCAL",
            "AbsoluteMPFBias",
            "AbsoluteScale",
            "Fragmentation",
            "PileUpDataMC",
            "RelativeFSR",
            "PileUpPtRef"
        ]
    }
    
    config["jecUncAbsoluteYearUp"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : 1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "AbsoluteStat",
            "TimePtEta",
            "RelativeStatFSR"
        ]
    }
    config["jecUncAbsoluteYearDown"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : -1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "AbsoluteStat",
            "TimePtEta",
            "RelativeStatFSR"
        ]
    }
  return config
