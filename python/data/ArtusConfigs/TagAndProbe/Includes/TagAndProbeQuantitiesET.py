#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

def build_list():
  quantities_list = [
    "run",
    "lumi",
    "evt",
    # "m_vis",
    # Tag (muon) related quantities
    "pt_t", "pt_p",
    "eta_t", "eta_p",
    "phi_t", "phi_p",
    "iso_t", "mt_t", #transverse mass of muon and met
    "id_t",
    # Probe (tau) related quantities
    "againstElectronVLooseMVA6_p",
    "againstElectronLooseMVA6_p",
    "againstElectronMediumMVA6_p",
    "againstElectronTightMVA6_p",
    "againstElectronVTightMVA6_p",
    "againstMuonLoose3_p",
    "againstMuonTight3_p",
    "byIsolationMVArun2017v2DBoldDMwLTraw2017_p",
    "byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_p",
    "byVLooseIsolationMVArun2017v2DBoldDMwLT2017_p",
    "byLooseIsolationMVArun2017v2DBoldDMwLT2017_p",
    "byMediumIsolationMVArun2017v2DBoldDMwLT2017_p",
    "byTightIsolationMVArun2017v2DBoldDMwLT2017_p",
    "byVTightIsolationMVArun2017v2DBoldDMwLT2017_p",
    "byVVTightIsolationMVArun2017v2DBoldDMwLT2017_p",
    "byIsolationMVArun2017v1DBoldDMwLTraw2017_p",
    "byVVLooseIsolationMVArun2017v1DBoldDMwLT2017_p",
    "byVLooseIsolationMVArun2017v1DBoldDMwLT2017_p",
    "byLooseIsolationMVArun2017v1DBoldDMwLT2017_p",
    "byMediumIsolationMVArun2017v1DBoldDMwLT2017_p",
    "byTightIsolationMVArun2017v1DBoldDMwLT2017_p",
    "byVTightIsolationMVArun2017v1DBoldDMwLT2017_p",
    "byVVTightIsolationMVArun2017v1DBoldDMwLT2017_p",

    "byDeepTau2017v2p1VSjetraw",
    "byVVVLooseDeepTau2017v2p1VSjet_p",
    "byVVLooseDeepTau2017v2p1VSjet_p",
    "byVLooseDeepTau2017v2p1VSjet_p",
    "byLooseDeepTau2017v2p1VSjet_p",
    "byMediumDeepTau2017v2p1VSjet_p",
    "byTightDeepTau2017v2p1VSjet_p",
    "byVTightDeepTau2017v2p1VSjet_p",
    "byVVTightDeepTau2017v2p1VSjet_p",
    "byDeepTau2017v2p1VSeraw",
    "byVVVLooseDeepTau2017v2p1VSe_p",
    "byVVLooseDeepTau2017v2p1VSe_p",
    "byVLooseDeepTau2017v2p1VSe_p",
    "byLooseDeepTau2017v2p1VSe_p",
    "byMediumDeepTau2017v2p1VSe_p",
    "byTightDeepTau2017v2p1VSe_p",
    "byVTightDeepTau2017v2p1VSe_p",
    "byVVTightDeepTau2017v2p1VSe_p",
    "byDeepTau2017v2p1VSmuraw",
    "byVLooseDeepTau2017v2p1VSmu_p",
    "byLooseDeepTau2017v2p1VSmu_p",
    "byMediumDeepTau2017v2p1VSmu_p",
    "byTightDeepTau2017v2p1VSmu_p",

    "decayModeFinding_p",
    "decayModeFindingNewDMs_p",
    "decayMode_p",
    "gen_match_p",
    "trkpt_p", # pT of the leading charged hadron track of the tau
    # Event quantities
    "m_ll",
    "metPt",
    "isOS",
    # Trigger decisions
    "trg_singleelectron_35",
    "trg_crosselectron_ele24tau30",
    "trg_crosselectron_ele24tau30_hps",
    # Weights
    "puWeight",
    "bkgSubWeight"
    ]

  return quantities_list
