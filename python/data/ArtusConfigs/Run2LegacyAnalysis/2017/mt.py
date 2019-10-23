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
  tau_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "tau-es" else False
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
  isSignal = re.search("h1M125tautau|HToTauTau",nickname)
  isNMSSM = re.search("h1M125",nickname)
  isHWW = re.search("HToWW",nickname)
  isGluonFusion = re.search("GluGluHToTauTauM125", nickname)
  isMSSMggH = re.search("SUSYGluGuToH", nickname)

  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsVetoMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauES",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMinimalPlotlevelFilter_mt"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname, **kwargs)

  # explicit configuration
  config["Channel"] = "MT"
  config["MinNMuons"] = 1
  config["MinNTaus"] = 1

  ### HLT & Trigger Object configuration
  config["HltPaths"] = [
          "HLT_IsoMu24",
          "HLT_IsoMu27",
          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
          "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
  ]
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
  config["CheckLepton1TriggerMatch"] = [
      "trg_singlemuon_24",
      "trg_singlemuon_27",
      "trg_singletau_leading",
      "trg_singleelectron_27",
      "trg_singleelectron_32",
      "trg_singleelectron_32_fallback",
      "trg_singleelectron_35",

      "trg_crossmuon_mu20tau27",
      "trg_crossele_ele24tau30",
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso",
      "trg_muonelectron_mu12ele23",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
  ]
  config["CheckLepton2TriggerMatch"] = [
      "trg_singletau_trailing",

      "trg_crossmuon_mu20tau27",
      "trg_crossele_ele24tau30",
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso",
      "trg_muonelectron_mu12ele23",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
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
  ]
  if isEmbedded:
    config["MuonTriggerFilterNames"] = [
            "HLT_IsoMu24_v:hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07",
            "HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
            "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07",
      ]
    config["TauTriggerFilterNames"] = [
            "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltL1sMu18erTau24erIorMu20erTau24er",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltPFTau180TrackPt50LooseAbsOrRelMediumHighPtRelaxedIsoIso",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSelectedPFTau180MediumChargedIsolationL1HLTMatched"
      ]
  else:
    config["MuonTriggerFilterNames"] = [
            "HLT_IsoMu24_v:hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07",
            "HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
            "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07",
            "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded",
      ]
    config["TauTriggerFilterNames"] = [
            "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched",
            "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltPFTau180TrackPt50LooseAbsOrRelMediumHighPtRelaxedIsoIso",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSelectedPFTau180MediumChargedIsolationL1HLTMatched"
      ]

  ### Electron scale and smear corrections
  config["ElectronScaleAndSmearUsed"] = True if not isEmbedded else False
  config["ElectronScaleAndSmearTag"] = "ecalTrkEnergyPostCorr"

  ### Signal pair selection configuration
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = False
  config["MuonLowerPtCuts"] = ["21.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.1"]
  config["TauLowerPtCuts"] = ["23.0"]
  config["TauUpperAbsEtaCuts"] = ["2.3"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DeltaRTriggerMatchingTaus"] = 0.5
  config["DeltaRTriggerMatchingMuons"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["TauTauRestFrameReco"] = "collinear_approximation"
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["OSChargeLeptons"] = True
  config["AddGenMatchedParticles"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedMuons"] = True
  config["BranchGenMatchedTaus"] = True

  ### Efficiencies & weights configuration
  config["TauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2017.root"
  config["TauTriggerInputKIT"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/tauTriggerEfficiencies2017KIT.root"
  config["TauTrigger"] = "mutau"
  config["TauTriggerWorkingPoints"] = [
       "vloose",
       "loose",
       "medium",
       "tight",
       "vtight",
       "vvtight",
  ]
  config["TauTriggerIDTypes"] = [
       "MVAv2",
  ]
  if isEmbedded:
    config["TauTriggerEfficiencyWeightNames"] = [
        "1:crossTriggerDataEfficiencyWeight",
        "1:crossTriggerKITDataEfficiencyWeight",
        "1:crossTriggerEMBEfficiencyWeight",  
    ]
  else:
    config["TauTriggerEfficiencyWeightNames"] = [
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
  config["TauIDScaleFactorWeightNames"] = [
      "1:tauIDScaleFactorWeight",
  ]
  if isEmbedded:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2017.root"
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2017.root"
    config["EmbeddedWeightWorkspaceWeightNames"]=[
          "0:muonEffTrgWeight",
          "0:muonEffIDWeight",
          "1:muonEffIDWeight",

          "0:crossTriggerMCEfficiencyWeight",
          "0:crossTriggerDataEfficiencyWeight",

          "0:crossTriggerMCEfficiencyWeightKIT",
          "0:crossTriggerDataEfficiencyWeightKIT",
          "0:crossTriggerEmbeddedEfficiencyWeightKIT",

          "0:crossTriggerEmbeddedWeight",
          "1:crossTriggerEmbeddedWeight",

          "0:isoWeight",
          "0:idWeight",

          "0:singleTriggerMCEfficiencyWeightKIT",
          "0:singleTriggerDataEfficiencyWeightKIT",
          "0:singleTriggerEmbeddedEfficiencyWeightKIT",

          "0:trigger_24_Weight",
          "0:trigger_27_Weight",
          "0:trigger_24_27_Weight"
          ]
    config["EmbeddedWeightWorkspaceObjectNames"]=[
          "0:m_sel_trg_ratio",
          "0:m_sel_idEmb_ratio",
          "1:m_sel_idEmb_ratio",

          "0:m_trg_MuTau_Mu20Leg_desy_mc",
          "0:m_trg_MuTau_Mu20Leg_desy_data",

          "0:m_trg_MuTau_Mu20Leg_kit_mc",
          "0:m_trg_MuTau_Mu20Leg_kit_data",
          "0:m_trg_MuTau_Mu20Leg_kit_embed",

          "0:m_trg_MuTau_Mu20Leg_embed_kit_ratio",
          "1:mt_emb_LooseChargedIsoPFTau27_kit_ratio",

          "0:m_iso_binned_embed_kit_ratio",
          "0:m_id_embed_kit_ratio",

          "0:m_trg24_27_kit_mc",
          "0:m_trg24_27_kit_data",
          "0:m_trg24_27_kit_embed",

          "0:m_trg24_embed_kit_ratio",
          "0:m_trg27_embed_kit_ratio",
          "0:m_trg24_27_embed_kit_ratio"
          ]
    config["EmbeddedWeightWorkspaceObjectArguments"] = [
          "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
          "0:gt_pt,gt_eta",
          "1:gt_pt,gt_eta",

          "0:m_pt,m_eta",
          "0:m_pt,m_eta",

          "0:m_pt,m_eta",
          "0:m_pt,m_eta",
          "0:m_pt,m_eta",

          "0:m_pt,m_eta",
          "1:t_pt",

          "0:m_pt,m_eta,m_iso",
          "0:m_pt,m_eta",

          "0:m_pt,m_eta",
          "0:m_pt,m_eta",
          "0:m_pt,m_eta",

          "0:m_pt,m_eta",
          "0:m_pt,m_eta",
          "0:m_pt,m_eta"
          ]
  else:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2017.root"
    config["RooWorkspaceWeightNames"]=[
        "0:crossTriggerMCEfficiencyWeight",
        "0:crossTriggerDataEfficiencyWeight",

        "0:crossTriggerMCEfficiencyWeightKIT",
        "0:crossTriggerDataEfficiencyWeightKIT",

        "0:singleTriggerMCEfficiencyWeightDESY",
        "0:singleTriggerDataEfficiencyWeightDESY",

        "0:singleTriggerMCEfficiencyWeightKIT",
        "0:singleTriggerDataEfficiencyWeightKIT",

        "0:isoWeight",
        "0:idWeight",
#        "0:trackWeight", # new recommendation for 2017 data/MC is to remove it (will result in SF = 1.0).
    ]
    config["RooWorkspaceObjectNames"] = [
        "0:m_trg_MuTau_Mu20Leg_desy_mc",
        "0:m_trg_MuTau_Mu20Leg_desy_data",

        "0:m_trg_MuTau_Mu20Leg_kit_mc",
        "0:m_trg_MuTau_Mu20Leg_kit_data",

        "0:m_trg_SingleMu_Mu24ORMu27_desy_mc",
        "0:m_trg_SingleMu_Mu24ORMu27_desy_data",

        "0:m_trg24_27_kit_mc",
        "0:m_trg24_27_kit_data",

        "0:m_iso_kit_ratio",
        "0:m_id_kit_ratio",
#        "0:m_trk_ratio",
    ]
    config["RooWorkspaceObjectArguments"] = [
        "0:m_pt,m_eta",
        "0:m_pt,m_eta",
        
        "0:m_pt,m_eta",
        "0:m_pt,m_eta",

        "0:m_pt,m_eta",
        "0:m_pt,m_eta",

        "0:m_pt,m_eta",
        "0:m_pt,m_eta",

        "0:m_pt,m_eta",
        "0:m_pt,m_eta",
#        "0:m_eta",
    ]
  config["EventWeight"] = "eventWeight"
  config["TopPtReweightingStrategy"] = "Run1"

  ### Ntuple output quantities configuration
  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(minimal_setup=minimal_setup, isMC = (not isData) and (not isEmbedded), nickname = nickname)
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.zptQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.lheWeights").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend(tauTriggerWeights)
  config["Quantities"].extend([
      "had_gen_match_pT_1",
      "had_gen_match_pT_2",
      "flagMETFilter",
      "trigger_24_Weight_1", "trigger_27_Weight_1", "trigger_24_27_Weight_1","singleTriggerDataEfficiencyWeightDESY_1","singleTriggerMCEfficiencyWeightDESY_1"
  ])
  if isEmbedded:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.embeddedDecayModeWeightQuantities").build_list())
    config["Quantities"].extend([
          "muonEffTrgWeight", "muonEffIDWeight_1","muonEffIDWeight_2", "crossTriggerEmbeddedWeight_1", "crossTriggerEmbeddedWeight_2"
          ])
  if re.search("HToTauTauM125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1p1cat",
      "htxs_stage1p1finecat"
    ])
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.ggHNNLOQuantities").build_list())
  if isNMSSM:
    config["Quantities"].extend(["genBosonMass_h1","genBosonMass_h2","genBosonMass_h3","genBosonPt_h1","genBosonPt_h2","genBosonPt_h3","genBosonEta_h1","genBosonEta_h2","genBosonEta_h3"])
  config["Quantities"].extend([
      "diBJetPt",
      "diBJetEta",
      "diBJetPhi",
      "diBJetMass",
      "diBJetDeltaPhi",
      "diBJetAbsDeltaEta",
      "diBJetdiLepPhi",
      "pt_ttvisbb",
      "pt_ttbb",
      "pt_ttbb_puppi",
      "m_ttvisbb",
      "m_ttbb",
      "m_ttbb_puppi"])
  ### Processors & consumers configuration
  config["Processors"] =   []#                                  ["producer:MuonCorrectionsProducer"] if isEmbedded else []
  #if not (isEmbedded):           config["Processors"].append( "producer:ElectronCorrectionsProducer")
  config["Processors"].extend((                               "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:HltProducer",
                                                              "producer:MetCollector",
                                                              "producer:ValidMuonsProducer",
                                                              "filter:ValidMuonsFilter",
                                                              "producer:MuonTriggerMatchingProducer",
                                                              "filter:MinMuonsCountFilter",
                                                              "producer:HttValidVetoMuonsProducer",
                                                              "producer:ValidElectronsProducer"))
  if not isData:                 config["Processors"].append( "producer:HttValidGenTausProducer")
  if not (isData): config["Processors"].append( "producer:TauCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
                                                              "producer:NewValidMTPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:Run2DecayChannelProducer",
                                                              "producer:DiVetoMuonVetoProducer"))
  if not (isData or isEmbedded): config["Processors"].append( "producer:TaggedJetCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"))
  config["Processors"].append(                                "filter:MinimalPlotlevelFilter")

  if btag_eff: config["ProcessorsBtagEff"] = copy.deepcopy(config["Processors"])
  config["Processors"].extend((                               "producer:MetCorrector",
                                                              "producer:PuppiMetCorrector",
                                                              "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer",
                                                              "producer:DiBJetQuantitiesProducer"))
  if not isEmbedded:             config["Processors"].extend(("producer:SimpleEleTauFakeRateWeightProducer",
                                                              "producer:SimpleMuTauFakeRateWeightProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                       config["Processors"].append( "producer:ZPtReweightProducer")
  if not isData and not isEmbedded:                 config["Processors"].append( "producer:RooWorkspaceWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:TauDecayModeWeightProducer")
  if not isData:                 config["Processors"].append( "producer:TauTriggerEfficiencyProducer")
  if not isData:                 config["Processors"].append( "producer:TauIDScaleFactorProducer")
  config["Processors"].append(                                "producer:EventWeightProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  if isMSSMggH:                  config["Processors"].append( "producer:NLOreweightingWeightsProducer")
  config["Processors"].append(                                "producer:SvfitProducer")
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]

  # Subanalyses settings
  if btag_eff:
    config["Processors"] = copy.deepcopy(config["ProcessorsBtagEff"])
    if pipelines != ['nominal']:
        raise Exception("There is no use case for calculating btagging efficiency with systematics shifts: %s" % ' '.join(pipelines))

    return importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.btag_efficiency_subanalysis").build_config(nickname, nominal_config=config, channel='mt', **kwargs)

  if tau_es:
    # needed pipelines : nominal tauES_subanalysis tauMuFakeESperDM_shifts METunc_shifts METrecoil_shifts JECunc_shifts regionalJECunc_shifts btagging_shifts
    config["Quantities"].extend(["leadingTauEnergyAssymetry"])

  # pipelines - systematic shifts
  needed_pipelines = ['nominal', 'tauESperDM_shifts', 'tauMuFakeESperDM_shifts', 'regionalJECunc_shifts', 'METunc_shifts', 'METrecoil_shifts', 'btagging_shifts']
  if pipelines is None:
      raise Exception("pipelines is None in %s" % (__file__))
  elif 'auto' in pipelines:
      pipelines = needed_pipelines

  return_conf = jsonTools.JsonDict()
  for pipeline in pipelines:
      if pipeline not in needed_pipelines:
          log.warning("Warning: pipeline NOT in the list of needed pipelines. Still adding it.")
      log.info('Add pipeline: %s' %(pipeline))
      return_conf += ACU.apply_uncertainty_shift_configs('mt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis." + pipeline).build_config(nickname, **kwargs))

  return return_conf
