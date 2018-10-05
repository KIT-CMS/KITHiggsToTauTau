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
    "trg_t_Ele27",
    "trg_p_Ele27",
    "trg_t_Ele32",
    "trg_p_Ele32",
    "trg_t_Ele35",
    "trg_p_Ele35",
    "pt_t", "pt_p",
    "eta_t", "eta_p",
    "phi_t", "phi_p",
    "iso_t", "iso_p",
    "id_t",
    "id_p",
    "m_ll"
    ]

  return quantities_list
