
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/L1TauTriggerMatchingProducers.h"

TauL1TauTriggerMatchingProducer::TauL1TauTriggerMatchingProducer() :
        L1TauTriggerMatchingProducerBase<KTau>(&product_type::m_additionalL1TauMatchedTaus,
                                               &product_type::m_tauTriggerMatch,
                                               &product_type::m_validTaus,
                                               &product_type::m_settingsTauTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick,
                                               &product_type::m_settingsTauTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick,
                                               &setting_type::GetTauTriggerCheckAdditionalL1TauMatchLowerPtCut,
                                               &setting_type::GetTauTriggerCheckAdditionalL1TauMatchUpperEtaCut,
                                               &setting_type::GetTauTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau,
                                               &setting_type::GetInvertedTauL1TauMatching)
{
}

std::string TauL1TauTriggerMatchingProducer::GetProducerId() const
{
    return "TauL1TauTriggerMatchingProducer";
}

void TauL1TauTriggerMatchingProducer::Produce(event_type const& event, product_type& product,
                                            setting_type const& settings) const
{
    L1TauTriggerMatchingProducerBase<KTau>::Produce(event, product, settings);

    for (std::map<KTau*, std::map<std::string, bool> >::iterator it = product.m_additionalL1TauMatchedTaus.begin();
            it != product.m_additionalL1TauMatchedTaus.end(); it++)
    {
            product.m_additionalL1TauMatchedLeptons[&(*(it->first))] = &(it->second);
    }
}

MuonL1TauTriggerMatchingProducer::MuonL1TauTriggerMatchingProducer() :
        L1TauTriggerMatchingProducerBase<KMuon>(&product_type::m_additionalL1TauMatchedMuons,
                                                &product_type::m_muonTriggerMatch,
                                                &product_type::m_validMuons,
                                                &product_type::m_settingsMuonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick,
                                                &product_type::m_settingsMuonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick,
                                                &setting_type::GetMuonTriggerCheckAdditionalL1TauMatchLowerPtCut,
                                                &setting_type::GetMuonTriggerCheckAdditionalL1TauMatchUpperEtaCut,
                                                &setting_type::GetMuonTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau,
                                                &setting_type::GetInvertedMuonL1TauMatching)
{
}

std::string MuonL1TauTriggerMatchingProducer::GetProducerId() const
{
    return "MuonL1TauTriggerMatchingProducer";
}

void MuonL1TauTriggerMatchingProducer::Produce(event_type const& event, product_type& product,
                                            setting_type const& settings) const
{
    L1TauTriggerMatchingProducerBase<KMuon>::Produce(event, product, settings);

    for (std::map<KMuon*, std::map<std::string, bool> >::iterator it = product.m_additionalL1TauMatchedMuons.begin();
            it != product.m_additionalL1TauMatchedMuons.end(); it++)
    {
            product.m_additionalL1TauMatchedLeptons[&(*(it->first))] = &(it->second);
    }
}

ElectronL1TauTriggerMatchingProducer::ElectronL1TauTriggerMatchingProducer() :
        L1TauTriggerMatchingProducerBase<KElectron>(&product_type::m_additionalL1TauMatchedElectrons,
                                                    &product_type::m_electronTriggerMatch,
                                                    &product_type::m_validElectrons,
                                                    &product_type::m_settingsElectronTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick,
                                                    &product_type::m_settingsElectronTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick,
                                                    &setting_type::GetElectronTriggerCheckAdditionalL1TauMatchLowerPtCut,
                                                    &setting_type::GetElectronTriggerCheckAdditionalL1TauMatchUpperEtaCut,
                                                    &setting_type::GetElectronTriggerCheckAdditionalL1TauMatchUseIsolatedL1Tau,
                                                    &setting_type::GetInvertedElectronL1TauMatching)
{
}

std::string ElectronL1TauTriggerMatchingProducer::GetProducerId() const
{
    return "ElectronL1TauTriggerMatchingProducer";
}

void ElectronL1TauTriggerMatchingProducer::Produce(event_type const& event, product_type& product,
                                            setting_type const& settings) const
{
    L1TauTriggerMatchingProducerBase<KElectron>::Produce(event, product, settings);

    for (std::map<KElectron*, std::map<std::string, bool> >::iterator it = product.m_additionalL1TauMatchedElectrons.begin();
            it != product.m_additionalL1TauMatchedElectrons.end(); it++)
    {
            product.m_additionalL1TauMatchedLeptons[&(*(it->first))] = &(it->second);
    }
}
