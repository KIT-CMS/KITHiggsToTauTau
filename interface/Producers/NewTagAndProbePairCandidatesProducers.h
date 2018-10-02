
#pragma once

#include <boost/regex.hpp>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producers for candidates of di-tau pairs
*/

template <class TLepton1, class TLepton2>
class NewTagAndProbePairCandidatesProducerBase : public ProducerBase<HttTypes>
{
  public:
    typedef typename HttTypes::event_type event_type;
    typedef typename HttTypes::product_type product_type;
    typedef typename HttTypes::setting_type setting_type;

    NewTagAndProbePairCandidatesProducerBase(std::vector<TLepton1 *> product_type::*validLeptonsMember1,
                                             std::vector<TLepton2 *> product_type::*validLeptonsMember2) : ProducerBase<HttTypes>(),
                                                                                                           m_validLeptonsMember1(validLeptonsMember1),
                                                                                                           m_validLeptonsMember2(validLeptonsMember2)
    {
    }

    virtual void Init(setting_type const &settings) override
    {
        ProducerBase<HttTypes>::Init(settings);

        // Lambda Functions for ID of both leptons

        LambdaNtupleConsumer<HttTypes>::AddVIntQuantity("id_muon_medium_t", [](event_type const &event, product_type const &product) {
            std::vector <int> id_muon;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                id_muon.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->idMedium());
            }
            return id_muon;
        });
        LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("pt_t", [](event_type const &event, product_type const &product) {
            std::vector <float> pt_1;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                pt_1.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4.Pt());
            }
            return pt_1;
        });
        LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("pt_p", [](event_type const &event, product_type const &product) {
            std::vector <float> pt_2;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                pt_2.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4.Pt());
            }
            return pt_2;
        });
        LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("iso_t", [](event_type const &event, product_type const &product) {
            std::vector <float> iso_1;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                iso_1.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->pfIso());
            }
            return iso_1;
        });
        LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("iso_p", [](event_type const &event, product_type const &product) {
            std::vector <float> iso_2;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                iso_2.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->pfIso());
            }
            return iso_2;
        });
        LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("eta_t", [](event_type const &event, product_type const &product) {
            std::vector <float> eta_1;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                eta_1.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4.Eta());
            }
            return eta_1;
        });
        LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("eta_p", [](event_type const &event, product_type const &product) {
            std::vector <float> eta_2;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                eta_2.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4.Eta());
            }
            return eta_2;
        });
        LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("phi_t", [](event_type const &event, product_type const &product) {
            std::vector <float> phi_1;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                phi_1.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4.Phi());
            }
            return phi_1;
        });
        LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("phi_p", [](event_type const &event, product_type const &product) {
            std::vector <float> phi_2;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                phi_2.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4.Phi());
            }
            return phi_2;
        });
        LambdaNtupleConsumer<HttTypes>::AddVIntQuantity("id_muon_medium_p", [](event_type const &event, product_type const &product) {
            std::vector <int> id_muon;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                id_muon.push_back(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->idMedium());
            }
            return id_muon;
        });
        LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("m_ll", [](event_type const &event, product_type const &product) {
            std::vector<float> mll;
            for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
            {
                mll.push_back(product.m_validMuons.size() >= 2 ? (static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->p4 + 
            static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->p4).M() : DefaultValues::UndefinedFloat);
            }
            return mll;
        });
                // LambdaNtupleConsumer<HttTypes>::AddIntQuantity("id_muon_tight_1", [](event_type const &event, product_type const &product) {
        //     return product.m_validMuons.size() >= 2 ? static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(0).first)->idTight() : DefaultValues::UndefinedFloat;
        // });
        // LambdaNtupleConsumer<HttTypes>::AddIntQuantity("id_muon_tight_2", [](event_type const &event, product_type const &product) {
        //     return product.m_validMuons.size() >= 2 ? static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(0).second)->idTight() : DefaultValues::UndefinedFloat;
        // });

        // configurations possible:
        // "cut" --> applied to all pairs
        // "<index in setting HltPaths>:<cut>" --> applied to pairs that fired and matched ONLY the indexed HLT path
        // "<HLT path regex>:<cut>" --> applied to pairs that fired and matched ONLY the given HLT path
        // m_lepton1LowerPtCutsByIndex = Utility::ParseMapTypes<size_t, float>(
        //         Utility::ParseVectorToMap(settings.GetDiTauPairLepton1LowerPtCuts()), m_lepton1LowerPtCutsByHltName
        // );
        // m_lepton2LowerPtCutsByIndex = Utility::ParseMapTypes<size_t, float>(
        //         Utility::ParseVectorToMap(settings.GetDiTauPairLepton2LowerPtCuts()), m_lepton2LowerPtCutsByHltName
        // );

        // m_lepton1UpperEtaCutsByIndex = Utility::ParseMapTypes<size_t, float>(
        //         Utility::ParseVectorToMap(settings.GetDiTauPairLepton1UpperEtaCuts()), m_lepton1UpperEtaCutsByHltName
        // );
        // m_lepton2UpperEtaCutsByIndex = Utility::ParseMapTypes<size_t, float>(
        //         Utility::ParseVectorToMap(settings.GetDiTauPairLepton2UpperEtaCuts()), m_lepton2UpperEtaCutsByHltName
        // );

        std::vector<std::string> lepton1CheckTriggerMatchByHltName = settings.GetCheckLepton1TriggerMatch();
        std::vector<std::string> lepton2CheckTriggerMatchByHltName = settings.GetCheckLepton2TriggerMatch();

        m_hltFiredBranchNames = Utility::ParseVectorToMap(settings.GetHLTBranchNames());

        // add possible quantities for the lambda ntuples consumers
        // LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nDiTauPairCandidates", [](event_type const& event, product_type const& product)
        // {
        //     return static_cast<int>(product.m_validDiTauPairCandidates.size());
        // });
        // LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nAllDiTauPairCandidates", [](event_type const& event, product_type const& product)
        // {
        //     return static_cast<int>(product.m_validDiTauPairCandidates.size()+product.m_invalidDiTauPairCandidates.size());
        // });

        // debug output in initialization step
        // LOG(DEBUG) << "Settings for Lepton 1 Pt Cuts: ";
        // for(unsigned int i = 0; i < settings.GetDiTauPairLepton1LowerPtCuts().size(); i++)
        // {
        //     LOG(DEBUG) << settings.GetDiTauPairLepton1LowerPtCuts().at(i);
        // }
        // LOG(DEBUG) << "Settings for Lepton 2 Pt Cuts: ";
        // for(unsigned int i = 0; i < settings.GetDiTauPairLepton2LowerPtCuts().size(); i++)
        // {
        //     LOG(DEBUG) << settings.GetDiTauPairLepton2LowerPtCuts().at(i);
        // }
        // LOG(DEBUG) << "Amount of lepton 1 Pt Cuts by Hlt Name: " << m_lepton1LowerPtCutsByHltName.size();
        // LOG(DEBUG) << "Amount of lepton 2 Pt Cuts by Hlt Name: " << m_lepton2LowerPtCutsByHltName.size();
        // LOG(DEBUG) << "Now, the new fancy Producer is active!";
        for (auto hltNames : m_hltFiredBranchNames)
        {
            // std::map<std::string, std::vector<float>> lepton1LowerPtCutsByHltName = m_lepton1LowerPtCutsByHltName;
            // std::map<std::string, std::vector<float>> lepton2LowerPtCutsByHltName = m_lepton2LowerPtCutsByHltName;
            // std::map<std::string, std::vector<float>> lepton1UpperEtaCutsByHltName = m_lepton1UpperEtaCutsByHltName;
            // std::map<std::string, std::vector<float>> lepton2UpperEtaCutsByHltName = m_lepton2UpperEtaCutsByHltName;
            bool lepton1CheckL1Match = settings.GetCheckL1MatchForDiTauPairLepton1();
            bool lepton2CheckL1Match = settings.GetCheckL1MatchForDiTauPairLepton2();
            LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(hltNames.first, [lepton1CheckL1Match, lepton2CheckL1Match, lepton1CheckTriggerMatchByHltName, lepton2CheckTriggerMatchByHltName, hltNames
                                                                             //lepton1LowerPtCutsByHltName, lepton2LowerPtCutsByHltName, lepton1UpperEtaCutsByHltName, lepton2UpperEtaCutsByHltName
            ](event_type const &event, product_type const &product) {
                std::vector <int> diTauPairFiredTriggerVector;
                for (size_t i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
                {
                    bool diTauPairFiredTrigger = false;
                    LOG(DEBUG) << "Beginning of lambda function for " << hltNames.first;
                    bool checkLep1 = std::find(lepton1CheckTriggerMatchByHltName.begin(), lepton1CheckTriggerMatchByHltName.end(), hltNames.first) != lepton1CheckTriggerMatchByHltName.end();
                    bool checkLep2 = std::find(lepton2CheckTriggerMatchByHltName.begin(), lepton2CheckTriggerMatchByHltName.end(), hltNames.first) != lepton2CheckTriggerMatchByHltName.end();
                    for (auto hltName : hltNames.second)
                    {
                        bool hltFired1 = false;
                        bool hltFired2 = false;
                        if (checkLep1)
                        {
                            LOG(DEBUG) << "Checking trigger object matching for lepton 1";
                            if (product.m_leptonTriggerMatch.find(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)) != product.m_leptonTriggerMatch.end())
                            {
                                auto trigger1 = product.m_leptonTriggerMatch.at(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first));
                                for (auto hlts : (*trigger1))
                                {
                                    if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
                                    {
                                        hltFired1 = hlts.second;
                                    }
                                }
                                LOG(DEBUG) << "Found trigger for the lepton 1? " << hltFired1;
                                // // passing kinematic cuts for trigger
                                // if (lepton1LowerPtCutsByHltName.find(hltName) != lepton1LowerPtCutsByHltName.end())
                                // {
                                //     hltFired1 = hltFired1 &&
                                //                     (product.m_validDiTauPairCandidates.at(0).first->p4.Pt() > *std::max_element(lepton1LowerPtCutsByHltName.at(hltName).begin(), lepton1LowerPtCutsByHltName.at(hltName).end()));
                                //     LOG(DEBUG) << "lepton 1 Pt: " << product.m_validDiTauPairCandidates.at(0).first->p4.Pt() << " threshold: " << *std::max_element(lepton1LowerPtCutsByHltName.at(hltName).begin(), lepton1LowerPtCutsByHltName.at(hltName).end());
                                // }
                                // if (lepton1UpperEtaCutsByHltName.find(hltName) != lepton1UpperEtaCutsByHltName.end())
                                // {
                                //     hltFired1 = hltFired1 &&
                                //                     (std::abs(product.m_validDiTauPairCandidates.at(0).first->p4.Eta()) < *std::min_element(lepton1UpperEtaCutsByHltName.at(hltName).begin(), lepton1UpperEtaCutsByHltName.at(hltName).end()));
                                //     LOG(DEBUG) << "lepton 1 |Eta|: " << std::abs(product.m_validDiTauPairCandidates.at(0).first->p4.Eta()) << " threshold: " << *std::min_element(lepton1UpperEtaCutsByHltName.at(hltName).begin(), lepton1UpperEtaCutsByHltName.at(hltName).end());
                                // }
                                // LOG(DEBUG) << "lepton 1 passes also kinematic cuts? " << hltFired1;
                                if (lepton1CheckL1Match)
                                {
                                    if (product.m_detailedL1MatchedLeptons.find(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)) != product.m_detailedL1MatchedLeptons.end())
                                    {
                                        auto l1_1 = product.m_detailedL1MatchedLeptons.at(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first));
                                        for (auto hlts : l1_1)
                                        {
                                            if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
                                            {
                                                hltFired1 = hltFired1 && hlts.second;
                                            }
                                        }
                                    }
                                    LOG(DEBUG) << "lepton 1 passes also l1 matching? " << hltFired1;
                                }
                            }
                        }
                        else
                            hltFired1 = true;
                        if (checkLep2)
                        {
                            LOG(DEBUG) << "Checking trigger object matching for lepton 2";
                            if (product.m_leptonTriggerMatch.find(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)) != product.m_leptonTriggerMatch.end())
                            {
                                auto trigger2 = product.m_leptonTriggerMatch.at(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second));
                                for (auto hlts : (*trigger2))
                                {
                                    if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
                                    {
                                        hltFired2 = hlts.second;
                                    }
                                }
                                LOG(DEBUG) << "Found trigger for the lepton 2? " << hltFired2;
                                // passing kinematic cuts for trigger
                                // if (lepton2LowerPtCutsByHltName.find(hltName) != lepton2LowerPtCutsByHltName.end())
                                // {
                                //     hltFired2 = hltFired2 &&
                                //             (product.m_validDiTauPairCandidates.at(0).second->p4.Pt() > *std::max_element(lepton2LowerPtCutsByHltName.at(hltName).begin(), lepton2LowerPtCutsByHltName.at(hltName).end()));
                                //     LOG(DEBUG) << "lepton 2 Pt: " << product.m_validDiTauPairCandidates.at(0).second->p4.Pt() << " threshold: " << *std::max_element(lepton2LowerPtCutsByHltName.at(hltName).begin(), lepton2LowerPtCutsByHltName.at(hltName).end());
                                // }
                                // if (lepton2UpperEtaCutsByHltName.find(hltName) != lepton2UpperEtaCutsByHltName.end())
                                // {
                                //     hltFired2 = hltFired2 &&
                                //                     (std::abs(product.m_validDiTauPairCandidates.at(0).second->p4.Eta()) < *std::min_element(lepton2UpperEtaCutsByHltName.at(hltName).begin(), lepton2UpperEtaCutsByHltName.at(hltName).end()));
                                //     LOG(DEBUG) << "lepton 2 |Eta|: " << std::abs(product.m_validDiTauPairCandidates.at(0).second->p4.Eta()) << " threshold: " << *std::min_element(lepton2UpperEtaCutsByHltName.at(hltName).begin(), lepton2UpperEtaCutsByHltName.at(hltName).end());
                                // }
                                // LOG(DEBUG) << "lepton 2 passes also kinematic cuts? " << hltFired2;
                                if (lepton2CheckL1Match)
                                {
                                    if (product.m_detailedL1MatchedLeptons.find(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)) != product.m_detailedL1MatchedLeptons.end())
                                    {
                                        auto l1_2 = product.m_detailedL1MatchedLeptons.at(static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second));
                                        for (auto hlts : l1_2)
                                        {
                                            if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
                                            {
                                                hltFired2 = hltFired2 && hlts.second;
                                            }
                                        }
                                    }
                                    LOG(DEBUG) << "lepton 2 passes also l1 matching? " << hltFired2;
                                }
                            }
                        }
                        else
                            hltFired2 = true;
                        bool hltFired = hltFired1 && hltFired2;
                        diTauPairFiredTrigger = diTauPairFiredTrigger || hltFired;
                    }
                    LOG(DEBUG) << "Tau pair with valid trigger match? " << diTauPairFiredTrigger;
                    diTauPairFiredTriggerVector.push_back(diTauPairFiredTrigger);
                }
                return diTauPairFiredTriggerVector;
            });
        }
    }

    virtual void Produce(event_type const &event, product_type &product,
                         setting_type const &settings) const override
    {
        product.m_validDiTauPairCandidates.clear();
        LOG(DEBUG) << this->GetProducerId() << " -----START-----";
        LOG(DEBUG) << "Processing run:lumi:event " << event.m_eventInfo->nRun << ":" << event.m_eventInfo->nLumi << ":" << event.m_eventInfo->nEvent;
        LOG(DEBUG) << "Size of valid candidates for lepton 1: " << (product.*m_validLeptonsMember1).size();
        LOG(DEBUG) << "Size of valid candidates for lepton 2: " << (product.*m_validLeptonsMember2).size();
        // Parse selection criteria from Config
        std::map<std::string, std::vector<float>> m_tagSelectionCuts;
        std::map<std::string, std::vector<float>> m_probeSelectionCuts;
        Utility::ParseMapTypes<size_t, float>(
            Utility::ParseVectorToMap(settings.GetTagAdditionalCriteria()), m_tagSelectionCuts);
        Utility::ParseMapTypes<size_t, float>(
            Utility::ParseVectorToMap(settings.GetTagAdditionalCriteria()), m_probeSelectionCuts);
        // build pairs for all combinations
        for (typename std::vector<TLepton1 *>::iterator lepton1 = (product.*m_validLeptonsMember1).begin();
             lepton1 != (product.*m_validLeptonsMember1).end(); ++lepton1)
        {
            for (typename std::vector<TLepton2 *>::iterator lepton2 = (product.*m_validLeptonsMember2).begin();
                 lepton2 != (product.*m_validLeptonsMember2).end(); ++lepton2)
            {
                // Check if lepton 1 passes the tag selection citerias, and lepton 2 passes probe selection criteria,
                // if so, a tagAndProbe Pair will be formed
                // Lepton 1 is the TAG Lepton
                // Lepton 2 is the Probe Lepton
                DiTauPair diTauPair(*lepton1, *lepton2);
                bool validDiTauPair = false;
                if (AdditionalTagCriteria(diTauPair, event, product, settings, m_tagSelectionCuts) && AdditionalProbeCriteria(diTauPair, event, product, settings, m_probeSelectionCuts))
                {
                    LOG(DEBUG) << "Pair passed Selection Criteria.";
                    // pair selections
                    validDiTauPair = true;
                    // delta R cut
                    validDiTauPair = validDiTauPair && ((settings.GetDiTauPairMinDeltaRCut() < 0.0) || (diTauPair.GetDeltaR() > static_cast<double>(settings.GetDiTauPairMinDeltaRCut())));
                    LOG(DEBUG) << "Pair passed the delta R cut of " << settings.GetDiTauPairMinDeltaRCut() << "? " << validDiTauPair << ", because computed value is " << diTauPair.GetDeltaR();
                }
                if (validDiTauPair)
                {
                    product.m_validDiTauPairCandidates.push_back(diTauPair);
                }
                else
                {
                    product.m_invalidDiTauPairCandidates.push_back(diTauPair);
                }
            }
        }

        // Loop over valid diTauPairs with deltaR:
        for (unsigned int i = 0; i < product.m_validDiTauPairCandidates.size(); i++)
        {
            LOG(DEBUG) << "Delta R separation within valid Pair:" << product.m_validDiTauPairCandidates.at(i).GetDeltaR();
        }
        if (product.m_validDiTauPairCandidates.size() > 0)
        {
            LOG(DEBUG) << "First Tau Candidate in first pair: " << product.m_validDiTauPairCandidates.at(0).first->p4;
            LOG(DEBUG) << "Second Tau Candidate in first pair: " << product.m_validDiTauPairCandidates.at(0).second->p4;
        }
        LOG(DEBUG) << "Number of valid Pairs: " << product.m_validDiTauPairCandidates.size();
        LOG(DEBUG) << this->GetProducerId() << " -----END-----";

        // Add Lambda Functions for additional Variables
    }

  protected:
    // Can be overwritten for special use cases
    virtual bool AdditionalTagCriteria(DiTauPair const &diTauPair, event_type const &event,
									   product_type &product, setting_type const &settings,
                                        std::map<std::string, std::vector<float>> m_tagSelectionCuts) const
    {
        bool validDiTauPair = true;
        return validDiTauPair;
    }
    virtual bool AdditionalProbeCriteria(DiTauPair const &diTauPair, event_type const &event,
                                         product_type &product, setting_type const &settings,
                                         std::map<std::string, std::vector<float>> m_probeSelectionCuts) const
    {
        bool validDiTauPair = true;
        return validDiTauPair;
    }

  private:
    std::vector<TLepton1 *> product_type::*m_validLeptonsMember1;
    std::vector<TLepton2 *> product_type::*m_validLeptonsMember2;

    // std::map<size_t, std::vector<float> > m_lepton1LowerPtCutsByIndex;
    // std::map<std::string, std::vector<float> > m_lepton1LowerPtCutsByHltName;
    // std::map<size_t, std::vector<float> > m_lepton2LowerPtCutsByIndex;
    // std::map<std::string, std::vector<float> > m_lepton2LowerPtCutsByHltName;

    // std::map<size_t, std::vector<float> > m_lepton1UpperEtaCutsByIndex;
    // std::map<std::string, std::vector<float> > m_lepton1UpperEtaCutsByHltName;
    // std::map<size_t, std::vector<float> > m_lepton2UpperEtaCutsByIndex;
    // std::map<std::string, std::vector<float> > m_lepton2UpperEtaCutsByHltName;

    std::map<std::string, std::vector<std::string>> m_hltFiredBranchNames;
};

class NewMMTagAndProbePairCandidatesProducer : public NewTagAndProbePairCandidatesProducerBase<KMuon, KMuon>
{
  public:
    NewMMTagAndProbePairCandidatesProducer();
    virtual std::string GetProducerId() const override;

  protected:
    virtual bool AdditionalTagCriteria(DiTauPair const &diTauPair, event_type const &event,
                                       product_type &product, setting_type const &settings,
                                       std::map<std::string, std::vector<float>> m_tagSelectionCuts) const override;
};