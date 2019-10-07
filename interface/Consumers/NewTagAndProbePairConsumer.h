
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
		FloatQuantities["sc_eta_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["phi_p"] = DefaultValues::UndefinedFloat;
		BoolQuantities["id_p"] = false;
		BoolQuantities["id_emb_p"] = false;
		BoolQuantities["id_loose_p"] = false;
		BoolQuantities["id_global_p"] = false;

		FloatQuantities["iso_p"] = DefaultValues::UndefinedFloat;

		FloatQuantities["m_ll"] = DefaultValues::UndefinedFloat;
		FloatQuantities["metPt"] = DefaultValues::UndefinedFloat;
		FloatQuantities["mt_t"] = DefaultValues::UndefinedFloat;

		FloatQuantities["againstMuonLoose3_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstMuonTight3_p"] = DefaultValues::UndefinedFloat;
		
		FloatQuantities["againstElectronVLooseMVA6_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstElectronLooseMVA6_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstElectronMediumMVA6_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstElectronTightMVA6_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["againstElectronVTightMVA6_p"] = DefaultValues::UndefinedFloat;

		FloatQuantities["byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVLooseIsolationMVArun2017v2DBoldDMwLT2017_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byLooseIsolationMVArun2017v2DBoldDMwLT2017_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byMediumIsolationMVArun2017v2DBoldDMwLT2017_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byTightIsolationMVArun2017v2DBoldDMwLT2017_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVTightIsolationMVArun2017v2DBoldDMwLT2017_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVVTightIsolationMVArun2017v2DBoldDMwLT2017_p"] = DefaultValues::UndefinedFloat;
                
                FloatQuantities["byIsolationMVArun2v1DBoldDMwLTraw_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVLooseIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVLooseIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byLooseIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byMediumIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byTightIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVTightIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["byVVTightIsolationMVArun2v1DBoldDMwLT_p"] = DefaultValues::UndefinedFloat;

		BoolQuantities["isOS"] = false;

		BoolQuantities["id_90_t"] = false;
		BoolQuantities["id_90_p"] = false;
		BoolQuantities["id_80_t"] = false;
		BoolQuantities["id_80_p"] = false;
		BoolQuantities["id_old_t"] = false;
		BoolQuantities["id_old_p"] = false;
		BoolQuantities["id_cutbased_t"] = false;
		BoolQuantities["id_cutbased_p"] = false;
		// BoolQuantities["id_oldcutbased_t"] = false;
		// BoolQuantities["id_oldcutbased_p"] = false;
		// BoolQuantities["idiso_cutbased_t"] = false;
		// BoolQuantities["idiso_cutbased_p"] = false;
		// BoolQuantities["idiso_80_t"] = false;
		// BoolQuantities["idiso_80_p"] = false;
		BoolQuantities["id_cutbased_sanity_t"] = false;
		BoolQuantities["id_cutbased_sanity_p"] = false;
		BoolQuantities["id_cutbased_t_step_0"] = false;
		BoolQuantities["id_cutbased_t_step_1"] = false;
		BoolQuantities["id_cutbased_t_step_2"] = false;
		BoolQuantities["id_cutbased_t_step_3"] = false;
		BoolQuantities["id_cutbased_t_step_4"] = false;
		BoolQuantities["id_cutbased_t_step_5"] = false;
		BoolQuantities["id_cutbased_t_step_6"] = false;
		BoolQuantities["id_cutbased_t_step_7"] = false;

		BoolQuantities["id_cutbased_p_step_0"] = false;
		BoolQuantities["id_cutbased_p_step_1"] = false;
		BoolQuantities["id_cutbased_p_step_2"] = false;
		BoolQuantities["id_cutbased_p_step_3"] = false;
		BoolQuantities["id_cutbased_p_step_4"] = false;
		BoolQuantities["id_cutbased_p_step_5"] = false;
		BoolQuantities["id_cutbased_p_step_6"] = false;
		BoolQuantities["id_cutbased_p_step_7"] = false;

		// Temporary for Electron ID Variables Check
		FloatQuantities["sigmaIetaIeta_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["sigmaIetaIeta_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["hadronicOverEm_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["hadronicOverEm_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["fbrem_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["fbrem_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["r9_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["r9_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["circularity_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["circularity_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["hoe_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["hoe_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["kfhits_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["kfhits_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["kfchi2_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["kfchi2_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["gsfchi2_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["gsfchi2_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["gsfhits_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["gsfhits_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["expectedMissingInnerHits_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["expectedMissingInnerHits_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["eop_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["eop_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["eleeopout_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["eleeopout_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["oneOverEminusOneOverP_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["oneOverEminusOneOverP_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["deta_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["deta_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["dphi_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["dphi_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["detacalo_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["detacalo_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["preShowerOverRaw_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["preShowerOverRaw_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["convVtxFitProbability_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["convVtxFitProbability_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["rho_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["rho_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["dEtaInSeed_p"] = DefaultValues::UndefinedFloat;
		FloatQuantities["dEtaInSeed_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["scetaseed_t"] = DefaultValues::UndefinedFloat;
		FloatQuantities["scetaseed_p"] = DefaultValues::UndefinedFloat;

		FloatQuantities["decayModeFinding_p"] = DefaultValues::UndefinedFloat;
                IntQuantities["decayMode_p"] = DefaultValues::UndefinedInt;
                FloatQuantities["trkpt_p"] = DefaultValues::UndefinedFloat;
                IntQuantities["gen_match_p"] = DefaultValues::UndefinedInt;

                FloatQuantities["puWeight"] = DefaultValues::UndefinedFloat;
                FloatQuantities["bkgSubWeight"] = DefaultValues::UndefinedFloat;

		// Create Map entries for selected trigger quantities
		m_hltFiredBranchNames = Utility::ParseVectorToMap(settings.GetHLTBranchNames());
		for (auto hltNames : m_hltFiredBranchNames)
		{
			BoolQuantities[hltNames.first] = false;
                        FloatQuantities["isAntiL1TauMatched_"+hltNames.first] = DefaultValues::UndefinedFloat;
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

        NewTagAndProbePairConsumerBase():
                            ConsumerBase<HttTypes>()
        {
        }

	void ProcessFilteredEvent(event_type const &event, product_type const &product, setting_type const &settings) override
	{
		ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings);
		LOG(DEBUG) << "Starting to write quantities to file!";
		// calculate values
		std::vector<std::string> tagCheckTriggerMatchByHltName = settings.GetCheckTagTriggerMatch();
		std::vector<std::string> probeCheckTriggerMatchByHltName = settings.GetCheckProbeTriggerMatch();
                std::map<std::string, std::vector<float> > checkLowerPtCutsByHltNick;
                Utility::ParseMapTypes<size_t, float>(Utility::ParseVectorToMap(settings.GetCheckTriggerLowerPtCutsByHltNick()), checkLowerPtCutsByHltNick);
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
					FloatQuantities["iso_t"] = SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (product.m_validDiTauPairCandidates.at(i).first), DefaultValues::UndefinedDouble)/static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4.Pt();
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
					FloatQuantities["iso_p"] = SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (product.m_validDiTauPairCandidates.at(i).second), DefaultValues::UndefinedDouble)/static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4.Pt();
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
                                                        std::map<std::string, std::vector<float> > additionalL1LowerPtCutsByHltNick;
                                                        Utility::ParseMapTypes<size_t, float>(Utility::ParseVectorToMap((settings.GetTauTriggerCheckAdditionalL1TauMatchLowerPtCut)()),additionalL1LowerPtCutsByHltNick);
                                                        bool checkL1Probe = additionalL1LowerPtCutsByHltNick.find(hltNames.first) != additionalL1LowerPtCutsByHltNick.end();
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
                                                                                                if (checkLowerPtCutsByHltNick.find(hltNames.first) != checkLowerPtCutsByHltNick.end())
                                                                                                {
                                                                                                    LOG(DEBUG) << "Checking pT of trigger: " << hltNames.first;
                                                                                                    LOG(DEBUG) << "pT of trigger object: " << product.m_triggerMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(i).second)).p4.Pt() << "\t threshold: " << *std::max_element(checkLowerPtCutsByHltNick.at(hltNames.first).begin(), checkLowerPtCutsByHltNick.at(hltNames.first).end());
                                                                                                    hltFiredProbe = hltFiredProbe && product.m_triggerMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(i).second)).p4.Pt() > *std::max_element(checkLowerPtCutsByHltNick.at(hltNames.first).begin(), checkLowerPtCutsByHltNick.at(hltNames.first).end());
                                                                                                    LOG(DEBUG) << "Trigger object passed additional pT cut? " << hltFiredProbe;
                                                                                                }
                                                                                                if (checkL1Probe)
                                                                                                {
                                                                                                    LOG(DEBUG) << "Checking for L1 matched pT of trigger: " << hltNames.first;
                                                                                                    hltFiredProbe = hltFiredProbe && product.m_additionalL1TauMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(i).second))->at(hltNames.first);
                                                                                                    LOG(DEBUG) << "Trigger object passes additional L1 matching? " << hltFiredProbe;
                                                                                                }
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
			// Debug: Print Maps
			// LOG(WARNING) << "Entries in BOOLMAP:";
			// for(auto elem : BoolQuantities)
			// {
			// 	LOG(WARNING) << elem.first << " : " << elem.second;
			// }
			// // fill tree
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
	std::map<std::string, std::vector<std::string>> m_hltFiredBranchNames;

  private:
	TTree *m_tree = nullptr;
	std::map<std::string, bool> BoolQuantities;
	std::map<std::string, int> IntQuantities;
	std::map<std::string, float> FloatQuantities;
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



class NewETTagAndProbePairConsumer : public NewTagAndProbePairConsumerBase
{
  public:
        NewETTagAndProbePairConsumer();
	virtual std::string GetConsumerId() const override;

  protected:
	virtual void AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
                                              std::map<std::string, bool>& BoolQuantities,
                                              std::map<std::string, int>& IntQuantities,
                                              std::map<std::string, float>& FloatQuantities) override;
};
