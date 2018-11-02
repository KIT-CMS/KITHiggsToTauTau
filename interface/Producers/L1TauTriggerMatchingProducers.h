
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

template<class TLepton>
class L1TauTriggerMatchingProducerBase: public ProducerBase<HttTypes>
{
    public:
        typedef typename HttTypes::event_type event_type;
        typedef typename HttTypes::product_type product_type;
        typedef typename HttTypes::setting_type setting_type;

        void Init(setting_type const& settings) override
        {
            ProducerBase<HttTypes>::Init(settings);
            Utility::ParseMapTypes<size_t, float>(Utility::ParseVectorToMap((settings.*GetLeptonTriggerCheckAdditionalL1TauMatchLowerPtCut)()), m_leptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNickFromSettings);
            Utility::ParseMapTypes<size_t, float>(Utility::ParseVectorToMap((settings.*GetLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCut)()), m_leptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNickFromSettings);
        }

        L1TauTriggerMatchingProducerBase(std::map<TLepton*, std::map<std::string, bool> > product_type::*additionalL1TauMatchedLeptons,
                                         std::map<TLepton*, std::map<std::string, bool> > product_type::*leptonTriggerMatch,
                                         std::vector<TLepton*> product_type::*validObjects,
                                         std::map<std::string, std::vector<float> > product_type::*settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick,
                                         std::map<std::string, std::vector<float> > product_type::*settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick,
                                         std::vector<std::string>& (setting_type::*GetLeptonTriggerCheckAdditionalL1TauMatchLowerPtCut)(void) const,
                                         std::vector<std::string>& (setting_type::*GetLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCut)(void) const,
                                         std::vector<std::string>& (setting_type::*GetLeptonTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau)(void) const,
                                         bool (setting_type::*GetInvertedLeptonL1TauMatching)(void) const):
                         ProducerBase<HttTypes>(),
                         m_additionalL1TauMatchedLeptons(additionalL1TauMatchedLeptons),
                         m_leptonTriggerMatch(leptonTriggerMatch),
                         m_validObjects(validObjects),
                         m_settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick(settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick),
                         m_settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick(settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick),
                         GetLeptonTriggerCheckAdditionalL1TauMatchLowerPtCut(GetLeptonTriggerCheckAdditionalL1TauMatchLowerPtCut),
                         GetLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCut(GetLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCut),
                         GetLeptonTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau(GetLeptonTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau),
                         GetInvertedLeptonL1TauMatching(GetInvertedLeptonL1TauMatching)
        {
        }

        virtual void Produce(event_type const& event, product_type& product,
                             setting_type const& settings) const override
        {
                if ((product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick).empty())
                {
                    (product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick).insert(m_leptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNickFromSettings.begin(),
                                                                                                        m_leptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNickFromSettings.end());
                }
                if ((product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick).empty())
                {
                    (product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick).insert(m_leptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNickFromSettings.begin(),
                                                                                                        m_leptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNickFromSettings.end());
                }

                std::map<std::string, bool> useL1TauIsolationByHltNick;
                for (auto hltNick : (settings.*GetLeptonTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau)())
                {
                    useL1TauIsolationByHltNick[hltNick] = true;
                }

                // TODO: Maybe clear products created later on
                if (m_leptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNickFromSettings.size() > 0)
                {
                    if ((settings.*GetInvertedLeptonL1TauMatching)())
                    {
                        LOG(DEBUG) << "Starting to find L1Tau objects not overlapping with leptons...";
                        // Search for L1 Tau in event fulfilling quality requirements not overlapping with considered Lepton.
                        for (typename std::vector<TLepton*>::iterator validObject = (product.*m_validObjects).begin();
                             validObject != (product.*m_validObjects).end(); ++validObject)
                        {
                            std::map<std::string, bool> hlt_to_l1;
                            for (std::map<std::string, std::vector<float> >::const_iterator hlt = (product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick).begin();                       
                                    hlt != (product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick).end(); ++hlt)
                            {
                                hlt_to_l1[hlt->first] = false;
                                float deltaRMin = 0.2;
                                for (std::vector<KL1Tau>::iterator l1o = event.m_l1taus->begin(); l1o != event.m_l1taus->end(); l1o++)
                                {
                                    float currentDeltaR = ROOT::Math::VectorUtil::DeltaR((*validObject)->p4, l1o->p4);
                                    if (currentDeltaR > deltaRMin)
                                    {
                                        LOG(DEBUG) << "Found L1Tau not overlapping with lepton. Checking for cuts now...";
                                        LOG(DEBUG) << "Checking for pT threshold of :" << *std::max_element(hlt->second.begin(), hlt->second.end());
                                        if (l1o->p4.Pt() > *std::max_element(hlt->second.begin(), hlt->second.end()))
                                        {
                                            LOG(DEBUG) << "L1Tau with pT " << l1o->p4.Pt() << " passes pT threshold. \n Checking for eta threshold if necessary.";
                                            if (!((product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick).find(hlt->first) != (product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick).end()) || std::abs(l1o->p4.Eta()) < *std::min_element((product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick)[hlt->first].begin(), (product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick)[hlt->first].end()))
                                            {
                                                LOG(DEBUG) << "L1Tau passes eta cut. \n Check for L1 isolation if necessary.";
                                                LOG(DEBUG) << "L1Tau object is isolated? " << l1o->hwIso;
                                                if (!(useL1TauIsolationByHltNick.find(hlt->first) != useL1TauIsolationByHltNick.end()) || l1o->hwIso)
                                                {
                                                        LOG(DEBUG) << "Found L1Tau not overlapping with lepton and passing all cuts.";
                                                        hlt_to_l1[hlt->first] = true;
                                                        break;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            (product.*m_additionalL1TauMatchedLeptons)[*(validObject)] = hlt_to_l1;
                        }
                    }
                    else
                    {
                        LOG(DEBUG) << "Starting to find L1Tau trigger matches...";
                        for (typename std::map<TLepton*, std::map<std::string, bool > >::iterator it = (product.*m_leptonTriggerMatch).begin();
                             it != (product.*m_leptonTriggerMatch).end(); ++it)
                        {
                                float deltaRMax = 0.5;
                                float bestL1Pt = -1.0;
                                for (std::vector<KL1Tau>::iterator l1o = event.m_l1taus->begin(); l1o != event.m_l1taus->end(); ++l1o)
                                {
                                        float currentDeltaR = ROOT::Math::VectorUtil::DeltaR((it->first)->p4, l1o->p4);
                                        if(currentDeltaR < deltaRMax)
                                        {
                                                bestL1Pt = l1o->p4.Pt();
                                                deltaRMax = currentDeltaR;
                                        }
                                }
                                std::map<std::string, bool> hlt_to_l1;
                                for (std::map<std::string, std::vector<float> >::const_iterator hlt = (product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick).begin();
                                        hlt != (product.*m_settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick).end(); ++hlt)
                                {
                                        LOG(DEBUG) << "Check L1 trigger matching for trigger nick: " << hlt->first << "\t with threshold: " << *std::max_element(hlt->second.begin(), hlt->second.end());
                                        hlt_to_l1[hlt->first] = bestL1Pt >= *std::max_element(hlt->second.begin(), hlt->second.end());
                                        LOG(DEBUG) << "Lepton matches to L1 object with pT " << bestL1Pt << "? " << hlt_to_l1[hlt->first];
                                }
                                (product.*m_additionalL1TauMatchedLeptons)[&(*(it->first))] = hlt_to_l1;
                        }
                    }
                }
        }

    private:
        std::map<TLepton*, std::map<std::string, bool> > product_type::*m_additionalL1TauMatchedLeptons;
        std::map<TLepton*, std::map<std::string, bool> > product_type::*m_leptonTriggerMatch;
        std::vector<TLepton*> product_type::*m_validObjects;
        std::map<std::string, std::vector<float> > product_type::*m_settingsLeptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick;
        std::map<std::string, std::vector<float> > product_type::*m_settingsLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick;
        std::vector<std::string>& (setting_type::*GetLeptonTriggerCheckAdditionalL1TauMatchLowerPtCut)(void) const;
        std::vector<std::string>& (setting_type::*GetLeptonTriggerCheckAdditionalL1TauMatchUpperEtaCut)(void) const;
        std::vector<std::string>& (setting_type::*GetLeptonTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau)(void) const;
        bool (setting_type::*GetInvertedLeptonL1TauMatching)(void) const;

        std::map<std::string, std::vector<float> > m_leptonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNickFromSettings;
        std::map<std::string, std::vector<float> > m_leptonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNickFromSettings;
};

class TauL1TauTriggerMatchingProducer : public L1TauTriggerMatchingProducerBase<KTau>
{
    public:
        TauL1TauTriggerMatchingProducer();
        virtual std::string GetProducerId() const override;
        void Produce(event_type const& event, product_type& product,
                     setting_type const& settings) const override;
};

class MuonL1TauTriggerMatchingProducer : public L1TauTriggerMatchingProducerBase<KMuon>
{
    public:
        MuonL1TauTriggerMatchingProducer();
        virtual std::string GetProducerId() const override;
        void Produce(event_type const& event, product_type& product,
                     setting_type const& settings) const override;
};

class ElectronL1TauTriggerMatchingProducer : public L1TauTriggerMatchingProducerBase<KElectron>
{
    public:
        ElectronL1TauTriggerMatchingProducer();
        virtual std::string GetProducerId() const override;
        void Produce(event_type const& event, product_type& product,
                     setting_type const& settings) const override;
};
