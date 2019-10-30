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
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsBTaggedJetID"]

  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname, **kwargs)

  # explicit configuration
  config["Channel"] = "ET"
  config["MinNTaus"] = 1
  config["MaxNLooseElectrons"] = 1
  config["MinNElectrons"] = 1
  config["NElectrons"] = 1

  #config["TauID"] = "TauIDRecommendation13TeV"
  config["TauID"] = "none"
  config["TauUseOldDMs"] = False
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DeltaRTriggerMatchingTaus"] = 0.5
  config["DeltaRTriggerMatchingMuons"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True

  config["CheckTagTriggerMatch"] = [
      "trg_singleelectron_35",
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_crosselectron_ele24tau30",
      "trg_crosselectron_ele24tau30_hps"

  ]
  config["HLTBranchNames"] = [
      "trg_singleelectron_35:HLT_Ele35_WPTight_Gsf",
      "trg_crosselectron_ele24tau30_hps:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1",
      "trg_crosselectron_ele24tau30:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",

  ]

  config["EventWeight"] = "eventWeight"
  if isEmbedded:
    config["ElectronTriggerFilterNames"] = [
            "HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",

      ]
    config["TauTriggerFilterNames"] = [
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3",

      ]
  else:
    config["ElectronTriggerFilterNames"] = [
            "HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30"
      ]
    config["TauTriggerFilterNames"] = [
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltHpsSelectedPFTau30LooseChargedIsolationL1HLTMatched",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltSelectedPFTau30LooseChargedIsolationL1HLTMatched",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30",
      ]
  

  #TriggerMatchingProducers
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  #ValidMuonsProducer
  config["DirectIso"] = True
  config["UseUWGenMatching"] = True

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.TagAndProbeQuantitiesET").build_list()

  config["Processors"] =   []

  config["Processors"].extend((                               "producer:MetSelector",
                                                              "producer:HttValidLooseElectronsProducer",
                                                              "filter:MaxLooseElectronsCountFilter",
                                                              "producer:ValidElectronsProducer",
                                                              "filter:ValidElectronsFilter",
                                                              "filter:ElectronsCountFilter",
                                                              "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "filter:MinTausCountFilter",
                                                              # "producer:HttValidLooseMuonProducer",   # Electrons for electron veto
                                                              # "filter:MaxLooseMuonsCountFilter",
                                                              "producer:ElectronTriggerMatchingProducer",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "producer:TauL1TauTriggerMatchingProducer",
                                                              "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer",
                                                              "producer:NewETTagAndProbePairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              ))

  config["Processors"].append(                                "producer:EventWeightProducer")


  config["AddGenMatchedParticles"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedMuons"] = True
  config["BranchGenMatchedTaus"] = True
  config["Consumers"] = ["NewETTagAndProbePairConsumer",
                         "cutflow_histogram"]

  # pipelines - systematic shifts
  return {"et": config}
