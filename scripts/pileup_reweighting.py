import ROOT as r
import os
import json

r.gROOT.SetBatch()

r.gStyle.SetOptStat(0)

nbins = 200 #set to the number used for the data distributions, e.g. 2000 for inclusive measurements or 200 if sample specific

#base_mc_path = "/ceph/swozniewski/SM_Htautau_Legacy/ntuples/2019_10_PU/2016/"
#base_mc_path = "/ceph/swozniewski/SM_Htautau_Legacy/ntuples/2019_10_PU/2018/"
base_mc_path = "/ceph/swozniewski/SM_Htautau_Legacy/ntuples/2019_10_PU/2017/"
pileup_weights_path = "pileup_weights_folder_30_10_2019"

cmssw_base = os.environ.get("CMSSW_BASE")
database = json.load(open(os.path.join(cmssw_base, "src/Kappa/Skimming/data/datasets.json")))


if not os.path.exists(pileup_weights_path):
    os.makedirs(pileup_weights_path)


#data_file =  r.TFile("MyDataPileupHistogramFull_69200_EOY2017ReReco_200Bins.root", "read")
#data_file =  r.TFile("MyDataPileupHistogram2016_90200_ReReco_07Aug2017_2000Bins.root", "read")
#data_file =  r.TFile("MyDataPileupHistogram2018_90200_17SeptEarlyReReco2018ABC_PromptEraD_2000Bins.root", "read")
data_file = r.TFile("MyDataPileupHistogram2017_90200_EOY2017ReReco_200Bins.root", "read")
npu_data = data_file.Get("pileup").Clone()

mc_samples_list = [s for s in os.listdir(base_mc_path) if os.path.isdir(os.path.join(base_mc_path,s))]
print mc_samples_list
pudistributions = r.TFile("pudistributions_2017.root","RECREATE")

mc_samples = {}

for s in mc_samples_list:
        mc_samples[s] = {}
        mc_samples[s]["input_mc"] = r.TFile(os.path.join(base_mc_path,s,s+".root"),"read")
        dbs = database[s]["dbs"].replace("/","#")
        mc_samples[s]["npu_mc"] = r.TH1D(dbs,dbs,nbins,0,200)
        mc_samples[s]["input_mc"].Get("pu_nominal").Get("ntuple").Draw("npu>>%s"%dbs)
        print "Output for %s created" %s

        mc_samples[s]["npu_mc_kit"] = r.TH1D(s,s,nbins,0,200)
        mc_samples[s]["input_mc"].Get("pu_nominal").Get("ntuple").Draw("npu>>%s"%s,"npu >= 0")
        mc_samples[s]["npu_mc_kit"].Scale(1./mc_samples[s]["npu_mc_kit"].GetEntries())
        mc_samples[s]["npu_data_kit"] = data_file.Get("pileup").Clone()
        mc_samples[s]["npu_data_kit"].Scale(1./mc_samples[s]["npu_data_kit"].Integral())
        mc_samples[s]["npu_data_kit"].Divide(mc_samples[s]["npu_mc_kit"])
        mc_samples[s]["output_kit"] = r.TFile(os.path.join(pileup_weights_path,s+".root"),"recreate")
        mc_samples[s]["output_kit"].cd()
        #mc_samples[s]["npu_mc_kit"].Write()
        mc_samples[s]["npu_data_kit"].Write()
        mc_samples[s]["output_kit"].Close()
        print "Entries in MC:",mc_samples[s]["npu_mc_kit"].GetEntries() 



pudistributions.cd()

for s in mc_samples:
    mc_samples[s]["npu_mc"].Write()

pudistributions.Close()
