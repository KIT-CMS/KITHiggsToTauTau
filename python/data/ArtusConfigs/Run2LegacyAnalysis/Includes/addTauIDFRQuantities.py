#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools

def build_list():
    quantities_list = [
        "pt_tau",
        "eta_tau",
        "mass_tau",
        "decayMode_tau",
        "gen_match_tau",
        "byCombinedIsolationDeltaBetaCorrRaw3Hits_tau",
        "byLooseCombinedIsolationDeltaBetaCorr3Hits_tau",
        "byMediumCombinedIsolationDeltaBetaCorr3Hits_tau",
        "byTightCombinedIsolationDeltaBetaCorr3Hits_tau",
        "againstElectronLooseMVA6_tau",
        "againstElectronMediumMVA6_tau",
        "againstElectronTightMVA6_tau",
        "againstElectronVLooseMVA6_tau",
        "againstElectronVTightMVA6_tau",
        "againstMuonLoose3_tau",
        "againstMuonTight3_tau",
        "byIsolationMVArun2v1DBoldDMwLTraw_tau",
        "byVLooseIsolationMVArun2v1DBoldDMwLT_tau",
        "byLooseIsolationMVArun2v1DBoldDMwLT_tau",
        "byMediumIsolationMVArun2v1DBoldDMwLT_tau",
        "byTightIsolationMVArun2v1DBoldDMwLT_tau",
        "byVTightIsolationMVArun2v1DBoldDMwLT_tau",
        "byVVTightIsolationMVArun2v1DBoldDMwLT_tau",
        "byIsolationMVArun2017v2DBoldDMwLTraw2017_tau",
        "byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_tau",
        "byVLooseIsolationMVArun2017v2DBoldDMwLT2017_tau",
        "byLooseIsolationMVArun2017v2DBoldDMwLT2017_tau",
        "byMediumIsolationMVArun2017v2DBoldDMwLT2017_tau",
        "byTightIsolationMVArun2017v2DBoldDMwLT2017_tau",
        "byVTightIsolationMVArun2017v2DBoldDMwLT2017_tau",
        "byVVTightIsolationMVArun2017v2DBoldDMwLT2017_tau",
        "byIsolationMVArun2017v1DBoldDMwLTraw2017_tau",
        "byVVLooseIsolationMVArun2017v1DBoldDMwLT2017_tau",
        "byVLooseIsolationMVArun2017v1DBoldDMwLT2017_tau",
        "byLooseIsolationMVArun2017v1DBoldDMwLT2017_tau",
        "byMediumIsolationMVArun2017v1DBoldDMwLT2017_tau",
        "byTightIsolationMVArun2017v1DBoldDMwLT2017_tau",
        "byVTightIsolationMVArun2017v1DBoldDMwLT2017_tau",
        "byVVTightIsolationMVArun2017v1DBoldDMwLT2017_tau",
        "chargedIsoPtSum_tau",
        "decayModeFinding_tau",
        "decayModeFindingNewDMs_tau",
        "neutralIsoPtSum_tau",
        "puCorrPtSum_tau",
        "footprintCorrection_tau",
        "photonPtSumOutsideSignalCone_tau",
        "decayDistX_tau",
        "decayDistY_tau",
        "decayDistZ_tau",
        "decayDistM_tau",
        "nPhoton_tau",
        "ptWeightedDetaStrip_tau",
        "ptWeightedDphiStrip_tau",
        "ptWeightedDrSignal_tau",
        "ptWeightedDrIsolation_tau",
        "leadingTrackChi2_tau",
        "eRatio_tau",
        ]
    return quantities_list
