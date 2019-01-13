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
  isSignal = re.search("HToTauTau",nickname)
  isGluonFusion = re.search("GluGluHToTauTauM125", nickname)
  
  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsVetoElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsMinimalPlotlevelFilter_em",
    #"HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsMVATestMethods"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["Channel"] = "EM"
  config["MinNElectrons"] = 1
  config["MinNMuons"] = 1
  # HltPaths_comment: The first path must be one with the higher pt cut on the electron. The second and last path must be one with the higher pt cut on the muon. Corresponding Pt cuts are implemented in the Run2DecayChannelProducer.
  if re.search("Run2016(B|C|D|E|F)|Summer16|Embedding2016", nickname): config["HltPaths"] = [
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]
  elif re.search("Run2016(G|H)", nickname): config["HltPaths"] = [
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]
  config["HLTBranchNames"] = [
          "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
          "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
          "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
          "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v",
          ]
  config["NoHltFiltering"] = True
  
  config["ElectronLowerPtCuts"] = ["13.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.5"]
  config["MuonLowerPtCuts"] = ["10.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.4"]
  config["DeltaRTriggerMatchingElectrons"] = 0.4
  config["DeltaRTriggerMatchingMuons"] = 0.4
  config["DiTauPairMinDeltaRCut"] = 0.3
  config["DiTauPairIsTauIsoMVA"] = True
  
  if re.search("Run2016(G|H)", nickname):
    config["DiTauPairLepton1LowerPtCuts"] = ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:-1.0"]
    config["DiTauPairLepton2LowerPtCuts"] = ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:-1.0"]
  #~ elif isEmbedded:
    #~ config["DiTauPairLepton1LowerPtCuts"] = ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:-1.0", "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:-1.0"]
    #~ config["DiTauPairLepton2LowerPtCuts"] = ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:-1.0", "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:-1.0"]
  else:
    config["DiTauPairLepton1LowerPtCuts"] = ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:-1.0"]
    config["DiTauPairLepton2LowerPtCuts"] = ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:-1.0"]
    
  #~ config["DiTauPairNoHLT"] = True if isEmbedded else False
  if isEmbedded:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_12_embedded.root"
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_12_embedded.root"
    config["EmbeddedWeightWorkspaceWeightNames"]=[
          "0:muonEffTrgWeight",
          "0:muonEffIDWeight",
          "1:muonEffIDWeight",
          
          #~ "1:isoWeight",
          "1:isoWeight",
          "1:idWeight",
          "1:trackWeight",

          "1:trigger_23_data_Weight",
          "1:trigger_23_embed_Weight",
          "1:trigger_8_data_Weight",
          "1:trigger_8_embed_Weight",
          
          "0:isoWeight",
          "0:idWeight",
          #~ "0:idisoWeight",
          "0:trackWeight",

          "0:trigger_23_data_Weight",
          "0:trigger_23_embed_Weight",
          "0:trigger_12_data_Weight",
          "0:trigger_12_embed_Weight",

          ]          
    config["EmbeddedWeightWorkspaceObjectNames"]=[
          "0:m_sel_trg_ratio",
          "0:m_sel_idEmb_ratio",
          "1:m_sel_idEmb_ratio",
          
          "1:m_looseiso_ratio",
          "1:m_id_ratio",
          "1:m_trk_ratio",
          
          "1:m_trg23_binned_ic_data",
          "1:m_trg23_binned_ic_embed",         
          "1:m_trg8_binned_ic_data",
          "1:m_trg8_binned_ic_embed",
          
          "0:e_looseiso_ratio",
          "0:e_id_ratio",
          "0:e_trk_ratio",

          "0:e_trg23_binned_ic_data",
          "0:e_trg23_binned_ic_embed",    
          "0:e_trg12_binned_ic_data",
          "0:e_trg12_binned_ic_embed",
          ]
    config["EmbeddedWeightWorkspaceObjectArguments"] = [
          "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
          "0:gt_pt,gt_eta",
          "1:gt_pt,gt_eta",
          
          "1:m_pt,m_eta",
          "1:m_pt,m_eta",
          "1:m_eta",

          "1:m_pt,m_eta,m_iso",
          "1:m_pt,m_eta,m_iso",
          "1:m_pt,m_eta,m_iso",
          "1:m_pt,m_eta,m_iso",
          
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          
          "0:e_pt,e_eta,e_iso",
          "0:e_pt,e_eta,e_iso",
          "0:e_pt,e_eta,e_iso",
          "0:e_pt,e_eta,e_iso",
        ]
  else:
      config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_5_2.root"
      config["RooWorkspaceWeightNames"] = [
          "0:trackWeight",     
          "1:trackWeight",
      ]
      config["RooWorkspaceObjectNames"] = [
          "0:e_trk_ratio",
          "1:m_trk_ratio",
          
      ]
      config["RooWorkspaceObjectArguments"] = [
          "0:e_eta,e_pt",
          "1:m_eta",
       
    ]
    
  #~ config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_2017_v1.root"
  config["QCDFactorWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_12_embedded.root"
  config["QCDFactorWorkspaceWeightNames"]=[
      "0:em_qcd_osss_binned_Weight",
      "0:em_qcd_extrap_up_Weight",
      "0:em_qcd_extrap_down_Weight",
      "0:em_qcd_osss_0jet_rateup_Weight",
      "0:em_qcd_osss_0jet_ratedown_Weight",
      "0:em_qcd_osss_0jet_shapeup_Weight",
      "0:em_qcd_osss_0jet_shapedown_Weight",
      "0:em_qcd_osss_1jet_rateup_Weight",
      "0:em_qcd_osss_1jet_ratedown_Weight",
      "0:em_qcd_osss_1jet_shapeup_Weight",
      "0:em_qcd_osss_1jet_shapedown_Weight",
      
      "0:em_qcd_extrap_uncert_Weight",
    ]

  config["QCDFactorWorkspaceObjectNames"] = [
      "0:em_qcd_osss_binned",
      "0:em_qcd_extrap_up",
      "0:em_qcd_extrap_down",
      "0:em_qcd_0jet_rateup",
      "0:em_qcd_0jet_ratedown",
      "0:em_qcd_0jet_shapeup",
      "0:em_qcd_0jet_shapedown",
      "0:em_qcd_1jet_rateup",
      "0:em_qcd_1jet_ratedown",
      "0:em_qcd_1jet_shapeup",
      "0:em_qcd_1jet_shapedown",
      
      "0:em_qcd_extrap_uncert",
  ]
  config["QCDFactorWorkspaceObjectArguments"] = [
      "0:e_pt,m_pt,dR,njets",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      
      "0:e_pt,m_pt",
    ]

  config["TriggerEfficiencyData"] = [
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele12leg_eff.root",
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele23leg_eff.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu8leg_2016BtoH_eff.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu23leg_2016BtoH_eff.root"]
  config["TriggerEfficiencyMc"] = [
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele12leg_eff.root",
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23leg_eff.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8leg_2016BtoH_eff.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu23leg_2016BtoH_eff.root"]
  config["IdentificationEfficiencyData"] = [
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p15_eff.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"]
  config["IdentificationEfficiencyMc"] = [
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p15_eff.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"]
  
  config["IdentificationEfficiencyMode"] = "multiply_weights"
  config["TauTauRestFrameReco"] = "collinear_approximation"
  config["TriggerEfficiencyMode"] = "correlate_triggers"
  
  if re.search("Run2016(G|H)", nickname):
    config["ElectronTriggerFilterNames"] = [
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLDZFilter",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter"]
    config["MuonTriggerFilterNames"] = [
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLDZFilter",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter"]
  else:
    config["ElectronTriggerFilterNames"] = [
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter"]
    config["MuonTriggerFilterNames"] = [
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8"]
  
  config["InvalidateNonMatchingElectrons"] = True
  config["InvalidateNonMatchingMuons"] = True
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["EventWeight"] = "eventWeight"

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.fourVectorQuantities").build_list()
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.syncQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.svfitSyncQuantities").build_list())
  #config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.splitJecUncertaintyQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend([
      "nVetoElectrons",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
      "nLooseElectrons",
      "nLooseMuons",
      "nDiTauPairCandidates",
      "nAllDiTauPairCandidates",
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
      "idisoweight_1",
      "idWeight_1",
      "isoWeight_1",
      "idWeight_2",
      "isoWeight_2",
      "trackWeight_1",
      "trackWeight_2",
      "diLepMetMt",
      "pZetaVis",
      "pZetaMiss",
      "mt_tt",
      #"htxs_stage0cat",
      #"htxs_stage1cat",
      "flagMETFilter",
      "pt_ttjj",
      "mt_tot"
  ])
  if isEmbedded:
    config["Quantities"].extend([
          "muonEffTrgWeight", "muonEffIDWeight_1","muonEffIDWeight_2", 
          "trigger_23_data_Weight_2","trigger_23_embed_Weight_2","trigger_8_embed_Weight_2" ,"trigger_8_data_Weight_2",
          "trigger_23_data_Weight_1","trigger_23_embed_Weight_1","trigger_12_embed_Weight_1" ,"trigger_12_data_Weight_1",
          "looseIsoWeight_2","idisoWeight_1","idisoWeight_2"             
           ])
  elif not isData:
    config["Quantities"].extend([
          "trigger_23_data_Weight_2","trigger_23_mc_Weight_2","trigger_8_mc_Weight_2" ,"trigger_8_data_Weight_2",
          "trigger_23_data_Weight_1","trigger_23_mc_Weight_1","trigger_12_mc_Weight_1" ,"trigger_12_data_Weight_1"           
           ])    
    config["Quantities"].extend([
    "trigger_12_Weight_1","trigger_23_Weight_1","trigger_8_Weight_2","trigger_23_Weight_2"         
    ])
  if re.search("HToTauTauM125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1cat"
    ])
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.ggHNNLOQuantities").build_list())

  config["Quantities"].extend(["dr_tt", "pt_ttjj",
      "em_qcd_osss_binned_Weight",
      "em_qcd_extrap_up_Weight",
      "em_qcd_extrap_down_Weight",
      "em_qcd_osss_0jet_rateup_Weight",
      "em_qcd_osss_0jet_ratedown_Weight",
      "em_qcd_osss_0jet_shapeup_Weight",
      "em_qcd_osss_0jet_shapedown_Weight",
      "em_qcd_osss_1jet_rateup_Weight",
      "em_qcd_osss_1jet_ratedown_Weight",
      "em_qcd_osss_1jet_shapeup_Weight",
      "em_qcd_osss_1jet_shapedown_Weight",
        "em_qcd_extrap_uncert_Weight"])
  config["OSChargeLeptons"] = True
  
  config["Processors"] = [                                    "producer:HltProducer",
                                                              "filter:HltFilter",
                                                              "producer:MetSelector"]
  if not isData:                 config["Processors"].append( "producer:ElectronCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidElectronsProducer",
                                                              "filter:ValidElectronsFilter",
                                                              "producer:ElectronTriggerMatchingProducer",
                                                              "filter:MinElectronsCountFilter",
                                                              "producer:ValidMuonsProducer",
                                                              "filter:ValidMuonsFilter",
                                                              "producer:MuonTriggerMatchingProducer",
                                                              "filter:MinMuonsCountFilter",
                                                              "producer:ValidTausProducer",
                                                              "producer:ValidEMPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:HttValidVetoElectronsProducer",
                                                              "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:Run2DecayChannelProducer",
                                                              "producer:DiVetoElectronVetoProducer",
                                                              "producer:TaggedJetCorrectionsProducer",
                                                              "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"))
                                                              #"producer:TaggedJetUncertaintyShiftProducer"))
  if not isData: config["Processors"].append( "producer:HttValidGenTausProducer")  
  if not isData and not isEmbedded:
    config["Processors"].append( "producer:MetCorrector") #"producer:MvaMetCorrector"
    config["Processors"].append( "producer:GroupedJetUncertaintyShiftProducer") #"producer:MvaMetCorrector"
    config["Processors"].append( "producer:TriggerWeightProducer")
    config["Processors"].append( "producer:IdentificationWeightProducer")

  config["Processors"].extend((                               "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer"))
  if not isData:                 config["Processors"].extend(("producer:SimpleEleTauFakeRateWeightProducer",
                                  "producer:SimpleMuTauFakeRateWeightProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                       config["Processors"].append( "producer:ZPtReweightProducer")
  if isEmbedded:
    config["Processors"].append( "producer:EmbeddedWeightProducer")
  config["Processors"].append( "producer:QCDFactorProducer")
  config["Processors"].extend((                               "filter:MinimalPlotlevelFilter",
                                                              "producer:SvfitProducer",
                                                              "producer:ImpactParameterCorrectionsProducer")) #"producer:MVATestMethodsProducer"
  if not isData and not isEmbedded:                 config["Processors"].append( "producer:RooWorkspaceWeightProducer")
  config["Processors"].append(                                "producer:EventWeightProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  
  
  config["AddGenMatchedParticles"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedElectrons"] = True
  config["BranchGenMatchedTaus"] = True
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"] 
  
  
  # pipelines - systematic shifts
  return ACU.apply_uncertainty_shift_configs('em', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.nominal").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('em', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.eleES_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('em', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.JECunc_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('em', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.METunc_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('em', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.METrecoil_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('em', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.btagging_shifts").build_config(nickname))
