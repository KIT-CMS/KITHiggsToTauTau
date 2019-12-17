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
    "THU_qqH_TOT",
    "THU_qqH_PTH200",
    "THU_qqH_Mjj60",
    "THU_qqH_Mjj120",
    "THU_qqH_Mjj350",
    "THU_qqH_Mjj700",
    "THU_qqH_Mjj1000",
    "THU_qqH_Mjj1500",
    "THU_qqH_25",
    "THU_qqH_JET01"
  ]
  
  return quantities_list