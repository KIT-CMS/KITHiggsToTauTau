
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TaggedJetUncertaintyShiftProducer.h"

std::string TaggedJetUncertaintyShiftProducer::GetProducerId() const
{
	return "TaggedJetUncertaintyShiftProducer";
}

void TaggedJetUncertaintyShiftProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// Settings JEC
	uncertaintyFile = settings.GetJetEnergyCorrectionSplitUncertaintyParameters();
	individualUncertainties = settings.GetJetEnergyCorrectionSplitUncertaintyParameterNames();
	assert(uncertaintyFile != "");
	assert(individualUncertainties.size() > 0);
	jec_shifts_applied = settings.GetJetEnergyCorrectionSplitUncertainty() && settings.GetJetEnergyCorrectionUncertaintyShift() != 0.0;

	// Settings Jet ID
	jetIDVersion = KappaEnumTypes::ToJetIDVersion(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetJetIDVersion())));
	jetID = KappaEnumTypes::ToJetID(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetJetID())));
	lowerPtCuts = Utility::ParseMapTypes<std::string, float>(Utility::ParseVectorToMap(settings.GetJetLowerPtCuts()));
	upperAbsEtaCuts = Utility::ParseMapTypes<std::string, float>(Utility::ParseVectorToMap(settings.GetJetUpperAbsEtaCuts()));

	if (lowerPtCuts.size() > 1)
		LOG(FATAL) << "TaggedJetUncertaintyShiftProducer: lowerPtCuts.size() = " << lowerPtCuts.size() << ". Current implementation requires it to be <= 1.";

	if (upperAbsEtaCuts.size() > 1)
		LOG(FATAL) << "TaggedJetUncertaintyShiftProducer: upperAbsEtaCuts.size() = " << upperAbsEtaCuts.size() << ". Current implementation requires it to be <= 1.";

	// Settings BTagged Jet ID : some inputs needed for b-tagging
	std::map<std::string, std::vector<float> > bTagWorkingPointsTmp = Utility::ParseMapTypes<std::string, float>(Utility::ParseVectorToMap(settings.GetBTaggerWorkingPoints()));

	// Initialize b-tag scale factor class only if shifts are to be applied
	if (jec_shifts_applied && settings.GetUseJECShiftsForBJets())
	{
		std::string f_btag_sf = settings.GetBTagScaleFactorFile();
		std::string f_btag_efff = settings.GetBTagEfficiencyFile();
		assert(!f_btag_sf.empty() && "BTagScaleFactorFile config is not set");
		assert(!f_btag_efff.empty() && "BTagEfficiencyFile config is not set");

		m_bTagSf = BTagSF(f_btag_sf, f_btag_efff);
		m_bTagWorkingPoint = bTagWorkingPointsTmp.begin()->second.at(0);

		if (settings.GetApplyBTagSF() && !settings.GetInputIsData())
		{
			m_bTagSFMethod = KappaEnumTypes::ToBTagScaleFactorMethod(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetBTagSFMethod())));
			m_bTagSf.initBtagwp(bTagWorkingPointsTmp.begin()->first);
		}
	}

	for (auto const& uncertainty : individualUncertainties)
	{
		// Construct list of enum individual uncertainties
		HttEnumTypes::JetEnergyUncertaintyShiftName individualUncertainty = HttEnumTypes::ToJetEnergyUncertaintyShiftName(uncertainty);
		if (individualUncertainty == HttEnumTypes::JetEnergyUncertaintyShiftName::NONE) continue;
		individualUncertaintyEnums.push_back(individualUncertainty);

		// Create uncertainty map (only if shifts are to be applied)
		if (jec_shifts_applied && individualUncertainty != HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
		{
			JetCorrectorParameters jetCorPar(uncertaintyFile, uncertainty);
			JetUncMap[individualUncertainty] = std::make_unique<JetCorrectionUncertainty>(jetCorPar);
		}

		// Add quantities to event
		std::string njetsQuantity = "njetspt30_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(njetsQuantity, [individualUncertainty](event_type const& event, product_type const& product, setting_type const& settings)
		{
			int nJetsPt30 = 0;
			if ((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				nJetsPt30 = KappaProduct::GetNJetsAbovePtThreshold((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty)->second, 30.0);
			}
			return nJetsPt30;
		});

		std::string mjjQuantity = "mjj_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(mjjQuantity, [individualUncertainty](event_type const& event, product_type const& product, setting_type const& settings)
		{
			if ((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				std::vector<std::shared_ptr<KJet> > const shiftedJets = (product.m_correctedJetsBySplitUncertainty).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? (shiftedJets.at(0)->p4 + shiftedJets.at(1)->p4).mass() : -11.f;
			}
			return -11.f;
		});

		std::string jdetaQuantity = "jdeta_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(jdetaQuantity, [individualUncertainty](event_type const& event, product_type const& product, setting_type const& settings)
		{
			float jdeta = -1;
			if ((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				std::vector<std::shared_ptr<KJet> > const shiftedJets = (product.m_correctedJetsBySplitUncertainty).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? std::abs(shiftedJets.at(0)->p4.Eta() - shiftedJets.at(1)->p4.Eta()) : -1;
			}
			return jdeta;
		});

		std::string nbjetsQuantity = "nbtag_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(nbjetsQuantity, [individualUncertainty](event_type const& event, product_type const& product, setting_type const& settings)
		{
			int nbtag = 0;
			if ((product.m_correctedBTaggedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				nbtag = KappaProduct::GetNJetsAbovePtThreshold((product.m_correctedBTaggedJetsBySplitUncertainty).find(individualUncertainty)->second, 20.0);
			}
			return nbtag;
		});
	}
}

void TaggedJetUncertaintyShiftProducer::Produce(event_type const& event, product_type& product,
		setting_type const& settings) const
{
	// Only do all of this if uncertainty shifts should be applied
	if (jec_shifts_applied)
	{
		// Shifting copies of previously corrected jets
		std::vector<double> closureUncertainty((product.m_correctedTaggedJets).size(), 0.);

		(product.m_correctedJetsBySplitUncertainty).clear();
		(product.m_correctedBTaggedJetsBySplitUncertainty).clear();

		for (auto const& uncertainty : individualUncertaintyEnums)
		{
			// Construct copies of jets in order not to modify actual (corrected) jets by the uncertainty
			std::vector<std::shared_ptr<KJet>> shifted_copied_jets;
			for (typename std::vector<std::shared_ptr<KJet> >::iterator jet = (product.m_correctedTaggedJets).begin(); jet != (product.m_correctedTaggedJets).end(); ++jet)
				shifted_copied_jets.push_back(std::make_shared<KJet>(*(jet->get())));

			unsigned iJet = 0;
			for (std::vector<std::shared_ptr<KJet>>::iterator jet = shifted_copied_jets.begin(); jet != shifted_copied_jets.end(); ++jet, ++iJet)
			{
				double unc = 0;
				if (std::abs((*jet)->p4.Eta()) < 5.2 && (*jet)->p4.Pt() > 9. && uncertainty != HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
				{
					JetUncMap.at(uncertainty)->setJetEta((*jet)->p4.Eta());
					JetUncMap.at(uncertainty)->setJetPt((*jet)->p4.Pt());
					unc = JetUncMap.at(uncertainty)->getUncertainty(true);
				}
				closureUncertainty.at(iJet) = closureUncertainty.at(iJet) + pow(unc, 2);

				// Evaluating in last loop iteration if evaluated
				if (uncertainty == HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
					unc = std::sqrt(closureUncertainty.at(iJet));

				// Varying just the 4-momenta by uncertainty
				(*jet)->p4 = (*jet)->p4 * (1 + unc * settings.GetJetEnergyCorrectionUncertaintyShift());
			}

			// Sort vectors of shifted jets (shifted_copied_jets holds jets varied maximum by one uncertainty) by pt
			std::sort(shifted_copied_jets.begin(), shifted_copied_jets.end(),
					  [](std::shared_ptr<KJet> const jet1, std::shared_ptr<KJet> const jet2) -> bool
					  { return jet1->p4.Pt() > jet2->p4.Pt(); }
			);

			// Create new vector from shifted jets that pass ID as in ValidJetsProducer
			std::vector<std::shared_ptr<KJet>> shiftedJets;
			std::vector<std::shared_ptr<KJet>> shiftedBTaggedJets;
			for (std::vector<std::shared_ptr<KJet>>::iterator jet = shifted_copied_jets.begin(); jet != shifted_copied_jets.end(); ++jet)
			{
				bool validJet = true;

				// Passing jet ID
				validJet = validJet && ValidJetsProducer::passesJetID((*jet).get(), jetIDVersion, jetID);

				// Kinematical cuts
				for (std::map<std::string, std::vector<float> >::const_iterator lowerPtCut = lowerPtCuts.begin(); lowerPtCut != lowerPtCuts.end() && validJet; ++lowerPtCut)
					if ((*jet)->p4.Pt() < *std::max_element(lowerPtCut->second.begin(), lowerPtCut->second.end()))
						validJet = false;

				for (std::map<std::string, std::vector<float> >::const_iterator upperAbsEtaCut = upperAbsEtaCuts.begin(); upperAbsEtaCut != upperAbsEtaCuts.end() && validJet; ++upperAbsEtaCut)
					if (std::abs((*jet)->p4.Eta()) > *std::min_element(upperAbsEtaCut->second.begin(), upperAbsEtaCut->second.end()))
						validJet = false;

				// Remove leptons from list of jets via simple DeltaR isolation eg failed -> is lepton not a jet
				for (std::vector<KLepton*>::const_iterator lepton = product.m_validLeptons.begin(); validJet && lepton != product.m_validLeptons.end(); ++lepton)
					validJet = validJet && ROOT::Math::VectorUtil::DeltaR((*jet)->p4, (*lepton)->p4) > settings.GetJetLeptonLowerDeltaRCut();

				// Apply additional criteria if needed (check ValidTaggedJetsProducer settings)
				if (validJet) shiftedJets.push_back(*jet);

				if (settings.GetUseJECShiftsForBJets())
				{
					auto tjet = static_cast<std::shared_ptr<KJet>>(*jet);

					// Determine if jet is btagged
					bool validBJet = true;
					float combinedSecondaryVertex = tjet->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);

					if (combinedSecondaryVertex < m_bTagWorkingPoint || std::abs(tjet->p4.eta()) > settings.GetBTaggedJetAbsEtaCut())
						validBJet = false;

					// Entry point for Scale Factor (SF) of btagged jets
					if (settings.GetApplyBTagSF() && !settings.GetInputIsData())
					{
						//https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#2a_Jet_by_jet_updating_of_the_b
						if (m_bTagSFMethod == KappaEnumTypes::BTagScaleFactorMethod::PROMOTIONDEMOTION)
						{

							int jetflavor = tjet->hadronFlavour;
							unsigned int btagSys = BTagSF::kNo;
							unsigned int bmistagSys = BTagSF::kNo;

							bool taggedBefore = validBJet;
							validBJet = m_bTagSf.isbtagged(
									tjet->p4.pt(),
									tjet->p4.eta(),
									tjet->p4.phi(),
									combinedSecondaryVertex,
									jetflavor,
									btagSys,
									bmistagSys,
									settings.GetYear(),
									m_bTagWorkingPoint
							);

							if (taggedBefore != validBJet) LOG_N_TIMES(20, DEBUG) << "Promoted/demoted : " << validBJet;
						}
						else if (m_bTagSFMethod == KappaEnumTypes::BTagScaleFactorMethod::OTHER)
						{
							// TODO
						}
					}
					//check again non-btag related jet selection criteria as promote/demote scaling ignores them
					validBJet = validBJet && (std::abs(tjet->p4.eta()) <= settings.GetBTaggedJetAbsEtaCut());

					if (validBJet)
					{
						shiftedBTaggedJets.push_back(tjet);
						validJet = true; // Mark jet as not to be deleted
					}
				}

				// Delete non valid (b)jets
				// if (!validJet) delete *jet;
			}

			(product.m_correctedJetsBySplitUncertainty)[uncertainty] = shiftedJets;
			(product.m_correctedBTaggedJetsBySplitUncertainty)[uncertainty] = shiftedBTaggedJets;
		}
	}
}

