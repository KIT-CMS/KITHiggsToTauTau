
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/NewTagAndProbePairCandidatesProducers.h"


NewMMTagAndProbePairCandidatesProducer::NewMMTagAndProbePairCandidatesProducer() :
	NewTagAndProbePairCandidatesProducerBase<KMuon, KMuon>(
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_validMuons
	)
{
	   
}

bool NewMMTagAndProbePairCandidatesProducer::AdditionalTagCriteria(DiTauPair const& diTauPair, event_type const& event,
                            product_type& product, setting_type const& settings) const
{
	// Reading the additional criteria for Tag and Probe Leptons
	std::vector<float> tagSelection = settings.GetTagAdditionalCriteria();
	KLepton* muon = static_cast<KLepton*>(diTauPair.first);
	double chargedIsolationPtSum = muon->sumChargedHadronPt;
	double neutralIsolationPtSum = muon->sumNeutralHadronEt;
	double photonIsolationPtSum = muon->sumPhotonEt;
	double deltaBetaIsolationPtSum = muon->sumPUPt;
	double isolationPtSum = (chargedIsolationPtSum + std::max(0.0,neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum))/muon->p4.Pt();
		
	bool validDiTauPair = false;
	if (diTauPair.first->p4.Pt() > tagSelection[0] && (static_cast<KLepton*>(diTauPair.first)->idMedium() == true) && isolationPtSum < 0.15)
	{
		validDiTauPair = true;
	}
	LOG(DEBUG) << "Muon1 pt: " << diTauPair.first->p4.Pt();
	LOG(DEBUG) << "Muon1 Iso Sum: " << static_cast<KLepton*>(diTauPair.first)->idMedium();
	LOG(DEBUG) << "IsolationPtSum: " << isolationPtSum;
	LOG(DEBUG) << validDiTauPair;

	return validDiTauPair;
}

std::string NewMMTagAndProbePairCandidatesProducer::GetProducerId() const
{
	return "NewMMTagAndProbePairCandidatesProducer";
}