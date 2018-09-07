#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include <TMath.h>
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SMggHNNLOProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/ggF_qcd_uncertainty_2017.cxx"
#include <assert.h>

void SMggHNNLOProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
        // set variables
	std::string filename = settings.GetggHNNLOweightsRootfile();
	std::string generator = settings.GetGenerator();
        TDirectory *savedir(gDirectory);
        TFile *savefile(gFile);
        TFile rootFile(filename.c_str(), "READ");
        gSystem->AddIncludePath("-I$ROOFITSYS/include");
        if (generator == "powheg"){
		WeightsGraphs[0] = (TGraphErrors*)rootFile.Get("gr_NNLOPSratio_pt_powheg_0jet");
		WeightsGraphs[1] = (TGraphErrors*)rootFile.Get("gr_NNLOPSratio_pt_powheg_1jet");
		WeightsGraphs[2] = (TGraphErrors*)rootFile.Get("gr_NNLOPSratio_pt_powheg_2jet");
		WeightsGraphs[3] = (TGraphErrors*)rootFile.Get("gr_NNLOPSratio_pt_powheg_3jet");
        }
	else if (generator == "amcatnlo"){
		WeightsGraphs[0] = (TGraphErrors*)rootFile.Get("gr_NNLOPSratio_pt_mcatnlo_0jet");
		WeightsGraphs[1] = (TGraphErrors*)rootFile.Get("gr_NNLOPSratio_pt_mcatnlo_1jet");
		WeightsGraphs[2] = (TGraphErrors*)rootFile.Get("gr_NNLOPSratio_pt_mcatnlo_2jet");
		WeightsGraphs[3] = (TGraphErrors*)rootFile.Get("gr_NNLOPSratio_pt_mcatnlo_3jet");
        }
        else std::cout << "WARNING: Invalid option <Generator> for ggH NNLO reweighting. Weights are set to 1.0, ggH qcd uncertainties are however calculated!"<< std::endl;
        rootFile.Close();
        gDirectory = savedir;
        gFile = savefile;
        
        
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggh_NNLO_weight", [](event_type const& event, product_type const& product) {
		return product.m_ggh_NNLO_weight;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_ggH_Mu", [](event_type const& event, product_type const& product) {
		return product.m_THU_ggH[0];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_ggH_Res", [](event_type const& event, product_type const& product) {
		return product.m_THU_ggH[1];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_ggH_Mig01", [](event_type const& event, product_type const& product) {
		return product.m_THU_ggH[2];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_ggH_Mig12", [](event_type const& event, product_type const& product) {
		return product.m_THU_ggH[3];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_ggH_VBF2j", [](event_type const& event, product_type const& product) {
		return product.m_THU_ggH[4];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_ggH_VBF3j", [](event_type const& event, product_type const& product) {
		return product.m_THU_ggH[5];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_ggH_PT60", [](event_type const& event, product_type const& product) {
		return product.m_THU_ggH[6];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_ggH_PT120", [](event_type const& event, product_type const& product) {
		return product.m_THU_ggH[7];
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_ggH_qmtop", [](event_type const& event, product_type const& product) {
		return product.m_THU_ggH[8];
	});
}

void SMggHNNLOProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings) const
{   
	// get inputs
	int stxs1flag = event.m_genEventInfo->htxs_stage1cat;
	int njets = event.m_genEventInfo->htxs_njets30;
	double higgsPt = event.m_genEventInfo->htxs_higgsPt;

	// determine uncertainties
	product.m_THU_ggH = qcd_ggF_uncertSF_2017(njets, higgsPt, stxs1flag);

	// determine reweighting weight
	if (njets>3) njets = 3;
	static double cutoff[4] = {125.0, 625.0, 800.0, 925.0};
	if (njets>=0) product.m_ggh_NNLO_weight = WeightsGraphs[njets]->Eval(std::min(higgsPt, cutoff[njets]));
}
