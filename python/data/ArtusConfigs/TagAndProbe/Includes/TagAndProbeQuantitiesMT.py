#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

def build_list(year):
  # Trigger decisions
  if year == 2016:
      trigger_flags = [
          "trg_singlemuon_24",
          "trg_singlemuon_27",
          "trg_crossmuon_mu19tau20_singlel1",
          "trg_crossmuon_mu19tau20",
          "trg_monitor_mu19tau30",
          "trg_monitor_mu19tau35_mediso",
          "trg_monitor_mu19tau35_medcombiso",
          "trg_singletau_leading",
          "trg_singletau_trailing",
      ]
  elif year == 2017:
      trigger_flags = [
          "trg_singlemuon_27",
          "trg_crossmuon_mu20tau27",
          "trg_monitor_mu20tau27",
          "trg_monitor_mu24tau40_mediso_tightid",
          "trg_monitor_mu24tau40_tightiso",
          "trg_monitor_mu24tau35_tightiso_tightid",
          "trg_singletau_leading",
          "trg_singletau_trailing",
      ]
  elif year == 2018:
      trigger_flags = [
          "trg_singlemuon_27",
          "trg_crossmuon_mu20tau27_hps",
          "trg_crossmuon_mu20tau27",
          "trg_monitor_mu20tau27_hps",
          "trg_monitor_mu20tau27",
          "trg_monitor_mu24tau35_mediso_hps",
          "trg_monitor_mu24tau35_mediso",
          "trg_monitor_mu24tau40_mediso_tightid_hps",
          "trg_monitor_mu24tau40_mediso_tightid",
          "trg_monitor_mu24tau40_tightiso_hps",
          "trg_monitor_mu24tau40_tightiso",
          "trg_monitor_mu24tau35_tightiso_tightid_hps",
          "trg_monitor_mu24tau35_tightiso_tightid",
          "trg_monitor_mu27tau20_hps",
          "trg_monitor_mu27tau20",
          "trg_singletau_leading",
          "trg_singletau_trailing",
      ]

  quantities_list = trigger_flags + [
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
        "decayModeFinding_p",
        "decayMode_p",
        "gen_match_p",
        "trkpt_p", # pT of the leading charged hadron track of the tau
        # Event quantities
        "m_ll",
        "metPt",
        "isOS",
        # Weights
        "puWeight",
        "bkgSubWeight"
  ]

  return quantities_list
