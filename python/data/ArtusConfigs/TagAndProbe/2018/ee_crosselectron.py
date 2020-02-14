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
  config["Year"] = 2018

  # Electron Requirements
  config["ElectronLowerPtCuts"] = ["10.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.1"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["TagElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp90"
  #config["OldElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTri  #config["TagElectronSecondIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90"
  config["ElectronID"] = "user"
  config["ElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp90"
  config["ElectronTrackDxyCut"] = 0.05
  config["ElectronTrackDzCut"] = 0.1
  config["ElectronIsoPtSumOverPtUpperThresholdEE"] = 0.1
  config["ElectronIsoPtSumOverPtUpperThresholdEB"] = 0.1
  config["DirectIso"] = True
    
  config["ElectronTriggerFilterNames"] = [
      "HLT_Ele27_WPTight_Gsf_v:hltEle27WPTightGsfTrackIsoFilter",
      "HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter",
      "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",
  ]
  if isEmbedded:
    config["TauTriggerFilterNames"] = [
      "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3",
      "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3"]
  else:
    config["TauTriggerFilterNames"] = [
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltSelectedPFTau30LooseChargedIsolationL1HLTMatched",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltHpsSelectedPFTau30LooseChargedIsolationL1HLTMatched",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30"]

  config["HLTBranchNames"] = [
      "trg_t_Ele27:HLT_Ele27_WPTight_Gsf_v",
      "trg_t_Ele35:HLT_Ele35_WPTight_Gsf_v",
      "trg_p_ele24tau30:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v",
      "trg_p_ele24tau30:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v"
  ]

  config["CheckTagTriggerMatch"] = [
      "trg_t_Ele35",
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_p_ele24tau30"
  ]
  
  config["TagAdditionalCriteria"] = [
    "pt:29.0",
    "eta:2.1",
    "iso_sum:0.1",
    "dxy:0.05",
    "dz:0.1",
  ]

  config["EventWeight"] = "eventWeight"

  config["InvertedElectronL1TauMatching"] = True
  config["ElectronTriggerCheckAdditionalL1TauMatchLowerPtCut"] = [
          "trg_p_ele24tau30:26."
  ]
  config["ElectronTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau"] = [
          "trg_p_ele24tau30"
  ]

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.TagAndProbeQuantitiesEECross").build_list()

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
