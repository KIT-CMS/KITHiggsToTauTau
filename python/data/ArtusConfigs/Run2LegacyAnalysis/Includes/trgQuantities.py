#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


def build_list(**kwargs):
    minimal_setup = True if "minimal_setup" in kwargs and kwargs["minimal_setup"] else False
    year = kwargs["year"]

    # triggers flags that are needed to run the analysis
    quantities = []
    if year == 2016:
        quantities = [
            "trg_singleelectron",
            "trg_singlemuon",
            "trg_singletau_leading",

            "trg_mutaucross",
             "trg_eletaucross",
            "trg_doubletau",
            "trg_muonelectron_mu23ele12",
            "trg_muonelectron_mu8ele23",

            "trg_singletau_trailing",
        ]
    elif year == 2017:
        quantities = [
             "trg_singlemuon_24",
             "trg_singlemuon_27",
             "trg_singletau_leading",
             "trg_singleelectron_27",
             "trg_singleelectron_32",
             "trg_singleelectron_32_fallback",
             "trg_singleelectron_35",

             "trg_crossmuon_mu20tau27",
             "trg_crossele_ele24tau30",
             "trg_doubletau_35_tightiso_tightid",
             "trg_doubletau_40_mediso_tightid",
             "trg_doubletau_40_tightiso",
             "trg_muonelectron_mu12ele23",
             "trg_muonelectron_mu23ele12",
             "trg_muonelectron_mu8ele23",

             "trg_singletau_trailing",
        ]
    elif year == 2018:
        quantities = [
            "trg_singlemuon_24",
            "trg_singlemuon_27",
            "trg_singletau_leading",
            "trg_singleelectron_27",
            "trg_singleelectron_32",
            "trg_singleelectron_32_fallback",
            "trg_singleelectron_35",

            "trg_crossmuon_mu20tau27",
            "trg_crossmuon_mu20tau27_hps",
            "trg_crossele_ele24tau30",
            "trg_crossele_ele24tau30_hps",
            "trg_doubletau_35_tightiso_tightid",
            "trg_doubletau_40_mediso_tightid",
            "trg_doubletau_40_tightiso",
            "trg_doubletau_35_mediso_hps",
            "trg_muonelectron_mu12ele23",
            "trg_muonelectron_mu23ele12",
            "trg_muonelectron_mu8ele23",

            "trg_singletau_trailing",
        ]

    return list(set(quantities))
