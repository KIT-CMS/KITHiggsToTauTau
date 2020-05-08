#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

def build_list(**kwargs):
  nmssm = True if ("nmssm" in kwargs and kwargs["nmssm"]) else False
  quantities_list = [
    "muR1p0_muF1p0_weight",
    "muR1p0_muF2p0_weight",
    "muR1p0_muF0p5_weight",
    "muR2p0_muF1p0_weight",
    "muR2p0_muF2p0_weight",
    "muR2p0_muF0p5_weight",
    "muR0p5_muF1p0_weight",
    "muR0p5_muF2p0_weight",
    "muR0p5_muF0p5_weight"
  ]

  if nmssm:
    quantities_list = [ # Vary muR (renormalization scale)  and #muF (factorization scale) by 0.5 / 2.0
        "muR0p5_muF0p5_weight",  # For NMSSM muR (renormalization scale) variation makes no difference as dynamic scale is chosen - use choice variations below
        "muR0p5_muF0p5_scale_sumpt_weight",
        "muR0p5_muF0p5_scale_ht_weight",
        "muR0p5_muF0p5_scale_htover2_weight",
        "muR0p5_muF0p5_scale_sqrts_weight",
        "muR0p5_muF1p0_weight",
        "muR0p5_muF1p0_scale_sumpt_weight",
        "muR0p5_muF1p0_scale_ht_weight",
        "muR0p5_muF1p0_scale_htover2_weight",
        "muR0p5_muF1p0_scale_sqrts_weight",
        "muR0p5_muF2p0_weight",
        "muR0p5_muF2p0_scale_sumpt_weight",
        "muR0p5_muF2p0_scale_ht_weight",
        "muR0p5_muF2p0_scale_htover2_weight",
        "muR0p5_muF2p0_scale_sqrts_weight",

        "muR1p0_muF0p5_weight",
        "muR1p0_muF0p5_scale_sumpt_weight",
        "muR1p0_muF0p5_scale_ht_weight",
        "muR1p0_muF0p5_scale_htover2_weight",
        "muR1p0_muF0p5_scale_sqrts_weight",

        "muR1p0_muF1p0_scale_sumpt_weight", # Choose sum pT as dynamic scale choice
        "muR1p0_muF1p0_scale_ht_weight",  # Choose HT as dynamic scale choice
        "muR1p0_muF1p0_scale_htover2_weight",  # Choose HT/2 as dynamic scale choice
        "muR1p0_muF1p0_scale_sqrts_weight",  # Choose sqrt(s) as dynamic scale choice (default)

        "muR1p0_muF2p0_weight",
        "muR1p0_muF2p0_scale_sumpt_weight",
        "muR1p0_muF2p0_scale_ht_weight",
        "muR1p0_muF2p0_scale_htover2_weight",
        "muR1p0_muF2p0_scale_sqrts_weight",

        "muR2p0_muF0p5_weight",
        "muR2p0_muF0p5_scale_sumpt_weight",
        "muR2p0_muF0p5_scale_ht_weight",
        "muR2p0_muF0p5_scale_htover2_weight",
        "muR2p0_muF0p5_scale_sqrts_weight",
  
        "muR2p0_muF1p0_weight",
        "muR2p0_muF1p0_scale_sumpt_weight",
        "muR2p0_muF1p0_scale_ht_weight",
        "muR2p0_muF1p0_scale_htover2_weight",
        "muR2p0_muF1p0_scale_sqrts_weight",
  
        "muR2p0_muF2p0_weight",
        "muR2p0_muF2p0_scale_sumpt_weight",
        "muR2p0_muF2p0_scale_ht_weight",
        "muR2p0_muF2p0_scale_htover2_weight",
        "muR2p0_muF2p0_scale_sqrts_weight",

        "NNPDF23_lo_as_0130_qed_weight", #below are 100 individual components of the NNPDF statistical ensemble. this weight is the standard deviation of all of them, only this is written out

        # "NNPDF23_lo_as_0130_qed_0_weight",
        # "NNPDF23_lo_as_0130_qed_1_weight",
        # "NNPDF23_lo_as_0130_qed_2_weight",
        # "NNPDF23_lo_as_0130_qed_3_weight",
        # "NNPDF23_lo_as_0130_qed_4_weight",
        # "NNPDF23_lo_as_0130_qed_5_weight",
        # "NNPDF23_lo_as_0130_qed_6_weight",
        # "NNPDF23_lo_as_0130_qed_7_weight",
        # "NNPDF23_lo_as_0130_qed_8_weight",
        # "NNPDF23_lo_as_0130_qed_9_weight",
        # "NNPDF23_lo_as_0130_qed_10_weight",
        # "NNPDF23_lo_as_0130_qed_11_weight",
        # "NNPDF23_lo_as_0130_qed_12_weight",
        # "NNPDF23_lo_as_0130_qed_13_weight",
        # "NNPDF23_lo_as_0130_qed_14_weight",
        # "NNPDF23_lo_as_0130_qed_15_weight",
        # "NNPDF23_lo_as_0130_qed_16_weight",
        # "NNPDF23_lo_as_0130_qed_17_weight",
        # "NNPDF23_lo_as_0130_qed_18_weight",
        # "NNPDF23_lo_as_0130_qed_19_weight",
        # "NNPDF23_lo_as_0130_qed_20_weight",
        # "NNPDF23_lo_as_0130_qed_21_weight",
        # "NNPDF23_lo_as_0130_qed_22_weight",
        # "NNPDF23_lo_as_0130_qed_23_weight",
        # "NNPDF23_lo_as_0130_qed_24_weight",
        # "NNPDF23_lo_as_0130_qed_25_weight",
        # "NNPDF23_lo_as_0130_qed_26_weight",
        # "NNPDF23_lo_as_0130_qed_27_weight",
        # "NNPDF23_lo_as_0130_qed_28_weight",
        # "NNPDF23_lo_as_0130_qed_29_weight",
        # "NNPDF23_lo_as_0130_qed_30_weight",
        # "NNPDF23_lo_as_0130_qed_31_weight",
        # "NNPDF23_lo_as_0130_qed_32_weight",
        # "NNPDF23_lo_as_0130_qed_33_weight",
        # "NNPDF23_lo_as_0130_qed_34_weight",
        # "NNPDF23_lo_as_0130_qed_35_weight",
        # "NNPDF23_lo_as_0130_qed_36_weight",
        # "NNPDF23_lo_as_0130_qed_37_weight",
        # "NNPDF23_lo_as_0130_qed_38_weight",
        # "NNPDF23_lo_as_0130_qed_39_weight",
        # "NNPDF23_lo_as_0130_qed_40_weight",
        # "NNPDF23_lo_as_0130_qed_41_weight",
        # "NNPDF23_lo_as_0130_qed_42_weight",
        # "NNPDF23_lo_as_0130_qed_43_weight",
        # "NNPDF23_lo_as_0130_qed_44_weight",
        # "NNPDF23_lo_as_0130_qed_45_weight",
        # "NNPDF23_lo_as_0130_qed_46_weight",
        # "NNPDF23_lo_as_0130_qed_47_weight",
        # "NNPDF23_lo_as_0130_qed_48_weight",
        # "NNPDF23_lo_as_0130_qed_49_weight",
        # "NNPDF23_lo_as_0130_qed_50_weight",
        # "NNPDF23_lo_as_0130_qed_51_weight",
        # "NNPDF23_lo_as_0130_qed_52_weight",
        # "NNPDF23_lo_as_0130_qed_53_weight",
        # "NNPDF23_lo_as_0130_qed_54_weight",
        # "NNPDF23_lo_as_0130_qed_55_weight",
        # "NNPDF23_lo_as_0130_qed_56_weight",
        # "NNPDF23_lo_as_0130_qed_57_weight",
        # "NNPDF23_lo_as_0130_qed_58_weight",
        # "NNPDF23_lo_as_0130_qed_59_weight",
        # "NNPDF23_lo_as_0130_qed_60_weight",
        # "NNPDF23_lo_as_0130_qed_61_weight",
        # "NNPDF23_lo_as_0130_qed_62_weight",
        # "NNPDF23_lo_as_0130_qed_63_weight",
        # "NNPDF23_lo_as_0130_qed_64_weight",
        # "NNPDF23_lo_as_0130_qed_65_weight",
        # "NNPDF23_lo_as_0130_qed_66_weight",
        # "NNPDF23_lo_as_0130_qed_67_weight",
        # "NNPDF23_lo_as_0130_qed_68_weight",
        # "NNPDF23_lo_as_0130_qed_69_weight",
        # "NNPDF23_lo_as_0130_qed_70_weight",
        # "NNPDF23_lo_as_0130_qed_71_weight",
        # "NNPDF23_lo_as_0130_qed_72_weight",
        # "NNPDF23_lo_as_0130_qed_73_weight",
        # "NNPDF23_lo_as_0130_qed_74_weight",
        # "NNPDF23_lo_as_0130_qed_75_weight",
        # "NNPDF23_lo_as_0130_qed_76_weight",
        # "NNPDF23_lo_as_0130_qed_77_weight",
        # "NNPDF23_lo_as_0130_qed_78_weight",
        # "NNPDF23_lo_as_0130_qed_79_weight",
        # "NNPDF23_lo_as_0130_qed_80_weight",
        # "NNPDF23_lo_as_0130_qed_81_weight",
        # "NNPDF23_lo_as_0130_qed_82_weight",
        # "NNPDF23_lo_as_0130_qed_83_weight",
        # "NNPDF23_lo_as_0130_qed_84_weight",
        # "NNPDF23_lo_as_0130_qed_85_weight",
        # "NNPDF23_lo_as_0130_qed_86_weight",
        # "NNPDF23_lo_as_0130_qed_87_weight",
        # "NNPDF23_lo_as_0130_qed_88_weight",
        # "NNPDF23_lo_as_0130_qed_89_weight",
        # "NNPDF23_lo_as_0130_qed_90_weight",
        # "NNPDF23_lo_as_0130_qed_91_weight",
        # "NNPDF23_lo_as_0130_qed_92_weight",
        # "NNPDF23_lo_as_0130_qed_93_weight",
        # "NNPDF23_lo_as_0130_qed_94_weight",
        # "NNPDF23_lo_as_0130_qed_95_weight",
        # "NNPDF23_lo_as_0130_qed_96_weight",
        # "NNPDF23_lo_as_0130_qed_97_weight",
        # "NNPDF23_lo_as_0130_qed_98_weight",
        # "NNPDF23_lo_as_0130_qed_99_weight",
        # "NNPDF23_lo_as_0130_qed_100_weight",
    ]
  
  return quantities_list