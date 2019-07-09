#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import os
import copy
import importlib

import HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.ArtusConfigUtility as ACU


def build_config(nickname, nominal_config, channel, **kwargs):

    btag_eff_unwanted = ["KappaLambdaNtupleConsumer", "CutFlowTreeConsumer", "KappaElectronsConsumer", "KappaTausConsumer", "KappaTaggedJetsConsumer", "RunTimeConsumer", "PrintEventsConsumer"]
    for unwanted in btag_eff_unwanted:
        if unwanted in nominal_config["Consumers"]:
            nominal_config["Consumers"].remove(unwanted)

    nominal_config["Consumers"].append("BTagEffConsumer")

    btag_conf = {}
    return_conf = jsonTools.JsonDict()
    for bwp in kwargs["btager_wp"]:
        conf_name = kwargs["btager"] + '_' + bwp
        btag_conf[conf_name] = copy.deepcopy(nominal_config)
        btag_conf[conf_name].update(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsBTaggedJetID").build_config(nickname, **{"btager":kwargs["btager"], "btager_wp":bwp}))
        log.debug(nominal_config["BTagWPs"][0] + ' -> ' + btag_conf[conf_name]["BTagWPs"][0])

        log.info('Add pipeline: %s' % (conf_name))
        pipe = ACU.apply_uncertainty_shift_configs(channel, btag_conf[conf_name], importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.nominal").build_config(nickname, **kwargs))
        newname = pipe.keys()[0] + '_' + conf_name
        log.info('rename pipeline %s -> %s' % (pipe.keys()[0], newname))
        pipe[newname] = pipe.pop(pipe.keys()[0])
        return_conf += pipe

    return return_conf
