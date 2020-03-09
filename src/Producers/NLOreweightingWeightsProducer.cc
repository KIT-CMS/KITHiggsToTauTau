#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include <TMath.h>
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/NLOreweightingWeightsProducer.h"
#include <assert.h>
#include "Artus/Utility/interface/RootFileHelper.h"

void NLOreweightingWeightsProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggh_t_weight", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return (product.m_ggh_t_weight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggh_b_weight", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return (product.m_ggh_b_weight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggh_i_weight", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return (product.m_ggh_i_weight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggH_t_weight", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return (product.m_ggH_t_weight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggH_b_weight", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return (product.m_ggH_b_weight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggH_i_weight", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return (product.m_ggH_i_weight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggA_t_weight", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return (product.m_ggA_t_weight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggA_b_weight", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return (product.m_ggA_b_weight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ggA_i_weight", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return (product.m_ggA_i_weight);
	});
}

void NLOreweightingWeightsProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings) const
{
	// set variables
	std::string filename = settings.GetNLOweightsRooWorkspace();
	std::string mass = settings.GetHiggsBosonMass();

	// Load workspace containing the weights
	TFile* rootFile = new TFile(filename.c_str(), "READ");
	static RooWorkspace* w = static_cast<RooWorkspace*>(rootFile->Get("w"));
	if (w == nullptr)
	{
		LOG(FATAL) << "Cannot load \"" << "w" << "\" from directory \"" << rootFile->GetName() << "\"!";
	}

	//get weights
	w->var("h_pt")->setVal(product.m_genBosonLV.Pt());
	//std::cout << product.m_genBosonLV.Pt() << std::endl;
	//std::cout << product.m_genBosonLV.M() << std::endl;
	product.m_ggh_t_weight = w->function(("h_"+mass+"_t_ratio").c_str())->getVal();
	//std::cout << product.m_ggh_t_weight << std::endl;
	product.m_ggh_b_weight = w->function(("h_"+mass+"_b_ratio").c_str())->getVal();
	product.m_ggh_i_weight = w->function(("h_"+mass+"_i_ratio").c_str())->getVal();
	product.m_ggH_t_weight = w->function(("H_"+mass+"_t_ratio").c_str())->getVal();
	product.m_ggH_b_weight = w->function(("H_"+mass+"_b_ratio").c_str())->getVal();
	product.m_ggH_i_weight = w->function(("H_"+mass+"_i_ratio").c_str())->getVal();
	product.m_ggA_t_weight = w->function(("A_"+mass+"_t_ratio").c_str())->getVal();
	product.m_ggA_b_weight = w->function(("A_"+mass+"_b_ratio").c_str())->getVal();
	product.m_ggA_i_weight = w->function(("A_"+mass+"_i_ratio").c_str())->getVal();

	rootFile->Close();
	delete rootFile;
}
