
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EmbeddingMETCorrector.h"

std::string EmbeddingMETCorrector::GetProducerId() const
{
	return "EmbeddingMETCorrector";
}

void EmbeddingMETCorrector::Produce( event_type const& event, product_type & product,
	                     setting_type const& settings) const
{
	LOG(DEBUG) << "\n" << this->GetProducerId() << " -----START-----";
	LOG(DEBUG) << "Processing run:lumi:event " << event.m_eventInfo->nRun << ":" << event.m_eventInfo->nLumi << ":" << event.m_eventInfo->nEvent << "with pipeline " << settings.GetRootFileFolder();

	RMFLV neutrinos;
	for (KGenParticles::const_iterator genParticle = event.m_genParticles->begin();
						genParticle != event.m_genParticles->end(); ++genParticle){
		if (
			((abs(genParticle->pdgId) == 12 )||(abs(genParticle->pdgId) == 14)||(abs(genParticle->pdgId) == 16))
			&& (genParticle->isPrompt() || genParticle->isDirectPromptTauDecayProduct())
			)
			{
				LOG(DEBUG) << "Neutrino found: pt: " << genParticle->p4.Pt() << " / eta: "  << genParticle->p4.Eta() << " / phi: "  << genParticle->p4.Phi() << std::endl;
				neutrinos += genParticle->p4;
			}

	}
		// get fake MET 4-vector by subtracting neutrino 4-vector from MET
		// Note there will be a Z-component to this vector - we will deal with this later
		RMFLV fake_met_vec = (product.m_puppimet.p4 - neutrinos);
		// determine era and channel dependent scale which will be used to scale the fake MET
		float scale = settings.GetEmbedddingFakeMETCorrection();
		// scale the fake met component
		fake_met_vec*=scale;
		// add back the genuine met from the neutrinos 4-vector
		// we only need to determine the phi and pT since we need to remove the Z component from the MET 4-vector
		double new_pt = (fake_met_vec + neutrinos).Pt();
		double new_phi = (fake_met_vec + neutrinos).Phi();
		// set the new MET 4-vector
		// note Z component is eliminated by setting eta to 0., and mass component is eliminated by setting E = pT
		RMFLV new_met_vec(new_pt,0., new_phi, new_pt);
		LOG(DEBUG) << "[INFO] old MET: " << product.m_puppimet.p4.Pt() << std::endl;
		product.m_puppimet.p4 = new_met_vec;
		LOG(DEBUG) << "[INFO] new MET: " << product.m_puppimet.p4.Pt() << std::endl;
		LOG(DEBUG) << this->GetProducerId() << " -----END-----";
}
