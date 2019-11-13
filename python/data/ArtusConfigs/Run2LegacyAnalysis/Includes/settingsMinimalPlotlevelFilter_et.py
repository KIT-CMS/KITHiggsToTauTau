#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
#import os

def build_config(nickname, **kwargs):
  etau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "etau-fake-es" else False
  tau_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "tau-es" else False

  config = jsonTools.JsonDict()
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  config["PlotlevelFilterExpressionQuantities"] = [
    "flagMETFilter",
    "byTightDeepTau2017v2p1VSe_2",
    "byVLooseDeepTau2017v2p1VSmu_2",
    "byVVVLooseDeepTau2017v2p1VSjet_2",
  ]
  config["PlotlevelFilterExpression"] = "(flagMETFilter > 0.5)*(byVLooseDeepTau2017v2p1VSmu_2 > 0.5)*(byTightDeepTau2017v2p1VSe_2 > 0.5)*(byVVVLooseDeepTau2017v2p1VSjet_2 > 0.5)"

  if not etau_fake_es and not tau_es:
    config["PlotlevelFilterExpressionQuantities"].append('nDiElectronVetoPairsOS')
    config["PlotlevelFilterExpression"] += '*(nDiElectronVetoPairsOS < 0.5)'

    config["PlotlevelFilterExpressionQuantities"].append("extraelec_veto")
    config["PlotlevelFilterExpression"] += '*(extraelec_veto < 0.5)'

    config["PlotlevelFilterExpressionQuantities"].append("extramuon_veto")
    config["PlotlevelFilterExpression"] += '*(extramuon_veto < 0.5)'
  else:
    pass
    # Should not be used with data-driven bg estimation techniques !
    # config["PlotlevelFilterExpressionQuantities"].append('nojets')
    # config["PlotlevelFilterExpression"] += '*(njets == 0)'
    # config["PlotlevelFilterExpressionQuantities"].append('byLooseIsolationMVArun2017v2DBoldDMwLT2017_2')
    # config["PlotlevelFilterExpression"] += '*(byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)'

  return config
