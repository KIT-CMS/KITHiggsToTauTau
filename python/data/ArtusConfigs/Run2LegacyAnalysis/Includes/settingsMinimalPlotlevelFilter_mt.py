#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.Utility.jsonTools as jsonTools


def build_config(nickname, **kwargs):
    tau_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "tau-es" else False
    mtau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "mtau-fake-es" else False
    tau_es_method = kwargs["tau_es_method"] if "tau_es_method" in kwargs else 'classical'  # classical, gamma

    config = jsonTools.JsonDict()
    # datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

    config["PlotlevelFilterExpressionQuantities"] = [
        "flagMETFilter",
        "byVVLooseDeepTau2017v2p1VSe_2",
        "byLooseDeepTau2017v2p1VSmu_2",
        "byVVVLooseDeepTau2017v2p1VSjet_2",
    ]
    config["PlotlevelFilterExpression"] = "(flagMETFilter > 0.5)*(byLooseDeepTau2017v2p1VSmu_2 > 0.5)*(byVVLooseDeepTau2017v2p1VSe_2 > 0.5)*(byVVVLooseDeepTau2017v2p1VSjet_2 > 0.5)"

    # as for the TES version of 2016
    if not tau_es and not mtau_fake_es:
        config["PlotlevelFilterExpressionQuantities"].append('nDiMuonVetoPairsOS')
        config["PlotlevelFilterExpression"] += '*(nDiMuonVetoPairsOS < 0.5)'

        config["PlotlevelFilterExpressionQuantities"].append("extramuon_veto")
        config["PlotlevelFilterExpression"] += '*(extramuon_veto < 0.5)'

        config["PlotlevelFilterExpressionQuantities"].append("extraelec_veto")
        config["PlotlevelFilterExpression"] += '*(extraelec_veto < 0.5)'

    elif tau_es and not mtau_fake_es:
        # version consistent with Izaak for 2017
        config["PlotlevelFilterExpressionQuantities"].append('nDiMuonVetoPairsOS')
        config["PlotlevelFilterExpression"] += '*(nDiMuonVetoPairsOS < 0.5)'

        # version for 2018 reprocessing
        config["PlotlevelFilterExpressionQuantities"].append("extramuon_veto")
        config["PlotlevelFilterExpression"] += '*(extramuon_veto < 0.5)'

        if tau_es_method == 'gamma':
            config["PlotlevelFilterExpressionQuantities"].append("decayMode_2")
            config["PlotlevelFilterExpression"] += '*(decayMode_2 > 0)*(decayMode_2 < 2)'  # selecting only DM1

    elif not tau_es and mtau_fake_es:
        pass

    return config
