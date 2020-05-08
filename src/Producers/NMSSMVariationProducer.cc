#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/NMSSMVariationProducer.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include <cmath>

std::string NMSSMVariationProducer::GetProducerId() const
{
	return "NMSSMVariationProducer";
}

void NMSSMVariationProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
}

void NMSSMVariationProducer::Produce(event_type const& event, product_type & product, 
	                 setting_type const& settings) const
{
	float pdfstd = 0.;
	int n_pdf = 0;
	for(uint index = 0; index<settings.GetGenEventInfoMetadataNames().size(); index++)
	{
		if(settings.GetGenEventInfoMetadataNames().at(index).find("PDF") != std::string::npos){
			pdfstd += pow(event.m_genEventInfo->lheWeight[index+1] - 1., 2);
			++n_pdf;
		}
		LOG(DEBUG) << "Fill LHE weight " << settings.GetGenEventInfoMetadataNames().at(index) << " : " << event.m_genEventInfo->lheWeight[index+1] ;

		product.m_optionalWeights[settings.GetGenEventInfoMetadataNames().at(index)] = event.m_genEventInfo->lheWeight[index+1];
	}
	pdfstd = sqrt(pdfstd/float(n_pdf));
	product.m_optionalWeights["NNPDF23_lo_as_0130_qed_weight"] = 1.0+pdfstd;


}
