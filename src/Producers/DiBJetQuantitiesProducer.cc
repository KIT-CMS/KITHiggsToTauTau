
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiBJetQuantitiesProducer.h"


double DiBJetQuantitiesProducer::GetDiBJetQuantity(product_type const& product,
                                                 dibjet_extractor_lambda dibjetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_diBJetSystemAvailable ? dibjetQuantity((static_cast<HttProduct const&>(product)).m_diBJetSystem) : DefaultValues::UndefinedDouble);
}

double DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product_type const& product,
                                                 dibjet_extractor_lambda dibjetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_JetPlusBJetSystemAvailable ? dibjetQuantity((static_cast<HttProduct const&>(product)).m_JetPlusBJetSystem) : DefaultValues::UndefinedDouble);
}

void DiBJetQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetPt", [this](event_type const& event, product_type const& product, setting_type const& settings) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity(product, [](RMDLV diBJetSystem) -> double
	{
		return diBJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetEta", [this](event_type const& event, product_type const& product, setting_type const& settings) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity(product, [](RMDLV diBJetSystem) -> double
	{
		return diBJetSystem.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetPhi", [this](event_type const& event, product_type const& product, setting_type const& settings) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity(product, [](RMDLV diBJetSystem) -> double
	{
		return diBJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetMass", [this](event_type const& event, product_type const& product, setting_type const& settings) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity(product, [](RMDLV diBJetSystem) -> double
	{
		return diBJetSystem.mass(); });
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetDeltaPhi", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return product.m_diBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4, product.m_bTaggedJets[1]->p4) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetAbsDeltaEta", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return product.m_diBJetSystemAvailable ? std::abs(product.m_bTaggedJets[0]->p4.Eta() - product.m_bTaggedJets[1]->p4.Eta()) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetdiLepPhi", [](event_type const& event, product_type const& product, setting_type const& settings) {
		return product.m_diBJetSystemAvailable ? (product.m_diBJetSystem + product.m_diLeptonSystem).Phi() :
		                                        DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetPt", [this](event_type const& event, product_type const& product, setting_type const& settings) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product, [](RMDLV JetPlusBJetSystem) -> double
	{
		return JetPlusBJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetEta", [this](event_type const& event, product_type const& product, setting_type const& settings) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product, [](RMDLV JetPlusBJetSystem) -> double
	{
		return JetPlusBJetSystem.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetPhi", [this](event_type const& event, product_type const& product, setting_type const& settings) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product, [](RMDLV JetPlusBJetSystem) -> double
	{
		return JetPlusBJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetMass", [this](event_type const& event, product_type const& product, setting_type const& settings) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product, [](RMDLV JetPlusBJetSystem) -> double
	{
		return JetPlusBJetSystem.mass(); });
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetDeltaPhi", [](event_type const& event, product_type const& product, setting_type const& settings) {
		if (product.m_leadJetIsBJet) {
			return product.m_JetPlusBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4, product.m_validJets[1]->p4) :
		                                        DefaultValues::UndefinedFloat;
		}
		else {
			return product.m_JetPlusBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4, product.m_validJets[0]->p4) :
		                                        DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetAbsDeltaEta", [](event_type const& event, product_type const& product, setting_type const& settings) {
		if (product.m_leadJetIsBJet) {
			return product.m_JetPlusBJetSystemAvailable ? std::abs(product.m_bTaggedJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) :
		                                        DefaultValues::UndefinedFloat;
		}
		else {
			return product.m_JetPlusBJetSystemAvailable ? std::abs(product.m_bTaggedJets[0]->p4.Eta() - product.m_validJets[0]->p4.Eta()) :
		                                        DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("jetUsedFordiBJetSystemIsTrueBJet", [settings](event_type const& event, product_type const& product, setting_type const& settings) {
		if (settings.GetInputIsData()) return DefaultValues::UndefinedInt;
		if (product.m_JetPlusBJetSystemAvailable) {
			if (product.m_leadJetIsBJet) {
				if (static_cast<KJet*>(product.m_validJets[1])->hadronFlavour == 5) {
					return 1;
				}
				else {
					return 0;
				}
			}
			else {
				if (static_cast<KJet*>(product.m_validJets[0])->hadronFlavour == 5) {
					return 1;
				}
				else {
					return 0;
				}
			}
		}
		else return DefaultValues::UndefinedInt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetdiLepPhi", [](event_type const& event, product_type const& product, setting_type const& settings) {
			return product.m_JetPlusBJetSystemAvailable ? (product.m_JetPlusBJetSystem + product.m_diLeptonSystem).Phi() : DefaultValues::UndefinedFloat;
	});
}

void DiBJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings) const
{
	// If >=2 b jets are present, calculate everything from the two leading b jets
	if (product.m_bTaggedJets.size() >= 2)
	{
		product.m_diBJetSystem = (product.m_bTaggedJets[0]->p4 + product.m_bTaggedJets[1]->p4);
		product.m_diBJetSystemAvailable = true;
		product.m_JetPlusBJetSystemAvailable = false;
	}
	// If only 1 b jet is present, calculate everything from b jet + jet leading in pT (or subleading if leading jet is b jet)
	else if ((product.m_bTaggedJets.size() == 1)&&(product.m_validJets.size() >=2 ))
	{
		product.m_JetPlusBJetSystemAvailable = true;
		product.m_diBJetSystemAvailable = false;
		if (ROOT::Math::VectorUtil::DeltaR(product.m_bTaggedJets[0]->p4,product.m_validJets[0]->p4) < 0.001) {
			product.m_leadJetIsBJet = true;
			product.m_JetPlusBJetSystem = (product.m_validJets[1]->p4 + product.m_bTaggedJets[0]->p4);
		}
		else {
			product.m_JetPlusBJetSystem = (product.m_validJets[0]->p4 + product.m_bTaggedJets[0]->p4);
		}
	}
	else
	{
		product.m_JetPlusBJetSystemAvailable = false;
		product.m_diBJetSystemAvailable = false;
	}

}
