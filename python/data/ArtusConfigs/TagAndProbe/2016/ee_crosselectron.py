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
  btag_eff = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "btag-eff" else False

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  isSignal = re.search("HToTauTau",nickname)

  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.ee_settingsElectronID",
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["Channel"] = "EE"
  config["MinNLooseElectrons"] = 2
  config["MinNElectrons"] = 2
  config["Year"] = 2016

  # Electron Requirements
  config["ElectronLowerPtCuts"] = ["10.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.4"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["TagElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp90"
  config["TagElectronSecondIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp80"
 
  config["ElectronTrackDxyCut"] = 0.05
  config["ElectronTrackDzCut"] = 0.1
  config["ElectronIsoPtSumOverPtUpperThresholdEE"] = 0.1
  config["ElectronIsoPtSumOverPtUpperThresholdEB"] = 0.1
  config["DirectIso"] = True
    
  config["HltPaths"] = [
      "HLT_Ele25_eta2p1_WPTight_Gsf"
  ]

  #########################################################
  # for the lepton leg measurement, only the lepton leg 
  # of the crosstrigger has to be matched, 
  # not the tau leg of the crosstrigger !
  #########################################################
  config["ElectronTriggerFilterNames"] = [
    "HLT_Ele25_eta2p1_WPTight_Gsf_v:hltEle25erWPTightGsfTrackIsoFilter",
    "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v:hltEle24WPLooseL1SingleIsoEG22erGsfTrackIsoFilter",
    "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v:hltEle24WPLooseL1IsoEG22erTau20erGsfTrackIsoFilter",
    "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v:hltEle24WPLooseL1IsoEG22erIsoTau26erGsfTrackIsoFilter",
    ]

  config["HLTBranchNames"] = [
      "trg_t_Ele25eta2p1WPTight:HLT_Ele25_eta2p1_WPTight_Gsf_v",
      "trg_p_ele24tau20_singleL1:HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v",
      "trg_p_ele24tau20_crossL1:HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v",
      "trg_p_ele24tau30_crossL1:HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v"    
  ]

  config["CheckTagTriggerMatch"] = [
      "trg_t_Ele25eta2p1WPTight"
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_p_ele24tau20_singleL1",
      "trg_p_ele24tau20_crossL1",
      "trg_p_ele24tau30_crossL1"
  ]
  config["TagAdditionalCriteria"] = [
    "pt:26.0",
    "eta:2.1",
    "iso_sum:0.1",
    "dxy:0.045",
    "dz:0.1",
  ]

  config["EventWeight"] = "eventWeight"

  config["InvertedElectronL1TauMatching"] = True
  config["ElectronTriggerCheckAdditionalL1TauMatchLowerPtCut"] = [
          "trg_p_ele24tau20_singleL1:19",
          "trg_p_ele24tau20_crossL1:19",
          "trg_p_ele24tau30_crossL1:25"
  ]
  config["ElectronTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau"] = [
          "trg_p_ele24tau20_singleL1:2.1",
          "trg_p_ele24tau20_crossL1:2.1",
          "trg_p_ele24tau30_crossL1:2.1"
  ]

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.TagAndProbeQuantitiesEECross").build_list(config["Year"])

  config["Processors"] =   [#"producer:HltProducer",
                            "producer:ValidElectronsProducer",
                            "filter:ValidElectronsFilter",
                            "producer:ElectronTriggerMatchingProducer",
                            "producer:ElectronL1TauTriggerMatchingProducer",
                            "filter:MinElectronsCountFilter",
                            "producer:NewEETagAndProbePairCandidatesProducer",
                            "filter:ValidDiTauPairCandidatesFilter"]

  config["Consumers"] = [#"KappaLambdaNtupleConsumer",
                         "NewEETagAndProbePairConsumer",
                         "cutflow_histogram"]

  # pipelines - systematic shifts
  return {'ee_crosselectron': config}
