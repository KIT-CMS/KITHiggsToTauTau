
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EmbeddingMETCorrector.h"
#include <TMath.h>
#include <TF2.h>

std::string EmbeddingMETCorrector::GetProducerId() const
{
	return "EmbeddingMETCorrector";
}

void EmbeddingMETCorrector::Produce( event_type const& event, product_type & product,
	                     setting_type const& settings) const
{
	// Latest version of the Correction:
	// https://indico.cern.ch/event/1018074/contributions/4272593/attachments/2207311/3734956/embed_met_corrections_improved.pdf

	LOG(DEBUG) << "\n" << this->GetProducerId() << " -----START-----";
	LOG(DEBUG) << "Processing run:lumi:event " << event.m_eventInfo->nRun << ":" << event.m_eventInfo->nLumi << ":" << event.m_eventInfo->nEvent << "with pipeline " << settings.GetRootFileFolder();
	int number_of_shifts = settings.GetEmbeddingFakeMETCorrectionNumApplies();

	RMFLV neutrinos;
	for (KGenParticles::const_iterator genParticle = event.m_genParticles->begin();
						genParticle != event.m_genParticles->end(); ++genParticle){
		if (
			((abs(genParticle->pdgId) == 12 )||(abs(genParticle->pdgId) == 14)||(abs(genParticle->pdgId) == 16))
			&& (genParticle->isPrompt() || genParticle->isDirectPromptTauDecayProduct())
			)
			{
				LOG(DEBUG) << "Neutrino found: pt: " << genParticle->p4.Pt() << " / eta: "  << genParticle->p4.Eta() << " / phi: "  << genParticle->p4.Phi();
				neutrinos += genParticle->p4;
			}

	}

		// get fake MET 4-vector by subtracting neutrino 4-vector from MET
		// define a TF2 function to calculate corrected MET i component (i=x,y):
		// Input x is reco METi,
		// y is gen METi
		// function returns corrected reco METi
		std::string scale_str = settings.GetEmbeddingFakeMETCorrection();
		// dont do anythingg if the sf of 1.0 is set
		LOG(DEBUG) << "Using SF: " << scale_str;
		if ((scale_str.compare("1.0") != 0) && number_of_shifts > 0)
		{
			// convert this string of the form "(x-y)*0.984 + y*(1.+-0.002)" to a function
			auto func = new TF2("func", scale_str.c_str());

			double new_px = func->Eval(product.m_puppimet.p4.Px(), neutrinos.Px());
			double new_py = func->Eval(product.m_puppimet.p4.Py(), neutrinos.Py());

			// now build a new vector from the two scaled components
			TVector3 scaled_met(new_px,new_py,0.);
			double new_pt = scaled_met.Pt();
			double new_phi = scaled_met.Phi();
			// set the new MET 4-vector
			// note Z component is eliminated by setting eta to 0., and mass component is eliminated by setting E = pT
			RMFLV new_met_vec(new_pt,0., new_phi, new_pt);
			LOG(DEBUG) << "[INFO] old MET: " << product.m_puppimet.p4.Pt();
			product.m_puppimet.p4 = new_met_vec;
		}
		if (number_of_shifts == 2){
			LOG(DEBUG) << "Applying shift a second time for variation";
			// apply the function shift twice
			auto func = new TF2("func", scale_str.c_str());
			double new_px_2 = func->Eval(product.m_puppimet.p4.Px(), neutrinos.Px());
			double new_py_2 = func->Eval(product.m_puppimet.p4.Py(), neutrinos.Py());
			// now build a new vector from the two scaled components
			TVector3 scaled_met(new_px_2,new_py_2,0.);
			double new_pt_2 = scaled_met.Pt();
			double new_phi_2 = scaled_met.Phi();
			// set the new MET 4-vector
			// note Z component is eliminated by setting eta to 0., and mass component is eliminated by setting E = pT
			RMFLV new_met_vec(new_pt_2,0., new_phi_2, new_pt_2);
			product.m_puppimet.p4 = new_met_vec;
			}

		LOG(DEBUG) << "[INFO] new MET: " << product.m_puppimet.p4.Pt();
		LOG(DEBUG) << this->GetProducerId() << " -----END-----";
}
