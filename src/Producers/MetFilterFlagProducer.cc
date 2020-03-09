
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetFilterFlagProducer.h"

void MetFilterFlagProducer::Init(setting_type const& settings)
{
    ProducerBase<HttTypes>::Init(settings);
    //FilterBase<HttTypes>::Init(settings);

    LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("flagMETFilter", [](event_type const& event, product_type const& product, setting_type const& settings) {
        return product.m_MetFilter;
    });

    // Single filters: DO NOT SUPPORT '!' SYNTAX!
    LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("Flag_goodVertices", [](event_type const& event, product_type const& product, setting_type const& settings) {
        int filterid = event.m_triggerObjectMetadata->metFilterPos("Flag_goodVertices");
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        return result;
    });
    LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("Flag_globalSuperTightHalo2016Filter", [](event_type const& event, product_type const& product, setting_type const& settings) {
        int filterid = event.m_triggerObjectMetadata->metFilterPos("Flag_globalSuperTightHalo2016Filter");
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        return result;
    });
    LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("Flag_HBHENoiseFilter", [](event_type const& event, product_type const& product, setting_type const& settings) {
        int filterid = event.m_triggerObjectMetadata->metFilterPos("Flag_HBHENoiseFilter");
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        return result;
    });
    LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("Flag_HBHENoiseIsoFilter", [](event_type const& event, product_type const& product, setting_type const& settings) {
        int filterid = event.m_triggerObjectMetadata->metFilterPos("Flag_HBHENoiseIsoFilter");
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        return result;
    });
    LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("Flag_EcalDeadCellTriggerPrimitiveFilter", [](event_type const& event, product_type const& product, setting_type const& settings) {
        int filterid = event.m_triggerObjectMetadata->metFilterPos("Flag_EcalDeadCellTriggerPrimitiveFilter");
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        return result;
    });
    LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("Flag_BadPFMuonFilter", [](event_type const& event, product_type const& product, setting_type const& settings) {
        int filterid = event.m_triggerObjectMetadata->metFilterPos("Flag_BadPFMuonFilter");
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        return result;
    });
    LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("Flag_BadChargedCandidateFilter", [](event_type const& event, product_type const& product, setting_type const& settings) {
        int filterid = event.m_triggerObjectMetadata->metFilterPos("Flag_BadChargedCandidateFilter");
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        return result;
    });
    LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("Flag_eeBadScFilter", [](event_type const& event, product_type const& product, setting_type const& settings) {
        int filterid = event.m_triggerObjectMetadata->metFilterPos("Flag_eeBadScFilter");
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        return result;
    });
    LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("ecalBadCalibReducedMINIAODFilter", [](event_type const& event, product_type const& product, setting_type const& settings) {
        int filterid = event.m_triggerObjectMetadata->metFilterPos("ecalBadCalibReducedMINIAODFilter");
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        return result;
    });


    std::vector<std::string> tmpMetFiltersToFlag = settings.GetMetFilterToFlag();
    for(auto filter: tmpMetFiltersToFlag)
    {
        if(filter.at(0) == '!')
        {
            std::string filterName = filter.substr(1);
            m_invertedFilters_flag.push_back(filterName);
            m_metFilters_flag.push_back(filterName);
        }
        else
        {
            m_metFilters_flag.push_back(filter);
        }
    }
}

void MetFilterFlagProducer::Produce(event_type const& event, product_type& product,
                            setting_type const& settings) const
{
    for (auto metfilter : m_metFilters_flag)
    {
        int filterid = event.m_triggerObjectMetadata->metFilterPos(metfilter);
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        //std::cout << "MetFilter Name: " << metfilter << " Decision: " << result << std::endl;
        // check if the filter should be inverted
        if(std::find(m_invertedFilters_flag.begin(),m_invertedFilters_flag.end(), metfilter) != m_invertedFilters_flag.end())
        {
            result = !result;
        }
        product.m_MetFilter = product.m_MetFilter && result;
    }
}

