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
  isDY = re.search("DY.?JetsToLLM(10to50|50)", nickname)
  isWjets = re.search("(W.?Jets|WG)ToLNu", nickname)

  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMinimalPlotlevelFilter_ee"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname, **kwargs)

  # explicit configuration
  config["Channel"] = "EE"
  config["MinNElectrons"] = 2


  ### HLT & Trigger Object configuration
  config["HltPaths"] = [
          "HLT_Ele27_WPTight_Gsf",
          "HLT_Ele32_WPTight_Gsf",
          "HLT_Ele32_WPTight_Gsf_DoubleL1EG",
          "HLT_Ele35_WPTight_Gsf",
  ]
  config["DiTauPairLepton1LowerPtCuts"] = [
          "HLT_Ele27_WPTight_Gsf_v:28.0",
          "HLT_Ele32_WPTight_Gsf_v:33.0",
          "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:33.0",
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
    config["ElectronTriggerFilterNames"] = [
            "HLT_Ele27_WPTight_Gsf_v:hltEle27WPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_v:hltEle32WPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEle32L1DoubleEGWPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEGL1SingleEGOrFilter",
            "HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter",
      ]
  else:
    config["ElectronTriggerFilterNames"] = [
            "HLT_Ele27_WPTight_Gsf_v:hltEle27WPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_v:hltEle32WPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEle32L1DoubleEGWPTightGsfTrackIsoFilter",
            "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEGL1SingleEGOrFilter",
            "HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter",
      ]

  ### Signal pair selection configuration
  config["ElectronScaleAndSmearUsed"] = True if not isEmbedded else False
  config["ElectronScaleAndSmearTag"] = "ecalTrkEnergyPostCorr"
  config["ElectronLowerPtCuts"] = ["25.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.1"]
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
  config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2017.root"
  if isEmbedded:
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2017.root"
    config["EmbeddedWeightWorkspaceWeightNames"] = [
          "0:muonEffTrgWeight",
          "0:muonEffIDWeight",
          "1:muonEffIDWeight",

          "0:singleTriggerMCEfficiencyWeightKIT",
          "0:singleTriggerDataEfficiencyWeightKIT",
          "0:singleTriggerEmbeddedEfficiencyWeightKIT",
          "0:singleTriggerMCEfficiencyWeightKIT_32fb",
          "0:singleTriggerDataEfficiencyWeightKIT_32fb",
          "0:singleTriggerEmbeddedEfficiencyWeightKIT_32fb",

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

          "0:e_trg27_trg32_trg35_kit_mc",
          "0:e_trg27_trg32_trg35_kit_data",
          "0:e_trg27_trg32_trg35_kit_embed",
          "0:e_trg32fb_kit_mc",
          "0:e_trg32fb_kit_data",
          "0:e_trg32fb_kit_embed",

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
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",

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
        "0:singleTriggerMCEfficiencyWeightKIT",
        "0:singleTriggerDataEfficiencyWeightKIT",

        "0:singleTriggerMCEfficiencyWeightKIT_32",
        "0:singleTriggerDataEfficiencyWeightKIT_32",
        "0:singleTriggerMCEfficiencyWeightKIT_32fb",
        "0:singleTriggerDataEfficiencyWeightKIT_32fb",
        "0:singleTriggerMCEfficiencyWeightKIT_35",
        "0:singleTriggerDataEfficiencyWeightKIT_35",
        "0:singleTriggerMCEfficiencyWeightKIT_27or35",
        "0:singleTriggerDataEfficiencyWeightKIT_27or35",

        "0:idWeight",
        "0:isoWeight",
        "0:trackWeight",
    ]
    config["RooWorkspaceObjectNames"] = [
        "0:e_trg27_trg32_trg35_kit_mc",
        "0:e_trg27_trg32_trg35_kit_data",

        "0:e_trg32_kit_mc",
        "0:e_trg32_kit_data",
        "0:e_trg32fb_kit_mc",
        "0:e_trg32fb_kit_data",
        "0:e_trg35_kit_mc",
        "0:e_trg35_kit_data",
        "0:e_trg27_trg35_kit_mc",
        "0:e_trg27_trg35_kit_data",

        "0:e_iso_kit_ratio",
        "0:e_id90_kit_ratio",
        "0:e_trk_ratio",
    ]
    config["RooWorkspaceObjectArguments"] = [
        "0:e_pt,e_eta",
        "0:e_pt,e_eta",

        "0:e_pt,e_eta",
        "0:e_pt,e_eta",
        "0:e_pt,e_eta",
        "0:e_pt,e_eta",
        "0:e_pt,e_eta",
        "0:e_pt,e_eta",
        "0:e_pt,e_eta",
        "0:e_pt,e_eta",

        "0:e_pt,e_eta",
        "0:e_pt,e_eta",
        "0:e_eta,e_pt",
    ]
  config["EventWeight"] = "eventWeight"
  config["TopPtReweightingStrategy"] = "Run1"

  ### Ntuple output quantities configuration
  print nickname
  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(minimal_setup=False, isMC = (not isData) and (not isEmbedded), nickname = nickname)

  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend([
      "had_gen_match_pT_1",
      "had_gen_match_pT_2",
      "flagMETFilter",
      "singleTriggerMCEfficiencyWeightKIT_35_1",
      "singleTriggerDataEfficiencyWeightKIT_35_1",
      "singleTriggerMCEfficiencyWeightKIT_27or35_1",
      "singleTriggerDataEfficiencyWeightKIT_27or35_1",
      "trigger_27_35_Weight_1","trigger_27_32_32fb_Weight_1","trigger_27_32_Weight_1",
      "trigger_27_35_Weight_1",
      "trigger_27_32_Weight_1",
      "trigger_32_35_Weight_1",
      "trigger_27_32_35_Weight_1",
      "trigger_27_Weight_1",
      "trigger_32_Weight_1",
      "trigger_32fb_Weight_1",
      "trigger_35_Weight_1"
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
  if isEmbedded:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.embeddedDecayModeWeightQuantities").build_list())
    config["Quantities"].extend([
          "muonEffTrgWeight", "muonEffIDWeight_1","muonEffIDWeight_2", "crossTriggerEmbeddedWeight_1", "crossTriggerEmbeddedWeight_2"
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
                                                              "producer:ValidMuonsProducer"]
  if not (isData): config["Processors"].append( "producer:TauCorrectionsProducer")
  if not isData:                 config["Processors"].append( "producer:HttValidGenTausProducer")
  config["Processors"].extend((                               "producer:NewValidEEPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:Run2DecayChannelProducer"))
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
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                       config["Processors"].append( "producer:ZPtReweightProducer")
  if not isData and not isEmbedded:                 config["Processors"].append( "producer:RooWorkspaceWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  config["Processors"].append(                                "producer:EventWeightProducer")

  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]

  # Subanalyses settings
  if btag_eff:
    config["Processors"] = copy.deepcopy(config["ProcessorsBtagEff"])
    if pipelines != ['nominal']:
        raise Exception("There is no use case for calculating btagging efficiency with systematics shifts: %s" % ' '.join(pipelines))

    return importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.btag_efficiency_subanalysis").build_config(nickname, nominal_config=config, channel='et', **kwargs)

  # pipelines - systematic shifts
  needed_pipelines = ['nominal', 'eleES_shifts'] # missing other shifts, if needed
  if pipelines is None:
      raise Exception("pipelines is None in %s" % (__file__))
  elif 'auto' in pipelines:
      pipelines = needed_pipelines

  return_conf = jsonTools.JsonDict()
  for pipeline in pipelines:
      if pipeline not in needed_pipelines:
          log.warning("Warning: pipeline NOT in the list of needed pipelines. Still adding it.")
      log.info('Add pipeline: %s' %(pipeline))
      return_conf += ACU.apply_uncertainty_shift_configs('ee', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis." + pipeline).build_config(nickname, **kwargs))
  return return_conf
