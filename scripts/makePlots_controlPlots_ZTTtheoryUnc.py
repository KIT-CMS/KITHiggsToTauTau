#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys
import pprint
import ROOT
import glob

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
from Artus.Utility.tools import make_multiplication, clean_multiplication

def merge(config_list):
	for i in range(len(config_list) - 1):
			config_list[0] = sample_settings.merge_configs(config_list[0], config_list[i + 1])

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs=1,
	                    default=["ztt"],
	                    choices=["ztt", "zttpospol", "zttnegpol", "zll", "zl", "zj", "ttj", "ttjt", "ttt", "ttjj", "ttjl", "vv", "vvt", "vvl", "wj", "wjt", "wjl", "qcd", "ewk", "ff", "ggh", "qqh", "bbh", "vh", "htt", "data"],
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--stack-signal", default=False, action="store_true",
	                    help="Draw signal (htt) stacked on top of each backgrounds. [Default: %(default)s]")
	parser.add_argument("--scale-signal", type=int, default=1,
	                    help="Scale signal (htt). Allowed values are 1, 10, 25, 100 and 250. [Default: %(default)s]")
	parser.add_argument("--sbratio", default=False, action="store_true",
	                    help="Add s/sqrt(b) subplot [Default: %(default)s]")
	parser.add_argument("--blinding-threshold", default=0, type=float,
	                    help="Threshold above of s/sqrt(b) above which data is being blinded [Default: %(default)s]")
	parser.add_argument("--ztt-from-mc", default=False, action="store_true",
	                    help="Use MC simulation to estimate ZTT. [Default: %(default)s]")
	parser.add_argument("--blinding-methods", default=["soversqrtb"], nargs="*",
	                    help="Blinding Method. Chose soversqrtb or ams. [Default: %(default)s]")
	parser.add_argument("--blinding-parameter", default=0.0, type=float,
	                    help="b_reg. [Default: %(default)s]")
	parser.add_argument("--blinding-variables", default=["all"], nargs="*",
	                    help="Variables to blind. [Default: %(default)s]")
	parser.add_argument("--integrated-sob", default=False, action="store_true",
	                    help="Add integrated s/sqrt(b) subplot [Default: %(default)s]")
	parser.add_argument("--integration-methods", default="soversqrtb", choices = ["soversqrtb", "soversplusb", "soversqrtsplusb"],
	                    help="Integration Method. [Default: %(default)s]")
	parser.add_argument("--integration-directions", default=["righttoleft", "righttoleft"], nargs="*",
	                    help="Integration direction. Chose lefttoright or righttoleft, !!!combination needs to be specified last!!!. [Default: %(default)s]")
	parser.add_argument("--integration-output", default=None,
						help="outputfile to specifiy where to write calculated maxima/minima, None is no output [Default:%(default)s]")
	parser.add_argument("--integration-nicks",nargs="+", default=["htt"],
						help="integration signal nicks [Default:%(default)s]")
	parser.add_argument("--integration-backgrounds", nargs="+", default=["all"],
						help="integration background nicks [Default:%(default)s]")
	parser.add_argument("--full-integral", action="store_true",
						help="calculate full integral of all histograms and write to file")
	parser.add_argument("-ff", "--fakefactor-method", choices = ["standard", "comparison"],
			help="Optional background estimation using the Fake-Factor method. [Default: %(default)s]")
	parser.add_argument("--scale-mc-only", default="1.0",
                        help="scales only MC events. [Default: %(default)s]")
	parser.add_argument("--cut-mc-only", default="1.0",
                        help="cut applied only on MC. [Default: %(default)s]")
	parser.add_argument("--project-to-lumi", default=1.0,
                        help="multiplies current lumi. 2 would mean double lumi you have right now [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
	                    default=["tt", "mt", "et", "em", "mm"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="*",
	                    default=["integral",
	                             "pt_1", "eta_1", "phi_1", "m_1", "iso_1", "mt_1",
	                             "pt_2", "eta_2", "phi_2", "m_2", "iso_2", "mt_2",
	                             "pt_sv", "eta_sv", "phi_sv", "m_sv", "m_vis", "ptvis",
	                             "met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
	                             "mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
	                             "pZetaMissVis", "pzetamiss", "pzetavis",
	                             "jpt_1", "jeta_1", "jphi_1",
	                             "jpt_2", "jeta_2", "jphi_2",
	                             "njetspt30", "mjj", "jdeta", "njetingap20", "njetingap",
	                             "trigweight_1", "trigweight_2", "puweight",
	                             "npv", "npu", "rho"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-j", "--json-dir", default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/",
	                    help="Base directory for optional JSON configs. [Default: %(default)s]")
	parser.add_argument("--run1", default=False, action="store_true",
	                    help="Use Run1 samples. [Default: %(default)s]")
	parser.add_argument("--embedding-selection", default=False, action="store_true",
	                    help="Use samples to consider selection for embedding. [Default: %(default)s]")
	parser.add_argument("--cms", default=False, action="store_true",
	                    help="CMS Preliminary lable. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("--controlregions", action="store_true", default=False,
	                    help="Also create histograms for control regions. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--qcd-subtract-shapes", action="store_false", default=True, help="subtract shapes for QCD estimation [Default:%(default)s]")
	parser.add_argument("-b", "--background-method", default=["classic"], nargs="+",
	                    help="Background estimation method to be used, channel dependent. [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--mva", default=False, action="store_true",
	                    help="Produce plots for the mva studies. [Default: %(default)s]")
	parser.add_argument("--polarisation", default=False, action="store_true",
	                    help="Produce the plots for the polarisation analysis. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
	parser.add_argument("--era", default="2015",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("--shapes", default=False, action="store_true",
	                    help="Show shape comparisons. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/control_plots/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="control_plots",
	                    help="Publish plots. [Default: %(default)s]")
	parser.add_argument("--emb", default=False, action="store_true",
	                    help="Use embedded samples. [Default: %(default)s]")
	parser.add_argument("--pdfkey", default="", help="PDF set  KEY Name [Default: %(default)s]")# Htt : NNPDF30
	parser.add_argument("--addpdfs", default=[], help="PDF set Name [Default: %(default)s]")# NNPDF30_nlo_as_0119_weight NNPDF30_nlo_as_0118_00_weight NNPDF30_nlo_as_0117_weight
	
	args = parser.parse_args()
	logger.initLogger(args)

	lheweights_names = []
	pdfkey = args.pdfkey
	addpdfs = args.addpdfs
	if args.samples[0] == "ztt":
		pdfkey = "NNPDF30_lo_as_0130"
		addpdfs = ["NNPDF30_lo_as_0118_0_weight"]
	elif args.samples[0] == "htt":
		pdfkey = "NNPDF30_nlo_as_0118"
		addpdfs = ["NNPDF30_nlo_as_0119_weight", "NNPDF30_nlo_as_0117_weight"]

	if args.run1:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run1 as samples
	elif args.embedding_selection:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_embedding_selection as samples
	else:
		if (args.era == "2015") or (args.era == "2015new"):
			import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
		elif args.era == "2016":
			import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
			if args.lumi == parser.get_default("lumi"):
				args.lumi = samples.default_lumi/1000.0
		else:
			log.critical("Invalid era string selected: " + args.era)
			sys.exit(1)

	if args.fakefactor_method is not None:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_ff as samples

	if args.shapes: args.ratio = False

	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Samples, sample)]

	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	print "list_of_samples", list_of_samples
	if args.emb:
		if args.run1:
			log.critical("Embedding --emb only valid for run2. Remove --emb or select run2 samples.")
			sys.exit(1)
		sample_settings = samples.Samples(embedding=True)
	else: 
		sample_settings = samples.Samples()

	if args.mssm:
		bkg_samples = [sample for sample in args.samples if sample not in ["data", "htt", "ggh", "bbh"]]
		sig_samples_raw = [sample for sample in args.samples if sample in ["htt", "ggh", "bbh"]]
	else:
		bkg_samples = [sample for sample in args.samples if sample not in ["data", "htt", "ggh", "qqh", "vh"]]
		sig_samples_raw = [sample for sample in args.samples if sample in ["htt", "ggh", "qqh", "vh"]]
	sig_samples = []
	for mass in args.higgs_masses:
		scale_str = "_%i"%args.scale_signal
		if int(args.scale_signal) == 1: scale_str = ""
		for sample in sig_samples_raw:
			sig_samples.append(sample + "%s%s"%(mass, scale_str))


	log.debug("used bkg + signal nicks")
	log.debug(" ".join(bkg_samples + sig_samples))
	binnings_settings = binnings.BinningsDict()


	args.categories = [None if category == "None" else category for category in args.categories]

	# fill in hp-style
	for index in range(len(args.channels) - len(args.background_method)):
		args.background_method.append(args.background_method[index])

	# Category and Cut type assignment for respective studies
	global_category_string = "catHtt13TeV"
	global_cut_type = "baseline"
	if args.mssm:
		global_category_string = "catHttMSSM13TeV"
		global_cut_type = "mssm"
	elif args.mva: 			global_category_string = "catMVAStudies"
	elif args.polarisation: global_category_string = "catZttPol13TeV"
	if args.era == "2016": global_cut_type += "2016"

	if pdfkey != "" or len(addpdfs) != 0:
		if args.categories[0] != None: category_string = (global_category_string + "_{channel}_{category}").format(channel = args.channels[0], category = args.categories[0])
		else:	category_string = None
		config = sample_settings.get_config( samples = list_of_samples, channel = args.channels[0], category = category_string )
		file_name = args.input_dir + config['files'][0].split()[6]
		print "file_name", file_name
		file_name = glob.glob(file_name)[0]
		if log.isEnabledFor(logging.DEBUG): print "lheweight picked up from file: ", file_name
		root_file = ROOT.TFile(file_name, "READ")
		#print dir(sample_settings)
		#print help(sample_settings)
		eventTree = ROOT.gDirectory.Get(sample_settings.root_file_folder("tt"))
		n_entries = eventTree.GetEntries()
		list_of_leaves = eventTree.GetListOfLeaves()

		for leave in list_of_leaves:
			if pdfkey == "_".join(leave.GetTitle().split("_")[:-2]) or "muR" in leave.GetTitle() or leave.GetTitle() in addpdfs:
				if not any(c in leave.GetTitle() for c in ("muR0p5_muF2p0", "muR2p0_muF0p5")): 
					lheweights_names.append(str(leave.GetTitle()))
		if log.isEnabledFor(logging.DEBUG): print "lheweights_names:", lheweights_names

	plot_configs = {}
	plot_configs_scale_only = {}
	plot_configs_pdf_only = {}
	plot_configs_alphas_only = {}
	# Loop for producing configure files
	for channel, background_method in zip(args.channels, args.background_method):
		if log.isEnabledFor(logging.DEBUG): print "channel", channel, "background_method", background_method
		for category in args.categories:
			if log.isEnabledFor(logging.DEBUG): print "\tcategory", category
			plot_configs[category] = []
			plot_configs_scale_only[category] = []
			plot_configs_pdf_only[category] = []
			plot_configs_alphas_only[category] = []
			for quantity in args.quantities:
				if log.isEnabledFor(logging.DEBUG): print "\t\tquantity", quantity
				if category != None:
					category_string = (global_category_string + "_{channel}_{category}").format(channel = channel, category = category)
				else:
					category_string = None
				json_config = {}
				json_filenames = [os.path.join(args.json_dir, "8TeV" if args.run1 else "13TeV", channel_dir, quantity+".json") for channel_dir in [channel, "default"]]
				for json_filename in json_filenames:
					json_filename = os.path.expandvars(json_filename)
					if os.path.exists(json_filename):
						json_config = jsonTools.JsonDict(json_filename).doIncludes().doComments()
						break
				quantity = json_config.pop("x_expressions", [quantity])[0]
					
				for lheweight in lheweights_names:
					config = sample_settings.get_config(
							samples = list_of_samples,
							channel = channel,
							category = category_string,
							higgs_masses = args.higgs_masses,
							normalise_signal_to_one_pb = False,
							ztt_from_mc = args.ztt_from_mc,
							weight = lheweight + "*" + make_multiplication([clean_multiplication(json_config.pop("weights", ["1.0"])[0]), args.weight]),
							lumi  =  args.lumi * 1000,
							exclude_cuts = args.exclude_cuts + json_config.pop("exclude_cuts", []),
							blind_expression = channel + "_" + quantity,
							fakefactor_method = args.fakefactor_method,
							stack_signal = args.stack_signal,
							scale_signal = args.scale_signal,
							project_to_lumi = args.project_to_lumi,
							cut_mc_only = args.cut_mc_only,
							scale_mc_only = args.scale_mc_only,
							estimationMethod = background_method,
							mssm = args.mssm,
							controlregions = args.controlregions,
							cut_type = global_cut_type,
							nick_suffix = "_" + category + "_" + lheweight,
					)
					print config["files"][0]
					if args.era == "2016": config["files"] = [config["files"][0].split()[6]] #temporary! for running only on one merged DYM50 sample
					config["x_expressions"] = [("0" if "pol_gen" in nick else json_config.pop("x_expressions", [quantity])) for nick in config["nicks"]]
					config["category"] = category

					binning_string = None
					if args.mssm: 			binning_string = "binningHttMSSM13TeV"
					elif args.mva: 			binning_string = "binningMVAStudies"
					elif args.polarisation: binning_string = "binningZttPol13TeV"
					else: 					binning_string = "binningHtt13TeV"
					
					binnings_key = None
					if binnings_key in binnings_settings.binnings_dict:
						binnings_key = (binning_string + "_{channel}_{category}").format(channel=channel, category=category)
					elif channel + "_" + quantity in binnings_settings.binnings_dict: 
						binnings_key = channel + "_" + quantity
					
					if binnings_key is not None:
						config["x_bins"] = [("1,-1,1" if "pol_gen" in nick else json_config.pop("x_bins", [binnings_key])) for nick in config["nicks"]]

					config["x_label"] = json_config.pop("x_label", channel + "_" + quantity)

					config["title"] = "channel_" + channel

					config["directories"] = [args.input_dir]

					if args.shapes:
						if "stacks" in config:
							config.pop("stacks")
						if "NormalizeToUnity" not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("NormalizeToUnity")
						config["y_label"] = "arb. u."
						config["markers"] = "LINE"
						config["legend_markers"] = "L"
						config["line_widths"] = 3

					if args.ratio:
						bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
						if "Ratio" not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("Ratio")
						config.setdefault("ratio_numerator_nicks", []).extend([" ".join(bkg_samples_used), "data"])
						config.setdefault("ratio_denominator_nicks", []).extend([" ".join(bkg_samples_used)] * 2)
						config.setdefault("ratio_result_nicks", []).extend(["ratio_MC", "ratio_Data"])
						config.setdefault("colors", []).extend(["#000000"] * 2)
						config.setdefault("markers", []).extend(["E2", "E"])
						config.setdefault("legend_markers", []).extend(["ELP"]*2)
						config.setdefault("labels", []).extend([""] * 2)
						config.setdefault("stacks", []).extend(["unc", "ratio"])


					for analysis_module in args.analysis_modules:
						if analysis_module not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append(analysis_module)

					if log.isEnabledFor(logging.DEBUG) and (not "PrintInfos" in config.get("analysis_modules", [])):
						config.setdefault("analysis_modules", []).append("PrintInfos")

					if not "--y-log" in args.args: config["y_lims"] = [0.0]

					if args.cms:
						config["cms"] = True
						config["extra_text"] = "Preliminary"
						config["legend"] = [0.7, 0.4, 0.95, 0.83] if args.ratio or args.integrated_sob or args.sbratio else [0.7, 0.5, 0.9, 0.85]
					elif args.shapes:
						config["legend"] = [0.55, 0.65, 0.9, 0.88]
					else:
						config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 1.5 if args.ratio or args.integrated_sob or args.sbratio else 1.4]
						config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio or args.integrated_sob or args.sbratio else [0.23, 0.73, 0.9, 0.89]
						config["legend_cols"] = 3

					if not args.shapes:
						if args.lumi is not None:
							config["lumis"] = [float("%.1f" % args.lumi)]
						config["energies"] = [8] if args.run1 else [13]
						if not args.run1:
							config["year"] = args.era

					if(args.full_integral):
						bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
						hmass_temp = 125
						if len(args.higgs_masses) > 0 and "125" not in args.higgs_masses:
							hmass_temp = int(args.higgs_masses[0])
						sig_nick = "htt%i"%hmass_temp
						bkg_samples_used.append(sig_nick)
						config["full_integral_nicks"] = [" ".join(bkg_samples_used)]
						config["analysis_modules"].append("FullIntegral")

					config["output_dir"] = os.path.expandvars(os.path.join(
							args.output_dir,
							channel if len(args.channels) > 1 else "",
							category if len(args.categories) > 1 else ""
					))
					
					if args.www is not None: config["www"] = os.path.join(args.www, channel, "" if category is None else category)

					config.update(json_config)

					# Saving produced configuration file in the list 
					plot_configs[category].append(config)
					if log.isEnabledFor(logging.DEBUG): print "\t\t\t", lheweight
					if pdfkey == "_".join(lheweight.split("_")[:-2]):
						log.debug("\t\t\t\tplot_configs_pdf_only")
						plot_configs_pdf_only[category].append(config)
					if pdfkey + "_0_weight" == lheweight or lheweight in addpdfs:
						log.debug("\t\t\t\tplot_configs_alphas_only")
						plot_configs_alphas_only[category].append(config)
					if "muF" in lheweight:
						log.debug("\t\t\t\tplot_configs_scale_only")
						plot_configs_scale_only[category].append(config)
	
	if log.isEnabledFor(logging.DEBUG): pprint.pprint(plot_configs)

	# Saving configuration into separate files
	print "Saving configuration into separate files"
	configs_dict = {"_all_": plot_configs, 
					"_pdf_only_": plot_configs_pdf_only,
					"_alphas_only_": plot_configs_alphas_only,
					"_scale_only_": plot_configs_scale_only
					}
	for category in args.categories:
		log.debug(category)
		for (key, value) in configs_dict.items():
			merge(value[category])
			if category != 'inclusive' and 'inclusive' in args.categories: 
				value[category][0] = sample_settings.merge_configs(value[category][0], value['inclusive'][0])
			log.debug(args.quantities[0] + key + str(category))
			value[category][0]["filename"] = args.samples[0] + args.quantities[0] + key + str(category)
			
			fout = open("merged" + key + str(category) + ".json", "w")
			fout.write(pprint.pformat(value[category][0]).replace("u'D", "'D").replace("'", '"'))

	if log.isEnabledFor(logging.DEBUG): print "Addititonal args for the configuration files:", [args.args]
	# This is not working BECAUSE of the single quotes. 
	#pprint.pprint([configs_dict.values()[0][0]])
	higgsplot.HiggsPlotter(list_of_config_dicts=[configs_dict["_all_"][args.categories[0]][0]], list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	#higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs[args.categories[0]][0], list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

