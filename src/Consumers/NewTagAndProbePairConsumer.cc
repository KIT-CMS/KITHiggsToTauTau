#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/NewTagAndProbePairConsumer.h"

NewMMTagAndProbePairConsumer::NewMMTagAndProbePairConsumer() : NewTagAndProbePairConsumerBase()
{
}
void NewMMTagAndProbePairConsumer::AdditionalQuantities(int i, std::string quantity, product_type const &product,
				 					 std::map<std::string, bool>& BoolQuantities)
{
	if (quantity == "id_t")
	{
		BoolQuantities["id_t"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).first)->idMedium();
	}
	else if (quantity == "id_p")
	{
		BoolQuantities["id_p"] = static_cast<KLepton *>(product.m_validDiTauPairCandidates.at(i).second)->idMedium();
	}


}

std::string NewMMTagAndProbePairConsumer::GetConsumerId() const
{
	return "NewMMTagAndProbePairConsumer";
}