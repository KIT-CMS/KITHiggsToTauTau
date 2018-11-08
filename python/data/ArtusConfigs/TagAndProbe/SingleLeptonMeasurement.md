# Measurement Recipe for Single Lepton Scalefactors

Disclamer:

---

*The is the Status of the v17_4 Measurement, newer measurements may not be covered by this documentation.*

**!! In all these steps, it is crutial to pay attention to the correct naming of files and scale factors to not cause any wrong measurements !!**

---

The SingleLepton Scalefactors are measured using the TagAndProbe Method. Therefore, events with two Leptons are selected, one lepton must pass loose probe requirements, while the other lepton must pass tighter tag requirements. Depending on the quantity that is going to be measured, passing and failing probes are counted individually. Then, two seperate selections, the first one beeing tag + passing probe (pass) and tag + failing probe (fail) are fitted to an signal + background model. In this case, the selections are fitted to the Z-Mass peak. For more information check the Twiki (https://twiki.cern.ch/twiki/bin/view/CMSPublic/TagAndProbe). The efficiency is calculated by dividing the yield of the passed and the failed signal regions. 

---

Measuring Singlelepton Scalefactors requires multiple frameworks:

```
(1) Artus+KitHiggsTauTau (https://github.com/KIT-CMS/KITHiggsToTauTau/tree/scale_factor_measurements)
(2) ICHiggsTauTau (https://github.com/janekbechtel/ICHiggsTauTau)
(3) CorrectionsWorkspace (https://github.com/harrypuuter/CorrectionsWorkspace/tree/2017_17NovReRecoData_Fall17MC)
```

## Produce nTuples

The ntuples are produced using Artus+KitHiggsTauTau. The checkout script can be found [here](https://github.com/KIT-CMS/KITHiggsToTauTau/blob/scale_factor_measurements/scripts/checkout_packages_CMSSW94X.sh).

The TagAndProbe Analysis is run via

```
HiggsToTauTauAnalysis.py -a tagandprobe -i "samplesnames" --additionaloptions
```

In the case of SingleLeptons, there are two piplines, one for electron scalefactors and one for muon scalefactors. There are independently from each other and can be activated in the base TagAndProbe Config `HiggsAnalysis/KITHiggsToTauTau/python/data/ArtusConfigs/TagAndProbe_base.py`. 
```py
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.mumu_test").build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.ee_singleelectron").build_config(nickname)
```
### Samples 

#### Muon Scalefactors

|Samples   | Filelist                                                                         | 
| -------- | ------------------------------------------------                                 |
| MC       | DY* in `KITHiggsToTauTau/data/Samples/Fall17v2`                                  |
| Data     | SingleMuon_Run2017* in `KITHiggsToTauTau/data/Samples/Run2017/ReReco_31Mar2018/` |
| Embedded | Embedding2017_*MuonEmbedding* in `KITHiggsToTauTau/data/Samples/Embedding2017/`  |

##### Electron Scalefactors
|Samples   | Filelist                                                                           | 
| -------- | ------------------------------------------------                                   |
| MC       | DY* in `KITHiggsToTauTau/data/Samples/Fall17v2`                                    |
| Data | SingleElectron_Run2017* in `KITHiggsToTauTau/data/Samples/Run2017/ReReco_31Mar2018/`   |
| Embedded | Embedding2017_*ElectronEmbedding* in `KITHiggsToTauTau/data/Samples/Embedding2017/`|

### Selection Criteria
The Selection Citerias are defined in the two pipeline scripts

* Muons: `KITHiggsToTauTau/python/data/ArtusConfigs/TagAndProbe/mumu_test.py`
* Electrons: `python/data/ArtusConfigs/TagAndProbe/ee_singleelectron.py`

The basic setup is

1. Produce two valid Leptons using the probe selection (`producer:ValidElectronsProducer`)
2. Filter that there are at least two valid probe leptons in the event (`filter:ValidElectronsFilter` and `filter:MinElectronsCountFilter`)
3. Match trigger Paths (`producer:ElectronTriggerMatchingProducer`)
4. Produce TagAndProbe Pairs (`producer:NewEETagAndProbePairCandidatesProducer`)
    1. Looping over all valid leptons in an event and try to apply the tag selection to one lepton and the probe selection to another lepton
    2. If the requirements are met, the lepton pair is stored as a valid TagAndProbePair. This allows that multiple TagAndProbe Pairs are produced using only one event (if both leptons pass the tag requirements, the can both be used as probe increasing the statistics of the study)
5. The `NewEETagAndProbePairConsumer` produces the different quantities in the output sample. The quantities written to the outfile are defined in  `KITHiggsToTauTau/python/data/ArtusConfigs/TagAndProbe/Includes/TagAndProbeQuantitiesEE.py`

### Muon Selection

* General Selection:
    * Two Muons, opposite charge
    * `DeltaR > 0.5`
* Probe Selection:
    * `Pt > 10 GeV`
    * `Eta < 2.4`
    * `isTrackerMuon`
* Tag Selection:
    * Probe Selection plus:
        * `Pt > 23.0`
        * `id >= Medium`
        * `dxy < 0.045`
        * `dz < 0.2`
        * `iso_sum < 0.15`

### Muon Quantities
| Quantity                        | Explanation |
| -----------------------------   | ----------  |
|"trg_t_IsoMu27", "trg_p_IsoMu27" | HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07 |
|"trg_t_IsoMu24", "trg_p_IsoMu24" | HLT_IsoMu24_v:hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07 |
|"pt_t", "pt_p"                   | Pt of Tag and Probe Muon |
|"iso_t", "iso_p"                 | Isolation of Tag and Probe Muon |
|"id_t",  "id_p"                  | ID of Tag and Probe Muon |
|"m_ll"                           | DiLeptonMass |

### Electron Selection

* General Selection:
    * Two Electrons, opposite charge
    * `DeltaR > 0.5`
* Probe Selection:`
    * `Pt > 10 GeV`
    * `Eta < 2.4`
* Tag Selection:
    * Probe Selection plus:
        * `Pt > 26.0`
        * `idWP90`
        * `dxy < 0.045`
        * `dz < 0.2`
        * `iso_sum < 0.1`

### Electron Quantities

| Quantity                        | Explanation |
| -----------------------------   | ----------  |
|"trg_t_Ele27",   "trg_p_Ele27"    | HLT_Ele27_WPTight_Gsf_v:hltEle27WPTightGsfTrackIsoFilter |
|"trg_t_Ele32",   "trg_p_Ele32"    | HLT_Ele32_WPTight_Gsf_v:hltEle32WPTightGsfTrackIsoFilter |
|"trg_t_Ele35",   "trg_p_Ele35"    | HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter |
|"trg_t_Ele32_fb","trg_p_Ele32_fb" | HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEle32L1DoubleEGWPTightGsfTrackIsoFilter |
|"pt_t", "pt_p",                   | Pt of Tag and Probe Muon |
|"iso_t","iso_p",                  | Rho Corrected Isolation of Tag and Probe Muon |
|"id_90_t",	"id_90_p",            | egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp90 Electron ID |
|"id_80_t",	"id_80_p",            | egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp80 Electron ID |
|"m_ll"                          | DiLeptonMass | 

## Histrogam selection

In the next step, the ntuples are filled into different histograms, creating the pass and the fail category. This is done using the ICHiggsTauTau Framework (`ICHiggsTauTau/Analysis/HiggsTauTau/scripts/electronTagAndProbe_reimplementation.py`). In this script, the different quantities, for which scalefactors sould be measured are defined.

Example

```py
{
    'name': 'Trg35_Iso_pt_eta_bins',
    'var': 'm_ll(50,65,115)',
    'tag': 'trg_t_Ele35 &&  id_90_t && iso_p < 0.15',
    'probe': '(trg_p_Ele35)',
    'binvar_x': 'pt_p',
    'bins_x': [10., 20., 25., 26., 27., 28., 29., 30., 31, 32., 33., 34., 35., 36., 37., 38., 39., 40., 42., 44., 46., 48., 50., 100., 200., 1000.],
    'binvar_y': 'abs(eta_p)',
    'bins_y': [0, 1.0, 1.479, 1.653, 2.1, 2.4]
},
```
This defines the measurement of the Ele35 Trigger. As a tagtrigger, the Ele35 is used, the tag Electron needs an IDWp90 and the probe Electron Isolation must be higher then 0.15. The Scalefactors are binned in probe pt, as well as probe eta. This binning is defined with `bins_x` and `bins_y`.

The Input Files from Artus are defined in the end of the script

```py
trees = {
    'DYJetsToLL': analysis.TTreeEvaluator('ee_singleelectron_nominal/ntuple', '/storage/9/sbrommer/artus_outputs/TPZee/2018-10-29/output/Electron_DY.root'),
    'Data': analysis.TTreeEvaluator('ee_singleelectron_nominal/ntuple', '/storage/9/sbrommer/artus_outputs/TPZee/2018-10-29/output/SingleElectron.root'),
    'Embedding':  analysis.TTreeEvaluator('ee_singleelectron_nominal/ntuple', '/storage/9/sbrommer/artus_outputs/TPZee/2018-10-29/output/Electron_Embedding.root')
} 
```
## Histogram Fitting

After the histograms are filled, each bin will be fitted with an signal+background model. This is done using the `ICHiggsTauTau/Analysis/HiggsTauTau/scripts/runTagAndProbeFits_v17_4.py` script. Here, the model of Signal and Background are specified

example:

```py
"Trg35_Iso_pt_eta_bins":{
        "SMALL": "eff.Trg_35Iso",
        "DIR": dir,
        "TITLE": "Trg Ele(35)",
        "BKG": "Exponential",
        "SIG": "DoubleVCorr"
    },
```
In this case, the background is defined as an Exponential Background and the signal is an Z peak. The definition of this models can be found in the corresonding fitting script (`ICHiggsTauTau/Analysis/HiggsTauTau/scripts/fitTagAndProbe_script.py`) The script is run by 

```
python scripts/runTagAndProbeFits_v17_4.py --channel e --fit
```

After running these two steps, a small fit result file for every quantity will be produced. 

## Creating the Workspace

The Workspace can be produced using the `CorrectionsWorkspace/makeCorrectionsWorkspace_17_4.py` script. In this script, the fit results are loaded and turned into scalefactors. Since the results are binned in pt and eta, the resulting scalefactors are binned in the same way.

Loading the files:
```py
(loc+'ZeeTP_Data_Fits_Trg35_Iso_pt_eta_bins.root:Trg35_Iso_pt_eta_bins',      'e_trg35_kit_data'),
(loc+'ZeeTP_DYJetsToLL_Fits_Trg35_Iso_pt_eta_bins.root:Trg35_Iso_pt_eta_bins',        'e_trg35_kit_mc'),
(loc+'ZeeTP_Embedding_Fits_Trg35_Iso_pt_eta_bins.root:Trg35_Iso_pt_eta_bins', 'e_trg35_kit_embed'),
(loc+'ZeeTP_Data_Fits_Trg35_AIso_pt_bins_inc_eta.root:Trg35_AIso_pt_bins_inc_eta',      'e_trg35_aiso_kit_data'),
(loc+'ZeeTP_DYJetsToLL_Fits_Trg35_AIso_pt_bins_inc_eta.root:Trg35_AIso_pt_bins_inc_eta',        'e_trg35_aiso_kit_mc'),
(loc+'ZeeTP_Embedding_Fits_Trg35_AIso_pt_bins_inc_eta.root:Trg35_AIso_pt_bins_inc_eta', 'e_trg35_aiso_kit_embed'),
```

Binning in pt and eta:

```py
for task in histsToWrap:
    print task
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])
```

Calcualting the scalefactor for MC and embedded Samples by dividing the efficiency of data with the MC or embedded efficieny:

```py
for t in ['trg35']:
    w.factory('expr::e_%s_kit_ratio("min(10.,(@0/@1))", e_%s_kit_data, e_%s_kit_mc)' % (t, t, t))
    w.factory('expr::e_%s_embed_kit_ratio("min(10.,(@0/@1))", e_%s_kit_data, e_%s_kit_embed)' % (t, t, t))
```

By running the script with 

```
python makeCorrectionsWorkspace_17_4.py  
```
and RooWorkspace called `htt_scalefactors_v17_4.root` is produced. 