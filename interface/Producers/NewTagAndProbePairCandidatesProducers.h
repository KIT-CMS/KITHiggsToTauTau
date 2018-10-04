
#pragma once

#include <boost/regex.hpp>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
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
        for (typename std::vector<TLepton1 *>::iterator tag = (product.*m_validLeptonsMember1).begin();
             tag != (product.*m_validLeptonsMember1).end(); ++tag)
        {
            for (typename std::vector<TLepton2 *>::iterator probe = (product.*m_validLeptonsMember2).begin();
                 probe != (product.*m_validLeptonsMember2).end(); ++probe)
            {
                // Check if lepton 1 passes the tag selection citerias, and lepton 2 passes probe selection criteria,
                // if so, a tagAndProbe Pair will be formed
                // Lepton 1 is the TAG Lepton
                // Lepton 2 is the Probe Lepton
                DiTauPair diTauPair(*tag, *probe);
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

class NewMTTagAndProbePairCandidatesProducer : public NewTagAndProbePairCandidatesProducerBase<KMuon, KTau>
{
  public:
    NewMTTagAndProbePairCandidatesProducer();
    virtual std::string GetProducerId() const override;

  protected:
    virtual bool AdditionalTagCriteria(DiTauPair const &diTauPair, event_type const &event,
                                       product_type &product, setting_type const &settings,
                                       std::map<std::string, std::vector<float>> m_tagSelectionCuts) const override;
    virtual bool AdditionalProbeCriteria(DiTauPair const &diTauPair, event_type const &event,
                                       product_type &product, setting_type const &settings,
                                       std::map<std::string, std::vector<float>> m_probeSelectionCuts) const override;
};
