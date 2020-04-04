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
    "weight",
    "hltWeight",
    "triggerWeight_1",
    "triggerWeight_2",
    "idWeight_1",
    "idWeight_2",
    "isoWeight_1",
    "isoWeight_2",
    "identificationWeight_1",
    "identificationWeight_2",
    "puWeight",
    'puweight',   # note the small w
    "tauEnergyScaleWeight",
    "generatorWeight",
    "crossSectionPerEventWeight",
    "numberGeneratedEventsWeight",
    "embeddingWeight",
    "eventWeight",
    "sampleStitchingWeight",
    "antiEVLooseSFWeight_1",
    "antiELooseSFWeight_1",
    "antiEMediumSFWeight_1",
    "antiETightSFWeight_1",
    "antiEVTightSFWeight_1",
    "antiEVLooseSFWeight_2",
    "antiELooseSFWeight_2",
    "antiEMediumSFWeight_2",
    "antiETightSFWeight_2",
    "antiEVTightSFWeight_2",
    "emuQcdWeightUp",
    "emuQcdWeightNom",
    "emuQcdWeightDown",
    "topPtReweightWeight",
    "topPtReweightWeightRun1",
    "topPtReweightWeightRun2",
    "topPtReweightWeightTTH",
    "zPtReweightWeight",
    "eleTauFakeRateWeight",
    "muTauFakeRateWeight"
  ]

  return quantities_list
