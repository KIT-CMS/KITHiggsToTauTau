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
    "pt_t", "pt_p",
    "eta_t", "eta_p",
    "phi_t", "phi_p",
    "id_p",
    "m_ll",
    "trg_singlemuon_18",
    "trg_singlemuon_20",
    "trg_singlemuon_22",
    "trg_singlemuon_22_eta",
    "trg_singlemuon_24",
    "trg_singlemuon_27",
    "trg_crossmuon_mu19tau20",
    "trg_crossmuon_mu19tau20_single",
    "trg_monitor_mu19tau32_Iso",
    "trg_monitor_mu19tau32_combinedIso",
    "metPt",
    "mt", #transverse mass of muon and met
    "againstElectronVLooseMVA6_p",
    "againstElectronLooseMVA6_p",
    "againstElectronMediumMVA6_p",
    "againstElectronTightMVA6_p",
    "againstElectronVTightMVA6_p",
    "againstMuonLoose3_p",
    "againstMuonTight3_p",
    "byIsolationMVArun2v1DBoldDMwLTraw_p",
    "byVLooseIsolationMVArun2v1DBoldDMwLT_p",
    "byLooseIsolationMVArun2v1DBoldDMwLT_p",
    "byMediumIsolationMVArun2v1DBoldDMwLT_p",
    "byTightIsolationMVArun2v1DBoldDMwLT_p",
    "byVTightIsolationMVArun2v1DBoldDMwLT_p",
    "byVVTightIsolationMVArun2v1DBoldDMwLT_p",
    "decayModeFinding_p",
    "decayMode_p",
    "isOS",
    ]

  return quantities_list
