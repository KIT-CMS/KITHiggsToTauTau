
#include <boost/algorithm/string.hpp>

#include "Artus/Utility/interface/Utility.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauIDScaleFactorProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

std::string TauIDScaleFactorProducer::GetProducerId() const
{
	return "TauIDScaleFactorProducer";
}

void TauIDScaleFactorProducer::Produce( event_type const& event, product_type & product,
												setting_type const& settings) const
{
        for (auto wp: settings.GetTauIDSFWorkingPoints())
        {
                for (auto t: settings.GetTauIDSFTypes())
                {
                        for(auto weightNames: m_weightNames)
                        {
                                KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
                                int dm = static_cast<KTau*>(lepton)->decayMode;
                                int genmatch = 0;
                                const bool useUWGenMatching = settings.GetUseUWGenMatching();
                                if (useUWGenMatching)
                                {
                                        KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(lepton), const_cast<const KLepton*>(lepton)));
                                        genmatch = Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton));
                                }
                                else
                                {
                                        KGenParticle* genParticle = product.m_flavourOrderedGenLeptons.at(weightNames.first);
                                        if (genParticle)
                                        {
                                                genmatch = Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCode(genParticle));
                                        }
                                        else
                                        {
                                                genmatch = Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_FAKE);
                                        }
                                }
                                for(size_t index = 0; index < weightNames.second.size(); index++)
                                {
                                    if (settings.GetChannel() == "TT")
                                    {
                                        product.m_weights[weightNames.second.at(index)+"_"+boost::algorithm::to_lower_copy(wp)+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauIDSFs.at(wp).at(t)->getSFvsDM(lepton->p4.Pt(), dm, genmatch, "");
                                        product.m_weights[weightNames.second.at(index)+"Up_"+boost::algorithm::to_lower_copy(wp)+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauIDSFs.at(wp).at(t)->getSFvsDM(lepton->p4.Pt(), dm, genmatch, "Up");
                                        product.m_weights[weightNames.second.at(index)+"Down_"+boost::algorithm::to_lower_copy(wp)+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauIDSFs.at(wp).at(t)->getSFvsDM(lepton->p4.Pt(), dm, genmatch, "Down");
                                    }
                                    else
                                    {
                                        product.m_weights[weightNames.second.at(index)+"_"+boost::algorithm::to_lower_copy(wp)+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauIDSFs.at(wp).at(t)->getSFvsPT(lepton->p4.Pt(), genmatch, "");
                                        product.m_weights[weightNames.second.at(index)+"Up_"+boost::algorithm::to_lower_copy(wp)+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauIDSFs.at(wp).at(t)->getSFvsPT(lepton->p4.Pt(), genmatch, "Up");
                                        product.m_weights[weightNames.second.at(index)+"Down_"+boost::algorithm::to_lower_copy(wp)+"_"+t+"_"+std::to_string(weightNames.first+1)] = TauIDSFs.at(wp).at(t)->getSFvsPT(lepton->p4.Pt(), genmatch, "Down");
                                    }
                                }
                        }
                }
        }
}
