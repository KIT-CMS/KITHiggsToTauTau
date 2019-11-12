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
  if year==2016:
      trigger_flags = [
       "trg_t_IsoMu22",
       "trg_p_IsoMu19Tau20",
       "trg_p_IsoMu19Tau20_singleL1",
       "trg_p_IsoMu19Tau20_crossL1",
       "isAntiL1TauMatched_trg_p_IsoMu19Tau20",
       "isAntiL1TauMatched_trg_p_IsoMu19Tau20_singleL1",
       "isAntiL1TauMatched_trg_p_IsoMu19Tau20_crossL1" 
       ]
  else:
      trigger_flags = [
    "trg_t_IsoMu24",
    "trg_p_mu20tau27",
    "trg_p_mu24tau20",
    "isAntiL1TauMatched_trg_p_mu20tau27",
          ]   
  quantities_list = trigger_flags + [
    "run",
    "lumi",
    "evt",
   # "m_vis",
    
    "pt_t", "pt_p",
    "eta_t", "eta_p",
    "phi_t", "phi_p",
    "iso_t", "iso_p",
    "id_t",
    "id_p",
    "m_ll"
    ]

  return quantities_list
