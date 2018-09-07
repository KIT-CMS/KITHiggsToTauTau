
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GroupedJetUncertaintyShiftProducer.h"

std::string GroupedJetUncertaintyShiftProducer::GetProducerId() const
{
	return "GroupedJetUncertaintyShiftProducer";
}

void GroupedJetUncertaintyShiftProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	uncertaintyFile = settings.GetJetEnergyCorrectionSplitUncertaintyParameters();
	individualUncertainties = settings.GetJetEnergyCorrectionSplitUncertaintyParameterNames();

	// make sure the necessary parameters are configured
	assert(uncertaintyFile != "");
	if (settings.GetUseGroupedJetEnergyCorrectionUncertainty()) assert(individualUncertainties.size() > 0);

	jetIDVersion = KappaEnumTypes::ToJetIDVersion(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetJetIDVersion())));
	jetID = KappaEnumTypes::ToJetID(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetJetID())));

	// implementation not nice at the moment. feel free to improve it :)
	lowerPtCuts = Utility::ParseMapTypes<std::string, float>(Utility::ParseVectorToMap(settings.GetJetLowerPtCuts()));
	upperAbsEtaCuts = Utility::ParseMapTypes<std::string, float>(Utility::ParseVectorToMap(settings.GetJetUpperAbsEtaCuts()));

	if (lowerPtCuts.size() > 1)
		LOG(FATAL) << "GroupedJetUncertaintyShiftProducer: lowerPtCuts.size() = " << lowerPtCuts.size() << ". Current implementation requires it to be <= 1.";
	if (upperAbsEtaCuts.size() > 1)
		LOG(FATAL) << "GroupedJetUncertaintyShiftProducer: upperAbsEtaCuts.size() = " << upperAbsEtaCuts.size() << ". Current implementation requires it to be <= 1.";
	
	// some inputs needed for b-tagging
	std::map<std::string, std::vector<float> > bTagWorkingPointsTmp = Utility::ParseMapTypes<std::string, float>(
			Utility::ParseVectorToMap(settings.GetBTaggerWorkingPoints())
	);

	// initialize b-tag scale factor class only if shifts are to be applied
	if (settings.GetUseGroupedJetEnergyCorrectionUncertainty()
		&& settings.GetJetEnergyCorrectionUncertaintyShift() != 0.0
		&& settings.GetUseJECShiftsForBJets())
	{
		m_bTagSf = BTagSF(settings.GetBTagScaleFactorFile(), settings.GetBTagEfficiencyFile());
		//m_bTagWorkingPoint = bTagWorkingPointsTmp.begin()->second.at(0);
		m_bTagWorkingPoint = SafeMap::Get(bTagWorkingPointsTmp, settings.GetBTagWPs().at(0)).at(0);
		if (settings.GetApplyBTagSF() && !settings.GetInputIsData())
		{
			m_bTagSFMethod = KappaEnumTypes::ToBTagScaleFactorMethod(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetBTagSFMethod())));
			m_bTagSf.initBtagwp(bTagWorkingPointsTmp.begin()->first);
		}
	}

	for (auto const& uncertainty : individualUncertainties)
	{
		// only do string comparison once per uncertainty
		HttEnumTypes::JetEnergyUncertaintyShiftName individualUncertainty = HttEnumTypes::ToJetEnergyUncertaintyShiftName(uncertainty);
		if (individualUncertainty == HttEnumTypes::JetEnergyUncertaintyShiftName::NONE)
			continue;
		individualUncertaintyEnums.push_back(individualUncertainty);

		// create uncertainty map (only if shifts are to be applied)
		if (settings.GetUseGroupedJetEnergyCorrectionUncertainty()
			&& settings.GetJetEnergyCorrectionUncertaintyShift() != 0.0
			&& individualUncertainty != HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
		{
			JetCorrectorParameters const * jetCorPar = new JetCorrectorParameters(uncertaintyFile, uncertainty);
			JetCorParMap[individualUncertainty] = jetCorPar;

			JetCorrectionUncertainty * jecUnc(new JetCorrectionUncertainty(*JetCorParMap[individualUncertainty]));
			JetUncMap[individualUncertainty] = jecUnc;
		}

		// add quantities to event
		/*std::string njetsQuantity = "njetspt30_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(njetsQuantity, [individualUncertainty](event_type const& event, product_type const& product)
		{
			int nJetsPt30 = 0;
			if ((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				nJetsPt30 = KappaProduct::GetNJetsAbovePtThreshold((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty)->second, 30.0);
			}
			return nJetsPt30;
		});

		std::string mjjQuantity = "mjj_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(mjjQuantity, [individualUncertainty](event_type const& event, product_type const& product)
		{
			if ((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				std::vector<KJet*> shiftedJets = (product.m_correctedJetsBySplitUncertainty).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? (shiftedJets.at(0)->p4 + shiftedJets.at(1)->p4).mass() : -11.f;
			}
			return -11.f;
		});

		std::string jdetaQuantity = "jdeta_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(jdetaQuantity, [individualUncertainty](event_type const& event, product_type const& product)
		{
			float jdeta = -1;
			if ((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				std::vector<KJet*> shiftedJets = (product.m_correctedJetsBySplitUncertainty).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? std::abs(shiftedJets.at(0)->p4.Eta() - shiftedJets.at(1)->p4.Eta()) : -1;
			}
			return jdeta;
		});

		std::string nbjetsQuantity = "nbtag_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(nbjetsQuantity, [individualUncertainty](event_type const& event, product_type const& product)
		{
			int nbtag = 0;
			if ((product.m_correctedBTaggedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				nbtag = KappaProduct::GetNJetsAbovePtThreshold((product.m_correctedBTaggedJetsBySplitUncertainty).find(individualUncertainty)->second, 20.0);
			}
			return nbtag;
		});*/
	}
}

void GroupedJetUncertaintyShiftProducer::Produce(event_type const& event, product_type& product,
		setting_type const& settings) const
{
	// only do all of this if uncertainty shifts should be applied
	if (settings.GetUseGroupedJetEnergyCorrectionUncertainty() && settings.GetJetEnergyCorrectionUncertaintyShift() != 0.0)
	{
		// run over all jets
                for (std::vector<KBasicJet*>::iterator jet = (product.m_validJets).begin();
                                 jet != (product.m_validJets).end(); ++jet)
                        {
                            // add jet momentum to met shift and later subtract shifted momentum in order to get MET shift
                            product.m_MET_shift.p4 += (*jet)->p4;
                            // shift corrected jets
                            double grouped_unc = 0.0;
                            for (auto const& uncertainty : individualUncertaintyEnums)
                            {
				double unc = 0.0;

				if (std::abs((*jet)->p4.Eta()) < 5.2 && (*jet)->p4.Pt() > 9.)
				{
					JetUncMap.at(uncertainty)->setJetEta((*jet)->p4.Eta());
					JetUncMap.at(uncertainty)->setJetPt((*jet)->p4.Pt());
					unc = JetUncMap.at(uncertainty)->getUncertainty(true);
                                        grouped_unc += unc * unc;
				}
                            }
                            grouped_unc = sqrt(grouped_unc);
                            (*jet)->p4 = (*jet)->p4 * (1 + grouped_unc * settings.GetJetEnergyCorrectionUncertaintyShift());
                            product.m_MET_shift.p4 -= (*jet)->p4;
			}
		// sort vectors of shifted jets by pt
		std::sort(product.m_validJets.begin(), product.m_validJets.end(),
				  [](KBasicJet* jet1, KBasicJet* jet2) -> bool
				  { return jet1->p4.Pt() > jet2->p4.Pt(); });

                // reevaluate ID as in ValidJetsProducer
		std::vector<KBasicJet*> shiftedJets;
		std::vector<KJet*> shiftedBTaggedJets;
		for (std::vector<KBasicJet*>::iterator jet = product.m_validJets.begin(); jet != product.m_validJets.end(); ++jet)
		{
			bool validJet = true;

			// passed jet id?
			validJet = validJet && ValidJetsProducer::passesJetID(*jet, jetIDVersion, jetID);

			// kinematic cuts
			// implementation not nice at the moment. feel free to improve it :)
			for (std::map<std::string, std::vector<float> >::const_iterator lowerPtCut = lowerPtCuts.begin(); lowerPtCut != lowerPtCuts.end() && validJet; ++lowerPtCut)
			{
				if ((*jet)->p4.Pt() < *std::max_element(lowerPtCut->second.begin(), lowerPtCut->second.end()))
				{
					validJet = false;
				}
			}
			for (std::map<std::string, std::vector<float> >::const_iterator upperAbsEtaCut = upperAbsEtaCuts.begin(); upperAbsEtaCut != upperAbsEtaCuts.end() && validJet; ++upperAbsEtaCut)
			{
				if (std::abs((*jet)->p4.Eta()) > *std::min_element(upperAbsEtaCut->second.begin(), upperAbsEtaCut->second.end()))
				{
					validJet = false;
				}
			}

			// remove leptons from list of jets via simple DeltaR isolation
			for (std::vector<KLepton*>::const_iterator lepton = product.m_validLeptons.begin();
				 validJet && lepton != product.m_validLeptons.end(); ++lepton)
			{
				validJet = validJet && ROOT::Math::VectorUtil::DeltaR((*jet)->p4, (*lepton)->p4) > settings.GetJetLeptonLowerDeltaRCut();
			}

			// apply additional criteria if needed (check ValidTaggedJetsProducer settings)

			if (validJet)
			{
				shiftedJets.push_back(*jet);
			}
			if (settings.GetUseJECShiftsForBJets())
			{
				// determine if jet is btagged
				bool validBJet = true;
				KJet* tjet = static_cast<KJet*>(*jet);

				float combinedSecondaryVertex = tjet->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);

				if (combinedSecondaryVertex < m_bTagWorkingPoint ||
					std::abs(tjet->p4.eta()) > settings.GetBTaggedJetAbsEtaCut()) {
					validBJet = false;
				}

				//entry point for Scale Factor (SF) of btagged jets
				if (settings.GetApplyBTagSF() && !settings.GetInputIsData())
				{
					//https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#2a_Jet_by_jet_updating_of_the_b
					if (m_bTagSFMethod == KappaEnumTypes::BTagScaleFactorMethod::PROMOTIONDEMOTION) {
					
						int jetflavor = tjet->flavour;
						unsigned int btagSys = BTagSF::kNo;
						unsigned int bmistagSys = BTagSF::kNo;

						bool taggedBefore = validBJet;
						validBJet = m_bTagSf.isbtagged(
								tjet->p4.pt(),
								tjet->p4.eta(),
								combinedSecondaryVertex,
								jetflavor,
								btagSys,
								bmistagSys,
								settings.GetYear(),
								m_bTagWorkingPoint
						);
							
						if (taggedBefore != validBJet)
							LOG_N_TIMES(20, DEBUG) << "Promoted/demoted : " << validBJet;
					}
					
					else if (m_bTagSFMethod == KappaEnumTypes::BTagScaleFactorMethod::OTHER) {
						//todo
					}
				}

				if (validBJet) {
					shiftedBTaggedJets.push_back(tjet);
					validJet = true; //mark jet as not to be deleted
				}
			}
			//delete non valid (b)jets
			//if(!validJet) delete *jet; instead replace collections below
		}

		product.m_validJets = shiftedJets;
		product.m_bTaggedJets = shiftedBTaggedJets;
	}
}

