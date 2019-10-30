#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/NewTagAndProbePairConsumer.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"
#include "Artus/Utility/interface/Utility.h"

NewMMTagAndProbePairConsumer::NewMMTagAndProbePairConsumer() : NewTagAndProbePairConsumerBase()
{
}

void NewMMTagAndProbePairConsumer::AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
				 					 std::map<std::string, bool>& BoolQuantities,
                                                                         std::map<std::string, int>& IntQuantities,
                                                                         std::map<std::string, float>& FloatQuantities)
{
	if (quantity == "id_t")
	{
		BoolQuantities["id_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->idMedium();
	}
	else if (quantity == "id_p")
	{
		BoolQuantities["id_p"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->idMedium();
	}
	else if (quantity == "id_loose_p")
	{
		BoolQuantities["id_loose_p"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->idLoose();
	}
	else if (quantity == "id_global_p")
	{
		BoolQuantities["id_global_p"] = static_cast<KMuon *>(product.m_validDiTauPairCandidates.at(i).second)->isGlobalMuon();
	}
	else if (quantity == "id_emb_p")
	{
		BoolQuantities["id_emb_p"] = static_cast<KMuon *>(product.m_validDiTauPairCandidates.at(i).second)->isGlobalMuon() && static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->idLoose();
	}
        else
        {
                for (auto hltNames : m_hltFiredBranchNames)
                {
                        if (quantity == "isAntiL1TauMatched_"+hltNames.first)
                        {
                                if (product.m_additionalL1TauMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(i).second))->find(hltNames.first) != product.m_additionalL1TauMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(i).second))->end())
                                {
                                        FloatQuantities["isAntiL1TauMatched_"+hltNames.first] = product.m_additionalL1TauMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(i).second))->at(hltNames.first);
                                }
                                else
                                {
                                        FloatQuantities["isAntiL1TauMatched_"+hltNames.first] = DefaultValues::UndefinedFloat;
                                } 
                        }
                }
        }
}

std::string NewMMTagAndProbePairConsumer::GetConsumerId() const
{
	return "NewMMTagAndProbePairConsumer";
}

NewEETagAndProbePairConsumer::NewEETagAndProbePairConsumer() : NewTagAndProbePairConsumerBase()
{
}

void NewEETagAndProbePairConsumer::AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
				 					 std::map<std::string, bool>& BoolQuantities,
                                                                         std::map<std::string, int>& IntQuantities,
                                                                         std::map<std::string, float>& FloatQuantities)
{
	if (quantity == "id_90_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		BoolQuantities["id_90_t"] = electron->getId(settings.GetTagElectronIDName(), event.m_electronMetadata);
	}
	else if (quantity == "id_90_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		BoolQuantities["id_90_p"] = electron->getId(settings.GetTagElectronIDName(), event.m_electronMetadata);
	}
	else if (quantity == "id_80_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		BoolQuantities["id_80_t"] = electron->getId(settings.GetTagElectronSecondIDName(), event.m_electronMetadata);
	}
	else if (quantity == "id_80_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		BoolQuantities["id_80_p"] = electron->getId(settings.GetTagElectronSecondIDName(), event.m_electronMetadata);
	}

	else if (quantity == "id_cutbased_sanity_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		BoolQuantities["id_cutbased_sanity_t"] = electron->getId(settings.GetTagElectronCutIDSanity(), event.m_electronMetadata);
	}
	else if (quantity == "id_cutbased_sanity_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		BoolQuantities["id_cutbased_sanity_p"] = electron->getId(settings.GetTagElectronCutIDSanity(), event.m_electronMetadata);
	}
	else if (quantity == "sc_eta_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["sc_eta_p"] = electron->superclusterPosition.Eta();
	}
    // else if (quantity == "id_old_t")
    // {
    //     std::string electronIDName = settings.GetOldElectronIDName();
	// 	double electronMvaIDCutEB1 = settings.GetElectronMvaIDCutEB1();
	// 	double electronMvaIDCutEB2 = settings.GetElectronMvaIDCutEB2();
	// 	double electronMvaIDCutEE = settings.GetElectronMvaIDCutEE();
    //     KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
    //     bool validElectron = true;
	// 	validElectron = validElectron && (electron->track.nInnerHits <= 1);
	// 	validElectron = validElectron && (! (electron->electronType & (1 << KElectronType::hasConversionMatch)));
	// 	validElectron = validElectron &&
	// 		(
	// 			(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId(electronIDName, event.m_electronMetadata) > electronMvaIDCutEB1)
	// 			||
	// 			(std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId(electronIDName, event.m_electronMetadata) > electronMvaIDCutEB2)
	// 			||
	// 			(std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId(electronIDName, event.m_electronMetadata) > electronMvaIDCutEE)
	// 		);
    //     BoolQuantities["id_old_t"] = validElectron;
    // }
    // else if (quantity == "id_old_p")
    // {
    //     std::string electronIDName = settings.GetOldElectronIDName();
	// 	double electronMvaIDCutEB1 = settings.GetElectronMvaIDCutEB1();
	// 	double electronMvaIDCutEB2 = settings.GetElectronMvaIDCutEB2();
	// 	double electronMvaIDCutEE = settings.GetElectronMvaIDCutEE();
    //     KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
    //     bool validElectron = true;
	// 	validElectron = validElectron && (electron->track.nInnerHits <= 1);
	// 	validElectron = validElectron && (! (electron->electronType & (1 << KElectronType::hasConversionMatch)));
	// 	validElectron = validElectron &&
	// 		(
	// 			(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId(electronIDName, event.m_electronMetadata) > electronMvaIDCutEB1)
	// 			||
	// 			(std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId(electronIDName, event.m_electronMetadata) > electronMvaIDCutEB2)
	// 			||
	// 			(std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId(electronIDName, event.m_electronMetadata) > electronMvaIDCutEE)
	// 		);
    //     BoolQuantities["id_old_p"] = validElectron;
    // }
        
    else if (quantity.find("cutbased_t") != std::string::npos)
    {
        KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
        BoolQuantities["id_cutbased_t_step_0"] = true;
        BoolQuantities["id_cutbased_t_step_1"] = false;
        BoolQuantities["id_cutbased_t_step_2"] = false;
        BoolQuantities["id_cutbased_t_step_3"] = false;
        BoolQuantities["id_cutbased_t_step_4"] = false;
        BoolQuantities["id_cutbased_t_step_5"] = false;
        BoolQuantities["id_cutbased_t_step_6"] = false;
        BoolQuantities["id_cutbased_t_step_7"] = false;
        double esc = electron->superclusterEnergy;
        if (electron->superclusterPosition.Eta() <= 1.479)
        {
            if (electron->full5x5_sigmaIetaIeta < 0.0106)
            {
                BoolQuantities["id_cutbased_t_step_1"] = true;
                //if (std::abs(electron->dEtaInSeed) < 0.0032)
                if (true)
                {
                    BoolQuantities["id_cutbased_t_step_2"] = true;
                    if (std::abs(electron->dPhiIn) < 0.0547)
                    {
                        BoolQuantities["id_cutbased_t_step_3"] = true;
                        if (electron->hadronicOverEm < 0.046 + 1.16/esc + 0.0324 * event.m_pileupDensity->rho/esc)
                        {
                            BoolQuantities["id_cutbased_t_step_4"] = true;
                            if (SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (product.m_validDiTauPairCandidates.at(i).first), DefaultValues::UndefinedDouble)/static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4.Pt() < 0.0478 + 0.506/electron->p4.Pt())
                            {
                                BoolQuantities["id_cutbased_t_step_5"] = true; 
                                if (electron->oneOverEminusOneOverP < 0.184 )
                                {
                                    BoolQuantities["id_cutbased_t_step_6"] = true;  
                                    if (electron->expectedMissingInnerHits <= 1)
                                    {
                                        BoolQuantities["id_cutbased_t_step_7"] = true;
                                    }
                                } 
                            }  
                        }
                    }
                }
            }

        }
        else if (electron->superclusterPosition.Eta() > 1.479)
        {
            if (electron->full5x5_sigmaIetaIeta < 0.0387)
            {
                BoolQuantities["id_cutbased_t_step_1"] = true;
                //if (std::abs(electron->dEtaInSeed) < 0.00632)
                if (true)
                {
                    BoolQuantities["id_cutbased_t_step_2"] = true;
                    if (std::abs(electron->dPhiIn) < 0.0394)
                    {
                        BoolQuantities["id_cutbased_t_step_3"] = true;
                        if (electron->hadronicOverEm < 0.0275 + 2.52/esc + 0.183 * event.m_pileupDensity->rho/esc)
                        {
                            BoolQuantities["id_cutbased_t_step_4"] = true;
                            if (SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (product.m_validDiTauPairCandidates.at(i).first), DefaultValues::UndefinedDouble)/static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4.Pt() < 0.0658 + 0.963/electron->p4.Pt())
                            {
                                BoolQuantities["id_cutbased_t_step_5"] = true; 
                                if (electron->oneOverEminusOneOverP < 0.0721)
                                {
                                    BoolQuantities["id_cutbased_t_step_6"] = true;  
                                    if (electron->expectedMissingInnerHits <= 1)
                                    {
                                        BoolQuantities["id_cutbased_t_step_7"] = true;  
                                    }
                                } 
                            }  
                        }
                    }
                }
            }
        }
        BoolQuantities["id_cutbased_t"] = BoolQuantities["id_cutbased_t_step_7"];
    }

    else if (quantity.find("cutbased_p") != std::string::npos)
    {
        KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
        BoolQuantities["id_cutbased_p_step_0"] = true;
        BoolQuantities["id_cutbased_p_step_1"] = false;
        BoolQuantities["id_cutbased_p_step_2"] = false;
        BoolQuantities["id_cutbased_p_step_3"] = false;
        BoolQuantities["id_cutbased_p_step_4"] = false;
        BoolQuantities["id_cutbased_p_step_5"] = false;
        BoolQuantities["id_cutbased_p_step_6"] = false;
        BoolQuantities["id_cutbased_p_step_7"] = false;
        double esc = electron->superclusterEnergy;
        if (electron->superclusterPosition.Eta() <= 1.479)
        {
            if (electron->full5x5_sigmaIetaIeta < 0.0106)
            {
                BoolQuantities["id_cutbased_p_step_1"] = true;
                //if (std::abs(electron->dEtaInSeed) < 0.0032)
                if (true)
                {
                    BoolQuantities["id_cutbased_p_step_2"] = true;
                    if (std::abs(electron->dPhiIn) < 0.0547)
                    {
                        BoolQuantities["id_cutbased_p_step_3"] = true;
                        if (electron->hadronicOverEm < 0.046 + 1.16/esc + 0.0324 * event.m_pileupDensity->rho/esc)
                        {
                            BoolQuantities["id_cutbased_p_step_4"] = true;
                            if (SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (product.m_validDiTauPairCandidates.at(i).second), DefaultValues::UndefinedDouble)/static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4.Pt() < 0.0478 + 0.506/electron->p4.Pt())
                            {
                                BoolQuantities["id_cutbased_p_step_5"] = true; 
                                if (electron->oneOverEminusOneOverP < 0.184 )
                                {
                                    BoolQuantities["id_cutbased_p_step_6"] = true;  
                                    if (electron->expectedMissingInnerHits <= 1)
                                    {
                                        BoolQuantities["id_cutbased_p_step_7"] = true;
                                    }
                                } 
                            }  
                        }
                    }
                }
            }

        }
        else if (electron->superclusterPosition.Eta() > 1.479)
        {
            if (electron->full5x5_sigmaIetaIeta < 0.0387)
            {
                BoolQuantities["id_cutbased_p_step_1"] = true;
                //if (std::abs(electron->dEtaInSeed) < 0.00632)
                if (true)
                {
                    BoolQuantities["id_cutbased_p_step_2"] = true;
                    if (std::abs(electron->dPhiIn) < 0.0394)
                    {
                        BoolQuantities["id_cutbased_p_step_3"] = true;
                        if (electron->hadronicOverEm < 0.0275 + 2.52/esc + 0.183 * event.m_pileupDensity->rho/esc)
                        {
                            BoolQuantities["id_cutbased_p_step_4"] = true;
                            if (SafeMap::GetWithDefault(product.m_leptonIsolation,static_cast<KLepton *> (product.m_validDiTauPairCandidates.at(i).second), DefaultValues::UndefinedDouble)/static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4.Pt() < 0.0658 + 0.963/electron->p4.Pt())
                            {
                                BoolQuantities["id_cutbased_p_step_5"] = true; 
                                if (electron->oneOverEminusOneOverP < 0.0721)
                                {
                                    BoolQuantities["id_cutbased_p_step_6"] = true;  
                                    if (electron->expectedMissingInnerHits <= 1)
                                    {
                                        BoolQuantities["id_cutbased_p_step_7"] = true;  
                                    }
                                } 
                            }  
                        }
                    }
                }
            }
        }
        BoolQuantities["id_cutbased_p"] = BoolQuantities["id_cutbased_p_step_7"];
    }
    else if (quantity == "sigmaIetaIeta_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["sigmaIetaIeta_t"] = electron->sigmaIetaIeta;
	}
	else if (quantity == "sigmaIetaIeta_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["sigmaIetaIeta_p"] = electron->sigmaIetaIeta;
	}


    else if (quantity == "hadronicOverEm_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["hadronicOverEm_t"] = electron->hadronicOverEm;
	}
	else if (quantity == "hadronicOverEm_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["hadronicOverEm_p"] = electron->hadronicOverEm;
	}


    else if (quantity == "fbrem_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["fbrem_t"] = electron->fbrem;
	}
	else if (quantity == "fbrem_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["fbrem_p"] = electron->fbrem;
	}


    else if (quantity == "r9_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["r9_t"] = electron->r9;
	}
	else if (quantity == "r9_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["r9_p"] = electron->r9;
	}


    else if (quantity == "circularity_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["circularity_t"] = electron->circularity;
	}
	else if (quantity == "circularity_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["circularity_p"] = electron->circularity;
	}


    else if (quantity == "hoe_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["hoe_t"] = electron->hoe;
	}
	else if (quantity == "hoe_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["hoe_p"] = electron->hoe;
	}


    else if (quantity == "kfhits_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["kfhits_t"] = electron->kfhits;
	}
	else if (quantity == "kfhits_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["kfhits_p"] = electron->kfhits;
	}


    else if (quantity == "kfchi2_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["kfchi2_t"] = electron->kfchi2;
	}
	else if (quantity == "kfchi2_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["kfchi2_p"] = electron->kfchi2;
	}


    else if (quantity == "gsfchi2_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["gsfchi2_t"] = electron->gsfchi2;
	}
	else if (quantity == "gsfchi2_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["gsfchi2_p"] = electron->gsfchi2;
	}


    else if (quantity == "gsfhits_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["gsfhits_t"] = electron->gsfhits;
	}
	else if (quantity == "gsfhits_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["gsfhits_p"] = electron->gsfhits;
	}


    else if (quantity == "expectedMissingInnerHits_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["expectedMissingInnerHits_t"] = electron->expectedMissingInnerHits;
	}
	else if (quantity == "expectedMissingInnerHits_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["expectedMissingInnerHits_p"] = electron->expectedMissingInnerHits;
	}


    else if (quantity == "eop_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["eop_t"] = electron->eop;
	}
	else if (quantity == "eop_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["eop_p"] = electron->eop;
	}


    else if (quantity == "eleeopout_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["eleeopout_t"] = electron->eleeopout;
	}
	else if (quantity == "eleeopout_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["eleeopout_p"] = electron->eleeopout;
	}


    else if (quantity == "oneOverEminusOneOverP_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["oneOverEminusOneOverP_t"] = electron->oneOverEminusOneOverP;
	}
	else if (quantity == "oneOverEminusOneOverP_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["oneOverEminusOneOverP_p"] = electron->oneOverEminusOneOverP;
	}


    else if (quantity == "deta_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["deta_t"] = electron->deta;
	}
	else if (quantity == "deta_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["deta_p"] = electron->deta;
	}


    else if (quantity == "dphi_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["dphi_t"] = electron->dphi;
	}
	else if (quantity == "dphi_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["dphi_p"] = electron->dphi;
	}


    else if (quantity == "detacalo_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["detacalo_t"] = electron->detacalo;
	}
	else if (quantity == "detacalo_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["detacalo_p"] = electron->detacalo;
	}


    else if (quantity == "preShowerOverRaw_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["preShowerOverRaw_t"] = electron->preShowerOverRaw;
	}
	else if (quantity == "preShowerOverRaw_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["preShowerOverRaw_p"] = electron->preShowerOverRaw;
	}


    else if (quantity == "convVtxFitProbability_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["convVtxFitProbability_t"] = electron->convVtxFitProbability;
	}
	else if (quantity == "convVtxFitProbability_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["convVtxFitProbability_p"] = electron->convVtxFitProbability;
	}


    else if (quantity == "rho_t")
	{
		FloatQuantities["rho_t"] = event.m_pileupDensity->rho;
	}
	else if (quantity == "rho_p")
	{
		FloatQuantities["rho_p"] = event.m_pileupDensity->rho;
    }


    else if (quantity == "scetaseed_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["scetaseed_t"] = electron->dEtaInSeed - electron->deta + electron->superclusterPosition.Eta();

	}
	else if (quantity == "scetaseed_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["scetaseed_p"] = electron->dEtaInSeed - electron->deta + electron->superclusterPosition.Eta();
	}

    else if (quantity == "dEtaInSeed_t")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).first);
		FloatQuantities["dEtaInSeed_t"] = std::abs(electron->dEtaInSeed);
	}
	else if (quantity == "dEtaInSeed_p")
	{
		KElectron *electron = static_cast<KElectron *>(product.m_validDiTauPairCandidates.at(i).second);
		FloatQuantities["dEtaInSeed_p"] = std::abs(electron->dEtaInSeed);
	}
        else
        {
                for (auto hltNames : m_hltFiredBranchNames)
                {
                        if (quantity == "isAntiL1TauMatched_"+hltNames.first)
                        {
                                if (product.m_additionalL1TauMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(i).second))->find(hltNames.first) != product.m_additionalL1TauMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(i).second))->end())
                                {
                                        FloatQuantities["isAntiL1TauMatched_"+hltNames.first] = product.m_additionalL1TauMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(i).second))->at(hltNames.first);
                                }
                                else
                                {
                                        FloatQuantities["isAntiL1TauMatched_"+hltNames.first] = DefaultValues::UndefinedFloat;
                                } 
                        }
                }
        }
}

std::string NewEETagAndProbePairConsumer::GetConsumerId() const
{
	return "NewEETagAndProbePairConsumer";
}

NewMTTagAndProbePairConsumer::NewMTTagAndProbePairConsumer() : NewTagAndProbePairConsumerBase()
{
}

void NewMTTagAndProbePairConsumer::AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
				 					 std::map<std::string, bool>& BoolQuantities,
                                                                         std::map<std::string, int>& IntQuantities,
                                                                         std::map<std::string, float>& FloatQuantities)
{
	if (quantity == "id_t")
	{
		BoolQuantities["id_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(0).first)->idMedium();
	}
        else if (quantity == "isOS")
        {
                BoolQuantities["isOS"] = product.m_validDiTauPairCandidates.at(0).IsOppositelyCharged(); 
        }

        std::vector<std::string> tauDiscriminators;
        tauDiscriminators.push_back("againstElectronVLooseMVA6");
        tauDiscriminators.push_back("againstElectronLooseMVA6");
        tauDiscriminators.push_back("againstElectronMediumMVA6");
        tauDiscriminators.push_back("againstElectronTightMVA6");
        tauDiscriminators.push_back("againstElectronVTightMVA6");
        tauDiscriminators.push_back("againstMuonLoose3");
        tauDiscriminators.push_back("againstMuonTight3");
        tauDiscriminators.push_back("byIsolationMVArun2v1DBoldDMwLTraw");
        tauDiscriminators.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byLooseIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byMediumIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byTightIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byVTightIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byIsolationMVArun2017v2DBoldDMwLTraw2017");
        tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byVLooseIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byLooseIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byMediumIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byTightIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byVTightIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byVVTightIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byIsolationMVArun2017v1DBoldDMwLTraw2017");
        tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byVLooseIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byLooseIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byMediumIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byTightIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byVTightIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byVVTightIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byDeepTau2017v2p1VSjetraw");
        //tauDiscriminators.push_back("byVVVLooseDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byVVLooseDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byVLooseDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byLooseDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byMediumDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byTightDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byVTightDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byVVTightDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byDeepTau2017v2p1VSeraw");
        //tauDiscriminators.push_back("byVVVLooseDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byVVLooseDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byVLooseDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byLooseDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byMediumDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byTightDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byVTightDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byVVTightDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byDeepTau2017v2p1VSmuraw");
        tauDiscriminators.push_back("byVLooseDeepTau2017v2p1VSmu");
        tauDiscriminators.push_back("byLooseDeepTau2017v2p1VSmu");
        tauDiscriminators.push_back("byMediumDeepTau2017v2p1VSmu");
        tauDiscriminators.push_back("byTightDeepTau2017v2p1VSmu");
        tauDiscriminators.push_back("decayModeFinding");
        tauDiscriminators.push_back("decayModeFindingNewDMs");

        for (std::string tauDiscriminator : tauDiscriminators)
        {
            if (quantity == tauDiscriminator + "_p")
            {
                FloatQuantities[tauDiscriminator+"_p"] = static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->getDiscriminator(tauDiscriminator, event.m_tauMetadata);
            }
        }
        //temporary fix for VVVLoose deep tau ID WP
	if (quantity == "byVVVLooseDeepTau2017v2p1VSjet_p")
        {
                FloatQuantities["byVVVLooseDeepTau2017v2p1VSjet_p"] = float(static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->getDiscriminator("byDeepTau2017v2p1VSjetraw", event.m_tauMetadata) > 0.2599605);
	};
	if (quantity == "byVVVLooseDeepTau2017v2p1VSe_p")
        {
                FloatQuantities["byVVVLooseDeepTau2017v2p1VSe_p"] = float(static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->getDiscriminator("byDeepTau2017v2p1VSeraw", event.m_tauMetadata) > 0.0630386);
	};
        //end of fix
        if (quantity == "metPt")
        {
                FloatQuantities["metPt"] = (static_cast<HttProduct const&>(product)).m_met.p4.Pt();
        }
        else if (quantity == "mt_t")
        {
                FloatQuantities["mt_t"] = Quantities::CalculateMt(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).first)->p4,product.m_met.p4);
        }

        if (quantity == "decayMode_p")
        {
            IntQuantities["decayMode_p"] = static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->decayMode;
        }

        if (quantity == "trkpt_p")
        {
            FloatQuantities["trkpt_p"] = static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->chargedHadronCandidates.size() > 0 ? static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->chargedHadronCandidates[0].p4.Pt() : DefaultValues::UndefinedFloat;
        }

        if (quantity == "gen_match_p")
        {
            KLepton* lepton = static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).second);
            if (settings.GetUseUWGenMatching())
            {
                IntQuantities["gen_match_p"] = Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCodeUW(event, lepton));
            }
            else
            {
                KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(                                                                                                                  
                                                        lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons
                                                        );
                if (genParticle)
                {
                    IntQuantities["gen_match_p"] =  Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCode(genParticle));
                }
                else
                {
                    IntQuantities["gen_match_p"] =  Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_FAKE);
                }
            }
        }

        if (quantity == "puWeight")
        {
            FloatQuantities["puWeight"] = SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), SafeMap::GetWithDefault(product.m_optionalWeights, std::string("puWeight"), 1.0));
        }
        if (quantity == "bkgSubWeight")
        {
            FloatQuantities["bkgSubWeight"] = (product.m_isSingleMuon && !product.m_validDiTauPairCandidates.at(0).IsOppositelyCharged()) ? -1. : 1.; 
        }
}

std::string NewMTTagAndProbePairConsumer::GetConsumerId() const
{
	return "NewMTTagAndProbePairConsumer";
}



NewETTagAndProbePairConsumer::NewETTagAndProbePairConsumer() : NewTagAndProbePairConsumerBase()
{
}

void NewETTagAndProbePairConsumer::AdditionalQuantities(int i, std::string quantity, product_type const &product, event_type const& event, setting_type const &settings,
				 					 std::map<std::string, bool>& BoolQuantities,
                                                                         std::map<std::string, int>& IntQuantities,
                                                                         std::map<std::string, float>& FloatQuantities)
{
	if (quantity == "id_t")
	{
		BoolQuantities["id_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(0).first)->idMedium();
	}
        else if (quantity == "isOS")
        {
                BoolQuantities["isOS"] = product.m_validDiTauPairCandidates.at(0).IsOppositelyCharged(); 
        }

        std::vector<std::string> tauDiscriminators;
        tauDiscriminators.push_back("againstElectronVLooseMVA6");
        tauDiscriminators.push_back("againstElectronLooseMVA6");
        tauDiscriminators.push_back("againstElectronMediumMVA6");
        tauDiscriminators.push_back("againstElectronTightMVA6");
        tauDiscriminators.push_back("againstElectronVTightMVA6");
        tauDiscriminators.push_back("againstMuonLoose3");
        tauDiscriminators.push_back("againstMuonTight3");
        tauDiscriminators.push_back("byIsolationMVArun2v1DBoldDMwLTraw");
        tauDiscriminators.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byLooseIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byMediumIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byTightIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byVTightIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT");
        tauDiscriminators.push_back("byIsolationMVArun2017v2DBoldDMwLTraw2017");
        tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byVLooseIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byLooseIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byMediumIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byTightIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byVTightIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byVVTightIsolationMVArun2017v2DBoldDMwLT2017");
        tauDiscriminators.push_back("byIsolationMVArun2017v1DBoldDMwLTraw2017");
        tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byVLooseIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byLooseIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byMediumIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byTightIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byVTightIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byVVTightIsolationMVArun2017v1DBoldDMwLT2017");
        tauDiscriminators.push_back("byDeepTau2017v2p1VSjetraw");
        //tauDiscriminators.push_back("byVVVLooseDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byVVLooseDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byVLooseDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byLooseDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byMediumDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byTightDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byVTightDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byVVTightDeepTau2017v2p1VSjet");
        tauDiscriminators.push_back("byDeepTau2017v2p1VSeraw");
        //tauDiscriminators.push_back("byVVVLooseDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byVVLooseDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byVLooseDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byLooseDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byMediumDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byTightDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byVTightDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byVVTightDeepTau2017v2p1VSe");
        tauDiscriminators.push_back("byDeepTau2017v2p1VSmuraw");
        tauDiscriminators.push_back("byVLooseDeepTau2017v2p1VSmu");
        tauDiscriminators.push_back("byLooseDeepTau2017v2p1VSmu");
        tauDiscriminators.push_back("byMediumDeepTau2017v2p1VSmu");
        tauDiscriminators.push_back("byTightDeepTau2017v2p1VSmu");
        tauDiscriminators.push_back("decayModeFinding");
        tauDiscriminators.push_back("decayModeFindingNewDMs");

        for (std::string tauDiscriminator : tauDiscriminators)
        {
            if (quantity == tauDiscriminator + "_p")
            {
                FloatQuantities[tauDiscriminator+"_p"] = static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->getDiscriminator(tauDiscriminator, event.m_tauMetadata);
            }
        }
	//temporary fix for VVVLoose deep tau ID WP
        if (quantity == "byVVVLooseDeepTau2017v2p1VSjet_p")
        {
                FloatQuantities["byVVVLooseDeepTau2017v2p1VSjet_p"] = float(static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->getDiscriminator("byDeepTau2017v2p1VSjetraw", event.m_tauMetadata) > 0.2599605);
        };
        if (quantity == "byVVVLooseDeepTau2017v2p1VSe_p")
        {
                FloatQuantities["byVVVLooseDeepTau2017v2p1VSe_p"] = float(static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->getDiscriminator("byDeepTau2017v2p1VSeraw", event.m_tauMetadata) > 0.0630386);
        };
	//end of fix
        if (quantity == "metPt")
        {
                FloatQuantities["metPt"] = (static_cast<HttProduct const&>(product)).m_met.p4.Pt();
        }
        else if (quantity == "mt_t")
        {
                FloatQuantities["mt_t"] = Quantities::CalculateMt(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).first)->p4,product.m_met.p4);
        }

        if (quantity == "decayMode_p")
        {
            IntQuantities["decayMode_p"] = static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->decayMode;
        }

        if (quantity == "trkpt_p")
        {
            FloatQuantities["trkpt_p"] = static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->chargedHadronCandidates.size() > 0 ? static_cast<KTau*>(product.m_validDiTauPairCandidates.at(0).second)->chargedHadronCandidates[0].p4.Pt() : DefaultValues::UndefinedFloat;
        }

        if (quantity == "gen_match_p")
        {
            KLepton* lepton = static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).second);
            if (settings.GetUseUWGenMatching())
            {
                IntQuantities["gen_match_p"] = Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCodeUW(event, lepton));
            }
            else
            {
                KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(                                                                                                                  
                                                        lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons
                                                        );
                if (genParticle)
                {
                    IntQuantities["gen_match_p"] =  Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCode(genParticle));
                }
                else
                {
                    IntQuantities["gen_match_p"] =  Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_FAKE);
                }
            }
        }

        if (quantity == "puWeight")
        {
            FloatQuantities["puWeight"] = SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), SafeMap::GetWithDefault(product.m_optionalWeights, std::string("puWeight"), 1.0));
        }
        if (quantity == "bkgSubWeight")
        {
            FloatQuantities["bkgSubWeight"] = (product.m_isSingleMuon && !product.m_validDiTauPairCandidates.at(0).IsOppositelyCharged()) ? -1. : 1.; 
        }
}

std::string NewETTagAndProbePairConsumer::GetConsumerId() const
{
	return "NewETTagAndProbePairConsumer";
}
