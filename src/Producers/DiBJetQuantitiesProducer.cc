
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiBJetQuantitiesProducer.h"


double DiBJetQuantitiesProducer::GetDiBJetQuantity(product_type const& product,
                                                 dibjet_extractor_lambda dibjetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_diBJetSystemAvailable ? dibjetQuantity((static_cast<HttProduct const&>(product)).m_diBJetSystem) : DefaultValues::UndefinedDouble);
}

void DiBJetQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetPt", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity(product, [](RMDLV diBJetSystem) -> double
	{
		return diBJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetEta", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity(product, [](RMDLV diBJetSystem) -> double
	{
		return diBJetSystem.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetPhi", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity(product, [](RMDLV diBJetSystem) -> double
	{
		return diBJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetMass", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity(product, [](RMDLV diBJetSystem) -> double
	{
		return diBJetSystem.mass(); });
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetDeltaPhi", [](event_type const& event, product_type const& product) {
		return product.m_diBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4, product.m_bTaggedJets[1]->p4) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetAbsDeltaEta", [](event_type const& event, product_type const& product) {
		return product.m_diBJetSystemAvailable ? std::abs(product.m_bTaggedJets[0]->p4.Eta() - product.m_bTaggedJets[1]->p4.Eta()) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetdiLepPhi", [](event_type const& event, product_type const& product) {
		return product.m_diBJetSystemAvailable ? (product.m_diBJetSystem + product.m_diLeptonSystem).Phi() :
		                                        DefaultValues::UndefinedFloat;
	});

}

void DiBJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings) const
{

	if (product.m_bTaggedJets.size() >= 2)
	{
		product.m_diBJetSystem = (product.m_bTaggedJets[0]->p4 + product.m_bTaggedJets[1]->p4);
		product.m_diBJetSystemAvailable = true;
	}
	else
	{
		product.m_diBJetSystemAvailable = false;
	}
}
