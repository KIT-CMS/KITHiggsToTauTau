#pragma once

#include "Artus/Core/interface/ProducerBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

//template <class HttTypes>
class TauQuantitiesForTauIDFakeRateMeasurementProducer : public ProducerBase<HttTypes>
{
  public:
	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

        virtual std::string GetProducerId() const override
        {
            return "TauQuantitiesForTauIDFakeRateMeasurementProducer";
        }

	void Init(setting_type const &settings) override;

	void Produce(event_type const& event, product_type& product, setting_type const& settings) const override;

  private:
};
