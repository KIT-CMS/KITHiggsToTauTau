
#pragma once

#include <cstdint>
#include <cassert>

#include <boost/algorithm/string/predicate.hpp>

#include <TTree.h>
#include <Math/Vector4D.h>
#include <Math/Vector4Dfwd.h>
#include "TMath.h"

#include "Artus/Core/interface/EventBase.h"
#include "Artus/Core/interface/ProductBase.h"
#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Configuration/interface/SettingsBase.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

#include "Kappa/DataFormats/interface/Kappa.h"
#include <boost/regex.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

//template <class HttTypes>
class NewTagAndProbePairConsumerBase : public ConsumerBase<HttTypes>
{
  public:
	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	// std::string GetConsumerId() const override
	// {
	// 	return "NewTagAndProbePairConsumer";
	// }

	void Init(setting_type const &settings) override
	{
		ConsumerBase<HttTypes>::Init(settings);

		//fill quantity maps
		IntQuantities["run"] = DefaultValues::UndefinedInt;
		IntQuantities["lumi"] = DefaultValues::UndefinedInt;
		IntQuantities["evt"] = DefaultValues::UndefinedInt;

		FloatQuantities["pt_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["eta_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["phi_t"] = DefaultValues::UndefinedFloat;
		BoolQuantities["id_t"] = false;
		FloatQuantities["iso_t"] = DefaultValues::UndefinedFloat;

		FloatQuantities["pt_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["eta_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["phi_p"] = DefaultValues::UndefinedFloat;
		BoolQuantities["id_p"] = false;
		FloatQuantities["iso_p"] = DefaultValues::UndefinedFloat;

		FloatQuantities["m_ll"] = DefaultValues::UndefinedFloat;
		FloatQuantities["Met"] = DefaultValues::UndefinedFloat;
		FloatQuantities["MT"] = DefaultValues::UndefinedFloat;

		FloatQuantities["againstMuonLoose3_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstMuonTight3_p"] = DefaultValues::UndefinedFloat;
		
		FloatQuantities["againstElectronVLooseMVA6_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstElectronLooseMVA6_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstElectronMediumMVA6_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstElectronTightMVA6_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstElectronVTightMVA6_p"] = DefaultValues::UndefinedFloat;

		FloatQuantities["byVVLooseIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVLooseIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byLooseIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVLooseIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byTightIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVTightIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVVTightIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		BoolQuantities["isOS"] = false;

		BoolQuantities["id_90_t"] = false;
		BoolQuantities["id_90_p"] = false;

		IntQuantities["decayModeFinding_p"] = DefaultValues::UndefinedInt;

		// IntQuantities["trg_t_IsoMu24"]=false;
		// IntQuantities["trg_t_IsoMu27"]=false;
		// IntQuantities["trg_p_IsoMu24"]=false;
		// IntQuantities["trg_p_IsoMu27"]=false;
		// Create Map entries for selected trigger quantities
		m_hltFiredBranchNames = Utility::ParseVectorToMap(settings.GetHLTBranchNames());
		for (auto hltNames : m_hltFiredBranchNames)
		{
			BoolQuantities[hltNames.first] = false;
		}
		// create tree
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree = new TTree("ntuple", ("Tree for Pipeline \"" + settings.GetName() + "\"").c_str());

		// create branches
		for (std::vector<std::string>::iterator quantity = settings.GetQuantities().begin();
			 quantity != settings.GetQuantities().end(); ++quantity)
		{
			if (BoolQuantities.find(*quantity) != BoolQuantities.end())
			{
				m_tree->Branch(quantity->c_str(), &(BoolQuantities[*quantity]), (*quantity + "/O").c_str());
			}
			else if (IntQuantities.find(*quantity) != IntQuantities.end())
			{
				m_tree->Branch(quantity->c_str(), &(IntQuantities[*quantity]), (*quantity + "/I").c_str());
			}
			else if (FloatQuantities.find(*quantity) != FloatQuantities.end())
			{
				m_tree->Branch(quantity->c_str(), &(FloatQuantities[*quantity]), (*quantity + "/F").c_str());
			}
		}
	}

	void ProcessFilteredEvent(event_type const &event, product_type const &product, setting_type const &settings) override
	{
		ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings);
		LOG(DEBUG) << "Starting to write quantities to file!";
		// calculate values
		std::vector<std::string> tagCheckTriggerMatchByHltName = settings.GetCheckTagTriggerMatch();
		std::vector<std::string> probeCheckTriggerMatchByHltName = settings.GetCheckProbeTriggerMatch();
		//bool IsData = settings.GetInputIsData();
		for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
		{
			for (std::vector<std::string>::iterator quantity = settings.GetQuantities().begin();
				 quantity != settings.GetQuantities().end(); ++quantity)
			{
				if (*quantity == "run")
				{
					IntQuantities["run"] = event.m_eventInfo->nRun;
				}
				else if (*quantity == "lumi")
				{
					IntQuantities["lumi"] = event.m_eventInfo->nLumi;
				}
				else if (*quantity == "evt")
				{
					IntQuantities["evt"] = event.m_eventInfo->nEvent;
				}
				else if (*quantity == "pt_t")
				{
					FloatQuantities["pt_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4.Pt();
				}
				else if (*quantity == "eta_t")
				{
					FloatQuantities["eta_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4.Eta();
				}
				else if (*quantity == "phi_t")
				{
					FloatQuantities["phi_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4.Phi();
				}
				else if (*quantity == "iso_t")
				{
<<<<<<< HEAD
					// double chargedIsolationPtSum = TagAndProbePair->first->sumChargedHadronPtR04;
					// double neutralIsolationPtSum = TagAndProbePair->first->sumNeutralHadronEtR04;
					// double photonIsolationPtSum = TagAndProbePair->first->sumPhotonEtR04;
					// double deltaBetaIsolationPtSum = TagAndProbePair->first->sumPUPtR04;
					// FloatQuantities["iso_t"] = (chargedIsolationPtSum + std::max(0.0, neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum)) / TagAndProbePair->first->p4.Pt();
					// FloatQuantities["iso_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->isolationPtSum();
=======
>>>>>>> Add producer and consumer for tau leg measurements in the mt channel
					FloatQuantities["iso_t"] = SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (product.m_validDiTauPairCandidates.at(i).first), DefaultValues::UndefinedDouble);
				}
				else if (*quantity == "pt_p")
				{
					FloatQuantities["pt_p"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4.Pt();
				}
				else if (*quantity == "eta_p")
				{
					FloatQuantities["eta_p"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4.Eta();
				}
				else if (*quantity == "phi_p")
				{
					FloatQuantities["phi_p"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4.Phi();
				}
				else if (*quantity == "iso_p")
				{
<<<<<<< HEAD
					// 	double chargedIsolationPtSum = TagAndProbePair->second->sumChargedHadronPtR04;
					// 	double neutralIsolationPtSum = TagAndProbePair->second->sumNeutralHadronEtR04;
					// 	double photonIsolationPtSum = TagAndProbePair->second->sumPhotonEtR04;
					// 	double deltaBetaIsolationPtSum = TagAndProbePair->second->sumPUPtR04;
					// 	FloatQuantities["iso_p"] = (chargedIsolationPtSum + std::max(0.0, neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum)) / TagAndProbePair->second->p4.Pt();
					FloatQuantities["iso_t"] = SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (product.m_validDiTauPairCandidates.at(i).second), DefaultValues::UndefinedDouble);
=======
					FloatQuantities["iso_p"] = SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (product.m_validDiTauPairCandidates.at(i).second), DefaultValues::UndefinedDouble);
>>>>>>> Add producer and consumer for tau leg measurements in the mt channel
				}
				else if (*quantity == "m_ll")
				{
					FloatQuantities["m_ll"] = (static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4 +
											   static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4)
												  .M();
				}
				else
				{
					for (auto hltNames : m_hltFiredBranchNames)
					{
						if (*quantity == hltNames.first)
						{
							bool diTauPairFiredTrigger = false;
							LOG(DEBUG) << "Beginning of lambda function for " << hltNames.first;
							bool checkTag = std::find(tagCheckTriggerMatchByHltName.begin(), tagCheckTriggerMatchByHltName.end(), hltNames.first) != tagCheckTriggerMatchByHltName.end();
							bool checkProbe = std::find(probeCheckTriggerMatchByHltName.begin(), probeCheckTriggerMatchByHltName.end(), hltNames.first) != probeCheckTriggerMatchByHltName.end();
							for (auto hltName : hltNames.second)
							{
								bool hltFiredTag = false;
								bool hltFiredProbe = false;
								if (checkTag)
								{
									LOG(DEBUG) << "Checking trigger object matching for tag lepton";
									if (product.m_leptonTriggerMatch.find(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)) != product.m_leptonTriggerMatch.end())
									{
										auto trigger1 = product.m_leptonTriggerMatch.at(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first));
										for (auto hlts : (*trigger1))
										{
											if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
											{
												hltFiredTag = hlts.second;
											}
										}
										LOG(DEBUG) << "Found trigger for the tag lepton? " << hltFiredTag;
									}
								}
								else
									hltFiredTag = true;
								if (checkProbe)
								{
									LOG(DEBUG) << "Checking trigger object matching for probe lepton";
									if (product.m_leptonTriggerMatch.find(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)) != product.m_leptonTriggerMatch.end())
									{
										auto trigger2 = product.m_leptonTriggerMatch.at(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second));
										for (auto hlts : (*trigger2))
										{
											if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
											{
												hltFiredProbe = hlts.second;
											}
										}
										LOG(DEBUG) << "Found trigger for the probe lepton? " << hltFiredProbe;
									}
								}
								else
									hltFiredProbe = true;
								bool hltFired = hltFiredTag && hltFiredProbe;
								diTauPairFiredTrigger = diTauPairFiredTrigger || hltFired;
							}
							LOG(DEBUG) << "Tau pair with valid trigger match? " << diTauPairFiredTrigger;
							BoolQuantities[hltNames.first] = diTauPairFiredTrigger;
						}
					}
				}
				//std::map<std::string, bool>* AdditionalBoolQuantities;
				AdditionalQuantities(i, *quantity, product, event, settings, BoolQuantities, IntQuantities, FloatQuantities);
			}

			// fill tree
			this->m_tree->Fill();
		}
	}

	void Finish(setting_type const &settings) override
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree->Write(m_tree->GetName());
	}
  protected:
	virtual void AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
                                              std::map<std::string, bool>& BoolQuantities,
                                              std::map<std::string, int>& IntQuantities,
                                              std::map<std::string, float>& FloatQuantities)
        {
        }

  private:
	TTree *m_tree = nullptr;
	std::map<std::string, bool> BoolQuantities;
	std::map<std::string, int> IntQuantities;
	std::map<std::string, float> FloatQuantities;
	std::map<std::string, std::vector<std::string>> m_hltFiredBranchNames;
};

class NewMMTagAndProbePairConsumer : public NewTagAndProbePairConsumerBase
{
  public:
	NewMMTagAndProbePairConsumer();
	virtual std::string GetConsumerId() const override;

  protected:
	virtual void AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
					  std::map<std::string, bool>& BoolQuantities,
                                          std::map<std::string, int>& IntQuantities,
                                          std::map<std::string, float>& FloatQuantities) override;
};

class NewEETagAndProbePairConsumer : public NewTagAndProbePairConsumerBase
{
  public:
	NewEETagAndProbePairConsumer();
	virtual std::string GetConsumerId() const override;

  protected:
	virtual void AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
					  std::map<std::string, bool>& BoolQuantities,
                                          std::map<std::string, int>& IntQuantities,
                                          std::map<std::string, float>& FloatQuantities) override;
};

class NewMTTagAndProbePairConsumer : public NewTagAndProbePairConsumerBase
{
  public:
        NewMTTagAndProbePairConsumer();
	virtual std::string GetConsumerId() const override;

  protected:
	virtual void AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
                                              std::map<std::string, bool>& BoolQuantities,
                                              std::map<std::string, int>& IntQuantities,
                                              std::map<std::string, float>& FloatQuantities) override;
};
