
#pragma once

#include "../HttTypes.h"


class DiBJetQuantitiesProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	typedef std::function<double(RMDLV const&)> dibjet_extractor_lambda;
	
	static double GetDiBJetQuantity(product_type const& product,
	                               dibjet_extractor_lambda dibjetQuantity);

	static double GetJetPlusBJetQuantity(product_type const& product,
	                               dibjet_extractor_lambda dibjetQuantity);

	static double GetHighCSVJetPlusBJetQuantity(product_type const& product,
	                               dibjet_extractor_lambda dibjetQuantity);

	static double GetDiBJetQuantity_bReg(product_type const& product,
	                               dibjet_extractor_lambda dibjetQuantity);

	static double GetJetPlusBJetQuantity_bReg(product_type const& product,
	                               dibjet_extractor_lambda dibjetQuantity);

	static double GetHighCSVJetPlusBJetQuantity_bReg(product_type const& product,
	                               dibjet_extractor_lambda dibjetQuantity);


	virtual std::string GetProducerId() const override {
		return "DiBJetQuantitiesProducer";
	}
	
	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;
};

