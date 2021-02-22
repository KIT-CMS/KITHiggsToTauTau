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
  nmssm = True if ("nmssm" in kwargs and kwargs["nmssm"]) else False

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
  isGluonFusion = re.search("(GluGluHToTauTau|ggZHHToTauTauZToQQ).*M125", nickname)
  isVBF = re.search("(VBFHToTauTau.*M125|^W(minus|plus)HToTauTau.*125.*|^ZHToTauTau.*125.*)", nickname)
  isMSSMggH = re.search("SUSYGluGluToH", nickname)

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
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauES",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMinimalPlotlevelFilter_et"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname, **kwargs)

  # explicit configuration
  config["Channel"] = "ET"
  config["MinNElectrons"] = 1
  config["MinNTaus"] = 1

  ### HLT & Trigger Object configuration
  config["HltPaths"] = [
      "HLT_Ele25_eta2p1_WPTight_Gsf",
      "HLT_VLooseIsoPFTau120_Trk50_eta2p1",
      "HLT_VLooseIsoPFTau140_Trk50_eta2p1",
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"
  ]
  config["DiTauPairLepton1LowerPtCuts"] = [
      "HLT_Ele25_eta2p1_WPTight_Gsf_v:26.0",
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v:25.0"
  ]
  config["DiTauPairLepton2LowerPtCuts"] = [
          "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v:25.0"
  ]
  config["DiTauPairLepton2UpperEtaCuts"] = [
          "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v:2.1",
          "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v:2.1",
          "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v:2.1",
  ]
  config["CheckLepton1TriggerMatch"] = [
      "trg_singleelectron",
      "trg_singlemuon",

      "trg_mutaucross",
      "trg_doubletau",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
      "trg_eletaucross",
      "trg_singletau140_leading",
  ]
  config["CheckLepton2TriggerMatch"] = [
      "trg_mutaucross",
      "trg_doubletau",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
      "trg_eletaucross",
      "trg_singletau120_trailing",
      "trg_singletau140_trailing",
  ]
  config["HLTBranchNames"] = [
      "trg_singleelectron:HLT_Ele25_eta2p1_WPTight_Gsf_v",
      "trg_singlemuon:HLT_IsoMu22_v",
      "trg_singlemuon:HLT_IsoTkMu22_v",
      "trg_singlemuon:HLT_IsoMu22_eta2p1_v",
      "trg_singlemuon:HLT_IsoTkMu22_eta2p1_v",
      #"trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
      "trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v",
      "trg_doubletau:HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v",
      "trg_doubletau:HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v",
      "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
      "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v",
      "trg_eletaucross:HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v",
      "trg_singletau120_leading:HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
      "trg_singletau120_trailing:HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
      "trg_singletau140_leading:HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
      "trg_singletau140_trailing:HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
  ]

  config["ElectronTriggerFilterNames"] = [
      "HLT_Ele25_eta2p1_WPTight_Gsf_v:hltEle25erWPTightGsfTrackIsoFilter",
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v:hltEle24WPLooseL1SingleIsoEG22erGsfTrackIsoFilter"
  ]
  config["TauTriggerFilterNames"] = [
          "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v:hltPFTau20TrackLooseIso",
          "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoEle24WPLooseGsfLooseIsoPFTau20",
          "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v:hltPFTau120TrackPt50LooseAbsOrRelVLooseIso",
          "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v:hltPFTau140TrackPt50LooseAbsOrRelVLooseIso",
  ]
  if isData:
    # these two trigger should be used data only
    config["ElectronTriggerFilterNames"].extend(
      ["HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v:hltEle24WPLooseL1IsoEG22erTau20erGsfTrackIsoFilter",
       "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v:hltEle24WPLooseL1IsoEG22erIsoTau26erGsfTrackIsoFilter"])
    config["HLTBranchNames"].extend(
       ["trg_eletaucross:HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v",
        "trg_eletaucross:HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v"])
    config["TauTriggerFilterNames"].extend(
       ["HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v:hltPFTau20TrackLooseIso",
        "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v:hltOverlapFilterIsoEle24WPLooseGsfLooseIsoPFTau20",
        "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v:hltPFTau30TrackLooseIso",
        "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v:hltOverlapFilterIsoEle24WPLooseGsfLooseIsoPFTau30"])
    config["HltPaths"].extend([
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20",
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30"])
    config["DiTauPairLepton1LowerPtCuts"].extend([
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v:25.0",
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v:25.0"])
    config["DiTauPairLepton2LowerPtCuts"].extend([
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v:25.0",
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v:35.0"])
    config["DiTauPairLepton2UpperEtaCuts"].extend([
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v:2.1",
      "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v:2.1"])

  ### Signal pair selection configuration
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = False
  config["TauVeto2ProngDMs"] = True
  config["ElectronScaleAndSmearUsed"] = True if not isEmbedded else False
  config["ElectronScaleAndSmearTag"] = "ecalTrkEnergyPostCorr"
  config["ElectronLowerPtCuts"] = ["25.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.1"]
  config["TauLowerPtCuts"] = ["30.0"]
  config["TauUpperAbsEtaCuts"] = ["2.3"]
  config["TriggerObjectLowerPtCut"] = -1.0
  config["DiTauPairMinDeltaRCut"] = 0.5
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
  config["BranchGenMatchedElectrons"] = True
  config["BranchGenMatchedTaus"] = True
  config["EventWeight"] = "eventWeight"
  config["TopPtReweightingStrategy"] = "Run1"

  ### Met correction SF for embedding
  if isEmbedded:
    config["EmbedddingFakeMETCorrection"] = 0.958

  ### Efficiencies & weights configuration
  config["TauTriggerInput"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/tauTriggerEfficiencies2016KIT_deeptau.root"
  config["TauTriggerInputKIT"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/tauTriggerEfficiencies2016KIT_deeptau.root"
  config["TauTrigger"] = "etau"
  config["TauTriggerWorkingPoints"] = [
       "VVVLoose",
       "VVLoose",
       "VLoose",
       "Loose",
       "Medium",
       "Tight",
       "VTight",
       "VVTight",
  ]
  config["TauTriggerIDTypes"] = [
       "DeepTau",
  ]
  if isEmbedded:
    config["TauTriggerEfficiencyWeightNames"] = [
        "1:crossTriggerDataEfficiencyWeight",
        "1:crossTriggerKITDataEfficiencyWeight",
        "1:crossTriggerEMBEfficiencyWeight",
        "1:crossTriggerMCEfficiencyWeight",
    ]
  else:
    config["TauTriggerEfficiencyWeightNames"] = [
        "1:crossTriggerMCEfficiencyWeight",
        "1:crossTriggerDataEfficiencyWeight",
    ]
  config["TauTriggerSFProviderInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/2016_tauTriggerEff_DeepTau2017v2p1.root"
  config["TauTriggerSFProviderWeightNames"] = [
        "1:crossTriggerDataEfficiencyWeight_POG",
        "1:crossTriggerMCEfficiencyWeight_POG",
        "1:crossTriggerSFWeight_POG",
    ]

   # Define weight names to be written out - only store weights that are actually filled
  tauTriggerWeights = []
  for WeightName in config["TauTriggerEfficiencyWeightNames"]:
    for shift in ["","Up","Down"]:
      for IDType in config["TauTriggerIDTypes"]:
        for wp in config["TauTriggerWorkingPoints"]:
          tauTriggerWeights.append(WeightName.split(":")[1]+shift+"_"+wp+"_"+IDType+"_"+str(int(WeightName.split(":")[0])+1))
  for WeightName in config["TauTriggerSFProviderWeightNames"]:
    for shift in ["","Up","Down"]:
        for wp in config["TauTriggerWorkingPoints"]:
          tauTriggerWeights.append(WeightName.split(":")[1]+shift+"_"+wp+"_"+str(int(WeightName.split(":")[0])+1))


  config["SingleTauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2016_singletau.root"
  config["SingleTauTriggerWorkingPoints"] = [
       "vvvloose",
       "vvloose",
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
  singleTauTriggerWeights = []
  if not isData:
    config["SingleTauTriggerEfficiencyWeightNames"] = [
        "1:singleTauTriggerMCEfficiencyWeight",
        "1:singleTauTriggerDataEfficiencyWeight",
    ]

    # Define weight names to be written out - only store weights that are actually filled
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
      "1:tauIDScaleFactorWeight",
  ]
  config["TauIDSFUseEMBSFs"] = isEmbedded
  config["TauIDSFUseTightVSeSFs"] = True

  config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2016.root"
  if isEmbedded:
      config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2016.root"
      config["EmbeddedWeightWorkspaceWeightNames"] = [
            "0:muonEffTrgWeight",
            "0:muonEffIDWeight",
            "1:muonEffIDWeight",

            "0:eleRecoWeight",
            "0:isoWeight",
            "0:idWeight",
            "0:singleTriggerEmbeddedEfficiencyWeightKIT",
            "0:singleTriggerDataEfficiencyWeightKIT",

            "0:crossTriggerEmbeddedEfficiencyWeightKIT",
            "0:crossTriggerDataEfficiencyWeightKIT"
            ]
      config["EmbeddedWeightWorkspaceObjectNames"] = [
            "0:m_sel_trg_kit_ratio",
            "0:m_sel_idemb_kit_ratio",
            "1:m_sel_idemb_kit_ratio",

            "0:e_trk_ratio",
            "0:e_iso_ratio_emb",
            "0:e_id_ratio_emb",
            "0:e_trg_emb",
            "0:e_trg_data",

            "0:e_trg_EleTau_Ele24Leg_kit_embed",
            "0:e_trg_EleTau_Ele24Leg_kit_data"
            ]
      config["EmbeddedWeightWorkspaceObjectArguments"] = [
            "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
            "0:gt_pt,gt_eta",
            "1:gt_pt,gt_eta",

            "0:e_pt,e_eta",
            "0:e_pt,e_eta",
            "0:e_pt,e_eta",
            "0:e_pt,e_eta",
            "0:e_pt,e_eta",

            "0:e_pt,e_eta",
            "0:e_pt,e_eta",
      ]
      config["HighPtTauWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_highpttau_legacy_2016.root"
      config["HighPtTauWeightWorkspaceWeightNames"] = [
              "1:tauIDScaleFactorWeight_highpt_deeptauid",

              "1:tauIDScaleFactorWeight_highpt_deeptauid_100To500Up",
              "1:tauIDScaleFactorWeight_highpt_deeptauid_100To500Down",
              "1:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up",
              "1:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down",
              ]
      config["HighPtTauWeightWorkspaceObjectNames"] = [
              "1:t_deeptauid_highpt_tightvse_embed",

              "1:t_deeptauid_highpt_tightvse_embed_bin5_up",
              "1:t_deeptauid_highpt_tightvse_embed_bin5_down",
              "1:t_deeptauid_highpt_tightvse_embed_bin6_up",
              "1:t_deeptauid_highpt_tightvse_embed_bin6_down",
              ]
      config["HighPtTauWeightWorkspaceObjectArguments"] = [
              "1:t_pt",

              "1:t_pt",
              "1:t_pt",
              "1:t_pt",
              "1:t_pt",
      ]
      config["LeptonTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_highpttau_legacy_2016.root"
      config["LeptonTauTriggerWeightWorkspaceWeightNames"] = [
              "0:etau_triggerweight_ic",

              "0:etau_triggerweight_ic_crosslep_up",
              "0:etau_triggerweight_ic_crosslep_down",

              "0:etau_triggerweight_ic_singlelep_up",
              "0:etau_triggerweight_ic_singlelep_down",

              "0:etau_triggerweight_ic_dm0_up",
              "0:etau_triggerweight_ic_dm0_down",
              "0:etau_triggerweight_ic_dm1_up",
              "0:etau_triggerweight_ic_dm1_down",
              "0:etau_triggerweight_ic_dm10_up",
              "0:etau_triggerweight_ic_dm10_down",
              "0:etau_triggerweight_ic_dm11_up",
              "0:etau_triggerweight_ic_dm11_down",

              "0:etau_triggerweight_ic_singletau_up",
              "0:etau_triggerweight_ic_singletau_down",
              ]
      config["LeptonTauTriggerWeightWorkspaceObjectNames"] = [
              "0:et_trg_embed_ratio",

              "0:et_trg_embed_ratio_crosslep_up",
              "0:et_trg_embed_ratio_crosslep_down",

              "0:et_trg_embed_ratio_singlelep_up",
              "0:et_trg_embed_ratio_singlelep_down",

              "0:et_trg_embed_ratio_dm0_up",
              "0:et_trg_embed_ratio_dm0_down",
              "0:et_trg_embed_ratio_dm1_up",
              "0:et_trg_embed_ratio_dm1_down",
              "0:et_trg_embed_ratio_dm10_up",
              "0:et_trg_embed_ratio_dm10_down",
              "0:et_trg_embed_ratio_dm11_up",
              "0:et_trg_embed_ratio_dm11_down",

              "0:et_trg_embed_ratio_singletau_up",
              "0:et_trg_embed_ratio_singletau_down",
              ]
      config["LeptonTauTriggerWeightWorkspaceObjectArguments"] = [
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",

              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",

              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",

              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",

              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
              "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm,t_phi",
      ]
  elif not isData:
    config["RooWorkspaceWeightNames"] = [
      "0:eleRecoWeight",
      "0:isoWeight",
      "0:idWeight",
      "0:singleTriggerMCEfficiencyWeightKIT",
      "0:singleTriggerDataEfficiencyWeightKIT",

      "0:crossTriggerMCEfficiencyWeightKIT",
      "0:crossTriggerDataEfficiencyWeightKIT"
    ]
    config["RooWorkspaceObjectNames"] = [
      "0:e_trk_ratio",
      "0:e_iso_ratio",
      "0:e_id_ratio",
      "0:e_trg_mc",
      "0:e_trg_data",

      "0:e_trg_EleTau_Ele24Leg_kit_mc",
      "0:e_trg_EleTau_Ele24Leg_kit_data"
    ]
    config["RooWorkspaceObjectArguments"] = [
      "0:e_pt,e_eta",
      "0:e_pt,e_eta",
      "0:e_pt,e_eta",
      "0:e_pt,e_eta",
      "0:e_pt,e_eta",

      "0:e_pt,e_eta",
      "0:e_pt,e_eta"
    ]
    config["HighPtTauWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_highpttau_legacy_2016.root"
    config["HighPtTauWeightWorkspaceWeightNames"] = [
            "1:tauIDScaleFactorWeight_highpt_deeptauid",

            "1:tauIDScaleFactorWeight_highpt_deeptauid_100To500Up",
            "1:tauIDScaleFactorWeight_highpt_deeptauid_100To500Down",
            "1:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up",
            "1:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down",
            ]
    config["HighPtTauWeightWorkspaceObjectNames"] = [
            "1:t_deeptauid_highpt",

            "1:t_deeptauid_highpt_bin5_up",
            "1:t_deeptauid_highpt_bin5_down",
            "1:t_deeptauid_highpt_bin6_up",
            "1:t_deeptauid_highpt_bin6_down",
            ]
    config["HighPtTauWeightWorkspaceObjectArguments"] = [
            "1:t_pt",

            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
    ]
    config["LeptonTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_highpttau_legacy_2016.root"
    config["LeptonTauTriggerWeightWorkspaceWeightNames"] = [
            "0:etau_triggerweight_ic",

            "0:etau_triggerweight_ic_crosslep_up",
            "0:etau_triggerweight_ic_crosslep_down",

            "0:etau_triggerweight_ic_singlelep_up",
            "0:etau_triggerweight_ic_singlelep_down",

            "0:etau_triggerweight_ic_dm0_up",
            "0:etau_triggerweight_ic_dm0_down",
            "0:etau_triggerweight_ic_dm1_up",
            "0:etau_triggerweight_ic_dm1_down",
            "0:etau_triggerweight_ic_dm10_up",
            "0:etau_triggerweight_ic_dm10_down",
            "0:etau_triggerweight_ic_dm11_up",
            "0:etau_triggerweight_ic_dm11_down",

            "0:etau_triggerweight_ic_singletau_up",
            "0:etau_triggerweight_ic_singletau_down",
            ]
    config["LeptonTauTriggerWeightWorkspaceObjectNames"] = [
            "0:et_trg_ratio",

            "0:et_trg_ratio_crosslep_up",
            "0:et_trg_ratio_crosslep_down",

            "0:et_trg_ratio_singlelep_up",
            "0:et_trg_ratio_singlelep_down",

            "0:et_trg_ratio_dm0_up",
            "0:et_trg_ratio_dm0_down",
            "0:et_trg_ratio_dm1_up",
            "0:et_trg_ratio_dm1_down",
            "0:et_trg_ratio_dm10_up",
            "0:et_trg_ratio_dm10_down",
            "0:et_trg_ratio_dm11_up",
            "0:et_trg_ratio_dm11_down",

            "0:et_trg_ratio_singletau_up",
            "0:et_trg_ratio_singletau_down",
            ]
    config["LeptonTauTriggerWeightWorkspaceObjectArguments"] = [
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",

            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",

            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",

            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",

            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
            "0:e_pt,e_eta,e_iso,t_pt,t_eta,t_dm",
    ]


  ### Ntuple output quantities configuration
  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(isMC = (not isData) and (not isEmbedded), nickname = nickname, nmssm=nmssm)
  # config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.zptQuantities").build_list())
  if isNMSSM: config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.lheWeights").build_list(nmssm=nmssm))
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend(tauTriggerWeights)
  config["Quantities"].extend(singleTauTriggerWeights)
  config["Quantities"].extend([
      "nVetoElectrons",
      "nLooseElectrons",
      "nLooseMuons",
      "nDiTauPairCandidates",
      "nAllDiTauPairCandidates",
      "trg_singleelectron",
      #"triggerWeight_singleEl_1",
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
      "idIsoWeight_1",
      "flagMETFilter",
      "tauIDScaleFactorWeight_highpt_deeptauid_2",
      "tauIDScaleFactorWeight_highpt_deeptauid_100To500Up_2", "tauIDScaleFactorWeight_highpt_deeptauid_100To500Down_2",
      "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up_2", "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down_2",
      "tauIDScaleFactorWeight_highpt_deeptauid_100To500Up_2", "tauIDScaleFactorWeight_highpt_deeptauid_100To500Down_2",
      "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up_2", "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down_2",
      "etau_triggerweight_ic",
      "etau_triggerweight_ic_crosslep_up", "etau_triggerweight_ic_crosslep_down",
      "etau_triggerweight_ic_singlelep_up", "etau_triggerweight_ic_singlelep_down",
      "etau_triggerweight_ic_dm0_up", "etau_triggerweight_ic_dm0_down", "etau_triggerweight_ic_dm1_up", "etau_triggerweight_ic_dm1_down", "etau_triggerweight_ic_dm10_up", "etau_triggerweight_ic_dm10_down", "etau_triggerweight_ic_dm11_up", "etau_triggerweight_ic_dm11_down",
      "etau_triggerweight_ic_singletau_up", "etau_triggerweight_ic_singletau_down",
  ])
  if isEmbedded:
   config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.embeddedDecayModeWeightQuantities").build_list())
   config["Quantities"].extend([
     "muonEffTrgWeight",
     "muonEffIDWeight_1",
     "muonEffIDWeight_2"
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
  if isMSSMggH and re.search("powheg", nickname):
    config["Quantities"].extend(["ggh_b_weight_hdamp_up", "ggh_i_weight_hdamp_up", "ggh_t_weight_hdamp_up",
                                 "ggh_b_weight_hdamp_down", "ggh_i_weight_hdamp_down", "ggh_t_weight_hdamp_down",
                                 "ggh_b_weight_scale_up", "ggh_i_weight_scale_up", "ggh_t_weight_scale_up",
                                 "ggh_b_weight_scale_down", "ggh_i_weight_scale_down", "ggh_t_weight_scale_down",
                                 "ggA_b_weight_hdamp_up", "ggA_i_weight_hdamp_up", "ggA_t_weight_hdamp_up",
                                 "ggA_b_weight_hdamp_down", "ggA_i_weight_hdamp_down", "ggA_t_weight_hdamp_down",
                                 "ggA_b_weight_scale_up", "ggA_i_weight_scale_up", "ggA_t_weight_scale_up",
                                 "ggA_b_weight_scale_down", "ggA_i_weight_scale_down", "ggA_t_weight_scale_down",
    ])
  ### Processors & consumers configuration
  config["Processors"] =                                     ["producer:ElectronCorrectionsProducer",
                                                              "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:HltProducer",
                                                              "producer:MetCollector",
                                                              "producer:ValidElectronsProducer",
                                                              "filter:ValidElectronsFilter",
                                                              "producer:ElectronTriggerMatchingProducer",
                                                              "filter:MinElectronsCountFilter",
                                                              "producer:HttValidVetoElectronsProducer",
                                                              "producer:ValidMuonsProducer"]
  if not (isData): config["Processors"].append( "producer:TauCorrectionsProducer")
  if not isData:                 config["Processors"].append( "producer:HttValidGenTausProducer")
  config["Processors"].extend((                               "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
                                                              "producer:NewValidETPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:Run2DecayChannelProducer",
                                                              "producer:DiVetoElectronVetoProducer"))
  if not (isData or isEmbedded): config["Processors"].append( "producer:TaggedJetCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"))
  config["Processors"].append(                                "filter:MinimalPlotlevelFilter")
  if btag_eff: config["ProcessorsBtagEff"] = copy.deepcopy(config["Processors"])
  config["Processors"].extend((                               "producer:DiJetQuantitiesProducer",
                                                              "producer:DiBJetQuantitiesProducer",
                                                              "producer:MetCorrector",
                                                              "producer:PuppiMetCorrector",
                                                              "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer"
                                                              ))
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddingMETCorrector")                                                            
  if not isEmbedded:             config["Processors"].extend(("producer:SimpleEleTauFakeRateWeightProducer",
                                                              "producer:SimpleMuTauFakeRateWeightProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                       config["Processors"].append( "producer:ZPtReweightProducer")
  if not isData and not isEmbedded:                 config["Processors"].append( "producer:RooWorkspaceWeightProducer")
  if isNMSSM:                    config["Processors"].append( "producer:NMSSMVariationProducer")
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:TauDecayModeWeightProducer")
  if not isData:                 config["Processors"].append( "producer:HighPtTauWeightProducer")
  if not isData:                 config["Processors"].append( "producer:LeptonTauTriggerWeightProducer")
  if not isData:                 config["Processors"].append( "producer:TauTriggerEfficiencyProducer")
  if not isData:                 config["Processors"].append( "producer:TauTriggerSFProviderProducer")
  if not isData:                 config["Processors"].append( "producer:SingleTauTriggerEfficiencyProducer")
  if not isData:                 config["Processors"].append( "producer:TauIDScaleFactorProducer")
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

    return importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.btag_efficiency_subanalysis").build_config(nickname, nominal_config=config, channel='et', **kwargs)

  if etau_fake_es:
    # needed : nominal, tauESperDM_shifts, et_eleFakeTauES_subanalysis, maybe METunc_shifts METrecoil_shifts JECunc_shifts
    pass

  # pipelines - systematic shifts
  needed_pipelines = ['nominal', 'tauESperDM_shifts', 'tauEleFakeESperDM_shifts', 'regionalJECunc_shifts', 'METunc_shifts', 'METrecoil_shifts', 'btagging_shifts', 'eleES_shifts']
  if pipelines is None:
      raise Exception("pipelines is None in %s" % (__file__))
  elif 'auto' in pipelines:
      pipelines = needed_pipelines

  return_conf = jsonTools.JsonDict()
  for pipeline in pipelines:
      if pipeline not in needed_pipelines:
          log.warning("Warning: pipeline NOT in the list of needed pipelines. Still adding it.")
      log.info('Add pipeline: %s' %(pipeline))
      return_conf += ACU.apply_uncertainty_shift_configs('et', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis." + pipeline).build_config(nickname, **kwargs))

  return return_conf
