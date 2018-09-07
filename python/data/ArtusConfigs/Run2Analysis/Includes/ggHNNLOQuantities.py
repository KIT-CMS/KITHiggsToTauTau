#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

def build_list():
  quantities_list = [
    "ggh_NNLO_weight",
    "THU_ggH_Mu",
    "THU_ggH_Res",
    "THU_ggH_Mig01",
    "THU_ggH_Mig12",
    "THU_ggH_VBF2j",
    "THU_ggH_VBF3j",
    "THU_ggH_PT60",
    "THU_ggH_PT120",
    "THU_ggH_qmtop"
  ]
  
  return quantities_list