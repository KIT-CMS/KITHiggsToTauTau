
#pragma once

#include <cstdint>
#include <cassert>

#include <boost/algorithm/string/predicate.hpp>

#include <TTree.h>
#include <Math/Vector4D.h>
#include <Math/Vector4Dfwd.h>

#include "Artus/Core/interface/EventBase.h"
#include "Artus/Core/interface/ProductBase.h"
#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Configuration/interface/SettingsBase.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "Kappa/DataFormats/interface/Kappa.h"
#include <boost/regex.hpp>

template<class TTypes>
class NewNNTagAndProbePairConsumer: public ConsumerBase<TTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	typedef typename TTypes::event_type event_type;
	typedef typename TTypes::product_type product_type;
	typedef typename TTypes::setting_type setting_type;
	
	std::string GetConsumerId() const override
	{
		return "NewMMTagAndProbePairConsumer";
	}
	
	void Init(setting_type const& settings) override {
		ConsumerBase<TTypes>::Init(settings);
		
		usedMuonIDshortTerm = (settings.GetMuonID() == "medium2016");
		
		//fill quantity maps
		IntQuantities["run"]=0;
		IntQuantities["lumi"]=0;
		IntQuantities["evt"]=0;

		FloatQuantities["pt_t"]=0.0;
		FloatQuantities["eta_t"]=0.0;
		FloatQuantities["phi_t"]=0.0;
		BoolQuantities["id_t"]=false;
		FloatQuantities["iso_t"]=0.0;

		FloatQuantities["pt_p"]=0.0;
		FloatQuantities["eta_p"]=0.0;
		FloatQuantities["phi_p"]=0.0;
		BoolQuantities["id_p"]=false;
		FloatQuantities["iso_p"]=0.0;
		FloatQuantities["dxy_p"]=0.0;
		FloatQuantities["m_ll"]=0.0;

		BoolQuantities["trg_t_IsoMu24"]=false;
		BoolQuantities["trg_t_IsoMu27"]=false;
		BoolQuantities["trg_p_IsoMu24"]=false;
		BoolQuantities["trg_p_IsoMu27"]=false;
		// create tree
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree = new TTree("ZmmTP", ("Tree for Pipeline \"" + settings.GetName() + "\"").c_str());

		// create branches
		for (std::vector<std::string>::iterator quantity = settings.GetQuantities().begin();
		     quantity != settings.GetQuantities().end(); ++quantity)
		{
			if(BoolQuantities.find(*quantity) != BoolQuantities.end()){
				m_tree->Branch(quantity->c_str(), &(BoolQuantities[*quantity]), (*quantity + "/O").c_str());
			}else if(IntQuantities.find(*quantity) != IntQuantities.end()){
				m_tree->Branch(quantity->c_str(), &(IntQuantities[*quantity]), (*quantity + "/I").c_str());
			}else if(FloatQuantities.find(*quantity) != FloatQuantities.end()){
				m_tree->Branch(quantity->c_str(), &(FloatQuantities[*quantity]), (*quantity + "/F").c_str());
			}
		}
	}

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings ) override
	{
		ConsumerBase<TTypes>::ProcessFilteredEvent(event, product, settings);

		// calculate values
		bool IsData = settings.GetInputIsData();
		for for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
		{
			for (std::vector<std::string>::iterator quantity = settings.GetQuantities().begin();
					quantity != settings.GetQuantities().end(); ++quantity)
			{
				}if(*quantity=="run"){
					IntQuantities["run"]=event.m_eventInfo->nRun;
				}else if(*quantity=="lumi"){
					IntQuantities["lumi"]=event.m_eventInfo->nLumi;
				}else if(*quantity=="evt"){
					IntQuantities["evt"]=event.m_eventInfo->nEvent;
				}else if(*quantity=="pt_t"){
					FloatQuantities["pt_t"]=TagAndProbePair->first->p4.Pt();
				}else if(*quantity=="eta_t"){
					FloatQuantities["eta_t"]=TagAndProbePair->first->p4.Eta();
				}else if(*quantity=="phi_t"){
					FloatQuantities["phi_t"]=TagAndProbePair->first->p4.Phi();
				}else if(*quantity=="id_t"){
					BoolQuantities["id_t"]=( usedMuonIDshortTerm ? IsMediumMuon2016ShortTerm(TagAndProbePair->first) : IsMediumMuon2016(TagAndProbePair->first) ) && std::abs(TagAndProbePair->first->dxy) < 0.045 && std::abs(TagAndProbePair->first->dz) < 0.2;
				}else if(*quantity=="iso_t"){
					double chargedIsolationPtSum = TagAndProbePair->first->sumChargedHadronPtR04;
					double neutralIsolationPtSum = TagAndProbePair->first->sumNeutralHadronEtR04;
					double photonIsolationPtSum = TagAndProbePair->first->sumPhotonEtR04;
					double deltaBetaIsolationPtSum = TagAndProbePair->first->sumPUPtR04;
					FloatQuantities["iso_t"]=(chargedIsolationPtSum + std::max(0.0,neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum))/TagAndProbePair->first->p4.Pt();
				}else if(*quantity=="muon_p"){
					BoolQuantities["muon_p"]=true;
				}else if(*quantity=="trk_p"){
					BoolQuantities["trk_p"]=false;
				}else if(*quantity=="pt_p"){
					FloatQuantities["pt_p"]=TagAndProbePair->second->p4.Pt();
				}else if(*quantity=="eta_p"){
					FloatQuantities["eta_p"]=TagAndProbePair->second->p4.Eta();
				}else if(*quantity=="phi_p"){
					FloatQuantities["phi_p"]=TagAndProbePair->second->p4.Phi();
				}else if(*quantity=="id_p"){
					BoolQuantities["id_p"]=( usedMuonIDshortTerm ? IsMediumMuon2016ShortTerm(TagAndProbePair->second) : IsMediumMuon2016(TagAndProbePair->second) ) && std::abs(TagAndProbePair->second->dxy) < 0.045 && std::abs(TagAndProbePair->second->dz) < 0.2;
				}else if(*quantity=="iso_p"){
					double chargedIsolationPtSum = TagAndProbePair->second->sumChargedHadronPtR04;
					double neutralIsolationPtSum = TagAndProbePair->second->sumNeutralHadronEtR04;
					double photonIsolationPtSum = TagAndProbePair->second->sumPhotonEtR04;
					double deltaBetaIsolationPtSum = TagAndProbePair->second->sumPUPtR04;
					FloatQuantities["iso_p"]=(chargedIsolationPtSum + std::max(0.0,neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum))/TagAndProbePair->second->p4.Pt();
				}else if(*quantity=="dxy_p"){
					FloatQuantities["dxy_p"]=std::abs(TagAndProbePair->second->dxy);
				}else if(*quantity=="dz_p"){
					FloatQuantities["dz_p"]=std::abs(TagAndProbePair->second->dz);
				}else if(*quantity=="gen_p"){
					if(IsData) BoolQuantities["gen_p"]=false;
					else BoolQuantities["gen_p"]=(product.m_genParticleMatchedMuons.find(TagAndProbePair->second) != product.m_genParticleMatchedMuons.end());
				}else if(*quantity=="genZ_p"){
					if(IsData) BoolQuantities["genZ_p"]=false;
					else if(product.m_genParticleMatchedMuons.find(TagAndProbePair->second) != product.m_genParticleMatchedMuons.end()){
						BoolQuantities["genZ_p"]=(std::find(product.m_genLeptonsFromBosonDecay.begin(), product.m_genLeptonsFromBosonDecay.end(), product.m_genParticleMatchedMuons.at(TagAndProbePair->second)) != product.m_genLeptonsFromBosonDecay.end());
					}else{
						BoolQuantities["genZ_p"]=false;
					}
				}else if(*quantity=="m_ll"){
					FloatQuantities["m_ll"]=(TagAndProbePair->first->p4 + TagAndProbePair->second->p4).M();
				}else if(*quantity=="trg_t_IsoMu22"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_IsoMu22"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_IsoMu22"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_IsoMu22"]=false;
						}
					}
				}else if(*quantity=="trg_t_IsoMu22_eta2p1"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_IsoMu22_eta2p1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_IsoMu22_eta2p1"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_IsoMu22_eta2p1"]=false;
						}
					}
				}else if(*quantity=="trg_t_IsoMu24"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_IsoMu24"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu24_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_IsoMu24"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_IsoMu24"]=false;
						}
					}
				}else if(*quantity=="trg_t_IsoMu19Tau"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_IsoMu19Tau"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_IsoMu19Tau"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_IsoMu19Tau"]=false;
						}
					}
				}else if(*quantity=="trg_p_IsoMu22"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu22"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu22"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu22"]=false;
						}
					}
				}else if(*quantity=="trg_p_IsoTkMu22"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoTkMu22"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu22_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoTkMu22"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoTkMu22"]=false;
						}
					}
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu22_eta2p1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu22_eta2p1"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu22_eta2p1"]=false;
						}
					}
				}else if(*quantity=="trg_p_IsoTkMu22_eta2p1"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoTkMu22_eta2p1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu22_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoTkMu22_eta2p1"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoTkMu22_eta2p1"]=false;
						}
					}
				}else if(*quantity=="trg_p_IsoMu24"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu24"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu24_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu24"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu24"]=false;
						}
					}
				}else if(*quantity=="trg_p_IsoTkMu24"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoTkMu24"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu24_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoTkMu24"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoTkMu24"]=false;
						}
					}
				}else if(*quantity=="trg_p_PFTau120"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_PFTau120"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_VLooseIsoPFTau120_Trk50_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltPFTau120TrackPt50LooseAbsOrRelVLooseIso"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_PFTau120"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_PFTau120"]=false;
						}
					}
				}else if(*quantity=="trg_p_IsoMu19TauL1"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu19TauL1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu19TauL1"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu19TauL1"]=false;
						}
					}
				}else if(*quantity=="trg_p_IsoMu19Tau"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu19Tau"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu19Tau"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu19Tau"]=false;
						}
					}
				}
			}
			
			// fill tree
			this->m_tree->Fill();
		}
				
	}

	void Finish(setting_type const& settings) override
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree->Write(m_tree->GetName());
	}


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	bool usedMuonIDshortTerm = false;
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Short_Term_Medium_Muon_Definitio
	bool IsMediumMuon2016ShortTerm(KMuon* muon) const
	{
	        bool goodGlob = muon->isGlobalMuon()
	                                        && muon->normalizedChiSquare < 3
	                                        && muon->chiSquareLocalPos < 12
        	                                && muon->trkKink < 20;
        	bool isMedium = muon->idLoose()
        	                               	&& muon->validFractionOfTrkHits > 0.49
        	                                && muon->segmentCompatibility > (goodGlob ? 0.303 : 0.451);
        	return isMedium;
	}
	bool IsMediumMuon2016(KMuon* muon) const
	{
	        bool goodGlob = muon->isGlobalMuon()
	                                        && muon->normalizedChiSquare < 3
	                                        && muon->chiSquareLocalPos < 12
        	                                && muon->trkKink < 20;
        	bool isMedium = muon->idLoose()
        	                               	&& muon->validFractionOfTrkHits > 0.8
        	                                && muon->segmentCompatibility > (goodGlob ? 0.303 : 0.451);
        	return isMedium;
	}
};

