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
  pipelines = kwargs["pipelines"] if "pipelines" in kwargs else None

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(50|150)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  isHtt = re.search("HToTauTau", nickname)


  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsVetoElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauES",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMinimalPlotlevelFilter_ee"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname, **kwargs)

  # explicit configuration
  config["Channel"] = "EE"
  config["MinNElectrons"] = 2
  # HltPaths_comment: The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer.
  if re.search("(Run2016|Embedding2016|Summer16)", nickname): config["HltPaths"] = [
          "HLT_IsoMu22",
          "HLT_IsoTkMu22",
          "HLT_IsoMu22_eta2p1",
          "HLT_IsoTkMu22_eta2p1",
          "HLT_VLooseIsoPFTau120_Trk50_eta2p1",
          "HLT_Ele25_eta2p1_WPTight_Gsf",
          "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg",
          "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"
    ]
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = True
  config["ElectronLowerPtCuts"] = ["26.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.1"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["DiTauPairNoHLT"] = False
  config["DiTauPairHLTLast"] = True
  config["HLTBranchNames"] = [
      "trg_singlemuon:HLT_IsoMu22_v",
      "trg_singlemuon:HLT_IsoTkMu22_v",
      "trg_singlemuon:HLT_IsoMu22_eta2p1_v",
      "trg_singlemuon:HLT_IsoTkMu22_eta2p1_v",
      "trg_singletau:HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
      "trg_singleelectron:HLT_Ele25_eta2p1_WPTight_Gsf_v",
      "trg_doubletau:HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v",
      "trg_doubletau:HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v",
      "trg_muonelectron:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v",
      "trg_muonelectron:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v"
  ]
  config["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
      "HLT_IsoMu22_v",
      "HLT_IsoTkMu22_v",
      "HLT_IsoMu22_eta2p1_v",
      "HLT_IsoTkMu22_eta2p1_v",
      "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
      "HLT_Ele25_eta2p1_WPTight_Gsf_v"
  ]
  config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_5.root"
  config["RooWorkspaceWeightNames"] = [
      "0:triggerWeight",
      "0:idweight",
      "0:isoweight",
      "0:trackWeight",
      "1:idweight",
      "1:isoweight",
      "1:trackWeight"
  ]
  config["RooWorkspaceObjectNames"] = [
      "0:e_trg_binned_ratio",
      "0:e_iso_binned_ratio",
      "0:e_id_ratio",
      "0:e_trk_ratio",
      "1:e_iso_binned_ratio",
      "1:e_id_ratio",
      "1:e_trk_ratio"
  ]
  config["RooWorkspaceObjectArguments"] = [
      "0:e_pt,e_eta,e_iso",
      "0:e_pt,e_eta,e_iso",
      "0:e_pt,e_eta",
      "0:e_pt,e_eta",
      "1:e_pt,e_eta,e_iso",
      "1:e_pt,e_eta",
      "1:e_pt,e_eta"
  ]
  config["EventWeight"] = "eventWeight"
  config["TauTauRestFrameReco"] = "collinear_approximation"
  if re.search("(Run2016|Embedding2016|Summer16)", nickname): config["ElectronTriggerFilterNames"] = [
          "HLT_Ele25_eta2p1_WPTight_Gsf_v:hltEle25erWPTightGsfTrackIsoFilter",
          "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v:hltPFTau120TrackPt50LooseAbsOrRelVLooseIso"
    ]
  config["BTagWPs"] = ["medium"]
  config["InvalidateNonMatchingElectrons"] = True
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True

  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(isMC = (not isData) and (not isEmbedded))
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.zptQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend([
      "nmediumbtag",
      "had_gen_match_pT_1",
      "had_gen_match_pT_2",
      "muR1p0_muF1p0_weight",
      "muR1p0_muF2p0_weight",
      "muR1p0_muF0p5_weight",
      "muR2p0_muF1p0_weight",
      "muR2p0_muF2p0_weight",
      "muR2p0_muF0p5_weight",
      "muR0p5_muF1p0_weight",
      "muR0p5_muF2p0_weight",
      "muR0p5_muF0p5_weight"
  ])

  config["OSChargeLeptons"] = True
  config["TopPtReweightingStrategy"] = "Run1"

  config["Processors"] = [                                  "producer:HttValidLooseElectronsProducer",
                                                            "producer:HttValidLooseMuonsProducer",
                                                            "producer:HltProducer",
                                                            "producer:MetSelector",
                                                            "producer:ValidElectronsProducer",
                                                            "filter:ValidElectronsFilter",
                                                            "producer:ElectronTriggerMatchingProducer",
                                                            "filter:MinElectronsCountFilter",
                                                            "producer:HttValidVetoElectronsProducer",
                                                            "producer:ValidMuonsProducer",
                                                            "producer:ValidTausProducer",
                                                            "producer:TauTriggerMatchingProducer",
                                                            "producer:ValidEEPairCandidatesProducer",
                                                            "filter:ValidDiTauPairCandidatesFilter",
                                                            "producer:Run2DecayChannelProducer", #"producer:MvaMetSelector",
                                                            "producer:DiVetoElectronVetoProducer"]
  if not isDY:                 config["Processors"].append( "producer:TaggedJetCorrectionsProducer")
  config["Processors"].extend((                             "producer:ValidTaggedJetsProducer",
                                                            "producer:ValidBTaggedJetsProducer"))
  if isDY or isWjets or isHtt: config["Processors"].append( "producer:MetCorrector") #"producer:MvaMetCorrector"
  config["Processors"].extend((                             "producer:TauTauRestFrameSelector",
                                                            "producer:DiLeptonQuantitiesProducer",
                                                            "producer:DiJetQuantitiesProducer"))
  if isTTbar:                  config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                     config["Processors"].append( "producer:ZPtReweightProducer")
  config["Processors"].extend((                             "filter:MinimalPlotlevelFilter", #"producer:MVATestMethodsProducer",
                                                            "producer:MVAInputQuantitiesProducer"))
  if not isData:               config["Processors"].append( #"producer:TriggerWeightProducer", "producer:IdentificationWeightProducer"
                                                            "producer:RooWorkspaceWeightProducer")
  config["Processors"].append(                              "producer:EventWeightProducer")

  config["AddGenMatchedParticles"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedElectrons"] = True
  config["BranchGenMatchedTaus"] = True
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]

  # pipelines - systematic shifts
  if pipelines is None:
    raise Exception("pipelines is None in %s" % (__file__))

  return_conf = jsonTools.JsonDict()
  for pipeline in pipelines:
    log.info('Add pipeline: %s' %(pipeline))
    return_conf += ACU.apply_uncertainty_shift_configs('mm', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis." + pipeline).build_config(nickname, **kwargs))
  return return_conf
