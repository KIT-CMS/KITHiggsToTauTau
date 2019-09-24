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
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.mt_settingsBTaggedJetID",
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

  #config["TauID"] = "TauIDRecommendation13TeV"
  config["TauID"] = "none"
  config["TauUseOldDMs"] = True
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DeltaRTriggerMatchingTaus"] = 0.5
  config["DeltaRTriggerMatchingMuons"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True

  config["CheckTagTriggerMatch"] = [
      "trg_singlemuon_27",
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_crossmuon_mu20tau27_hps",
      "trg_crossmuon_mu20tau27",
      "trg_monitor_mu20tau27_hps",
      "trg_monitor_mu20tau27",
      "trg_monitor_mu24tau35_mediso_hps",
      "trg_monitor_mu24tau35_mediso",
      "trg_monitor_mu24tau40_mediso_tightid_hps",
      "trg_monitor_mu24tau40_mediso_tightid",
      "trg_monitor_mu24tau40_tightiso_hps",
      "trg_monitor_mu24tau40_tightiso",
      "trg_monitor_mu24tau35_tightiso_tightid_hps",
      "trg_monitor_mu24tau35_tightiso_tightid",
      "trg_monitor_mu27tau20_hps",
      "trg_monitor_mu27tau20",
      "trg_singletau_trailing",
      "trg_singletau_leading",
  ]
  config["HLTBranchNames"] = [
      "trg_singlemuon_27:HLT_IsoMu27_v",

      "trg_crossmuon_mu20tau27_hps:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v",
      "trg_crossmuon_mu20tau27:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v",
      "trg_monitor_mu20tau27_hps:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v",
      "trg_monitor_mu20tau27:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v",

      "trg_monitor_mu24tau35_mediso_hps:HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v",
      # Measurement for 40 GeV legs performed with 35 GeV threshold tightened to 40 GeV.
      "trg_monitor_mu24tau40_mediso_tightid_hps:HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v",
      "trg_monitor_mu24tau40_tightiso_hps:HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v",
      "trg_monitor_mu24tau35_tightiso_tightid_hps:HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v",
      "trg_monitor_mu24tau35_mediso:HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v",
      # Measurement for 40 GeV legs performed with 35 GeV threshold tightened to 40 GeV.
      "trg_monitor_mu24tau40_mediso_tightid:HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v",
      "trg_monitor_mu24tau40_tightiso:HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v",
      "trg_monitor_mu24tau35_tightiso_tightid:HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v",

      "trg_monitor_mu27tau20_hps:HLT_IsoMu27_LooseChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1_v",
      "trg_monitor_mu27tau20:HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v",

      "trg_singletau_leading:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "trg_singletau_trailing:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
  ]
  config["TauTriggerInputOld"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2017.root"
  config["TauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2017_New.root"
  config["TauTriggerWorkingPoints"] = [
       "vvloose",
       "vloose",
       "loose",
       "medium",
       "tight",
       "vtight",
       "vvtight",
  ]
  config["TauTriggerIDTypes"] = [
       "MVA",
  ]

  config["EventWeight"] = "eventWeight"
  #TriggerMatchingProducers,HttTriggerSettingsProducer
  if isEmbedded:
      config["MuonTriggerFilterNames"] = [
              "HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",

              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v:hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered0p07",
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07",

              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",

              "HLT_IsoMu27_LooseChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
              "HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
        ]
      config["TauTriggerFilterNames"] = [
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v:hltL1sBigORMu18erTauXXer2p1",
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltL1sMu18erTau24erIorMu20erTau24er",

              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltSingleL2IsoTau26eta2p2",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltSingleL2IsoTau26eta2p2",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltSingleL2IsoTau26eta2p2",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltSingleL2IsoTau26eta2p2",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltSingleL2IsoTau26eta2p2",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltSingleL2IsoTau26eta2p2",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltSingleL2IsoTau26eta2p2",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltSingleL2IsoTau26eta2p2",

              "HLT_IsoMu27_LooseChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1_v:hltSingleL2IsoTau20eta2p2",
              "HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v:hltSingleL2IsoTau20eta2p2",

              "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSingleL2Tau80eta2p2",
        ]
  else:
      config["MuonTriggerFilterNames"] = [
              "HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",

              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v:hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered0p07",
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded",
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07",
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded",

              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu24MediumChargedIsoPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu24MediumChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu24TightChargedIsoPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu24TightChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_eta2p1_CrossL1_v:hltOverlapFilterIsoMu24MediumChargedIsoPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltOverlapFilterIsoMu24MediumChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltOverlapFilterIsoMu24TightChargedIsoPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltL3crIsoL1sBigOrMuXXerIsoTauYYerL1f0L2f10QL3f24QL3trkIsoFiltered0p07",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltOverlapFilterIsoMu24TightChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",

              "HLT_IsoMu27_LooseChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
              "HLT_IsoMu27_LooseChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1_v:hltHpsOverlapFilterIsoMu27LooseChargedIsoPFTau20",
              "HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
              "HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v:hltOverlapFilterIsoMu27LooseChargedIsoPFTau20",
        ]
      config["TauTriggerFilterNames"] = [
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v:hltHpsSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched",
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded",
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched",
              "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded",

              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltHpsSelectedPFTau35TrackPt1MediumChargedIsolationL1HLTMatchedReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu24MediumChargedIsoPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltHpsSelectedPFTau35TrackPt1MediumChargedIsolationAndTightOOSCPhotonsL1HLTMatchedReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu24MediumChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltHpsSelectedPFTau35TrackPt1TightChargedIsolationL1HLTMatchedReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu24TightChargedIsoPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltHpsSelectedPFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsL1HLTMatchedReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoMu24TightChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltSelectedPFTau35TrackPt1MediumChargedIsolationL1HLTMatchedReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltOverlapFilterIsoMu24MediumChargedIsoPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltSelectedPFTau35TrackPt1MediumChargedIsolationAndTightOOSCPhotonsL1HLTMatchedReg",
              "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltOverlapFilterIsoMu24MediumChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltSelectedPFTau35TrackPt1TightChargedIsolationL1HLTMatchedReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_CrossL1_v:hltOverlapFilterIsoMu24TightChargedIsoPFTau35MonitoringReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltSelectedPFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsL1HLTMatchedReg",
              "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_CrossL1_v:hltOverlapFilterIsoMu24TightChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",

              "HLT_IsoMu27_LooseChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1_v:hltHpsPFTau20TrackLooseChargedIsoAgainstMuon",
              "HLT_IsoMu27_LooseChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1_v:hltHpsOverlapFilterIsoMu27LooseChargedIsoPFTau20",
              "HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v:hltPFTau20TrackLooseChargedIsoAgainstMuon",
              "HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v:hltOverlapFilterIsoMu27LooseChargedIsoPFTau20",

              "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltPFTau180TrackPt50LooseAbsOrRelMediumHighPtRelaxedIsoIso",
              "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSelectedPFTau180MediumChargedIsolationL1HLTMatched",
        ]
  """
  if isEmbedded:
      config["CheckTriggerLowerPtCutsByHltNick"] = [
              "trg_monitor_mu20tau27_hps:30.0",
              "trg_monitor_mu20tau27:30.0",
              "trg_monitor_mu24tau35_mediso_hps:35.0",
              "trg_monitor_mu24tau35_mediso:35.0",
              "trg_monitor_mu24tau40_mediso_tightid_hps:40.0",
              "trg_monitor_mu24tau40_mediso_tightid:40.0",
              "trg_monitor_mu24tau40_tightiso_hps:40.0",
              "trg_monitor_mu24tau40_tightiso:40.0",
              "trg_monitor_mu24tau35_tightiso_tightid_hps:35.0",
              "trg_monitor_mu24tau35_tightiso_tightid:35.0",
      ]
  else:
      config["CheckTriggerLowerPtCutsByHltNick"] = [
              "trg_monitor_mu20tau27_hps:30.0",
              "trg_monitor_mu20tau27:30.0",
              "trg_monitor_mu24tau40_mediso_tightid_hps:40.0",
              "trg_monitor_mu24tau40_mediso_tightid:40.0",
              "trg_monitor_mu24tau40_tight_hps:40.0",
              "trg_monitor_mu24tau40_tight:40.0",
      ]
  """
  config["TauTriggerCheckAdditionalL1TauMatchLowerPtCut"] = [
          "trg_monitor_mu20tau27_hps:26.0",
          "trg_monitor_mu20tau27:26.0",
    ]
  config["TauTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau"] = [
          "trg_monitor_mu20tau27_hps",
          "trg_monitor_mu20tau27"
    ]

  #TriggerMatchingProducers
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  #ValidMuonsProducer
  config["DirectIso"] = True
  config["UseUWGenMatching"] = True

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.TagAndProbeQuantitiesMT").build_list(2018)

  config["Processors"] =   []

  config["Processors"].extend((                               "producer:MetSelector",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "filter:MaxLooseMuonsCountFilter",
                                                              "producer:ValidMuonsProducer",
                                                              "filter:ValidMuonsFilter",
                                                              "filter:MuonsCountFilter",
                                                              "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "filter:MinTausCountFilter",
                                                              "producer:HttValidLooseElectronsProducer",   # Electrons for electron veto
                                                              "filter:MaxLooseElectronsCountFilter",
                                                              "producer:MuonTriggerMatchingProducer",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "producer:TauL1TauTriggerMatchingProducer",
                                                              "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer",
                                                              "producer:NewMTTagAndProbePairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
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
