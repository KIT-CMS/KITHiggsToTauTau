#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

import re
import os
import importlib


def fshift_dict(shift=None, dm=None):
    if shift is None or dm is None:
        print "fshift_dict received wrong parameters"
        exit(1)
    config = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.nominal").build_config(nickname="pass")["nominal"]
    config[dm] = 1 + shift / 100.
    return config


def build_config(nickname, **kwargs):
    """Produce shifts for e->tau FR ES measurements"""
    log.debug("Produce shifts for e->tau FR ES measurements")
    etau_fake_es_group = kwargs["etau_fake_es_group"] if "etau_fake_es_group" in kwargs else None
    etau_fake_es_shifts = kwargs["etau_fake_es_shifts"] if "etau_fake_es_shifts" in kwargs else None

    etau_es_shifts_groups = [
        [-4, -3, -2, -1.75, -1.5, -1.25, -1, -0.75, -0.5, -0.25],
        [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5],
        [2.75, 3, 3.25, 3.5, 3.75, 4, 5, 6, 7, 8],
        [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        [0],
        [-4, -0.5, 0.5, 18],
    ]
    if isinstance(etau_fake_es_group, int) and abs(etau_fake_es_group) < len(etau_es_shifts_groups):
        etau_es_shifts = etau_es_shifts_groups[etau_fake_es_group]
        print "FES:", etau_es_shifts
    elif etau_fake_es_shifts is None:
        print "FES shifts not properly specified -> skipping. etau_fake_es_group :", etau_fake_es_group
        return
    else:
        etau_es_shifts = etau_fake_es_shifts


    config = jsonTools.JsonDict()
    datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

    # define frequently used conditions
    # isEmbedded = datasetsHelper.isEmbedded(nickname)
    isDY = re.search("DY.?JetsToLLM", nickname)
    isEWKZ2Jets = re.search("EWKZ2Jets", nickname)

    # Pipelines for producing shapes for calculating the TauElectronFakeEnergyCorrection*
    if isDY or isEWKZ2Jets:

        root_str = lambda x: str(x).replace("-", "neg").replace(".", "p")

        for es in etau_es_shifts:
            config["eleTauEsInclusiveShift_" + root_str(es)] = fshift_dict(es, "TauElectronFakeEnergyCorrectionShift")
            config["eleTauEsOneProngShift_" + root_str(es)] = fshift_dict(es, "TauElectronFakeEnergyCorrectionOneProngShift")
            config["eleTauEsOneProngPiZerosShift_" + root_str(es)] = fshift_dict(es, "TauElectronFakeEnergyCorrectionOneProngPiZerosShift")
            # config["eleTauEsThreeProngShift_" + root_str(es)] = fshift_dict(es, "TauElectronFakeEnergyCorrectionThreeProngShift")

    return config
