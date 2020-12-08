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
  # Select the JER correction method  - Possibilities are:
  # 1. stochasic method only
  # config["JetEnergyResolutionMethod"] = "stochastic"
  # 2. hybrid method = stochastic + scaling method
  # config["JetEnergyResolutionMethod"] = "hybrid"
	# Details: https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution#Smearing_procedures
  config["JetEnergyResolutionMethod"] = "hybrid"
  # explicit configuration
  if year == 2016:
    config["JetEnergyCorrectionSplitUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017GH_V11_L1fix_DATA_UncertaintySources_AK4PFchs.txt"
    config["JetEnergyResolutionSource"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_25nsV1_MC_PtResolution_AK4PFchs.txt"
    config["JetEnergyResolutionSFSource"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_25nsV1_MC_SF_AK4PFchs.txt"
  elif year == 2017:
    # v3 is the same as v3b for ak4chs jets
    config["JetEnergyCorrectionSplitUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017F_V32_DATA_UncertaintySources_AK4PFchs.txt"
    config["JetEnergyResolutionSource"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_V3_MC_PtResolution_AK4PFchs.txt"
    config["JetEnergyResolutionSFSource"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_V3_MC_SF_AK4PFchs.txt"
  elif year == 2018:
    config["JetEnergyCorrectionSplitUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunD_V19_DATA_UncertaintySources_AK4PFchs.txt"
    config["JetEnergyResolutionSource"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_V7b_MC_PtResolution_AK4PFchs.txt"
    config["JetEnergyResolutionSFSource"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_V7b_MC_SF_AK4PFchs.txt"


  return config
