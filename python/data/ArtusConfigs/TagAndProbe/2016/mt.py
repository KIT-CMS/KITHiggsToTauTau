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
      "trg_singlemuon_24",
      "trg_singlemuon_27",
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_crossmuon_mu19tau20_singlel1",
      "trg_crossmuon_mu19tau20",
      "trg_monitor_mu19tau30",
      "trg_monitor_mu19tau35_mediso",
      "trg_monitor_mu19tau35_medcombiso",
      "trg_singletau_leading",
      "trg_singletau_trailing",
  ]
  config["HLTBranchNames"] = [
      "trg_singlemuon_24:HLT_IsoMu24_v",
      "trg_singlemuon_27:HLT_IsoMu27_v",
      "trg_crossmuon_mu19tau20_singlel1:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v",
      "trg_crossmuon_mu19tau20:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
      "trg_monitor_mu19tau30:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
      "trg_monitor_mu19tau35_mediso:HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v",
      "trg_monitor_mu19tau35_medcombiso:HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v",
      "trg_singletau_leading:HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
      "trg_singletau_trailing:HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
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
  #TriggerMatchingProducers,HttTriggerSettingsProducer
  if isEmbedded:
      config["MuonTriggerFilterNames"] = [
              "HLT_IsoMu24_v:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09",
              "HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltL3crIsoL1sMu18erIsoTau26erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltL3crIsoL1sMu18erIsoTau26erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
        ]
      config["TauTriggerFilterNames"] = [
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL1sSingleMu18erIorSingleMu20er",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL1sMu18erTau20er",
              # "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltPFTau20",
              "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltL2IsoTau26eta2p2",
              "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltL2IsoTau26eta2p2",
              "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v:hltSingleL2Tau80eta2p2",
        ]
  else:
      config["MuonTriggerFilterNames"] = [
              "HLT_IsoMu24_v:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09",
              "HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
              "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltL3crIsoL1sMu18erIsoTau26erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumIsoPFTau32Reg",
              "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltL3crIsoL1sMu18erIsoTau26erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu24MediumChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
        ]
      config["TauTriggerFilterNames"] = [
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltPFTau20TrackLooseIsoAgainstMuon",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltPFTau20TrackLooseIsoAgainstMuon",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
              "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltPFTau32TrackPt1MediumIsolationL1HLTMatchedReg",
              "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumIsoPFTau32Reg",
              "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltSelectedPFTau35TrackPt1MediumChargedIsolationAndTightOOSCPhotonsL1HLTMatchedReg",
              "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu24MediumChargedIsoAndTightOOSCPhotonsPFTau35MonitoringReg",
              "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v:hltPFTau140TrackPt50LooseAbsOrRelVLooseIso",
        ]
  config["CheckTriggerLowerPtCutsByHltNick"] = [
          "trg_monitor_mu19tau30:30.0",
          "trg_monitor_mu19tau35_mediso:35.0",
          "trg_monitor_mu19tau35_medcombiso:35.0",
    ]
  config["TauTriggerCheckAdditionalL1TauMatchLowerPtCut"] = [
          "trg_monitor_mu19tau30:26.0",
    ]

  #TriggerMatchingProducers
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  #ValidMuonsProducer
  config["DirectIso"] = True
  config["UseUWGenMatching"] = True

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.TagAndProbeQuantitiesMT").build_list(2016)

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
