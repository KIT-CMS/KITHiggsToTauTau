
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/NewTagAndProbePairCandidatesProducers.h"

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
	double chargedIsolationPtSum = muon->sumChargedHadronPt;
	double neutralIsolationPtSum = muon->sumNeutralHadronEt;
	double photonIsolationPtSum = muon->sumPhotonEt;
	double deltaBetaIsolationPtSum = muon->sumPUPt;
	double isolationPtSum = (chargedIsolationPtSum + std::max(0.0, neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum)) / muon->p4.Pt();

	bool validDiTauPair = false;
	
	if (muon->p4.Pt() > m_tagSelectionCuts.find("pt")->second.at(0) && muon->idMedium() == true && isolationPtSum < m_tagSelectionCuts.find("iso_sum")->second.at(0) && muon->dxy < m_tagSelectionCuts.find("dxy")->second.at(0) && muon->dz < m_tagSelectionCuts.find("dz")->second.at(0))
	{
		validDiTauPair = true;
	}
	LOG(DEBUG) << "Muon1 pt: " << muon->p4.Pt();
	LOG(DEBUG) << "Muon1 Iso Sum: " << muon->idMedium();
	LOG(DEBUG) << "IsolationPtSum: " << isolationPtSum;
	LOG(DEBUG) << "dxy: " << muon->dxy << " < " << m_tagSelectionCuts.find("dxy")->second.at(0);
	LOG(DEBUG) << validDiTauPair;
	return validDiTauPair;
}

std::string NewMMTagAndProbePairCandidatesProducer::GetProducerId() const
{
	return "NewMMTagAndProbePairCandidatesProducer";
}