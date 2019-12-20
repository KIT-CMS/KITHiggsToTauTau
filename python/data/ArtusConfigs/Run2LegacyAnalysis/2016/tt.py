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
  etau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "etau-fake-es" else False
  pipelines = kwargs["pipelines"] if "pipelines" in kwargs else None
  minimal_setup = True if "minimal_setup" in kwargs and kwargs["minimal_setup"] else False

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50)", nickname)
  isWjets = re.search("(W.?Jets|WG)ToLNu", nickname)
  isSignal = re.search("NMSSM|HToTauTau",nickname)
  isNMSSM = re.search("NMSSM",nickname)
  isHWW = re.search("HToWW",nickname)
  isGluonFusion = re.search("GluGluHToTauTau.*M125", nickname)
  isVBF = re.search("VBFHToTauTau.*M125", nickname)
  isMSSMggH = re.search("SUSYGluGuToH", nickname)

  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauES",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMinimalPlotlevelFilter_tt"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname, **kwargs)

  # explicit configuration
  config["Channel"] = "TT"
  config["MinNTaus"] = 2

  ### HLT & Trigger Object configuration

  config["HLTBranchNames"] = [
    "trg_singleelectron:HLT_Ele25_eta2p1_WPTight_Gsf_v",
    "trg_singlemuon:HLT_IsoMu22_v",
    "trg_singlemuon:HLT_IsoTkMu22_v",
    "trg_singlemuon:HLT_IsoMu22_eta2p1_v",
    "trg_singlemuon:HLT_IsoTkMu22_eta2p1_v",
    #"trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
    "trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v",
    "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
    "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
    "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
    "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v",
    "trg_eletaucross:HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v"
    "trg_singletau_leading:HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
    "trg_singletau_trailing:HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
  ]
  config["CheckLepton1TriggerMatch"] = [
    "trg_singleelectron",
    "trg_singlemuon",

    "trg_mutaucross",
    "trg_doubletau",
    "trg_muonelectron_mu23ele12",
    "trg_muonelectron_mu8ele23",
    "trg_singletau_leading"
  ]
  config["CheckLepton2TriggerMatch"] = [
    "trg_mutaucross",
    "trg_doubletau",
    "trg_muonelectron_mu23ele12",
    "trg_muonelectron_mu8ele23",
    "trg_singletau_trailing"
  ]
  # split by run for data as the doubletau trigger path changes
  if re.search("Run2016(B|C|D|E|F|G)", nickname):
    config["TauTriggerFilterNames"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg",
                                       "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v:hltPFTau140TrackPt50LooseAbsOrRelVLooseIso"]
    config["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg",
                          "HLT_VLooseIsoPFTau140_Trk50_eta2p1"]
    config["HLTBranchNames"].append("trg_doubletau:HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v")
    config["DiTauPairLepton1LowerPtCuts"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg:40.0"]
    config["DiTauPairLepton2LowerPtCuts"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg:40.0"]
  elif re.search("Run2016H", nickname):
    config["TauTriggerFilterNames"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg",
                                       "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v:hltPFTau140TrackPt50LooseAbsOrRelVLooseIso"]
    config["HltPaths"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
                          "HLT_VLooseIsoPFTau140_Trk50_eta2p1"]
    config["HLTBranchNames"].append("trg_doubletau:HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v")
    config["DiTauPairLepton1LowerPtCuts"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg:40.0"]
    config["DiTauPairLepton2LowerPtCuts"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg:40.0"]
  else:
    config["TauTriggerFilterNames"] = [
    "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg",
    "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg",
    "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v:hltPFTau140TrackPt50LooseAbsOrRelVLooseIso"]
    config["HltPaths"] = [
    "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg",
    "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
    "HLT_VLooseIsoPFTau140_Trk50_eta2p1"]
    config["HLTBranchNames"].extend((
    "trg_doubletau:HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v",
    "trg_doubletau:HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v"))
    config["DiTauPairLepton1LowerPtCuts"] = [
    "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg:40.0",
    "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg:40.0"]
    config["DiTauPairLepton2LowerPtCuts"] = [
    "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg:40.0",
    "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg:40.0"]


  ### Electron scale and smear corrections
  config["ElectronScaleAndSmearUsed"] = True if not isEmbedded else False
  config["ElectronScaleAndSmearTag"] = "ecalTrkEnergyPostCorr"

  ### Signal pair selection configuration
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = False
  config["TauVeto2ProngDMs"] = True
  config["TauLowerPtCuts"] = ["40.0"]
  config["TauUpperAbsEtaCuts"] = ["2.1"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["TauTauRestFrameReco"] = "collinear_approximation"
  config["TriggerObjectLowerPtCut"] = 28.0
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["OSChargeLeptons"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedTaus"] = True

  ### Efficiencies & weights configuration
  config["TauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2016KIT_deeptau.root"
  config["TauTriggerInputKIT"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2016KIT_deeptau.root"
  config["TauTrigger"] = "ditau"
  config["TauTriggerWorkingPoints"] = [
       "vloose",
       "loose",
       "medium",
       "tight",
       "vtight",
       "vvtight",
  ]
  config["TauTriggerIDTypes"] = [
       "DeepTau",
  ]
  if isEmbedded:
    config["TauTriggerEfficiencyWeightNames"] = [
        "0:crossTriggerDataEfficiencyWeight",
        "0:crossTriggerKITDataEfficiencyWeight",
        "0:crossTriggerEMBEfficiencyWeight",
        "1:crossTriggerDataEfficiencyWeight",
        "1:crossTriggerKITDataEfficiencyWeight",
        "1:crossTriggerEMBEfficiencyWeight",
    ]
  else:
    config["TauTriggerEfficiencyWeightNames"] = [
        "0:crossTriggerMCEfficiencyWeight",
        "0:crossTriggerDataEfficiencyWeight",
        "1:crossTriggerMCEfficiencyWeight",
        "1:crossTriggerDataEfficiencyWeight",
    ]

  # Define weight names to be written out - only store weights that are actually filled
  tauTriggerWeights = []
  for WeightName in config["TauTriggerEfficiencyWeightNames"]:
    for shift in ["","Up","Down"]:
      for IDType in config["TauTriggerIDTypes"]:
        for wp in config["TauTriggerWorkingPoints"]:
          tauTriggerWeights.append(WeightName.split(":")[1]+shift+"_"+wp+"_"+IDType+"_"+str(int(WeightName.split(":")[0])+1))

  config["SingleTauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2016_singletau.root"
  config["SingleTauTriggerWorkingPoints"] = [
       # "vvvloose",
       # "vvloose",
       "vloose",
       "loose",
       "medium",
       "tight",
       "vtight",
       "vvtight",
  ]
  config["SingleTauTriggerIDTypes"] = [
       # "MVAv2",
       "DeepTau",
  ]
  if not isData:
    config["SingleTauTriggerEfficiencyWeightNames"] = [
        "0:singleTauTriggerMCEfficiencyWeight",
        "0:singleTauTriggerDataEfficiencyWeight",
        "1:singleTauTriggerMCEfficiencyWeight",
        "1:singleTauTriggerDataEfficiencyWeight",
    ]

  # Define weight names to be written out - only store weights that are actually filled
  singleTauTriggerWeights = []
  for WeightName in config["SingleTauTriggerEfficiencyWeightNames"]:
    for shift in ["","Up","Down"]:
        if "MC" in WeightName and shift in ["Up", "Down"]:
            continue
        for IDType in config["SingleTauTriggerIDTypes"]:
          for wp in config["SingleTauTriggerWorkingPoints"]:
            singleTauTriggerWeights.append(WeightName.split(":")[1]+shift+"_"+wp+"_"+IDType+"_"+str(int(WeightName.split(":")[0])+1))

  config["TauIDSFWorkingPoints"] = [
       "VVVLoose",
       "VVLoose",
       "VLoose",
       "Loose",
       "Medium",
       "Tight",
       "VTight",
       "VVTight",
  ]
  config["TauIDSFTypes"] = [
       "DeepTau2017v2p1VSjet",
  ]
  config["TauIDSFWeightNames"] = [
      "0:tauIDScaleFactorWeight",
      "1:tauIDScaleFactorWeight",
  ]
  config["TauIDSFUseEMBSFs"] = isEmbedded
  config["TauIDSFUseTightVSeSFs"] = False

  if isEmbedded:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2016.root"
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2016.root"
    config["EmbeddedWeightWorkspaceWeightNames"] = [
          "0:muonEffTrgWeight",
          "0:muonEffIDWeight",
          "1:muonEffIDWeight",

          #"0:triggerWeight",
          #"1:triggerWeight",
          #"0:TriggerEmbeddedEfficiencyWeight",
          #"1:TriggerEmbeddedEfficiencyWeight",
          #"0:TriggerDataEfficiencyWeight",
          #"1:TriggerDataEfficiencyWeight",
          #~ "0:doubleTauTrgWeight"
          ]
    config["EmbeddedWeightWorkspaceObjectNames"] = [
          "0:m_sel_trg_kit_ratio",
          "0:m_sel_idemb_kit_ratio",
          "1:m_sel_idemb_kit_ratio",

          #"0:t_TightIso_tt_emb_ratio",
          #"1:t_TightIso_tt_emb_ratio",
          #"0:t_TightIso_tt_emb",
          #"1:t_TightIso_tt_emb",
          #"0:t_genuine_TightIso_tt_data,t_fake_TightIso_tt_data",
          #"1:t_genuine_TightIso_tt_data,t_fake_TightIso_tt_data",
          #~ "0:doubletau_corr"
          ]
    config["EmbeddedWeightWorkspaceObjectArguments"] = [
          "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
          "0:gt_pt,gt_eta",
          "1:gt_pt,gt_eta",

          #"0:t_pt,t_dm",
          #"1:t_pt,t_dm",
          #"0:t_pt,t_dm",
          #"1:t_pt,t_dm",
          #"0:t_pt,t_dm",
          #"1:t_pt,t_dm",
          #~ "0:dR"
          ]
  # elif not isData:
  #   ### Efficiencies & weights configuration
  #   config["TauTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_v16_2.root"
  #   config["TauTauTriggerWeightWorkspaceWeightNames"] = [
  #       "0:triggerWeight",
  #       "1:triggerWeight"]
  #   config["TauTauTriggerWeightWorkspaceObjectNames"] = [
  #       "0:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio",
  #       "1:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio"]
  #   config["TauTauTriggerWeightWorkspaceObjectArguments"] = [
  #       "0:t_pt,t_dm",
  #       "1:t_pt,t_dm"]
  config["EventWeight"] = "eventWeight"
  config["TopPtReweightingStrategy"] = "Run1"

  ### Ntuple output quantities configuration
  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(minimal_setup=minimal_setup, isMC = (not isData) and (not isEmbedded), nickname = nickname)
  # config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.zptQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend(tauTriggerWeights)
  config["Quantities"].extend(singleTauTriggerWeights)
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
      #"drel0_1",
      #"drel0_2",
      #"drelZ_1",
      #"drelZ_2",
      "flagMETFilter"
  ])
  if isEmbedded:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.embeddedDecayModeWeightQuantities").build_list())
    config["Quantities"].extend([
          "muonEffTrgWeight",
          "TriggerEmbeddedEfficiencyWeight_1",
          "TriggerEmbeddedEfficiencyWeight_2",
          "TriggerDataEfficiencyWeight_1",
          "TriggerDataEfficiencyWeight_2",
          "muonEffIDWeight_1",
          "muonEffIDWeight_2",
          "doubleTauTrgWeight", #"trg_doubletau"
])
  if re.search("HToTauTau.*M125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1p1cat",
      "htxs_stage1p1finecat",
      "htxs_njets30",
      "htxs_higgsPt",
    ])
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.ggHNNLOQuantities").build_list())
  if isVBF:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.qqHNNLOQuantities").build_list())
  if isNMSSM:
    config["Quantities"].extend(["genBosonMass_h1","genBosonMass_h2","genBosonMass_h3","genBosonPt_h1","genBosonPt_h2","genBosonPt_h3","genBosonEta_h1","genBosonEta_h2","genBosonEta_h3"])
  ### Processors & consumers configuration
  config["Processors"] = []
  #if not (isEmbedded):           config["Processors"].append( "producer:ElectronCorrectionsProducer")
  config["Processors"].extend((                               "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:HltProducer",
                                                              "producer:MetCollector"))
  if not (isData): config["Processors"].append( "producer:TauCorrectionsProducer")
  if not isData:                 config["Processors"].append( "producer:HttValidGenTausProducer")
  config["Processors"].extend((                               "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
                                                              "producer:ValidElectronsProducer",
                                                              "producer:ValidMuonsProducer",
                                                              "producer:NewValidTTPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:Run2DecayChannelProducer"))
  config["Processors"].append(                                "filter:MinimalPlotlevelFilter")
  if not (isData or isEmbedded): config["Processors"].append( "producer:TaggedJetCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"))
  if btag_eff: config["ProcessorsBtagEff"] = copy.deepcopy(config["Processors"])
  config["Processors"].extend((                               "producer:MetCorrector",
                                                              "producer:PuppiMetCorrector",
                                                              "producer:SimpleEleTauFakeRateWeightProducer",
                                                              "producer:SimpleMuTauFakeRateWeightProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY or isEmbedded:        config["Processors"].append( "producer:ZPtReweightProducer")
  config["Processors"].extend((                               "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer",
                                                              "producer:DiBJetQuantitiesProducer"))
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:TauDecayModeWeightProducer")
  if not isData:                 config["Processors"].append( "producer:TauTriggerEfficiencyProducer")
  if not isData:                 config["Processors"].append( "producer:SingleTauTriggerEfficiencyProducer")
  if not isData:                 config["Processors"].append( "producer:TauIDScaleFactorProducer")
  if not isData:                 config["Processors"].append( "producer:TauTauTriggerWeightProducer")
  config["Processors"].append(                                "producer:EventWeightProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  if isVBF:                      config["Processors"].append( "producer:SMvbfNNLOProducer")
  if isMSSMggH:                  config["Processors"].append( "producer:NLOreweightingWeightsProducer")
  config["Processors"].append(                                "producer:SvfitProducer")
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]

  # Subanalyses settings
  if btag_eff:
    config["Processors"] = copy.deepcopy(config["ProcessorsBtagEff"])
    if pipelines != ['nominal']:
        raise Exception("There is no use case for calculating btagging efficiency with systematics shifts: %s" % ' '.join(pipelines))

    return importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.btag_efficiency_subanalysis").build_config(nickname, nominal_config=config, channel='tt', **kwargs)

  # pipelines - systematic shifts
  needed_pipelines = ['nominal', 'tauESperDM_shifts', 'regionalJECunc_shifts', 'METunc_shifts', 'METrecoil_shifts', 'btagging_shifts']
  if pipelines is None:
      raise Exception("pipelines is None in %s" % (__file__))
  elif 'auto' in pipelines:
      pipelines = needed_pipelines

  return_conf = jsonTools.JsonDict()
  for pipeline in pipelines:
      if pipeline not in needed_pipelines:
          log.warning("Warning: pipeline NOT in the list of needed pipelines. Still adding it.")
      log.info('Add pipeline: %s' %(pipeline))
      return_conf += ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis." + pipeline).build_config(nickname, **kwargs))

  return return_conf
