
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTriggerEfficiencyProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

std::string TauTriggerEfficiencyProducer::GetProducerId() const
{
	return "TauTriggerEfficiencyProducer";
}

void TauTriggerEfficiencyProducer::Produce( event_type const& event, product_type & product, 
												setting_type const& settings) const
{
        for (auto wp: settings.GetTauTriggerWorkingPoints())
        {
                for (auto t: settings.GetTauTriggerIDTypes())
                {
                        for(auto weightNames: m_weightNames)
                        {
                                KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
                                int dm = static_cast<KTau*>(lepton)->decayMode;
                                for(size_t index = 0; index < weightNames.second.size(); index++)
                                {
                                    bool mc_weight = MCWeight.at(weightNames.first).at(index);
                                    bool emb_weight = EMBWeight.at(weightNames.first).at(index);
                                    bool kitdata_weight = KITDataWeight.at(weightNames.first).at(index);

                                    if(mc_weight)
                                    {
                                            product.m_weights[weightNames.second.at(index)+"_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Up_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyMCUncertUp(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Down_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyMCUncertDown(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                    }
                                    else if(emb_weight)
                                    {
                                            product.m_weights[weightNames.second.at(index)+"_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyEMB(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Up_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyEMBUncertUp(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Down_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyEMBUncertDown(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                    }
                                    else if (kitdata_weight)
                                    {
                                            product.m_weights[weightNames.second.at(index)+"_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyKITData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Up_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyKITDataUncertUp(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Down_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyKITDataUncertDown(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                    }
                                    else
                                    {
                                            product.m_weights[weightNames.second.at(index)+"_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Up_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyDataUncertUp(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                            product.m_weights[weightNames.second.at(index)+"Down_"+wp+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauSFs.at(wp).at(t)->getTriggerEfficiencyDataUncertDown(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi(),dm);
                                    }
                                }
                        }
                }
        }
}
