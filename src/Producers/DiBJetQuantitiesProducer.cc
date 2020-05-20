
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiBJetQuantitiesProducer.h"


double DiBJetQuantitiesProducer::GetDiBJetQuantity(product_type const& product,
                                                 dibjet_extractor_lambda dibjetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_diBJetSystemAvailable ? dibjetQuantity((static_cast<HttProduct const&>(product)).m_diBJetSystem) : DefaultValues::UndefinedDouble);
}

double DiBJetQuantitiesProducer::GetDiBJetQuantity_bReg(product_type const& product,
                                                 dibjet_extractor_lambda dibjetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_diBJetSystemAvailable ? dibjetQuantity((static_cast<HttProduct const&>(product)).m_diBJetSystem_bReg) : DefaultValues::UndefinedDouble);
}

double DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product_type const& product,
                                                 dibjet_extractor_lambda dibjetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_JetPlusBJetSystemAvailable ? dibjetQuantity((static_cast<HttProduct const&>(product)).m_JetPlusBJetSystem) : DefaultValues::UndefinedDouble);
}

double DiBJetQuantitiesProducer::GetJetPlusBJetQuantity_bReg(product_type const& product,
                                                 dibjet_extractor_lambda dibjetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_JetPlusBJetSystemAvailable ? dibjetQuantity((static_cast<HttProduct const&>(product)).m_JetPlusBJetSystem_bReg) : DefaultValues::UndefinedDouble);
}

double DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity(product_type const& product,
                                                 dibjet_extractor_lambda dibjetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_JetPlusBJetSystemAvailable ? dibjetQuantity((static_cast<HttProduct const&>(product)).m_highCSVJetPlusBJetSystem) : DefaultValues::UndefinedDouble);
}

double DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity_bReg(product_type const& product,
                                                 dibjet_extractor_lambda dibjetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_JetPlusBJetSystemAvailable ? dibjetQuantity((static_cast<HttProduct const&>(product)).m_highCSVJetPlusBJetSystem_bReg) : DefaultValues::UndefinedDouble);
}


void DiBJetQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	std::string bTaggedJetCSVName = settings.GetBTaggedJetCombinedSecondaryVertexName();

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

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetPt", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product, [](RMDLV JetPlusBJetSystem) -> double
	{
		return JetPlusBJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetEta", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product, [](RMDLV JetPlusBJetSystem) -> double
	{
		return JetPlusBJetSystem.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetPhi", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product, [](RMDLV JetPlusBJetSystem) -> double
	{
		return JetPlusBJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetMass", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity(product, [](RMDLV JetPlusBJetSystem) -> double
	{
		return JetPlusBJetSystem.mass(); });
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetDeltaPhi", [](event_type const& event, product_type const& product) {
		if (product.m_leadJetIsBJet) {
			return product.m_JetPlusBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4, product.m_validJets[1]->p4) :
		                                        DefaultValues::UndefinedFloat;
		}
		else {
			return product.m_JetPlusBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4, product.m_validJets[0]->p4) :
		                                        DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetAbsDeltaEta", [](event_type const& event, product_type const& product) {
		if (product.m_leadJetIsBJet) {
			return product.m_JetPlusBJetSystemAvailable ? std::abs(product.m_bTaggedJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) :
		                                        DefaultValues::UndefinedFloat;
		}
		else {
			return product.m_JetPlusBJetSystemAvailable ? std::abs(product.m_bTaggedJets[0]->p4.Eta() - product.m_validJets[0]->p4.Eta()) :
		                                        DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("jetUsedFordiBJetSystemIsTrueBJet", [settings](event_type const& event, product_type const& product) {
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetUsedFordiBJetSystemCSV",[bTaggedJetCSVName](event_type const& event, product_type const& product) {
		if (product.m_JetPlusBJetSystemAvailable) {
			if (product.m_leadJetIsBJet) {
				return static_cast<KJet*>(product.m_validJets[1])->getTag(bTaggedJetCSVName, event.m_jetMetadata);
			}
			else {
				return static_cast<KJet*>(product.m_validJets[0])->getTag(bTaggedJetCSVName, event.m_jetMetadata);
			}
		}
		else return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetdiLepPhi", [](event_type const& event, product_type const& product) {
			return product.m_JetPlusBJetSystemAvailable ? (product.m_JetPlusBJetSystem + product.m_diLeptonSystem).Phi() : DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetPt", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity(product, [](RMDLV highCSVJetPlusBJetSystem) -> double
	{
		return highCSVJetPlusBJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetEta", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity(product, [](RMDLV highCSVJetPlusBJetSystem) -> double
	{
		return highCSVJetPlusBJetSystem.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetPhi", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity(product, [](RMDLV highCSVJetPlusBJetSystem) -> double
	{
		return highCSVJetPlusBJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetMass", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity(product, [](RMDLV highCSVJetPlusBJetSystem) -> double
	{
		return highCSVJetPlusBJetSystem.mass(); });
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetDeltaPhi", [](event_type const& event, product_type const& product) {

			return product.m_JetPlusBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4, product.m_validJets[product.m_highCSVJetIndex]->p4) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetAbsDeltaEta", [](event_type const& event, product_type const& product) {

			return product.m_JetPlusBJetSystemAvailable ? std::abs(product.m_bTaggedJets[0]->p4.Eta() - product.m_validJets[product.m_highCSVJetIndex]->p4.Eta()) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("highCSVjetUsedFordiBJetSystemIsTrueBJet", [settings](event_type const& event, product_type const& product) {
		if (settings.GetInputIsData()) return DefaultValues::UndefinedInt;
		if (product.m_JetPlusBJetSystemAvailable) {
			if (static_cast<KJet*>(product.m_validJets[product.m_highCSVJetIndex])->hadronFlavour == 5) {
				return 1;
			}
			else {
				return 0;
			}
		}
		else return DefaultValues::UndefinedInt;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetUsedFordiBJetSystemCSV", [bTaggedJetCSVName](event_type const& event, product_type const& product) {
		if (product.m_JetPlusBJetSystemAvailable) {
			return static_cast<KJet*>(product.m_validJets[product.m_highCSVJetIndex])->getTag(bTaggedJetCSVName, event.m_jetMetadata);
		}
		else return DefaultValues::UndefinedFloat;
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetUsedFordiBJetSystemPt", [bTaggedJetCSVName](event_type const& event, product_type const& product) {
                if (product.m_JetPlusBJetSystemAvailable) {
                        return static_cast<KJet*>(product.m_validJets[product.m_highCSVJetIndex])->p4.Pt();
                }
                else return DefaultValues::UndefinedFloat;
        });
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetUsedFordiBJetSystemEta", [bTaggedJetCSVName](event_type const& event, product_type const& product) {
                if (product.m_JetPlusBJetSystemAvailable) {
                        return static_cast<KJet*>(product.m_validJets[product.m_highCSVJetIndex])->p4.Eta();
                }
                else return DefaultValues::UndefinedFloat;
        });
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetUsedFordiBJetSystemPhi", [bTaggedJetCSVName](event_type const& event, product_type const& product) {
                if (product.m_JetPlusBJetSystemAvailable) {
                        return static_cast<KJet*>(product.m_validJets[product.m_highCSVJetIndex])->p4.Phi();
                }
                else return DefaultValues::UndefinedFloat;
        });
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetUsedFordiBJetSystemPt_bReg", [bTaggedJetCSVName](event_type const& event, product_type const& product) {
                if (product.m_JetPlusBJetSystemAvailable) {
                        return (static_cast<KJet*>(product.m_validJets[product.m_highCSVJetIndex])->p4*product.m_validJets[product.m_highCSVJetIndex]->bjetRegCorr).Pt();
                }
                else return DefaultValues::UndefinedFloat;
        });
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetUsedFordiBJetSystemEta_bReg", [bTaggedJetCSVName](event_type const& event, product_type const& product) {
                if (product.m_JetPlusBJetSystemAvailable) {
                        return (static_cast<KJet*>(product.m_validJets[product.m_highCSVJetIndex])->p4*product.m_validJets[product.m_highCSVJetIndex]->bjetRegCorr).Eta();
                }
                else return DefaultValues::UndefinedFloat;
        });
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetUsedFordiBJetSystemPhi_bReg", [bTaggedJetCSVName](event_type const& event, product_type const& product) {
                if (product.m_JetPlusBJetSystemAvailable) {
                        return (static_cast<KJet*>(product.m_validJets[product.m_highCSVJetIndex])->p4*product.m_validJets[product.m_highCSVJetIndex]->bjetRegCorr).Phi();
                }
                else return DefaultValues::UndefinedFloat;
        });
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetdiLepPhi", [](event_type const& event, product_type const& product) {
			return product.m_JetPlusBJetSystemAvailable ? (product.m_highCSVJetPlusBJetSystem + product.m_diLeptonSystem).Phi() : DefaultValues::UndefinedFloat;
	});	
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetUsedFordiBJetSystem_bRegCorr", [settings](event_type const& event, product_type const& product) {
		if (product.m_JetPlusBJetSystemAvailable) {
			return product.m_validJets[product.m_highCSVJetIndex]->bjetRegCorr;
		}
		else return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetUsedFordiBJetSystem_bRegRes", [settings](event_type const& event, product_type const& product) {
		if (product.m_JetPlusBJetSystemAvailable) {
			return product.m_validJets[product.m_highCSVJetIndex]->bjetRegRes;
		}
		else return DefaultValues::UndefinedFloat;
	});
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetPt_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity_bReg(product, [](RMDLV diBJetSystem_bReg) -> double
	{
		return diBJetSystem_bReg.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetEta_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity_bReg(product, [](RMDLV diBJetSystem_bReg) -> double
	{
		return diBJetSystem_bReg.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetPhi_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity_bReg(product, [](RMDLV diBJetSystem_bReg) -> double
	{
		return diBJetSystem_bReg.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetMass_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetDiBJetQuantity_bReg(product, [](RMDLV diBJetSystem_bReg) -> double
	{
		return diBJetSystem_bReg.mass(); });
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetDeltaPhi_bReg", [](event_type const& event, product_type const& product) {
		return product.m_diBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr, product.m_bTaggedJets[1]->p4*product.m_bTaggedJets[1]->bjetRegCorr) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetAbsDeltaEta_bReg", [](event_type const& event, product_type const& product) {
		return product.m_diBJetSystemAvailable ? std::abs((product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr).Eta() - (product.m_bTaggedJets[1]->p4*product.m_bTaggedJets[1]->bjetRegCorr).Eta()) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diBJetdiLepPhi_bReg", [](event_type const& event, product_type const& product) {
		return product.m_diBJetSystemAvailable ? (product.m_diBJetSystem_bReg + product.m_diLeptonSystem).Phi() :
		                                        DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetPt_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity_bReg(product, [](RMDLV JetPlusBJetSystem_bReg) -> double
	{
		return JetPlusBJetSystem_bReg.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetEta_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity_bReg(product, [](RMDLV JetPlusBJetSystem_bReg) -> double
	{
		return JetPlusBJetSystem_bReg.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetPhi_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity_bReg(product, [](RMDLV JetPlusBJetSystem_bReg) -> double
	{
		return JetPlusBJetSystem_bReg.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetMass_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetJetPlusBJetQuantity_bReg(product, [](RMDLV JetPlusBJetSystem_bReg) -> double
	{
		return JetPlusBJetSystem_bReg.mass(); });
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetDeltaPhi_bReg", [](event_type const& event, product_type const& product) {
		if (product.m_leadJetIsBJet) {
			return product.m_JetPlusBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr, product.m_validJets[1]->p4*product.m_validJets[1]->bjetRegCorr) :
		                                        DefaultValues::UndefinedFloat;
		}
		else {
			return product.m_JetPlusBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr, product.m_validJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr) :
		                                        DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetAbsDeltaEta_bReg", [](event_type const& event, product_type const& product) {
		if (product.m_leadJetIsBJet) {
			return product.m_JetPlusBJetSystemAvailable ? std::abs((product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr).Eta() - (product.m_validJets[1]->p4*product.m_validJets[1]->bjetRegCorr).Eta()) :
		                                        DefaultValues::UndefinedFloat;
		}
		else {
			return product.m_JetPlusBJetSystemAvailable ? std::abs((product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr).Eta() - (product.m_validJets[0]->p4*product.m_validJets[0]->bjetRegCorr).Eta()) :
		                                        DefaultValues::UndefinedFloat;
		}
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jetPlusBJetdiLepPhi_bReg", [](event_type const& event, product_type const& product) {
			return product.m_JetPlusBJetSystemAvailable ? (product.m_JetPlusBJetSystem_bReg + product.m_diLeptonSystem).Phi() : DefaultValues::UndefinedFloat;
	});


	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetPt_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity(product, [](RMDLV highCSVJetPlusBJetSystem_bReg) -> double
	{
		return highCSVJetPlusBJetSystem_bReg.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetEta_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity(product, [](RMDLV highCSVJetPlusBJetSystem_bReg) -> double
	{
		return highCSVJetPlusBJetSystem_bReg.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetPhi_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity(product, [](RMDLV highCSVJetPlusBJetSystem_bReg) -> double
	{
		return highCSVJetPlusBJetSystem_bReg.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetMass_bReg", [this](event_type const& event, product_type const& product) {
		return DiBJetQuantitiesProducer::GetHighCSVJetPlusBJetQuantity(product, [](RMDLV highCSVJetPlusBJetSystem_bReg) -> double
	{
		return highCSVJetPlusBJetSystem_bReg.mass(); });
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetDeltaPhi_bReg", [](event_type const& event, product_type const& product) {

			return product.m_JetPlusBJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr, product.m_validJets[product.m_highCSVJetIndex]->p4*product.m_validJets[product.m_highCSVJetIndex]->bjetRegCorr) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetAbsDeltaEta_bReg", [](event_type const& event, product_type const& product) {

			return product.m_JetPlusBJetSystemAvailable ? std::abs((product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr).Eta() - (product.m_validJets[product.m_highCSVJetIndex]->p4*product.m_validJets[product.m_highCSVJetIndex]->bjetRegCorr).Eta()) :
		                                        DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("highCSVjetPlusBJetdiLepPhi_bReg", [](event_type const& event, product_type const& product) {
			return product.m_JetPlusBJetSystemAvailable ? (product.m_highCSVJetPlusBJetSystem_bReg + product.m_diLeptonSystem).Phi() : DefaultValues::UndefinedFloat;
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

		product.m_diBJetSystem_bReg = (product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr + product.m_bTaggedJets[1]->p4*product.m_bTaggedJets[1]->bjetRegCorr);

	}
	// If only 1 b jet is present, calculate everything from b jet + jet leading in pT (or subleading if leading jet is b jet)
	else if ((product.m_bTaggedJets.size() == 1)&&(product.m_validJets.size() >=2 ))
	{
		product.m_JetPlusBJetSystemAvailable = true;
		product.m_diBJetSystemAvailable = false;
		if (ROOT::Math::VectorUtil::DeltaR(product.m_bTaggedJets[0]->p4,product.m_validJets[0]->p4) < 0.001) {
			product.m_leadJetIsBJet = true;
			product.m_JetPlusBJetSystem = (product.m_validJets[1]->p4 + product.m_bTaggedJets[0]->p4);
			product.m_JetPlusBJetSystem_bReg = (product.m_validJets[1]->p4*product.m_validJets[1]->bjetRegCorr + product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr);

		}
		else {
			product.m_JetPlusBJetSystem_bReg = (product.m_validJets[0]->p4*product.m_validJets[0]->bjetRegCorr + product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr);
			product.m_JetPlusBJetSystem = (product.m_validJets[0]->p4 + product.m_bTaggedJets[0]->p4);			
		}

		float maxCSV = -10.;
		std::string bTaggedJetCSVName = settings.GetBTaggedJetCombinedSecondaryVertexName();
		for(uint i=0;i<product.m_validJets.size();i++) {
			if(ROOT::Math::VectorUtil::DeltaR(product.m_bTaggedJets[0]->p4,product.m_validJets[i]->p4) < 0.001) continue;
			if(static_cast<KJet*>(product.m_validJets[i])->getTag(bTaggedJetCSVName, event.m_jetMetadata)>maxCSV) {
				maxCSV = static_cast<KJet*>(product.m_validJets[i])->getTag(bTaggedJetCSVName, event.m_jetMetadata);
				product.m_highCSVJetIndex = i;
			}
		}
		product.m_highCSVJetPlusBJetSystem = (product.m_validJets[product.m_highCSVJetIndex]->p4 + product.m_bTaggedJets[0]->p4);
		product.m_highCSVJetPlusBJetSystem_bReg = (product.m_validJets[product.m_highCSVJetIndex]->p4*product.m_validJets[product.m_highCSVJetIndex]->bjetRegCorr + product.m_bTaggedJets[0]->p4*product.m_bTaggedJets[0]->bjetRegCorr);

	}
	else
	{
		product.m_JetPlusBJetSystemAvailable = false;
		product.m_diBJetSystemAvailable = false;
	}

}
