
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
	//std::vector<float> tagSelection = settings.GetTagAdditionalCriteria();

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
	bool validDiTauPair = false;
	bool validElectron = (
			(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId(settings.GetTagElectronIDName(), event.m_electronMetadata) > settings.GetElectronMvaIDCutEB1())
			||
			(std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId(settings.GetTagElectronIDName(), event.m_electronMetadata) > settings.GetElectronMvaIDCutEB2())
			||
			(std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId(settings.GetTagElectronIDName(), event.m_electronMetadata) > settings.GetElectronMvaIDCutEE()));
	if (validElectron // ID Check
	&& electron->p4.Pt() > m_tagSelectionCuts.find("pt")->second.at(0) // pt Cut
	&& std::abs((electron)->p4.Eta()) < m_tagSelectionCuts.find("eta")->second.at(0)
	&& electron->pfIso(settings.GetElectronDeltaBetaCorrectionFactor())/(electron)->p4.Pt() < m_tagSelectionCuts.find("iso_sum")->second.at(0) // Isolation Cut
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

bool NewMTTagAndProbePairCandidatesProducer::AdditionalTagCriteria(DiTauPair const &diTauPair, event_type const &event,
																   product_type &product, setting_type const &settings,
																   std::map<std::string, std::vector<float>> m_tagSelectionCuts) const
{
	// Check for overlap of tag muon with a b-tagged jet and veto events where overlap is present.
	KLepton *muon = static_cast<KLepton *>(diTauPair.first);
	bool validDiTauPair = true;
	for (auto bJet : product.m_bTaggedJets)
	{
		if (ROOT::Math::VectorUtil::DeltaR(muon->p4, bJet->p4) < 0.5)
		{
			validDiTauPair = false;
			break;
		}
	}
	return validDiTauPair;
}

bool NewMTTagAndProbePairCandidatesProducer::AdditionalProbeCriteria(DiTauPair const &diTauPair, event_type const &event,
																	 product_type &product, setting_type const &settings,
																	 std::map<std::string, std::vector<float>> m_tagSelectionCuts) const
{
	// Check for overlap of tag muon with a b-tagged jet and veto events where overlap is present.
	KLepton *tau = static_cast<KLepton *>(diTauPair.second);
	bool validDiTauPair = true;
	for (auto bJet : product.m_bTaggedJets)
	{
		if (ROOT::Math::VectorUtil::DeltaR(tau->p4, bJet->p4) < 0.5)
		{
			validDiTauPair = false;
			break;
		}
	}
	return validDiTauPair;
}
