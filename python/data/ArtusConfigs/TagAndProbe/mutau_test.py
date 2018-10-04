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
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mutau_settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mutau_settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mutau_settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mutau_settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mutau_settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mutau_settingsBTaggedJetID",
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["Channel"] = "MT"
  config["MaxNLooseMuons"] = 1
  config["MinNTaus"] = 1
  config["MaxNLooseElectrons"] = 0
  config["NMuons"] = 1
  # HltPaths_comment: The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer..
  if re.search("(Run201|Embedding201|Summer1|Fall1)", nickname): config["HltPaths"] = [
          "HLT_IsoMu24",
          "HLT_IsoMu27",
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
          "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
          "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
  ]

  #config["TauID"] = "TauIDRecommendation13TeV"
  config["TauID"] = "none"
  config["TauUseOldDMs"] = True
  config["MuonLowerPtCuts"] = ["24.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.1"]
  config["TauLowerPtCuts"] = ["20.0"]
  config["TauUpperAbsEtaCuts"] = ["2.1"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DeltaRTriggerMatchingTaus"] = 0.5
  config["DeltaRTriggerMatchingMuons"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["DiTauPairLepton1LowerPtCuts"] = [
          "HLT_IsoMu24_v:25.0",
          "HLT_IsoMu27_v:28.0",
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:21.0",
  ]
  config["DiTauPairLepton2LowerPtCuts"] = [
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:32.0",
  ]
  config["DiTauPairLepton2UpperEtaCuts"] = [
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:2.1",
          "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:2.1",
  ]
  config["CheckTagTriggerMatch"] = [
      "trg_singlemuon_27",
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_singletau_trailing",

      "trg_crossmuon_mu20tau27",
      "trg_monitor_mu24tau35_medium_tightID",
      "trg_monitor_mu24tau35_tight",
      "trg_monitor_mu24tau35_tight_tightID",
  ]
  config["HLTBranchNames"] = [
      "trg_singlemuon_24:HLT_IsoMu24_v",
      "trg_singlemuon_27:HLT_IsoMu27_v",
      "trg_crossmuon_mu20tau27:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v",
      "trg_singleelectron_27:HLT_Ele27_WPTight_Gsf_v",
      "trg_singleelectron_32:HLT_Ele32_WPTight_Gsf_v",
      "trg_singleelectron_32_fallback:HLT_Ele32_WPTight_Gsf_DoubleL1EG_v",
      "trg_singleelectron_35:HLT_Ele35_WPTight_Gsf_v",
      "trg_crossele_ele24tau30:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v",
      "trg_doubletau_35_tightiso_tightid:HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v",
      "trg_doubletau_40_mediso_tightid:HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v",
      "trg_doubletau_40_tightiso:HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v",
      "trg_singletau_leading:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "trg_singletau_trailing:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "trg_muonelectron_mu12ele23:HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_monitor_mu24tau35_medium_tightID:HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v",
      "trg_monitor_mu24tau35_tight:HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v",
      "trg_monitor_mu24tau35_tight_tightID:HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v",
  ]
  config["TauTrigger2017InputOld"] = "$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017.root"
  config["TauTrigger2017Input"] = "$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017_New.root"
  config["TauTrigger2017WorkingPoints"] = [
       "vvloose",
       "vloose",
       "loose",
       "medium",
       "tight",
       "vtight",
       "vvtight",
  ]
  config["TauTrigger2017IDTypes"] = [
       "MVA",
  ]

  config["EventWeight"] = "eventWeight"
  config["MuonTriggerFilterNames"] = [
          "HLT_IsoMu24_v:hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07",
          "HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07",
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded",
          "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
          "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v:hltOverlapFilterIsoMu24MediumChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v:hltOverlapFilterIsoMu24TightChargedIsoPFTau35MonitoringReg",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v:hltOverlapFilterIsoMu24TightChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
    ]
  #TriggerMatchingProducers,HttTriggerSettingsProducer 
  config["TauTriggerFilterNames"] = [
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched",
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded",
          "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v:hltSelectedPFTau35TrackPt1MediumChargedIsolationAndTightOOSCPhotonsL1HLTMatchedReg",
          "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v:hltOverlapFilterIsoMu24MediumChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v:hltSelectedPFTau35TrackPt1TightChargedIsolationL1HLTMatchedReg",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v:hltOverlapFilterIsoMu24TightChargedIsoPFTau35MonitoringReg",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v:hltSelectedPFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsL1HLTMatchedReg",
          "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v:hltOverlapFilterIsoMu24TightChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
          "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltPFTau180TrackPt50LooseAbsOrRelMediumHighPtRelaxedIsoIso",
          "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSelectedPFTau180MediumChargedIsolationL1HLTMatched"
    ]

  #TriggerMatchingProducers
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  #ValidMuonsProducer
  config["DirectIso"] = True

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.TagAndProbeQuantitiesMT").build_list()
  #config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.NewTagAndProbe.Includes.trigQuantities").build_list()
  #config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  #config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.lheWeights").build_list())

  config["Processors"] =   []#                                  ["producer:MuonCorrectionsProducer"] if isEmbedded else []
#  if not (isEmbedded):           config["Processors"].append( "producer:ElectronCorrectionsProducer")

  config["Processors"].extend((                               "producer:HttValidLooseElectronsProducer",   # Electrons for electron veto
                                                              "filter:MaxLooseElectronsCountFilter",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "filter:MaxLooseMuonsCountFilter",
                                                              #"producer:HltProducer",
                                                              "producer:MetSelector",
                                                              "producer:ValidMuonsProducer",
                                                              "filter:ValidMuonsFilter",
                                                              "producer:MuonTriggerMatchingProducer",
                                                              "filter:MuonsCountFilter",
                                                              #"producer:HttValidVetoMuonsProducer",
                                                              "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
                                                              "producer:ValidBTaggedJetsProducer",
                                                              #"producer:ValidMTPairCandidatesProducer",
                                                              "producer:NewMTTagAndProbePairCandidatesProducer",
                                                              #"filter:ValidDiTauPairCandidatesFilter",
                                                              #"producer:Run2DecayChannelProducer",
                                                              #"producer:DiVetoMuonVetoProducer",
                                                              #"producer:TaggedJetCorrectionsProducer",
                                                              #"producer:DiLeptonQuantitiesProducer",
                                                              ))

  config["Processors"].append(                                "producer:EventWeightProducer")


  config["AddGenMatchedParticles"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedMuons"] = True
  config["BranchGenMatchedTaus"] = True
  config["Consumers"] = ["NewMTTagAndProbePairConsumer",
                         "cutflow_histogram"]

  # pipelines - systematic shifts
  return {"mt": config}
