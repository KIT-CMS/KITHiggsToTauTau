
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/NewTagAndProbePairCandidatesProducers.h"
#include "Math/VectorUtil.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"

NewMMTagAndProbePairCandidatesProducer::NewMMTagAndProbePairCandidatesProducer() : NewTagAndProbePairCandidatesProducerBase<KMuon, KMuon>(
																					   &HttTypes::product_type::m_validMuons,
																					   &HttTypes::product_type::m_validMuons)
{
}

bool NewMMTagAndProbePairCandidatesProducer::AdditionalTagCriteria(DiTauPair const &diTauPair, event_type const &event,
																   product_type &product, setting_type const &settings, std::map<std::string, std::vector<float>> m_tagSelectionCuts) const
{
	// Reading the additional criteria for Tag and Probe Leptons
	KLepton *muon = static_cast<KLepton *>(diTauPair.first);
	bool validDiTauPair = false;
	if (muon->p4.Pt() > m_tagSelectionCuts.find("pt")->second.at(0) // pt Cut
	&& muon->idMedium() == true // ID Cut
	&& SafeMap::GetWithDefault(product.m_leptonIsolation,muon,DefaultValues::UndefinedDouble)/(muon)->p4.Pt() < m_tagSelectionCuts.find("iso_sum")->second.at(0) // Isolation Cut
	&& std::abs(muon->dxy) < m_tagSelectionCuts.find("dxy")->second.at(0) // Dxy Cut
	&& std::abs(muon->dz) < m_tagSelectionCuts.find("dz")->second.at(0) // Dz Cut
	&& diTauPair.IsOppositelyCharged()) // Opposite Charge of the pair
	{
		validDiTauPair = true;
	}
	return validDiTauPair;
}

bool NewMMTagAndProbePairCandidatesProducer::AdditionalProbeCriteria(DiTauPair const &diTauPair, event_type const &event,
																   product_type &product, setting_type const &settings, std::map<std::string, std::vector<float>> m_tagSelectionCuts) const
{
	// Reading the additional criteria for Tag and Probe Leptons
	KMuon *muon = static_cast<KMuon *>(diTauPair.second);
	bool validDiTauPair = false;
	if (muon->isTrackerMuon())
	{
		validDiTauPair = true;
	}
	return validDiTauPair;
}

std::string NewMMTagAndProbePairCandidatesProducer::GetProducerId() const
{
	return "NewMMTagAndProbePairCandidatesProducer";
}

NewEETagAndProbePairCandidatesProducer::NewEETagAndProbePairCandidatesProducer() : NewTagAndProbePairCandidatesProducerBase<KElectron, KElectron>(
																					   &HttTypes::product_type::m_validElectrons,
																					   &HttTypes::product_type::m_validElectrons)
{
}

bool NewEETagAndProbePairCandidatesProducer::AdditionalTagCriteria(DiTauPair const &diTauPair, event_type const &event,
																   product_type &product, setting_type const &settings, std::map<std::string, std::vector<float>> m_tagSelectionCuts) const
{
	// Reading the additional criteria for Tag and Probe Leptons
	KElectron *electron = static_cast<KElectron *>(diTauPair.first);
	// if (std::abs(std::abs( 1.0 - electron->eop)*(1.0/electron->ecalEnergy) - std::abs(electron->oneOverEminusOneOverP)) > 0.0001)
	// {
	// 	LOG(WARNING) << "oneOverEminusOneOverP Kappa: " <<  std::abs(electron->oneOverEminusOneOverP) << " / new: " << std::abs( 1.0 - electron->eop)*(1.0/electron->ecalEnergy);
	// } 
	bool validDiTauPair = false;
	if (
	//electron->getId(settings.GetTagElectronIDName(), event.m_electronMetadata) // ID Check
	electron->p4.Pt() > m_tagSelectionCuts.find("pt")->second.at(0) // pt Cut
	&& std::abs((electron)->p4.Eta()) < m_tagSelectionCuts.find("eta")->second.at(0)
	&& SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (diTauPair.first), DefaultValues::UndefinedDouble)/static_cast<KLepton *>(diTauPair.first)->p4.Pt() < m_tagSelectionCuts.find("iso_sum")->second.at(0)
	//&& electron->pfIso(settings.GetElectronDeltaBetaCorrectionFactor())/(electron)->p4.Pt() < m_tagSelectionCuts.find("iso_sum")->second.at(0) // Isolation Cut
	&& std::abs(electron->dxy) < m_tagSelectionCuts.find("dxy")->second.at(0) // Dxy Cut
	&& std::abs(electron->dz) < m_tagSelectionCuts.find("dz")->second.at(0) // Dz Cut
	&& diTauPair.IsOppositelyCharged()) // Opposite Charge of the pair
	{
		validDiTauPair = true;
	}
	return validDiTauPair;
}

std::string NewEETagAndProbePairCandidatesProducer::GetProducerId() const
{
	return "NewEETagAndProbePairCandidatesProducer";
}

NewMTTagAndProbePairCandidatesProducer::NewMTTagAndProbePairCandidatesProducer() : NewTagAndProbePairCandidatesProducerBase<KMuon, KTau>(
																					   &HttTypes::product_type::m_validMuons,
																					   &HttTypes::product_type::m_validTaus)
{
}

std::string NewMTTagAndProbePairCandidatesProducer::GetProducerId() const
{
	return "NewMTTagAndProbePairCandidatesProducer";
}


bool NewMTTagAndProbePairCandidatesProducer::AdditionalCriteria(DiTauPair const &diTauPair, event_type const &event,
																	 product_type &product, setting_type const &settings) const
{
	// Check for overlap of tag muon with a b-tagged jet and veto events where overlap is present.
        KLepton *muon = static_cast<KLepton*>(diTauPair.first);
	KLepton *tau = static_cast<KLepton*>(diTauPair.second);
	bool validDiTauPair = true;
	for (auto bJet : product.m_bTaggedJets)
	{
		if (ROOT::Math::VectorUtil::DeltaR(tau->p4, bJet->p4) > 0.5 && ROOT::Math::VectorUtil::DeltaR(muon->p4, bJet->p4) > 0.5)
		{
			validDiTauPair = false;
                        break;
		}
	}
        LOG(DEBUG) << "Tau pair passing the b jet veto: " << validDiTauPair;
	return validDiTauPair;
}

void NewMTTagAndProbePairCandidatesProducer::Produce(event_type const &event, product_type &product,
                                                     setting_type const &settings) const
{
    NewTagAndProbePairCandidatesProducerBase::Produce(event, product, settings); 
    LOG(DEBUG) << this->GetProducerId() << " -----CONTINUE-----";
    LOG(DEBUG) << "Tau isolation of in unordered pairs:";
    for (std::vector<DiTauPair>::const_iterator pair = product.m_validDiTauPairCandidates.begin(); pair != product.m_validDiTauPairCandidates.end(); pair++)
    {
        LOG(DEBUG) << pair->second->p4.Pt()*SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, static_cast<KLepton*>(pair->second), static_cast<double>(static_cast<KLepton*>(pair->second)->pfIso()));
    }

    std::sort(product.m_validDiTauPairCandidates.begin(), product.m_validDiTauPairCandidates.end(),
              DiTauPairIsoPtComparator(&(product.m_leptonIsolationOverPt), settings.GetDiTauPairIsTauIsoMVA()));

    LOG(DEBUG) << "Tau isolation of ordered pairs:";
    for (std::vector<DiTauPair>::const_iterator pair = product.m_validDiTauPairCandidates.begin(); pair != product.m_validDiTauPairCandidates.end(); pair++)
    {
        LOG(DEBUG) << pair->second->p4.Pt()*SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, static_cast<KLepton*>(pair->second), static_cast<double>(static_cast<KLepton*>(pair->second)->pfIso()));
    }

    // Invalidate all pairs except the one with the most isolated tau.
    if (product.m_validDiTauPairCandidates.size() > 1)
    {
        LOG(DEBUG) << "Invalidate " << product.m_validDiTauPairCandidates.end() - (product.m_validDiTauPairCandidates.begin()+1) << " tau pair(s).";
        std::move(product.m_validDiTauPairCandidates.begin()+1, product.m_validDiTauPairCandidates.end(), std::back_inserter(product.m_invalidDiTauPairCandidates));
        product.m_validDiTauPairCandidates.erase(product.m_validDiTauPairCandidates.begin()+1, product.m_validDiTauPairCandidates.end());
    }
    LOG(DEBUG) << this->GetProducerId() << "-----END-----";
}


NewETTagAndProbePairCandidatesProducer::NewETTagAndProbePairCandidatesProducer() : NewTagAndProbePairCandidatesProducerBase<KElectron, KTau>(
																					   &HttTypes::product_type::m_validElectrons,
																					   &HttTypes::product_type::m_validTaus)
{
}

std::string NewETTagAndProbePairCandidatesProducer::GetProducerId() const
{
	return "NewETTagAndProbePairCandidatesProducer";
}


bool NewETTagAndProbePairCandidatesProducer::AdditionalCriteria(DiTauPair const &diTauPair, event_type const &event,
																	 product_type &product, setting_type const &settings) const
{
	// Check for overlap of tag electron with a b-tagged jet and veto events where overlap is present.
        KElectron *electron = static_cast<KElectron*>(diTauPair.first);
	KLepton *tau = static_cast<KLepton*>(diTauPair.second);
	bool validDiTauPair = true;
	for (auto bJet : product.m_bTaggedJets)
	{
		if (ROOT::Math::VectorUtil::DeltaR(tau->p4, bJet->p4) > 0.5 && ROOT::Math::VectorUtil::DeltaR(electron->p4, bJet->p4) > 0.5)
		{
			validDiTauPair = false;
                        break;
		}
	}
        LOG(DEBUG) << "Tau pair passing the b jet veto: " << validDiTauPair;
	return validDiTauPair;
}

void NewETTagAndProbePairCandidatesProducer::Produce(event_type const &event, product_type &product,
                                                     setting_type const &settings) const
{
    NewTagAndProbePairCandidatesProducerBase::Produce(event, product, settings); 
    LOG(DEBUG) << this->GetProducerId() << " -----CONTINUE-----";
    LOG(DEBUG) << "Tau isolation of in unordered pairs:";
    for (std::vector<DiTauPair>::const_iterator pair = product.m_validDiTauPairCandidates.begin(); pair != product.m_validDiTauPairCandidates.end(); pair++)
    {
        LOG(DEBUG) << pair->second->p4.Pt()*SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, static_cast<KLepton*>(pair->second), static_cast<double>(static_cast<KLepton*>(pair->second)->pfIso()));
    }

    std::sort(product.m_validDiTauPairCandidates.begin(), product.m_validDiTauPairCandidates.end(),
              DiTauPairIsoPtComparator(&(product.m_leptonIsolationOverPt), settings.GetDiTauPairIsTauIsoMVA()));

    LOG(DEBUG) << "Tau isolation of ordered pairs:";
    for (std::vector<DiTauPair>::const_iterator pair = product.m_validDiTauPairCandidates.begin(); pair != product.m_validDiTauPairCandidates.end(); pair++)
    {
        LOG(DEBUG) << pair->second->p4.Pt()*SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, static_cast<KLepton*>(pair->second), static_cast<double>(static_cast<KLepton*>(pair->second)->pfIso()));
    }

    // Invalidate all pairs except the one with the most isolated tau.
    if (product.m_validDiTauPairCandidates.size() > 1)
    {
        LOG(DEBUG) << "Invalidate " << product.m_validDiTauPairCandidates.end() - (product.m_validDiTauPairCandidates.begin()+1) << " tau pair(s).";
        std::move(product.m_validDiTauPairCandidates.begin()+1, product.m_validDiTauPairCandidates.end(), std::back_inserter(product.m_invalidDiTauPairCandidates));
        product.m_validDiTauPairCandidates.erase(product.m_validDiTauPairCandidates.begin()+1, product.m_validDiTauPairCandidates.end());
    }
    LOG(DEBUG) << this->GetProducerId() << "-----END-----";
}

