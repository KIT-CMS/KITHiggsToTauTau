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

import HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.ArtusConfigUtility as ACU

def build_config(nickname, **kwargs):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  isGluonFusion = re.search("GluGluHToTauTau.*M125", nickname)
  
  config["Quantities"] = [
    "npu",
    "numberGeneratedEventsWeight",
    "crossSectionPerEventWeight",
    "generatorWeight",
    "npartons",
    "topPtReweightWeightRun1",
    "topPtReweightWeightRun2",
    "htxs_stage0cat",
    "htxs_stage1p1cat",
    "htxs_stage1p1finecat",
    "htxs_njets30",
    "htxs_higgsPt",
    "genbosonmass",
  ]
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.ggHNNLOQuantities").build_list())
  
  
  
  config["Consumers"] = ["KappaLambdaNtupleConsumer"]
  
  # pipelines - systematic shifts
  return ACU.apply_uncertainty_shift_configs('pu', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.syst_shifts_nom").build_config(nickname))
