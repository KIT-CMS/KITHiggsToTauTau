
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "boost/functional/hash.hpp"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producer for the MET
*/


class MetCollector: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
        
        std::string GetProducerId() const
	{
		return "MetCollector";
	}
	
	void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
		
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metSumEt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.sumEt;
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metPt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.p4.Pt();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metPx", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.p4.Px();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metPy", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.p4.Py();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metPz", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.p4.Pz();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metPhi", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.p4.Phi();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metCov00", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.significance.At(0, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metCov01", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.significance.At(0, 1);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metCov10", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.significance.At(1, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metCov11", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.significance.At(1, 1);
		});

		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetSumEt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.sumEt;
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetPt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.p4.Pt();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetPhi", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.p4.Phi();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov00", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.significance.At(0, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov01", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.significance.At(0, 1);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov10", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.significance.At(1, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov11", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.significance.At(1, 1);
		});
	
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetSumEt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.sumEt;
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetPt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.p4.Pt();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetPx", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.p4.Px();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetPy", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.p4.Py();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetPz", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.p4.Pz();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetPhi", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.p4.Phi();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetCov00", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.significance.At(0, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetCov01", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.significance.At(0, 1);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetCov10", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.significance.At(1, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puppiMetCov11", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_puppimet.significance.At(1, 1);
		});
	}

	void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		if (event.m_met != nullptr) product.m_pfmetUncorr = (event.m_met);
                else assert(event.m_met != nullptr);
		if (event.m_puppiMet != nullptr) product.m_puppimetUncorr = (event.m_puppiMet);
                else assert(event.m_puppiMet != nullptr);
			
		// Copy the MET object, for possible future corrections
		product.m_pfmet = *(product.m_pfmetUncorr);
                product.m_puppimet = *(product.m_puppimetUncorr);
                
		product.m_metUncorr = product.m_pfmetUncorr;
		product.m_met = product.m_pfmet;
	}
	
};
