
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HTT-utilities/RecoilCorrections/interface/RecoilCorrector.h"
#include "HTT-utilities/RecoilCorrections/interface/MEtSys.h"

#include <boost/regex.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>


/**
   \brief Corrects the MET created by the MET producer
   
   Run this producer after the Valid(Tagged)JetsProducer, since it relies on the number of
   jets in the event.
*/


template<class TMet>
class MetCorrectorBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	enum CorrectionMethod { NONE=0, QUANTILE_MAPPING=1, MEAN_RESOLUTION=2, QUANTILE_MAPPING_HIST=3};
	
	MetCorrectorBase(TMet* product_type::*metMemberUncorrected,
			 TMet product_type::*metMemberCorrected,
			 std::vector<float> product_type::*metCorrections,
			 std::string (setting_type::*GetRecoilCorrectorFile)(void) const,
			 std::string (setting_type::*GetMetShiftCorrectorFile)(void) const,
			 bool (setting_type::*GetUpdateMetWithCorrectedLeptons)(void) const,
			 bool (setting_type::*GetUpdateMetWithCorrectedLeptonsFromSignalOnly)(void) const,
			 bool (setting_type::*GetUpdateMetWithBJetRegression)(void) const
	) :
		ProducerBase<HttTypes>(),
		m_metMemberUncorrected(metMemberUncorrected),
		m_metMemberCorrected(metMemberCorrected),
		m_metCorrections(metCorrections),
		GetRecoilCorrectorFile(GetRecoilCorrectorFile),
		GetMetShiftCorrectorFile(GetMetShiftCorrectorFile),
		GetUpdateMetWithCorrectedLeptons(GetUpdateMetWithCorrectedLeptons),
		GetUpdateMetWithCorrectedLeptonsFromSignalOnly(GetUpdateMetWithCorrectedLeptonsFromSignalOnly),
		GetUpdateMetWithBJetRegression(GetUpdateMetWithBJetRegression)
	{
	}

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
		
		m_recoilCorrector = new RecoilCorrector((settings.*GetRecoilCorrectorFile)());
		
		if ((settings.GetMetSysType() != 0) || (settings.GetMetSysShift() != 0))
		{
			m_metShiftCorrector = new MEtSys((settings.*GetMetShiftCorrectorFile)());

			if (settings.GetMetSysType() == 0)
			{
				m_sysType = MEtSys::SysType::Response;
			}
			else if (settings.GetMetSysType() == 1)
			{
				m_sysType = MEtSys::SysType::Resolution;
			}
			else
			{
				//m_sysType = MEtSys::SysType::NoType;
				LOG(FATAL) << "Invalid HttSettings::MetSysType option";
			}
			
			if (settings.GetMetSysShift() > 0)
			{
				m_sysShift = MEtSys::SysShift::Up;
			}
			else
			{
				m_sysShift = MEtSys::SysShift::Down;
			}
		}

		// determine process type, trigger several decisions later
		if (boost::regex_search(settings.GetNickname(), boost::regex("DY.?JetsToLL|(W.?Jets|WG|WGstar)ToLNu|HToTauTau|EWK|HToWW|ttHJetToTT|NMSSM", boost::regex::extended)))
		{
			m_processType = MEtSys::ProcessType::BOSON;
		}
		else if (boost::regex_search(settings.GetNickname(), boost::regex("TT", boost::regex::extended)))
		{
			m_processType = MEtSys::ProcessType::TOP;
		}
		else
		{
			m_processType = MEtSys::ProcessType::EWK;
		}
		m_isWJets = boost::regex_search(settings.GetNickname(), boost::regex("(W.?Jets|WG)ToLNu|EWKW", boost::regex::icase | boost::regex::extended));
		
		m_doMetSys = ((settings.GetMetSysType() != 0) || (settings.GetMetSysShift() != 0));

		if(settings.GetMetCorrectionMethod() == "quantileMapping")
			m_correctionMethod = MetCorrectorBase::CorrectionMethod::QUANTILE_MAPPING;
		else if(settings.GetMetCorrectionMethod() == "meanResolution")
			m_correctionMethod = MetCorrectorBase::CorrectionMethod::MEAN_RESOLUTION;
		else if(settings.GetMetCorrectionMethod() == "quantileMappingHist")
			m_correctionMethod = MetCorrectorBase::CorrectionMethod::QUANTILE_MAPPING_HIST;
		else if(settings.GetMetCorrectionMethod() == "none")
		{
			m_correctionMethod = MetCorrectorBase::CorrectionMethod::NONE;
			LOG(WARNING) << "MetCorrectionMethod is 'none'. No recoil corrections will be applied";
		}
        else
			LOG(FATAL) << "Invalid MetCorrectionMethod option. Available are 'quantileMapping' and 'meanResolution' and 'none'";
        LOG(DEBUG) << "MetCorrectionMethod is " << settings.GetMetCorrectionMethod() << std::endl;

		if (settings.GetMetUncertaintyShift())
		{
			m_metUncertaintyType = HttEnumTypes::ToMETUncertaintyType(settings.GetMetUncertaintyType());
		}

                m_decayChannel = HttEnumTypes::ToDecayChannel(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetChannel())));
                LOG(DEBUG) << "Defining lepton corrections for channel " << settings.GetChannel();
                if (m_decayChannel == HttEnumTypes::DecayChannel::ET)
                {
                        checkFirstElectron = true;
                        checkSecondTau = true;
                }
                else if (m_decayChannel == HttEnumTypes::DecayChannel::MT)
                {
                        checkFirstMuon = true;
                        checkSecondTau = true;
                }
                else if (m_decayChannel == HttEnumTypes::DecayChannel::TT)
                {
                        checkFirstTau = true;
                        checkSecondTau = true;
                }
                else if (m_decayChannel == HttEnumTypes::DecayChannel::EM)
                {
                        checkFirstMuon = true;
                        checkSecondElectron = true;
                }
                else if (m_decayChannel == HttEnumTypes::DecayChannel::MM)
                {
                        checkFirstMuon = true;
                        checkSecondMuon = true;
                }
                else if (m_decayChannel == HttEnumTypes::DecayChannel::EE)
                {
                        checkFirstElectron = true;
                        checkSecondElectron = true;
                }
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		LOG(DEBUG) << "\n" << this->GetProducerId() << " -----START-----";
		LOG(DEBUG) << "Processing run:lumi:event " << event.m_eventInfo->nRun << ":" << event.m_eventInfo->nLumi << ":" << event.m_eventInfo->nEvent << "with pipeline " << settings.GetRootFileFolder();
		assert(m_metMemberUncorrected != nullptr);

		// Retrieve the needed informations from the event content
		// and replace nominal met four vector by one shifted by
		// specific uncertainty in order to propagate it through
		// entire analysis if required by configuration
		float metX = settings.GetMetUncertaintyShift() ? (product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Px() : (product.*m_metMemberUncorrected)->p4.Px();
		float metY = settings.GetMetUncertaintyShift() ? (product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Py() : (product.*m_metMemberUncorrected)->p4.Py();
		float metEnergy = settings.GetMetUncertaintyShift() ? (product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].energy() : (product.*m_metMemberUncorrected)->p4.energy();
		float metResolution = std::sqrt(metEnergy * metEnergy - metX * metX - metY * metY);

		// Recalculate MET if lepton energies have been corrected:
		// MetX' = MetX + Px - Px'
		// MetY' = MetY + Py - Py'
		// MET' = sqrt(MetX' * MetX' + MetY' * MetY')
		if ((settings.*GetUpdateMetWithCorrectedLeptons)())
		{
                        KLV* lep1 = product.m_validDiTauPairCandidates[0].first;
                        KLV* lep2 = product.m_validDiTauPairCandidates[0].second;
                        LOG(DEBUG) << "First pair constituent p4 = " << lep1->p4;
                        LOG(DEBUG) << "Second pair constituent p4 = " << lep2->p4;
			// Electrons
			if (product.m_correctedElectrons.size() > 0) LOG(DEBUG) << "Propagating Electron Corrections to MET";
			for (std::vector<std::shared_ptr<KElectron> >::iterator electron = product.m_correctedElectrons.begin();
				 electron != product.m_correctedElectrons.end(); ++electron)
			{
                                // Check, whether electron corresponds to a pair consituent in the considered decay channel. If not, skip it
                                if ((settings.*GetUpdateMetWithCorrectedLeptonsFromSignalOnly)() && ((checkFirstElectron && electron->get()->p4 != lep1->p4) && (checkSecondElectron && electron->get()->p4 != lep2->p4)))
                                {
                                        LOG(DEBUG) << "\tElectron with p4 = " << electron->get()->p4 << " neglected, since not part of signal pair";
                                        continue;
                                }
				// Only update MET if there actually was a correction applied
				if (Utility::ApproxEqual(electron->get()->p4, const_cast<KLepton*>(product.m_originalLeptons[electron->get()])->p4))
                                {
                                        LOG(DEBUG) << "\tDifference between corrected p4 =  " << electron->get()->p4 << " and original p4 = " << const_cast<KLepton*>(product.m_originalLeptons[electron->get()])->p4 << " too small";
					continue;
                                }

				float eX = electron->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[electron->get()])->p4.Px();
				float eY = electron->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[electron->get()])->p4.Py();
                                LOG(DEBUG) << "\tCorrecting met with (px,py) " << eX << "," << eY << " for electron: " << electron->get()->p4;

				metX -= eX;
				metY -= eY;
			}

			// Muons
			if (product.m_correctedMuons.size() > 0) LOG(DEBUG) << "Propagating Muon Corrections to MET";
			for (std::vector<std::shared_ptr<KMuon> >::iterator muon = product.m_correctedMuons.begin();
				 muon != product.m_correctedMuons.end(); ++muon)
			{
                                // Check, whether muon corresponds to a pair consituent in the considered decay channel. If not, skip it
                                if ((settings.*GetUpdateMetWithCorrectedLeptonsFromSignalOnly)() && ((checkFirstMuon && muon->get()->p4 != lep1->p4) && (checkSecondMuon && muon->get()->p4 != lep2->p4)))
                                {
                                        LOG(DEBUG) << "\tMuon with p4 = " << muon->get()->p4 << " neglected, since not part of signal pair";
                                        continue;
                                }
				// Only update MET if there actually was a correction applied
				if (Utility::ApproxEqual(muon->get()->p4, const_cast<KLepton*>(product.m_originalLeptons[muon->get()])->p4))
                                {
                                        LOG(DEBUG) << "\tDifference between corrected p4 =  " << muon->get()->p4 << " and original p4 = " << const_cast<KLepton*>(product.m_originalLeptons[muon->get()])->p4 << " too small";
					continue;
                                }

				float eX = muon->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[muon->get()])->p4.Px();
				float eY = muon->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[muon->get()])->p4.Py();
                                LOG(DEBUG) << "\tCorrecting met with (px,py) " << eX << "," << eY << " for muon: " << muon->get()->p4;

				metX -= eX;
				metY -= eY;
			}

			// Taus
			if (product.m_correctedTaus.size() > 0) LOG(DEBUG) << "Correcting MET for Tau Corrections";
			for (std::vector<std::shared_ptr<KTau> >::iterator tau = product.m_correctedTaus.begin();
				 tau != product.m_correctedTaus.end(); ++tau)
			{
                                // Check, whether tau corresponds to a pair consituent in the considered decay channel. If not, skip it
                                if ((settings.*GetUpdateMetWithCorrectedLeptonsFromSignalOnly)() && ((checkFirstTau && tau->get()->p4 != lep1->p4) && (checkSecondTau && tau->get()->p4 != lep2->p4)))
                                {
                                        LOG(DEBUG) << "\tTau with p4 = " << tau->get()->p4 << " neglected, since not part of signal pair";
                                        continue;
                                }
				// Only update MET if there actually was a correction applied
				if (Utility::ApproxEqual(tau->get()->p4, const_cast<KLepton*>(product.m_originalLeptons[tau->get()])->p4))
                                {
                                        LOG(DEBUG) << "\tDifference between corrected p4 =  " << tau->get()->p4 << " and original p4 = " << const_cast<KLepton*>(product.m_originalLeptons[tau->get()])->p4 << " too small";
					continue;
                                }

				float eX = tau->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[tau->get()])->p4.Px();
				float eY = tau->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[tau->get()])->p4.Py();
                                LOG(DEBUG) << "\tCorrecting met with (px,py) " << eX << "," << eY << " for tau: " << tau->get()->p4;

				metX -= eX;
				metY -= eY;
			}
		}
		if ((settings.*GetUpdateMetWithBJetRegression)())
		{
			// b-jet regression
			if (product.m_bTaggedJets.size() > 0) LOG(DEBUG) << "Correcting MET for b-jet regression";
			for (uint ibjet=0; ibjet < product.m_bTaggedJets.size(); ibjet++)
				 {
					float eX = (product.m_bTaggedJets.at(ibjet)->p4.Px())*(product.m_bTaggedJets.at(ibjet)->bjetRegCorr) - (product.m_bTaggedJets.at(ibjet)->p4.Px());
					float eY = (product.m_bTaggedJets.at(ibjet)->p4.Py())*(product.m_bTaggedJets.at(ibjet)->bjetRegCorr) - (product.m_bTaggedJets.at(ibjet)->p4.Py());
					LOG(DEBUG) << "\tCorrecting met with (px,py) " << eX << "," << eY << " for b-jet: " << product.m_bTaggedJets.at(ibjet)->p4;
					metX -= eX;
					metY -= eY;
				 }


		}
		
		// Recoil corrections follow
		int nJets30 = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);

		// In selected W+Jets events one of the leptons is faked by hadronic jet and this 
		// jet should be counted as a part of hadronic recoil to the W boson
		if(m_isWJets)
		{
			nJets30 += 1;
		}
		
		float genPx = 0.;  // generator Z(W) px
		float genPy = 0.;  // generator Z(W) py
		float visPx = 0.;  // visible (generator) Z(W) px
		float visPy = 0.;  // visible (generator) Z(W) py
		
		if(m_correctionMethod != MetCorrectorBase::CorrectionMethod::NONE)
                {
                        for (KGenParticles::const_iterator genParticle = event.m_genParticles->begin();
                         genParticle != event.m_genParticles->end(); ++genParticle)
                        {
                                int pdgId = std::abs(genParticle->pdgId);
                                if ( (pdgId >= DefaultValues::pdgIdElectron && pdgId <= DefaultValues::pdgIdNuTau && genParticle->fromHardProcessFinalState()) ||
                                     (genParticle->isDirectHardProcessTauDecayProduct()) )
                                {
                                        genPx += genParticle->p4.Px();
                                        genPy += genParticle->p4.Py();
                                        if ( !(pdgId == DefaultValues::pdgIdNuE || pdgId == DefaultValues::pdgIdNuMu || pdgId == DefaultValues::pdgIdNuTau) )
                                        {
                                                visPx += genParticle->p4.Px();
                                                visPy += genParticle->p4.Py();
                                        }
                                }
                        }
                }
		
		// Save the ingredients for the correction
		(product.*m_metCorrections).push_back(genPx);
		(product.*m_metCorrections).push_back(genPy);
		(product.*m_metCorrections).push_back(visPx);
		(product.*m_metCorrections).push_back(visPy);
		
		float correctedMetX, correctedMetY;
                correctedMetX = metX;
                correctedMetY = metY;
		
		if(m_correctionMethod == MetCorrectorBase::CorrectionMethod::QUANTILE_MAPPING)
			m_recoilCorrector->Correct(
				metX,
				metY,
				genPx,
				genPy,
				visPx,
				visPy,
				nJets30,
				correctedMetX,
				correctedMetY);
		else if(m_correctionMethod == MetCorrectorBase::CorrectionMethod::MEAN_RESOLUTION)
			m_recoilCorrector->CorrectByMeanResolution(
				metX,
				metY,
				genPx,
				genPy,
				visPx,
				visPy,
				nJets30,
				correctedMetX,
				correctedMetY);
		else if(m_correctionMethod == MetCorrectorBase::CorrectionMethod::QUANTILE_MAPPING_HIST)
			m_recoilCorrector->CorrectWithHist(
				metX,
				metY,
				genPx,
				genPy,
				visPx,
				visPy,
				nJets30,
				correctedMetX,
				correctedMetY);
		
		(product.*m_metMemberCorrected) = *(product.*m_metMemberUncorrected);
		
		// Apply the recoil correction to the MET object (only for DY, W and Higgs samples)
		bool apply_RC = m_processType == MEtSys::ProcessType::BOSON && !(m_correctionMethod == MetCorrectorBase::CorrectionMethod::NONE);
		if (apply_RC)
		{
                        LOG(DEBUG) << "Applying recoil & lepton corrections";
			(product.*m_metMemberCorrected).p4.SetPxPyPzE(
				correctedMetX,
				correctedMetY,
				0.,
				std::sqrt(metResolution * metResolution + correctedMetX * correctedMetX + correctedMetY * correctedMetY));
			if (m_correctGlobalMet)
			{
				product.m_met = product.*m_metMemberCorrected;
			}
		}
		else if ((settings.*GetUpdateMetWithCorrectedLeptons)() || (settings.*GetUpdateMetWithBJetRegression)()) // Apply at least corrections from lepton adjustments or b-jet regression
		{
			LOG(DEBUG) << "Applying lepton corrections";
			(product.*m_metMemberCorrected).p4.SetPxPyPzE(
				metX,
				metY,
				0.,
				std::sqrt(metResolution * metResolution + metX * metX + metY * metY));
			if (m_correctGlobalMet)
			{
				product.m_met = product.*m_metMemberCorrected;
			}
		}
		else if (!apply_RC && settings.GetMetUncertaintyShift()) // If no other corrections are applied, use MET shifted by uncertainty if required by configuration. Note that in case of correction this shift is already imported above.
		{
			(product.*m_metMemberCorrected).p4.SetPxPyPzE(
				(product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Px(),
				(product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Py(),
				(product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Pz(),
				(product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].energy());
			if (m_correctGlobalMet)
			{
				product.m_met = product.*m_metMemberCorrected;
			}
		}
		if (!apply_RC)
                {
			(product.*m_metMemberCorrected).p4 += product.m_MET_shift.p4;
			if (m_correctGlobalMet)
			{
				product.m_met = product.*m_metMemberCorrected;
			}
                }
            	LOG(DEBUG) << "Original MET (px,py): " << (product.*m_metMemberUncorrected)->p4.Px() << "," << (product.*m_metMemberUncorrected)->p4.Py() << " corrected MET (px,py): " << (product.*m_metMemberCorrected).p4.Px() << "," << (product.*m_metMemberCorrected).p4.Py();
		
		// Apply the correction to the MET object, if required (done for all the samples)
		if (m_doMetSys && apply_RC)
		{
			float correctedMetShiftX, correctedMetShiftY;
			
			m_metShiftCorrector->ApplyMEtSys(
				(product.*m_metMemberCorrected).p4.Px(), (product.*m_metMemberCorrected).p4.Py(),
				genPx, genPy,
				visPx, visPy,
				nJets30,
				m_sysType,
				m_sysShift,
				correctedMetShiftX,
				correctedMetShiftY
			);
			
			(product.*m_metMemberCorrected).p4.SetPxPyPzE(
				correctedMetShiftX,
				correctedMetShiftY,
				0.,
				std::sqrt(metResolution * metResolution + correctedMetShiftX * correctedMetShiftX + correctedMetShiftY * correctedMetShiftY));
			if (m_correctGlobalMet)
			{
				product.m_met = product.*m_metMemberCorrected;
			}
		}
                LOG(DEBUG) << this->GetProducerId() << " -----END-----";
	}

protected:
	TMet* product_type::*m_metMemberUncorrected;
	TMet product_type::*m_metMemberCorrected;
	std::vector<float> product_type::*m_metCorrections;
	std::string (setting_type::*GetRecoilCorrectorFile)(void) const;
	std::string (setting_type::*GetMetShiftCorrectorFile)(void) const;
	RecoilCorrector* m_recoilCorrector;
	MEtSys* m_metShiftCorrector;
	MEtSys::ProcessType m_processType;
	MEtSys::SysType m_sysType;
	MEtSys::SysShift m_sysShift;
	bool m_isWJets;
	bool m_doMetSys;
	CorrectionMethod m_correctionMethod;
	bool m_correctGlobalMet;
	bool (setting_type::*GetUpdateMetWithCorrectedLeptons)(void) const;
	bool (setting_type::*GetUpdateMetWithCorrectedLeptonsFromSignalOnly)(void) const;
	bool (setting_type::*GetUpdateMetWithBJetRegression)(void) const;

	KMETUncertainty::Type m_metUncertaintyType;
        bool checkFirstElectron = false;
        bool checkSecondElectron = false;
        bool checkFirstMuon = false;
        bool checkSecondMuon = false;
        bool checkFirstTau = false;
        bool checkSecondTau = false;
	HttEnumTypes::DecayChannel m_decayChannel;
};



/**
   \brief Corrector for (PF) MET
*/
class MetCorrector: public MetCorrectorBase<KMET>
{
public:
	MetCorrector();
	virtual void Init(setting_type const& settings) override;
	virtual std::string GetProducerId() const override;
};

/**
   \brief Corrector for MVAMET
*/
class MvaMetCorrector: public MetCorrectorBase<KMET>
{
public:
	MvaMetCorrector();
	virtual void Init(setting_type const& settings) override;
	virtual std::string GetProducerId() const override;
};

/**
   \brief Corrector for PuppiMET
*/
class PuppiMetCorrector: public MetCorrectorBase<KMET>
{
public:
	PuppiMetCorrector();
	virtual void Init(setting_type const& settings) override;
	virtual std::string GetProducerId() const override;
};
