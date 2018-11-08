#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
import os

def build_config(nickname, **kwargs):
  analysis_channels = ['all'] if "analysis_channels" not in kwargs else kwargs["analysis_channels"]
  btag_eff = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "btag-eff" else False
  no_svfit = True if "no_svfit" in kwargs and kwargs["no_svfit"] else False
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))


  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50|150)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  isSUSYggH = re.search("SUSYGluGluToHToTauTau", nickname)


  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsKappa",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.lheWeightAssignment",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsSampleStitchingWeights"
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["SkipEvents"] = 0
  config["EventCount"] = -1
  config["Year"] = 2017
  config["InputIsData"] = isData

  if isSUSYggH:
    config["HiggsBosonMass"] = re.search("SUSYGluGluToHToTauTauM(\d+)_", nickname).groups()[0] #extracts generator mass from nickname
    config["NLOweightsRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NLOWeights/higgs_pt_v2_mssm_mode.root"

  BosonPdgIds = {
      "DY.?JetsToLL|EWKZ2Jets|Embedding(2016|MC)" : [
        23
      ],
      "^(GluGlu|GluGluTo|VBF|Wminus|Wplus|Z)(HToTauTau|H2JetsToTauTau)" : [
        25
      ],
      "W.?JetsToLN|EWKW" : [
        24
      ],
      "SUSY(BB|GluGlu|GluGluTo)(BB)?HToTauTau" : [
        25,
        35,
        36
        ]
  }
  config["BosonPdgIds"] = [0]
  for key, pdgids in BosonPdgIds.items():
    if re.search(key, nickname): config["BosonPdgIds"] = pdgids

  config["BosonStatuses"] = [62]
  config["ChooseMvaMet"] = False
  config["DeltaRMatchingRecoElectronGenParticle"] = 0.2
  config["DeltaRMatchingRecoElectronGenTau"] = 0.2
  config["DeltaRMatchingRecoMuonGenParticle"] = 0.2
  config["DeltaRMatchingRecoMuonGenTau"] = 0.2
  config["DeltaRMatchingRecoTauGenParticle"] = 0.2
  config["DeltaRMatchingRecoTauGenTau"] = 0.2
  config["RecoElectronMatchingGenParticlePdgIds"] = [11,13]
  config["RecoMuonMatchingGenParticlePdgIds"] = [11,13]
  config["RecoTauMatchingGenParticlePdgIds"] = [11,13]
  config["RecoElectronMatchingGenParticleMatchAllElectrons"] = "true"
  config["RecoMuonMatchingGenParticleMatchAllMuons"] = "true"
  config["RecoTauMatchingGenParticleMatchAllTaus"] = "true"
  config["MatchAllElectronsGenTau"] = "true"
  config["MatchAllMuonsGenTau"] = "true"
  config["MatchAllTausGenTau"] = "true"
  config["UpdateMetWithCorrectedLeptons"] = "true"


  config["OutputPath"] = "output.root"

  config["Processors"] = []
  #config["Processors"].append("filter:RunLumiEventFilter")
  #if not isEmbedded:                   config["Processors"].append( "filter:MetFilter")
  if isData or isEmbedded:             config["Processors"].append( "filter:JsonFilter")
  #if isDY or isTTbar:                  config["Processors"].append( "producer:ScaleVariationProducer")
  config["Processors"].append(                                      "producer:NicknameProducer")
  if not isData:
    if not isEmbedded:
      config["Processors"].extend((                                   "producer:CrossSectionWeightProducer",
                                                                      "producer:NumberGeneratedEventsWeightProducer"))
    if not isEmbedded:                 config["Processors"].append( "producer:PUWeightProducer")
    #if isWjets or isDY or isSUSYggH:   config["Processors"].append( "producer:GenBosonFromGenParticlesProducer")
    if isDY or isEmbedded:             config["Processors"].append( "producer:GenDiLeptonDecayModeProducer")
    config["Processors"].extend((                                   "producer:GenParticleProducer",
                                                                    "producer:GenPartonCounterProducer"))
    #if isSUSYggH:                      config["Processors"].append( "producer:NLOreweightingWeightsProducer")
    if isWjets or isDY or isEmbedded:  config["Processors"].extend(("producer:GenTauDecayProducer",
                                                                    "producer:GenBosonDiLeptonDecayModeProducer"))
    config["Processors"].extend((                                   "producer:GeneratorWeightProducer",
                                                                    "producer:RecoMuonGenParticleMatchingProducer",
                                                                    "producer:RecoMuonGenTauMatchingProducer",
                                                                    "producer:RecoElectronGenParticleMatchingProducer",
                                                                    "producer:RecoElectronGenTauMatchingProducer",
                                                                    "producer:RecoTauGenParticleMatchingProducer",
                                                                    "producer:RecoTauGenTauMatchingProducer",
                                                                    "producer:MatchedLeptonsProducer"))
    #if isTTbar:                        config["Processors"].append( "producer:TTbarGenDecayModeProducer")

  if isData or isEmbedded:                config["PileupWeightFile"] = "not needed"
  elif re.search(".*Summer17", nickname): config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927-306462_13TeVSummer17_PromptReco_69p2mbMinBiasXS.root"
  #elif re.search(".*Summer17", nickname): config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927-306462_13TeVSummer17_PromptReco_80p0mbMinBiasXS.root"
  elif re.search(".*Summer16", nickname): config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root"
  else:                                   config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2015_246908-260627_13TeVFall15MiniAODv2_PromptReco_69mbMinBiasXS.root"

  config["ZptRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_5.root"
  config["DoZptUncertainties"] = True
  config["MetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/TypeI-PFMet_Run2016BtoH.root"
  config["MetShiftCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/PFMEtSys_2016.root"
  config["MvaMetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MvaMET_2016BCD.root"
  config["MetCorrectionMethod"] = "meanResolution"
  config["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_moriond17_BtoH.csv"
  config["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies_moriond2017.root"

  if isData or isEmbedded:
    if   re.search("Run2017|Embedding2017", nickname):      config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt"]
    elif re.search("Run2016|Embedding2016", nickname):      config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"]
    elif re.search("Run2015(C|D)|Embedding2015", nickname): config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt"]
    elif re.search("Run2015B", nickname):                   config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_13TeV_16Dec2015ReReco_Collisions15_50ns_JSON_v2.txt"]

  if re.search("Fall15MiniAODv2", nickname):
    config["SimpleMuTauFakeRateWeightLoose"] = [1.0, 1.0, 1.0, 1.0, 1.0]
    config["SimpleMuTauFakeRateWeightTight"] = [1.0, 1.0, 1.0, 1.0, 1.0]
    config["SimpleEleTauFakeRateWeightVLoose"] = [1.02, 1.11]
    config["SimpleEleTauFakeRateWeightTight"] = [1.80, 1.30]
  else:
    config["SimpleMuTauFakeRateWeightLoose"] = [1.22, 1.12, 1.26, 1.22, 2.39]
    config["SimpleMuTauFakeRateWeightTight"] = [1.47, 1.55, 1.33, 1.72, 2.50]
    config["SimpleEleTauFakeRateWeightVLoose"] = [1.21, 1.38]
    config["SimpleEleTauFakeRateWeightTight"] = [1.40, 1.90]


  # pipelines - channels including systematic shifts
  config["Pipelines"] = jsonTools.JsonDict()
  #config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.inclusive").build_config(nickname)
  #config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.inclusiveZee").build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.mm_singlemuon").build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.mumu_crossmuon").build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.mutau_test").build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.ee_singleelectron").build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.ee_crosselectron").build_config(nickname)

  return config
