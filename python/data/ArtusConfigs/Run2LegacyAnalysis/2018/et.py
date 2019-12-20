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
  isGluonFusion = re.search("(GluGluHToTauTau|ggZHHToTauTauZToQQ).*M125", nickname)
  isVBF = re.search("(VBFHToTauTau.*M125|^W(minus|plus)HToTauTau.*125.*|^ZHToTauTau.*125.*)", nickname)
  isMSSMggH = re.search("SUSYGluGuToH", nickname)

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
          "HLT_Ele27_WPTight_Gsf",
          "HLT_Ele32_WPTight_Gsf",
          "HLT_Ele32_WPTight_Gsf_DoubleL1EG",
          "HLT_Ele35_WPTight_Gsf",
          "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
          "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1",
          "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
  ]
  config["DiTauPairLepton1LowerPtCuts"] = [
          "HLT_Ele27_WPTight_Gsf_v:28.0",
          "HLT_Ele32_WPTight_Gsf_v:33.0",
          "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:33.0",
          "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:25.0",
          "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:25.0",
          "HLT_Ele35_WPTight_Gsf_v:36.0",
  ]
  config["DiTauPairLepton2LowerPtCuts"] = [
          "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:35.0",
          "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:35.0",
  ]
  config["DiTauPairLepton2UpperEtaCuts"] = [
          "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:2.1",
          "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:2.1",
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
      "trg_crossmuon_mu20tau27_hps",
      "trg_crossele_ele24tau30",
      "trg_crossele_ele24tau30_hps",
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso",
      "trg_doubletau_35_mediso_hps",
      "trg_muonelectron_mu12ele23",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
  ]
  config["CheckLepton2TriggerMatch"] = [
      "trg_singletau_trailing",

      "trg_crossmuon_mu20tau27",
      "trg_crossmuon_mu20tau27_hps",
      "trg_crossele_ele24tau30",
      "trg_crossele_ele24tau30_hps",
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso",
      "trg_doubletau_35_mediso_hps",
      "trg_muonelectron_mu12ele23",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
  ]
  config["HLTBranchNames"] = [
      "trg_singlemuon_24:HLT_IsoMu24_v",
      "trg_singlemuon_27:HLT_IsoMu27_v",
      "trg_crossmuon_mu20tau27:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v",
      "trg_crossmuon_mu20tau27_hps:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v",
      "trg_singleelectron_27:HLT_Ele27_WPTight_Gsf_v",
      "trg_singleelectron_32:HLT_Ele32_WPTight_Gsf_v",
      "trg_singleelectron_32_fallback:HLT_Ele32_WPTight_Gsf_DoubleL1EG_v",
      "trg_singleelectron_35:HLT_Ele35_WPTight_Gsf_v",
      "trg_crossele_ele24tau30:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v",
      "trg_crossele_ele24tau30_hps:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v",
      "trg_doubletau_35_tightiso_tightid:HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v",
      "trg_doubletau_40_mediso_tightid:HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v",
      "trg_doubletau_40_tightiso:HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v",
      "trg_doubletau_35_mediso_hps:HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v",
      "trg_singletau_leading:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "trg_singletau_trailing:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "trg_muonelectron_mu12ele23:HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
  ]
  if isEmbedded:
    config["ElectronTriggerFilterNames"] = [
            "HLT_Ele27_WPTight_Gsf_v:hltEle27WPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_v:hltEle32WPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEle32L1DoubleEGWPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEGL1SingleEGOrFilter",
            "HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",
      ]
    config["TauTriggerFilterNames"] = [
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltPFTau180TrackPt50LooseAbsOrRelMediumHighPtRelaxedIsoIso",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSelectedPFTau180MediumChargedIsolationL1HLTMatched"
      ]
  else:
    config["ElectronTriggerFilterNames"] = [
            "HLT_Ele27_WPTight_Gsf_v:hltEle27WPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_v:hltEle32WPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEle32L1DoubleEGWPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEGL1SingleEGOrFilter",
            "HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30"

      ]
    config["TauTriggerFilterNames"] = [
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltSelectedPFTau30LooseChargedIsolationL1HLTMatched",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltHpsSelectedPFTau30LooseChargedIsolationL1HLTMatched",
            "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v:hltHpsOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltPFTau180TrackPt50LooseAbsOrRelMediumHighPtRelaxedIsoIso",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSelectedPFTau180MediumChargedIsolationL1HLTMatched"
      ]

  ### Signal pair selection configuration
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = True  # because using MVAoldDMv2
  config["TauVeto2ProngDMs"] = True
  config["ElectronScaleAndSmearUsed"] = True if not isEmbedded else False
  config["ElectronScaleAndSmearTag"] = "ecalTrkEnergyPostCorr"
  config["ElectronLowerPtCuts"] = ["25.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.1"]
  config["TauLowerPtCuts"] = ["23.0"]
  config["TauUpperAbsEtaCuts"] = ["2.3"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DeltaRTriggerMatchingTaus"] = 0.5
  config["DeltaRTriggerMatchingElectrons"] = 0.5
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

  ### Efficiencies & weights configuration
  config["TauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2018.root"
  config["TauTriggerInputKIT"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/tauTriggerEfficiencies2018KIT.root"
  config["TauTrigger"] = "etau"
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

  config["SingleTauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2018_singletau.root"
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
       "MVAv2",
       # "DeepTau",
  ]
  if not isData:
    config["SingleTauTriggerEfficiencyWeightNames"] = [
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
       "VLoose",
       "Loose",
       "Medium",
       "Tight",
       "VTight",
       "VVTight",
  ]
  config["TauIDSFTypes"] = [
       "MVAoldDM2017v2",
  ]
  config["TauIDScaleFactorWeightNames"] = [
      "1:tauIDScaleFactorWeight",
  ]
  config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2018.root"
  if isEmbedded:
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2018.root"
    config["EmbeddedWeightWorkspaceWeightNames"] = [
          "0:muonEffTrgWeight",
          "0:muonEffIDWeight",
          "1:muonEffIDWeight",

          "0:crossTriggerEmbeddedWeight",
          "1:crossTriggerEmbeddedWeight",


          "0:isoWeight",
          "0:idWeight",
          "0:trigger_27_35_Weight",
          "0:trigger_27_32_Weight",
          "0:trigger_32_35_Weight",
          "0:trigger_27_32_35_Weight",
          "0:trigger_27_Weight",
          "0:trigger_32_Weight",
          "0:trigger_32fb_Weight",
          "0:trigger_35_Weight"
          ]
    config["EmbeddedWeightWorkspaceObjectNames"] = [
          "0:m_sel_trg_ratio",
          "0:m_sel_idEmb_ratio",
          "1:m_sel_idEmb_ratio",

          "0:e_trg_EleTau_Ele24Leg_embed_kit_ratio",
          "1:et_emb_LooseChargedIsoPFTau30_tight_kit_ratio",


          "0:e_iso_binned_embed_kit_ratio",
          "0:e_id90_embed_kit_ratio",
          "0:e_trg27_trg35_embed_kit_ratio",
          "0:e_trg27_trg32_embed_kit_ratio",
          "0:e_trg32_trg35_embed_kit_ratio",
          "0:e_trg27_trg32_trg35_embed_kit_ratio",
          "0:e_trg27_embed_kit_ratio",
          "0:e_trg32_embed_kit_ratio",
          "0:e_trg32fb_embed_kit_ratio",
          "0:e_trg35_embed_kit_ratio"
          ]
    config["EmbeddedWeightWorkspaceObjectArguments"] = [
          "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
          "0:gt_pt,gt_eta",
          "1:gt_pt,gt_eta",

          "0:e_pt,e_eta",
          "1:t_pt",


          "0:e_pt,e_eta,e_iso",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta"
          ]
  elif not isData:
    config["RooWorkspaceWeightNames"] = [
          "0:crossTriggerMCEfficiencyWeight",
          "0:crossTriggerDataEfficiencyWeight",
          "0:crossTriggerMCWeight",

          "0:isoWeight",
          "0:idWeight",
          "0:trackWeight",

          "0:trigger_27_35_Weight",
          "0:trigger_27_32_Weight",
          "0:trigger_32_35_Weight",
          "0:trigger_27_32_35_Weight",
          "0:trigger_27_Weight",
          "0:trigger_32_Weight",
          "0:trigger_32fb_Weight",
          "0:trigger_35_Weight"
          ]
    config["RooWorkspaceObjectNames"] = [
          "0:e_trg_EleTau_Ele24Leg_desy_mc",
          "0:e_trg_EleTau_Ele24Leg_desy_data",
          "0:e_trg_EleTau_Ele24Leg_kit_ratio",

          "0:e_iso_binned_kit_ratio",
          "0:e_id90_kit_ratio",
          "0:e_trk_ratio",

          "0:e_trg27_trg35_kit_ratio",
          "0:e_trg27_trg32_kit_ratio",
          "0:e_trg32_trg35_kit_ratio",
          "0:e_trg27_trg32_trg35_kit_ratio",
          "0:e_trg27_kit_ratio",
          "0:e_trg32_kit_ratio",
          "0:e_trg32fb_kit_ratio",
          "0:e_trg35_kit_ratio"
          ]
    config["RooWorkspaceObjectArguments"] = [
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",

          "0:e_pt,e_eta,e_iso",
          "0:e_pt,e_eta",
          "0:e_eta",

          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta"
          ]
  config["EventWeight"] = "eventWeight"
  config["TopPtReweightingStrategy"] = "Run1"

  ### Ntuple output quantities configuration
  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(minimal_setup=minimal_setup, isMC = (not isData) and (not isEmbedded), nickname = nickname)
  # config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.zptQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend(tauTriggerWeights)
  config["Quantities"].extend(singleTauTriggerWeights)
  config["Quantities"].extend([
      "had_gen_match_pT_1",
      "had_gen_match_pT_2",
      "flagMETFilter",
      "trigger_27_35_Weight_1","trigger_27_32_32fb_Weight_1","trigger_27_32_Weight_1",
      "trigger_27_35_Weight_1",
      "trigger_27_32_Weight_1",
      "trigger_32_35_Weight_1",
      "trigger_27_32_35_Weight_1",
      "trigger_27_Weight_1",
      "trigger_32_Weight_1",
      "trigger_32fb_Weight_1",
      "crossTriggerMCWeight_1",
      "trigger_35_Weight_1"
  ])
  if isEmbedded:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.embeddedDecayModeWeightQuantities").build_list())
    config["Quantities"].extend([
          "muonEffTrgWeight", "muonEffIDWeight_1","muonEffIDWeight_2", "crossTriggerEmbeddedWeight_1", "crossTriggerEmbeddedWeight_2", "muon_crossTriggerEmbeddedWeight_2"
    ])
  if re.search("HToTauTauM125", nickname):
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
  config["Processors"].append(                                "filter:MinimalPlotlevelFilter")
  if not (isData or isEmbedded): config["Processors"].append( "producer:TaggedJetCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"))
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
  # if not isData:                 config["Processors"].append( "producer:SingleTauTriggerEfficiencyProducer")
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
