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
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsLooseElectronID",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsLooseMuonID",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsElectronID",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsVetoMuonID",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsMuonID",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsTauID",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsJEC",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsSvfit",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsJetID",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsBTaggedJetID",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsTauES",
   # "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsMinimalPlotlevelFilter_mt"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["Channel"] = "MM"
  config["MinNMuons"] = 2

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
  config["MuonLowerPtCuts"] = ["8.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.1"]
  config["MuonIsoPtSumOverPtUpperThresholdEB"] = 0.15
  config["MuonIsoPtSumOverPtUpperThresholdEE"] = 0.15
  config["DiTauPairMinDeltaRCut"] = 1.

  config["Year"] = 2018
    
  config["MuonTriggerFilterNames"] = [
          "HLT_IsoMu24_v:hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07",
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered0p07",#hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered0p07",
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v:hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered0p07",#hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered0p07",
          "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_eta2p1_SingleL1_v:hltL3crIsoL1sSingleMu22erL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
    ]

  config["HLTBranchNames"] = [
      "trg_t_IsoMu24:HLT_IsoMu24_v",
      "trg_p_mu20tau27:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v",
      "trg_p_mu20tau27:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v",
      "trg_p_mu24tau20:HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_eta2p1_SingleL1_v",
  ]

  config["CheckTagTriggerMatch"] = [
      "trg_t_IsoMu24"
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_p_mu20tau27",
      "trg_p_mu24tau20"
  ]
  
  config["TagAdditionalCriteria"] = [
    "pt:25.0",
    "iso_sum:0.15",
    "dxy:0.05",
    "dz:0.1",
  ]

  config["ProbeAdditionalCriteria"] = [
    "pt:10"]

  config["EventWeight"] = "eventWeight"

  config["InvertedMuonL1TauMatching"] = True
  config["MuonTriggerCheckAdditionalL1TauMatchLowerPtCut"] = [
          "trg_p_mu20tau27:24."
  ]
  config["MuonTriggerCheckAdditionalL1TauMatchUpperEtaCut"] = [
          "trg_p_mu20tau27:2.1"
  ]

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.TagAndProbeQuantitiesMMCross").build_list(2018)

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
