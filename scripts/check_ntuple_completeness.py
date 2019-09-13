import os
import ROOT as r
import json
import sys

incomplete_samples=[]
incomplete_samples_information=[]

exclusive_samples = {
        "et": ["EGamma","SingleElectron","ElTauFinalState"],
        "mt": ["SingleMuon","MuTauFinalState"],
        "tt": ["Tau_Run201","TauTauFinalState"],
        "em": ["MuonEG","ElMuFinalState"]
        }

if len(sys.argv) < 3:
	print "Give two arguments: Path to ntuples and channel: 'python get_initial.py /path/ mt'"
	exit()
path1 = sys.argv[1]
datasets_found = False
if "CMSSW_BASE" in os.environ:
	if os.path.exists(os.environ["CMSSW_BASE"]+"/src/Kappa/Skimming/data/datasets.json"):
		dataset_path = os.environ["CMSSW_BASE"]+"/src/Kappa/Skimming/data/datasets.json"
		datasets_found = True	
if not datasets_found:
	if os.path.exists("/ceph/htautau/datasets/datasets.json"):
		dataset_path = "/ceph/htautau/datasets/datasets.json"
	elif os.path.exists("datasets.json"):
		dataset_path = "datasets.json"
	else:
		print "No datasets.json could be located, please copy the most recent datasets.json in the current directory ({}) to run the script.".format(os.environ["PWD"])
		exit()
print "Using datasets from {}".format(dataset_path)

with open(dataset_path) as json_file:
	datasets=json.load(json_file)
if "merged" in path1 or "ceph" in path1:
	files=os.listdir(path1)
	for File in files:
		print "Checking "+File
		try:	
			f = r.TFile("{}{}/{}{}".format(path1,File,File,".root","read"))
			hist = f.Get("{}_nominal/cutFlowUnweighted".format(sys.argv[2]))	
			if float(hist.GetBinContent(1))/float(datasets[File]["n_events_generated"])<0.99 or float(hist.GetBinContent(1))/float(datasets[File]["n_events_generated"])>1.01:
				incomplete_samples.append(File)
				incomplete_samples_information.append(float(hist.GetBinContent(1))/float(datasets[File]["n_events_generated"]))
				print '\033[91m'+'Fraction of processed events is only {}'.format(float(hist.GetBinContent(1))/float(datasets[File]["n_events_generated"]))+'\033[0m'
			else:
				print '\033[92m'+'Everything here!'+'\033[0m'
		except:
			this_is_a_problem = True
			for channel in ["mt","et","tt","em"]:
				if channel==sys.argv[2]:
					continue
				for identifier in exclusive_samples[channel]:
					if identifier in File:
						this_is_a_problem = False
			if this_is_a_problem:
				print '\033[91m'+'Problem accessing {}_nominal in file - this should be possible.'.format(sys.argv[2])+'\033[0m'
			else:
				print '\033[92m'+'No channel {} in here - as expected'.format(sys.argv[2])+'\033[0m'	
				
			incomplete_samples.append(File)
			incomplete_samples_information.append(0)
			pass


else:
	folders=os.listdir(os.path.join(path1))
	if "gridka-nrg" in path1:
		add="root://cmsxrootd-redirectors.gridka.de//store/user/"
		path2=path1.replace("/storage/gridka-nrg/","")
		path2=add+path2
	for Folder in folders:
		events=0
		if os.path.isdir(os.path.join(path1,Folder)):
			files=os.listdir(os.path.join(path1,Folder))		
			for File in files:
				if not ".root" in File or File[0]==".":
					continue
				f = r.TFile.Open(os.path.join(path2,Folder,File),"read")

				hist = f.Get("{}_nominal/cutFlowUnweighted".format(sys.argv[2]))

				events+=hist.GetBinContent(1)
			if ((float(events)/float(datasets[Folder]["n_events_generated"]))<0.99999):
				incomplete_samples.append(Folder)
				incomplete_samples_information.append(float(events)/float(datasets[Folder]["n_events_generated"]))
			


incomplete_samples_cleaned = [x for x in incomplete_samples]

to_del = []
for i in range(len(incomplete_samples)):
	for channel in ["mt","et","tt","em"]:
		if channel==sys.argv[2]:
			continue
		for identifier in exclusive_samples[channel]:	
			if identifier in incomplete_samples[i]:
				incomplete_samples_cleaned.remove(incomplete_samples[i])
				to_del.append(i)
ratio_cleaned = []
for i in range(len(incomplete_samples_information)):
	if i in to_del:
		continue
	ratio_cleaned.append(incomplete_samples_information[i])
	
# Keep updated!
name_dict = {
	"jbechtel": "Janek",
	"sbrommer": "Sebastian",
	"swozniewski": "Sebastian",
	"akhmet": "Genosse Gottmann",
	"mburkart": "Max",
	"mscham": "Moritz",
	"ohlushch": "Olena",
	"wunsch": "Stefan"
	}

if os.environ["USER"] in name_dict:
	name = name_dict[os.environ["USER"]]
else:
	name = os.environ["USER"]
print "\nChecked {} samples.\n".format(len(files))
if len(incomplete_samples_cleaned) == 0:	
	print '\033[92m'+'Everything looks okay! Well done '+name+'!'+'\033[0m'
else:
	print '\033[91m'+'There seems to be a problem with these samples:'+'\033[0m'
for i in range(len(incomplete_samples_cleaned)):
	print incomplete_samples_cleaned[i]
	print "Only has fraction of {} of events..".format(ratio_cleaned[i])
