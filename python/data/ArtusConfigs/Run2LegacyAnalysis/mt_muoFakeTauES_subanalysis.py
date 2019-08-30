#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

import re
import importlib


def fshift_dict(shift=None, dm=None):
    if shift is None or dm is None:
        print "fshift_dict received wrong parameters"
        exit(1)
    config = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.nominal").build_config(nickname="pass")["nominal"]
    config[dm] = 1 + shift / 100.
    return config


def build_config(nickname, **kwargs):
    """Produce shifts for m->tau FR ES measurements"""
    log.debug("Produce shifts for m->tau FR ES measurements")
    mtau_fake_es_shifts = kwargs["mtau_fake_es_shifts"] if "mtau_fake_es_shifts" in kwargs else None

    if mtau_fake_es_shifts is None:
        log.warning("m->tau FES shifts not properly specified -> skipping.")
        return

    config = jsonTools.JsonDict()

    isDY = re.search("DY.?JetsToLLM", nickname)
    isEWKZ2Jets = re.search("EWKZ2Jets", nickname)

    # Pipelines for producing shapes for calculating the TauMuonFakeEnergyCorrection*
    if isDY or isEWKZ2Jets:

        root_str = lambda x: str(x).replace("-", "neg").replace(".", "p")

        for es in mtau_fake_es_shifts:
            config["muoTauEsInclusiveShift_" + root_str(es)] = fshift_dict(es, "TauMuonFakeEnergyCorrectionShift")
            config["muoTauEsOneProngShift_" + root_str(es)] = fshift_dict(es, "TauMuonFakeEnergyCorrectionOneProngShift")
            config["muoTauEsOneProngPiZerosShift_" + root_str(es)] = fshift_dict(es, "TauMuonFakeEnergyCorrectionOneProngPiZerosShift")
            # config["muoTauEsThreeProngShift_" + root_str(es)] = fshift_dict(es, "TauMuonFakeEnergyCorrectionThreeProngShift")

    return config
