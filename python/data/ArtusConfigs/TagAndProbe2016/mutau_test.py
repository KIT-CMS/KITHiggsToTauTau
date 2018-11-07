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
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe2016.Includes.mutau_settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe2016.Includes.mutau_settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe2016.Includes.mutau_settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe2016.Includes.mutau_settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe2016.Includes.mutau_settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe2016.Includes.mutau_settingsBTaggedJetID",
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
  config["MuonLowerPtCuts"] = ["10.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.1"]
  config["TauLowerPtCuts"] = ["18.0"]
  config["TauUpperAbsEtaCuts"] = ["2.1"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DeltaRTriggerMatchingTaus"] = 0.5
  config["DeltaRTriggerMatchingMuons"] = 0.5

  config["CheckTagTriggerMatch"] = [
      "trg_singlemuon_18",
      "trg_singlemuon_20",
      "trg_singlemuon_22",
      "trg_singlemuon_22_eta",
      "trg_singlemuon_24",
      "trg_singlemuon_27",
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_crossmuon_mu19tau20",
      "trg_crossmuon_mu19tau20_single",
  ]
  if re.search("Run2016(B|C|D|E|F|G)", nickname):
      config["CheckProbeTriggerMatch"].append("trg_monitor_mu19tau32_Iso")
  elif re.search("Run2016H", nickname):
      config["CheckProbeTriggerMatch"].append("trg_monitor_mu19tau32_combinedIso")
  else:
      config["CheckProbeTriggerMatch"].append("trg_monitor_mu19tau32_Iso")
      config["CheckProbeTriggerMatch"].append("trg_monitor_mu19tau32_combinedIso")

  config["HLTBranchNames"] = [
      "trg_singlemuon_18:HLT_IsoMu18_v",
      "trg_singlemuon_20:HLT_IsoMu20_v",
      "trg_singlemuon_22:HLT_IsoMu22_v",
      "trg_singlemuon_22_eta:HLT_IsoMu22_eta2p1_v",
      "trg_singlemuon_24:HLT_IsoMu24_v",
      "trg_singlemuon_27:HLT_IsoMu27_v",
      "trg_crossmuon_mu19tau20:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
      "trg_crossmuon_mu19tau20_single:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v",
  ]
  if re.search("Run2016(B|C|D|E|F|G)", nickname):
      config["HLTBranchNames"].append("trg_monitor_mu19tau32_Iso:HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v")
  elif re.search("Run2016H", nickname):
      config["HLTBranchNames"].append("trg_monitor_mu19tau32_combinedIso:HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v")
  else:
      config["HLTBranchNames"].append("trg_monitor_mu19tau32_Iso:HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v")
      config["HLTBranchNames"].append("trg_monitor_mu19tau32_combinedIso:HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v")
  #config["TauTrigger2017InputOld"] = "$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017.root"
  #config["TauTrigger2017Input"] = "$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017_New.root"
  #config["TauTrigger2017WorkingPoints"] = [
  #     "vvloose",
  #     "vloose",
  #     "loose",
  #     "medium",
  #     "tight",
  #     "vtight",
  #     "vvtight",
  #]
  #config["TauTrigger2017IDTypes"] = [
  #     "MVA",
  #]

  config["EventWeight"] = "eventWeight"
  #TriggerMatchingProducers,HttTriggerSettingsProducer 
  if isEmbedded:
      config["MuonTriggerFilterNames"] = [
              "HLT_IsoMu18_v:hltL3crIsoL1sMu16L1f0L2f10QL3f18QL3trkIsoFiltered0p09",
              "HLT_IsoMu20_v:hltL3crIsoL1sMu18L1f0L2f10QL3f20QL3trkIsoFiltered0p09",
              "HLT_IsoMu22_v:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
              "HLT_IsoMu22_eta2p1_v:hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09",
              "HLT_IsoMu24_v:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09",
              "HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
        ]
      config["TauTriggerFilterNames"] = [
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL1sMu18erTau20er",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL1sSingleMu18erIorSingleMu20er",
              "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltPFTau32Reg",
              "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltPFTau32Reg",
        ]
  else:
      config["MuonTriggerFilterNames"] = [
              "HLT_IsoMu18_v:hltL3crIsoL1sMu16L1f0L2f10QL3f18QL3trkIsoFiltered0p09",
              "HLT_IsoMu20_v:hltL3crIsoL1sMu18L1f0L2f10QL3f20QL3trkIsoFiltered0p09",
              "HLT_IsoMu22_v:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
              "HLT_IsoMu22_eta2p1_v:hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09",
              "HLT_IsoMu24_v:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09",
              "HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"
        ]
      config["TauTriggerFilterNames"] = [
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
              "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"
        ]
      if re.search("Run2016(B|C|D|E|F|G)", nickname):
          config["MuonTriggerFilterNames"].extend(["HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltL3crIsoL1sMu18erIsoTau26erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
                                                   "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumIsoPFTau32Reg"])
          config["TauTriggerFilterNames"].extend(["HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltPFTau32TrackPt1MediumIsolationL1HLTMatchedReg",
                                                  "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumIsoPFTau32Reg"])
      elif re.search("Run2016H", nickname):
          config["MuonTriggerFilterNames"].extend(["HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltL3crIsoL1sMu18erIsoTau26erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
                                                   "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumCombinedIsoPFTau32Reg"])
          config["TauTriggerFilterNames"].extend(["HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltPFTau32TrackPt1MediumCombinedIsolationL1HLTMatchedReg",
                                                  "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumCombinedIsoPFTau32Reg"])
      else:
          config["MuonTriggerFilterNames"].extend(["HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltL3crIsoL1sMu18erIsoTau26erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
                                                   "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumIsoPFTau32Reg",
                                                   "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltL3crIsoL1sMu18erIsoTau26erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
                                                   "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumCombinedIsoPFTau32Reg"])
          config["TauTriggerFilterNames"].extend(["HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltPFTau32TrackPt1MediumIsolationL1HLTMatchedReg",
                                                  "HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumIsoPFTau32Reg",
                                                  "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltPFTau32TrackPt1MediumCombinedIsolationL1HLTMatchedReg",
                                                  "HLT_IsoMu19_eta2p1_MediumCombinedIsoPFTau32_Trk1_eta2p1_Reg_v:hltOverlapFilterIsoMu19MediumCombinedIsoPFTau32Reg"])
  if re.search("Run2016(B|C|D|E|F|G)", nickname):
      config["CheckTriggerLowerPtCutsByHltNick"] = ["trg_monitor_mu19tau32_Iso:35.0"]
  elif re.search("Run2016H", nickname):
      config["CheckTriggerLowerPtCutsByHltNick"] = ["trg_monitor_mu19tau32_combinedIso:35.0"]
  else:
      config["CheckTriggerLowerPtCutsByHltNick"] = [
              "trg_monitor_mu19tau32_Iso:35.0",
              "trg_monitor_mu19tau32_combinedIso:35.0",
        ]
  if re.search("Run2016(B|C|D|E|F|G)", nickname):
      config["TauTriggerCheckAdditionalL1TauMatchLowerPtCut"] = ["trg_monitor_mu19tau32_Iso:26.0"]
  elif re.search("Run2016H", nickname):
      config["TauTriggerCheckAdditionalL1TauMatchLowerPtCut"] = ["trg_monitor_mu19tau32_combinedIso:26.0"]
  else:
      config["TauTriggerCheckAdditionalL1TauMatchLowerPtCut"] = [
              "trg_monitor_mu19tau32_Iso:26.0",
              "trg_monitor_mu19tau32_combinedIso:26.0"
        ]

  #TriggerMatchingProducers
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  #ValidMuonsProducer
  config["DirectIso"] = True

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe2016.Includes.TagAndProbeQuantitiesMT").build_list()

  config["Processors"] =   []

  config["Processors"].extend((                               "producer:HttValidLooseElectronsProducer",   # Electrons for electron veto
                                                              "filter:MaxLooseElectronsCountFilter",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "filter:MaxLooseMuonsCountFilter",
                                                              "producer:MetSelector",
                                                              "producer:ValidMuonsProducer",
                                                              "filter:ValidMuonsFilter",
                                                              "producer:MuonTriggerMatchingProducer",
                                                              "filter:MuonsCountFilter",
                                                              "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "producer:TauL1TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
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
