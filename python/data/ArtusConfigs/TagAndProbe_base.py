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
  year = datasetsHelper.base_dict[nickname]["year"]


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
  config["Year"] = year
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
  elif year == 2016: config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root"
  elif year == 2017: config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927-306462_13TeVFall17_31Mar2018ReReco_69p2mbMinBiasXS/%s.root"%nickname
  elif year == 2018: config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2018_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18.root"
  else:
    print "PileupWeightFile not defined"
    exit(1)

  if year == 2016:   config["ZptRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_v16_1.root" #TODO remeasure
  elif year == 2017: config["ZptRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_2017_v2.root"
  elif year == 2018: config["ZptRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_2017_v2.root" #TODO replace with 2018 measurements
  config["DoZptUncertainties"] = True
  if year == 2016:   config["MetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/TypeI-PFMet_Run2016_legacy.root"
  elif year == 2017: config["MetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/Type1_PFMET_2017.root"
  elif year == 2018: config["MetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/TypeI-PFMet_Run2018.root"
  if year == 2016:   config["MetShiftCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/PFMEtSys_2016.root"
  elif year == 2017: config["MetShiftCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MEtSys_2017.root"
  elif year == 2018: config["MetShiftCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MEtSys_2017.root"
  config["MvaMetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MvaMET_2016BCD.root"
  config["MetCorrectionMethod"] = "meanResolution"
  config["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_moriond17_BtoH.csv"
  config["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies_moriond2017.root"

  if isData or isEmbedded:
    if   year == 2016:      config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"]
    elif year == 2017:      config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"]
    elif year == 2018:      config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"]
    else:
      print "Luminosity GOLDEN JSON not defined"
      exit(1)

  if year == 2016:
    config["SimpleMuTauFakeRateWeightLoose"] = [1.22, 1.12, 1.26, 1.22, 2.39]
    config["SimpleMuTauFakeRateWeightTight"] = [1.47, 1.55, 1.33, 1.72, 2.50]
    config["SimpleEleTauFakeRateWeightVLoose"] = [1.21, 1.38]
    config["SimpleEleTauFakeRateWeightTight"] = [1.40, 1.90]
  elif year == 2017:
    config["SimpleMuTauFakeRateWeightLoose"] = [1.06, 1.02, 1.10, 1.03, 1.94]
    config["SimpleMuTauFakeRateWeightTight"] = [1.17, 1.29, 1.14, 0.93, 1.61]
    config["SimpleEleTauFakeRateWeightVLoose"] = [1.09, 1.19]
    config["SimpleEleTauFakeRateWeightTight"] = [1.80, 1.53]
  elif year == 2018:
    config["SimpleMuTauFakeRateWeightLoose"] = [1.05, 0.96, 1.06, 1.45, 1.75]
    config["SimpleMuTauFakeRateWeightTight"] = [1.23, 1.37, 1.12, 1.84, 2.01]
    config["SimpleEleTauFakeRateWeightVLoose"] = [1.089, 1.189]
    config["SimpleEleTauFakeRateWeightTight"] = [1.78, 1.55]


  # pipelines - channels including systematic shifts
  config["Pipelines"] = jsonTools.JsonDict()
  #config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.%i.inclusive"%year).build_config(nickname)
  #config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.%i.inclusiveZee"%year).build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.%i.mm_singlemuon"%year).build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.%i.mm_crossmuon"%year).build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.%i.mt"%year).build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.%i.ee_singleelectron"%year).build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.%i.ee_crosselectron"%year).build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.%i.et"%year).build_config(nickname)

  return config
