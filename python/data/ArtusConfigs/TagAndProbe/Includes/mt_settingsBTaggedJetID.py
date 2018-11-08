#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

import Artus.Utility.jsonTools as jsonTools


def build_config(nickname, **kwargs):
    config = jsonTools.JsonDict()

    # explicit configuration
    config["BTaggedJetID_documentation"] = [
        "https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#b_tagging",
    ]

    # 2017 CSVv2
    config["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_94XSF_V2_B_F.csv"
    config["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies_march2018_btageff-all_samp-inc-CSVv2_medium.root"
    config["BTaggedJetCombinedSecondaryVertexName"] = "pfCombinedInclusiveSecondaryVertexV2BJetTags"
    config["BTaggerWorkingPoints"] = [
        "tight:0.9693",
        "medium:0.8838",
        "loose:0.5803",
    ]

    # TODO: add to the skims: DeepFlavour https://twiki.cern.ch/twiki/bin/view/CMS/DeepJet
    # Settings for DeepCSV algorithm 94X recommendation (stated to perform better than CSVv2)
    # config["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepCSV_94XSF_V3_B_F.csv"
    # config["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies_march2018_btageff-all_samp-inc-DeepCSV_medium.root"
    # config["BTaggedJetCombinedSecondaryVertexName"] = "pfDeepCSVJetTagsprobbb+pfDeepCSVJetTagsprobb"
    # config["BTaggerWorkingPoints"] = [
    #     "tight:0.8001",
    #     "medium:0.4941",
    #     "loose:0.1522"
    # ]

    config["BTagWPs"] = ["medium"]

    config["BTaggedJetAbsEtaCut"] = 2.4  # 2017 value
    config["ApplyBTagSF"] = False
    config["JetTaggerUpperCuts"] = []
    config["BTagSFMethod"] = "PromotionDemotion"
    config["BTagShift"] = 0
    config["BMistagShift"] = 0

    config["ValidTaggedJetsProducerDebug"] = False
    # Further settings taken into account by ValidBTaggedJetsProducer:
    # - Year (should be 2017), written into the 'base' config

    # Further hard-coded settings in the ValidBTaggedJetsProducer:
    # lower pt_cut for the Jet: 20 GeV -> valid for 2016 & 2017
    # upper pt_cut for the Jet: 1000 GeV -> valid for 2016 & 2017
    # parton flavour definition: hadron-based
    # b- and c- jets: combined measurement type, light jets: inclusive measurement type

    return config
