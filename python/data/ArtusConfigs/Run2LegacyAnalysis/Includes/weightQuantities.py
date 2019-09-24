#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


def build_list(**kwargs):
    minimal_setup = True if "minimal_setup" in kwargs and kwargs["minimal_setup"] else False

    # quantities that are needed to run the analysis
    quantities = [
        "singleTriggerMCEfficiencyWeightKIT_1",
        "singleTriggerDataEfficiencyWeightKIT_1",
        "singleTriggerMCEfficiencyWeightKIT_2",
        "singleTriggerDataEfficiencyWeightKIT_2",

        "eleRecoWeight_1",
        "idWeight_1",
        "isoWeight_1",
        "idWeight_2",
        "isoWeight_2",
        
        "muonEffTrgWeight",
        "muonEffIDWeight_1",
        "muonEffIDWeight_2",
    ]

    if kwargs["isMC"]:
        quantities.extend([
            "prefiringweight",
            "prefiringweightup",
            "prefiringweightdown"
        ])

    if not minimal_setup:
        quantities.extend([
            "ggA_b_weight",
            "ggA_i_weight",
            "ggA_t_weight",
            "ggH_b_weight",
            "ggH_i_weight",
            "ggH_t_weight",
            "ggh_b_weight",  # note the small h
            "ggh_i_weight",  # note the small h
            "ggh_t_weight",  # note the small h
            "idWeight_1",
            "idWeight_2",
            "idisoweight_1",
            "idisoweight_2",
            "isoWeight_1",
            "isoWeight_2",
            "ptWeightedDetaStrip_1",
            "ptWeightedDetaStrip_2",
            "ptWeightedDphiStrip_1",
            "ptWeightedDphiStrip_2",
            "ptWeightedDrIsolation_1",
            "ptWeightedDrIsolation_2",
            "ptWeightedDrSignal_1",
            "ptWeightedDrSignal_2",
            "singleTriggerDataEfficiencyWeightIC_1",
            "singleTriggerDataEfficiencyWeightKIT_1",
            "singleTriggerDataEfficiencyWeightKIT_2",
            "singleTriggerDataEfficiencyWeight_1",
            "singleTriggerDataEfficiencyWeight_2",
            "singleTriggerEmbeddedEfficiencyWeightIC_1",
            "singleTriggerEmbeddedEfficiencyWeightKIT_1",
            "singleTriggerEmbeddedEfficiencyWeight_1",
            "singleTriggerMCEfficiencyWeightIC_1",
            "singleTriggerMCEfficiencyWeightKIT_1",
            "singleTriggerMCEfficiencyWeightKIT_2",
            "singleTriggerMCEfficiencyWeight_1",
            "singleTriggerMCEfficiencyWeight_2",
            "trackWeight_1",
            "trackWeight_2",
            "trigweight_1",
            "trigweight_2",
        ])

    return list(set(quantities))
