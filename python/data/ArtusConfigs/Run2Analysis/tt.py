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

def build_config(nickname):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  
  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("(DY.?JetsToLL|EWKZ2Jets)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  isGluonFusion = re.search("GluGluHToTauTauM125", nickname)
  
  
  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJEC",
    #"HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsMinimalPlotlevelFilter_tt",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsTauES",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsMVATestMethods"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["Channel"] = "TT"
  config["MinNTaus"] = 2
  # HltPaths_comment: The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer.
  if re.search("Run2016(B|C|D|E|F|G)", nickname): 
    config["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"]
    config["HLTBranchNames"] = ["trg_doubletau:HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v"]
  elif re.search("Run2016H", nickname):
    config["HltPaths"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"]
    config["HLTBranchNames"] = ["trg_doubletau:HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v"]
  elif isEmbedded: config["HltPaths"] = [""]
  else:
    config["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg",
                          "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"]
    config["HLTBranchNames"] = ["trg_doubletau:HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v",
                                "trg_doubletau:HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v"]
  
  config["NoHltFiltering"] = True if isEmbedded else False
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = True
  config["TauLowerPtCuts"] = ["40.0"]
  config["TauUpperAbsEtaCuts"] = ["2.1"]
  config["DiTauPairLepton1LowerPtCuts"] = [
      "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg:40.0",
      "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg:40.0"]
  config["DiTauPairLepton2LowerPtCuts"] = [
      "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg:40.0",
      "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg:40.0"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["DiTauPairNoHLT"] = True if isEmbedded else True
  config["DiTauPairHLTLast"] = False
  config["EventWeight"] = "eventWeight"
  config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
  config["TauTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
  config["TauTauTriggerWeightWorkspaceWeightNames"] = [
      "0:triggerWeight",
      "1:triggerWeight"]
  config["TauTauTriggerWeightWorkspaceObjectNames"] = [
      "0:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio",
      "1:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio"]
  config["TauTauTriggerWeightWorkspaceObjectArguments"] = [
      "0:t_pt,t_dm",
      "1:t_pt,t_dm"]
  config["EleTauFakeRateWeightFile"] = [
      "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root",
      "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"]
  config["TauTauRestFrameReco"] = "collinear_approximation"
  
  if re.search("Run2016(B|C|D|E|F|G)", nickname): config["TauTriggerFilterNames"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg"]
  elif re.search("Run2016H", nickname): config["TauTriggerFilterNames"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg"]
  else: config["TauTriggerFilterNames"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg",
                                          "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg"]
  
  config["TriggerObjectLowerPtCut"] = 28.0
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["UseUWGenMatching"] = "true"
  
  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.fourVectorQuantities").build_list()
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.syncQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.svfitSyncQuantities").build_list())
  #config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.splitJecUncertaintyQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend([
      "nLooseElectrons",
      "nLooseMuons",
      "nDiTauPairCandidates",
      "nAllDiTauPairCandidates",
      "trg_doubletau",
      "lep1ErrD0",
      "lep1ErrDz",
      "lep2ErrD0",
      "lep2ErrDz",
      "PVnDOF",
      #"PVchi2",
      "drel0_1",
      "drel0_2",
      "drelZ_1",
      "drelZ_2",
      #"htxs_stage0cat",
      #"htxs_stage1cat",
      "flagMETFilter",
      "pt_ttjj"
  ])
  if re.search("HToTauTauM125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1cat"
    ])  
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.ggHNNLOQuantities").build_list())

  
  config["OSChargeLeptons"] = True
  
  config["Processors"] = [                                    "producer:HltProducer",
                                                              "filter:HltFilter",
                                                              "producer:MetSelector"]
  if not isData:                 config["Processors"].append( "producer:TauCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
                                                              "producer:ValidElectronsProducer",
                                                              "producer:ValidMuonsProducer",
                                                              "producer:ValidTTPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:Run2DecayChannelProducer",
                                                              "producer:TaggedJetCorrectionsProducer",
                                                              "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer",
                                                              "producer:GroupedJetUncertaintyShiftProducer"))
                                                              #"producer:TaggedJetUncertaintyShiftProducer"))
  if not isData:                 config["Processors"].append( "producer:MetCorrector") #"producer:MvaMetCorrector"
  config["Processors"].extend((                               "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer"))
  if not (isData or isEmbedded): config["Processors"].extend(("producer:SimpleEleTauFakeRateWeightProducer",
                                                              "producer:SimpleMuTauFakeRateWeightProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                       config["Processors"].append( "producer:ZPtReweightProducer")
  config["Processors"].extend((                               "filter:MinimalPlotlevelFilter",
                                                              "producer:SvfitProducer",
                                                              "producer:ImpactParameterCorrectionsProducer")) #"producer:MVATestMethodsProducer"
  if not isData:                 config["Processors"].append( "producer:TauTauTriggerWeightProducer")
  config["Processors"].append(                                "producer:EventWeightProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  
  
  
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedTaus"] = True
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]
                         #"SvfitCacheConsumer"]
                         #"CutFlowTreeConsumer",
                         #"KappaElectronsConsumer",
                         #"KappaTausConsumer",
                         #"KappaTaggedJetsConsumer",
                         #"RunTimeConsumer",
                         #"PrintEventsConsumer"
  
  
  # pipelines - systematic shifts
  return ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.nominal").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.JECunc_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.METunc_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.tauESperDM_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.tauJetFakeESIncl_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.btagging_shifts").build_config(nickname))
