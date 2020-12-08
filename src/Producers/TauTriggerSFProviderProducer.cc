#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTriggerSFProviderProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

std::string TauTriggerSFProviderProducer::GetProducerId() const
{
        return "TauTriggerSFProviderProducer";
}

void TauTriggerSFProviderProducer::Produce( event_type const& event, product_type & product,
                                                                                                setting_type const& settings) const
{
        for (auto wp: settings.GetTauTriggerWorkingPoints())
        {
                for(auto weightNames: m_weightNames)
                {
                        KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
                        int dm = static_cast<KTau*>(lepton)->decayMode;
                        for(size_t index = 0; index < weightNames.second.size(); index++)
                        {
                            bool mc_weight = MCWeight.at(weightNames.first).at(index);
                            bool data_weight = DataWeight.at(weightNames.first).at(index);

                            if(mc_weight)
                            {
                                    product.m_weights[weightNames.second.at(index)+"_"+wp+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp)->getEfficiencyMC(lepton->p4.Pt(),dm);
                                    product.m_weights[weightNames.second.at(index)+"Up_"+wp+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp)->getEfficiencyMC(lepton->p4.Pt(),dm, 1);
                                    product.m_weights[weightNames.second.at(index)+"Down_"+wp+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp)->getEfficiencyMC(lepton->p4.Pt(),dm, -1);
                            }
                            else if (data_weight)
                            {
                                    product.m_weights[weightNames.second.at(index)+"_"+wp+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp)->getEfficiencyData(lepton->p4.Pt(),dm);
                                    product.m_weights[weightNames.second.at(index)+"Up_"+wp+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp)->getEfficiencyData(lepton->p4.Pt(),dm, 1);
                                    product.m_weights[weightNames.second.at(index)+"Down_"+wp+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp)->getEfficiencyData(lepton->p4.Pt(),dm, -1);
                            }
                            else
                            {
                                    product.m_weights[weightNames.second.at(index)+"_"+wp+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp)->getSF(lepton->p4.Pt(),dm);
                                    product.m_weights[weightNames.second.at(index)+"Up_"+wp+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp)->getSF(lepton->p4.Pt(),dm, 1);
                                    product.m_weights[weightNames.second.at(index)+"Down_"+wp+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp)->getSF(lepton->p4.Pt(),dm, -1);
                            }
                        }
                }
        }
}

