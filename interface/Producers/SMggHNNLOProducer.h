#pragma once

#include "../HttTypes.h"
#include "TGraph.h"
#include "TSystem.h"


class SMggHNNLOProducer: public ProducerBase<HttTypes> {
public:

    typedef typename HttTypes::event_type event_type;
    typedef typename HttTypes::product_type product_type;
    typedef typename HttTypes::setting_type setting_type;

    virtual std::string GetProducerId() const override {
        return "SMggHNNLOProducer";
    }
    
    virtual void Init(setting_type const& settings) override;

    virtual void Produce(event_type const& event, product_type& product,
                         setting_type const& settings) const override;

private:
    TGraphErrors* WeightsGraphs[4];
};