#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

/**
   Producer used to apply the correction of the FakeMET in embedded events
   Details: https://indico.cern.ch/event/1005631/contributions/4221822/attachments/2185217/3693362/Embed_MET_correction.pdf
*/

class EmbeddingMETCorrector: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
	}

	virtual void Produce(event_type const& event, product_type & product,
	                     setting_type const& settings) const override;

};