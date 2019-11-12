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

  includes = [
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["Channel"] = "MM"
  config["MinNMuons"] = 2
  
  config["HltPaths"] = [
          "HLT_IsoMu22",
          "HLT_IsoTkMu22",
          "HLT_IsoMu22_eta2p1",
          "HLT_IsoTkMu22_eta2p1",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1"
  ]

  # Muon Requirements
  config["MuonIsoTypeUserMode"] = "fromcmsswr04"
  config["MuonIsoType"] = "user"
  config["MuonIsoSignalConeSize"] = 0.4
  config["MuonID"] = "medium"
  config["MuonIso"] = "none"
  config["DirectIso"] = True
  config["MuonDeltaBetaCorrectionFactor"] = 0.5
  config["MuonTrackDxyCut"] = 0.05
  config["MuonTrackDzCut"] = 0.1
  config["MuonLowerPtCuts"] = ["10.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.1"]
  config["MuonIsoPtSumOverPtUpperThresholdEB"] = 0.15
  config["MuonIsoPtSumOverPtUpperThresholdEE"] = 0.15
  config["DiTauPairMinDeltaRCut"] = 1.

  config["Year"] = 2016


  #########################################################
  # for the lepton leg measurement, only the lepton leg 
  # of the crosstrigger has to be matched, 
  # not the tau leg of the crosstrigger !
  #########################################################
    
  config["MuonTriggerFilterNames"] = [
          "HLT_IsoMu22_v:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
          "HLT_IsoTkMu22_v:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09",
          "HLT_IsoMu22_eta2p1_v:hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09",
          "HLT_IsoTkMu22_eta2p1_v:hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
  ]

  config["HLTBranchNames"] = [
      "trg_t_IsoMu22:HLT_IsoMu22_v",
      "trg_t_IsoMu22:HLT_IsoTkMu22_v",
      "trg_t_IsoMu22:HLT_IsoMu22_eta2p1_v",
      "trg_t_IsoMu22:HLT_IsoTkMu22_eta2p1_v",
      "trg_p_IsoMu19Tau20:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
      "trg_p_IsoMu19Tau20:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v",
      "trg_p_IsoMu19Tau20_singleL1:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v",
      "trg_p_IsoMu19Tau20_crossL1:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
      
  ]

  config["CheckTagTriggerMatch"] = [
      "trg_t_IsoMu22"
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_p_IsoMu19Tau20",
      "trg_p_IsoMu19Tau20_singleL1",
      "trg_p_IsoMu19Tau20_crossL1"
  ]
  
  config["TagAdditionalCriteria"] = [
    "pt:23.0",
    "iso_sum:0.15",
    "dxy:0.05",
    "dz:0.1",
  ]

  config["ProbeAdditionalCriteria"] = [
    "pt:10"]

  config["EventWeight"] = "eventWeight"

  config["InvertedMuonL1TauMatching"] = True
  config["MuonTriggerCheckAdditionalL1TauMatchLowerPtCut"] = [
          "trg_p_IsoMu19Tau20:19.",
          "trg_p_IsoMu19Tau20_singleL1:19",
          "trg_p_IsoMu19Tau20_crossL1:19"
  ]
  config["MuonTriggerCheckAdditionalL1TauMatchUpperEtaCut"] = [
          "trg_p_IsoMu19Tau20:2.1",
          "trg_p_IsoMu19Tau20_singleL1:2.1",
          "trg_p_IsoMu19Tau20_crossL1:2.1"
  ]

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.TagAndProbeQuantitiesMMCross").build_list(2016)

  config["Processors"] =   ["producer:ValidMuonsProducer",
                            "filter:ValidMuonsFilter",
                            "producer:MuonTriggerMatchingProducer",
                            "producer:MuonL1TauTriggerMatchingProducer",
                            "filter:MinMuonsCountFilter",
                            "producer:NewMMTagAndProbePairCandidatesProducer",
                            "filter:ValidDiTauPairCandidatesFilter"]

  config["Consumers"] = [#"KappaLambdaNtupleConsumer",
                         "NewMMTagAndProbePairConsumer",
                         "cutflow_histogram"]

  # pipelines - systematic shifts
  return {"mm_crossmuon": config}
