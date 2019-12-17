#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SMvbfNNLOProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/qq2Hqq_uncert_scheme.cpp"

void SMvbfNNLOProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
        
        
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_TOT", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[0];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_PTH200", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[1];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_Mjj60", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[2];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_Mjj120", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[3];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_Mjj350", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[4];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_Mjj700", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[5];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_Mjj1000", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[6];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_Mjj1500", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[7];
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_25", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[8];
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("THU_qqH_JET01", [](event_type const& event, product_type const& product) {
		return product.m_THU_qqH[9];
	});
}

void SMvbfNNLOProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings) const
{   
	// get inputs
	int stxs1flag = event.m_genEventInfo->htxs_stage1p1finecat;

	// determine uncertainties
        product.m_THU_qqH.resize(10, 1.0);
        for(int i=0; i<10; i++) product.m_THU_qqH[i] = vbf_uncert_stage_1_1(i, stxs1flag, 1.0);
}
