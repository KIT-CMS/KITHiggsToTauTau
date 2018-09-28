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
    "m_vis",
    "trg_1_IsoMu27",
    "trg_2_IsoMu27",
    "trg_1_IsoMu24",
    "trg_2_IsoMu24",
    "pt_1", "pt_2",
    "eta_1", "eta_2",
    "phi_1", "phi_2",
    "iso_1", "iso_2",
    "id_muon_medium_1",
    "id_muon_tight_1",
    "id_muon_medium_2",
    "id_muon_tight_2",
    "m_ll"
    ]

  return quantities_list
