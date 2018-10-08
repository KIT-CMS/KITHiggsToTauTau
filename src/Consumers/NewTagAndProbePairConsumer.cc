#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/NewTagAndProbePairConsumer.h"

NewMMTagAndProbePairConsumer::NewMMTagAndProbePairConsumer() : NewTagAndProbePairConsumerBase()
{
}
void NewMMTagAndProbePairConsumer::AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
				 					 std::map<std::string, bool>& BoolQuantities,
                                                                         std::map<std::string, int>& IntQuantities,
                                                                         std::map<std::string, float>& FloatQuantities)
{
	if (quantity == "id_t")
	{
		BoolQuantities["id_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->idMedium();
	}
	else if (quantity == "id_p")
	{
		BoolQuantities["id_p"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->idMedium();
	}
}

std::string NewMMTagAndProbePairConsumer::GetConsumerId() const
{
	return "NewMMTagAndProbePairConsumer";
}

NewEETagAndProbePairConsumer::NewEETagAndProbePairConsumer() : NewTagAndProbePairConsumerBase()
{
}
void NewEETagAndProbePairConsumer::AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
				 					 std::map<std::string, bool>& BoolQuantities,
                                                                         std::map<std::string, int>& IntQuantities,
                                                                         std::map<std::string, float>& FloatQuantities)
{
	if (quantity == "id_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		BoolQuantities["id_t"] = electron->getId(settings.GetTagElectronIDName(), event.m_electronMetadata);
	}
	else if (quantity == "id_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		BoolQuantities["id_p"] = electron->getId(settings.GetTagElectronIDName(), event.m_electronMetadata);
	}
    if (quantity == "id_90_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		BoolQuantities["id_90_t"] = electron->getId(settings.GetTagElectronSecondIDName(), event.m_electronMetadata);
	}
	else if (quantity == "id_90_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		BoolQuantities["id_90_p"] = electron->getId(settings.GetTagElectronSecondIDName(), event.m_electronMetadata);
	}
}

std::string NewEETagAndProbePairConsumer::GetConsumerId() const
{
	return "NewEETagAndProbePairConsumer";
}

NewMTTagAndProbePairConsumer::NewMTTagAndProbePairConsumer() : NewTagAndProbePairConsumerBase()
{
}

void NewMTTagAndProbePairConsumer::AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
				 					 std::map<std::string, bool>& BoolQuantities,
                                                                         std::map<std::string, int>& IntQuantities,
                                                                         std::map<std::string, float>& FloatQuantities)
{
	if (quantity == "id_t")
	{
		BoolQuantities["id_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->idMedium();
	}
        // else if (quantity == "isOS")
        // {
        //         BoolQuantities["isOS"] = product.m_validDiTauPairCandidates.at(0).IsOppositelyCharged(); 
        // }
        // TODO: resolve issues with const product and non const method IsOppositelyCharged

        std::vector<std::string> tauDiscriminators;
        tauDiscriminators.push_back("againstElectronVLooseMVA6");
        tauDiscriminators.push_back("againstElectronLooseMVA6");
        tauDiscriminators.push_back("againstElectronMediumMVA6");
        tauDiscriminators.push_back("againstElectronTightMVA6");
        tauDiscriminators.push_back("againstElectronVTightMVA6");
        tauDiscriminators.push_back("againstMuonLoose3");
        tauDiscriminators.push_back("againstMuonTight3");
        tauDiscriminators.push_back("byIsolationMVArun2v1DBoldDMwLTraw");
        tauDiscriminators.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byLooseIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byMediumIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byTightIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byVTightIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byIsolationMVArun2017v2DBoldDMwLTraw2017");
        tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byVLooseIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byLooseIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byMediumIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byTightIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byVTightIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byVVTightIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byIsolationMVArun2017v1DBoldDMwLTraw2017");
        tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byVLooseIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byLooseIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byMediumIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byTightIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byVTightIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byVVTightIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("decayModeFinding");

        for (std::string tauDiscriminator : tauDiscriminators)
        {
            if (quantity == tauDiscriminator + "_p")
            {
                FloatQuantities[tauDiscriminator+"_p"] = static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->getDiscriminator(tauDiscriminator, event.m_tauMetadata);
            }
        }
        if (quantity == "Met")
        {
                FloatQuantities["Met"] = (static_cast<HttProduct const&>(product)).m_met.p4.Pt();
        }
        else if (quantity == "MT")
        {
                FloatQuantities["MT"] = Quantities::CalculateMt(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).first)->p4,product.m_met.p4);
        }

        if (quantity == "decayMode_p")
        {
            IntQuantities["decayMode_p"] = static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->decayMode;
        }
}

std::string NewMTTagAndProbePairConsumer::GetConsumerId() const
{
	return "NewMTTagAndProbePairConsumer";
}
