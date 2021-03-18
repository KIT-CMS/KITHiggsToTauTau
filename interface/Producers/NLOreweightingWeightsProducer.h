#pragma once

#include "../HttTypes.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"


class NLOreweightingWeightsProducer: public ProducerBase<HttTypes> {
public:

    typedef typename HttTypes::event_type event_type;
    typedef typename HttTypes::product_type product_type;
    typedef typename HttTypes::setting_type setting_type;

    virtual std::string GetProducerId() const override {
        return "NLOreweightingWeightsProducer";
    }
    
    virtual void Init(setting_type const& settings) override;

    virtual void Produce(event_type const& event, product_type& product,
                         setting_type const& settings) const override;

private:
    std::vector<std::string> m_higgs_bosons;
    std::vector<std::string> m_uncertainties;
    std::vector<std::string> m_contributions;
};
