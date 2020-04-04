
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TopPtReweightingProducer.h"

std::string TopPtReweightingProducer::GetProducerId() const
{
	return "TopPtReweightingProducer";
}

void TopPtReweightingProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	m_isTTbar = boost::regex_search(settings.GetNickname(), boost::regex("(TT_|TTTo)", boost::regex::icase | boost::regex::extended));
	std::string strategy = settings.GetTopPtReweightingStrategy();
	boost::algorithm::to_lower(strategy);
	if (strategy == "run1") m_oldStrategy = true;
}

void TopPtReweightingProducer::Produce( event_type const& event,
			product_type & product,
			setting_type const& settings) const
{
	if (m_isTTbar)
	{
		assert(event.m_genEventInfo != nullptr);
		std::vector<KGenParticle> tops;
		for (auto particle : *(event.m_genParticles))
			//for (KGenParticles::iterator part = event.m_genParticles->begin(); part != event.m_genParticles->end(); ++part)
		{
			if(std::abs(particle.pdgId) == 6 && particle.isLastCopy()) tops.push_back(particle);
		}

		assert(tops.size() == 2);

		float top1Pt = tops.at(0).p4.Pt();
		float top2Pt = tops.at(1).p4.Pt();

		// Run 1 specifications for a and b
		product.m_optionalWeights["topPtReweightWeightRun1"] = ComputeWeight(top1Pt, top2Pt, 0.156, -0.00137, 0.0, -1.0);
		// Run 2 specifications for a and b
		product.m_optionalWeights["topPtReweightWeightRun2"] = ComputeWeight(top1Pt, top2Pt, 0.0615, -0.0005, 0.0, -1.0);
		// ttH-AN specifications for a and b and c
		product.m_optionalWeights["topPtReweightWeightTTH"] = ComputeWeight(top1Pt, top2Pt, 0.088, -0.00087, 0.00000092, 472.0);
		product.m_optionalWeights["topPtReweightWeight"]  = m_oldStrategy ? product.m_optionalWeights["topPtReweightWeightRun1"] : product.m_optionalWeights["topPtReweightWeightRun2"];
	}
}

float TopPtReweightingProducer::ComputeWeight(float top1Pt, float top2Pt, float parameter_a, float parameter_b, float parameter_c, float setconst_threshold) const
{
	top1Pt = top1Pt > 400 ? 400 : top1Pt;
	top2Pt = top2Pt > 400 ? 400 : top2Pt; 
	if (setconst_threshold>=0.0){
		if (top1Pt>setconst_threshold) top1Pt = setconst_threshold;
		if (top2Pt>setconst_threshold) top2Pt = setconst_threshold;
	}
	return sqrt(exp(parameter_a + parameter_b*top1Pt + parameter_c*top1Pt*top1Pt)*exp(parameter_a + parameter_b*top2Pt + parameter_c*top2Pt*top2Pt));
}
