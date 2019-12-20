#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SingleTauTriggerEfficiencyProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

std::string SingleTauTriggerEfficiencyProducer::GetProducerId() const
{
	return "SingleTauTriggerEfficiencyProducer";
}

void SingleTauTriggerEfficiencyProducer::Produce( event_type const& event, product_type & product,
												setting_type const& settings) const
{
        for (auto wp: settings.GetSingleTauTriggerWorkingPoints())
        {
                for (auto t: settings.GetSingleTauTriggerIDTypes())
                {
                        for(auto weightNames: m_weightNames)
                        {
                                KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
                                int dm = static_cast<KTau*>(lepton)->decayMode;
                                for(size_t index = 0; index < weightNames.second.size(); index++)
                                {
                                    bool mc_weight = MCWeight.at(weightNames.first).at(index);

                                    if(mc_weight)
                                    {
                                            product.m_weights[weightNames.second.at(index)+"_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getSingleTauTriggerEfficiencyMC(lepton->p4.Pt(),dm);
                                    }
                                    else
                                    {
                                            product.m_weights[weightNames.second.at(index)+"_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getSingleTauTriggerEfficiencyData(lepton->p4.Pt(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Up_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getSingleTauTriggerEfficiencyDataUncertUp(lepton->p4.Pt(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Down_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getSingleTauTriggerEfficiencyDataUncertDown(lepton->p4.Pt(),dm);
                                    }
                                }
                        }
                }
        }
}
