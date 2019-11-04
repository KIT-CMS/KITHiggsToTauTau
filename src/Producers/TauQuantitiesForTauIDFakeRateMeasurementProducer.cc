
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauQuantitiesForTauIDFakeRateMeasurementProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"

void TauQuantitiesForTauIDFakeRateMeasurementProducer::Init(setting_type const& settings)
{
    ProducerBase<HttTypes>::Init(settings);

    // add quantities to be written out by the LambdaNtupleConsumer
    LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pt_tau", [](event_type const& event, product_type const& product)
    {
        return (product.m_validTauForTauIDFakeRateMeasurement != nullptr ? product.m_validTauForTauIDFakeRateMeasurement->p4.pt() : DefaultValues::UndefinedFloat);
    });
    LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("eta_tau", [](event_type const& event, product_type const& product)
    {
        return (product.m_validTauForTauIDFakeRateMeasurement != nullptr ? product.m_validTauForTauIDFakeRateMeasurement->p4.eta() : DefaultValues::UndefinedFloat);
    });
    LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mass_tau", [](event_type const& event, product_type const& product)
    {
        return (product.m_validTauForTauIDFakeRateMeasurement != nullptr ? product.m_validTauForTauIDFakeRateMeasurement->p4.mass() : DefaultValues::UndefinedFloat);
    });
    LambdaNtupleConsumer<HttTypes>::AddIntQuantity("decayMode_tau", [](event_type const& event, product_type const& product)
    {
        return (product.m_validTauForTauIDFakeRateMeasurement != nullptr ? product.m_validTauForTauIDFakeRateMeasurement->decayMode : DefaultValues::UndefinedInt);
    });
    // TauIds
    std::vector<std::string> tauDiscriminators;
    tauDiscriminators.push_back("byCombinedIsolationDeltaBetaCorrRaw3Hits");
    tauDiscriminators.push_back("byLooseCombinedIsolationDeltaBetaCorr3Hits");
    tauDiscriminators.push_back("byMediumCombinedIsolationDeltaBetaCorr3Hits");
    tauDiscriminators.push_back("byTightCombinedIsolationDeltaBetaCorr3Hits");
    tauDiscriminators.push_back("againstElectronLooseMVA6");
    tauDiscriminators.push_back("againstElectronMediumMVA6");
    tauDiscriminators.push_back("againstElectronTightMVA6");
    tauDiscriminators.push_back("againstElectronVLooseMVA6");
    tauDiscriminators.push_back("againstElectronVTightMVA6");
    tauDiscriminators.push_back("againstMuonLoose3");
    tauDiscriminators.push_back("againstMuonTight3");
    tauDiscriminators.push_back("byIsolationMVArun2v1DBoldDMwLTraw");
    tauDiscriminators.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT");
    tauDiscriminators.push_back("byLooseIsolationMVArun2v1DBoldDMwLT");
    tauDiscriminators.push_back("byMediumIsolationMVArun2v1DBoldDMwLT");
    tauDiscriminators.push_back("byTightIsolationMVArun2v1DBoldDMwLT");
    tauDiscriminators.push_back("byVTightIsolationMVArun2v1DBoldDMwLT");
    tauDiscriminators.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT");
    tauDiscriminators.push_back("byIsolationMVArun2017v2DBoldDMwLTraw2017");
    tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v2DBoldDMwLT2017");
    tauDiscriminators.push_back("byVLooseIsolationMVArun2017v2DBoldDMwLT2017");
    tauDiscriminators.push_back("byLooseIsolationMVArun2017v2DBoldDMwLT2017");
    tauDiscriminators.push_back("byMediumIsolationMVArun2017v2DBoldDMwLT2017");
    tauDiscriminators.push_back("byTightIsolationMVArun2017v2DBoldDMwLT2017");
    tauDiscriminators.push_back("byVTightIsolationMVArun2017v2DBoldDMwLT2017");
    tauDiscriminators.push_back("byVVTightIsolationMVArun2017v2DBoldDMwLT2017");
    tauDiscriminators.push_back("byIsolationMVArun2017v1DBoldDMwLTraw2017");
    tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v1DBoldDMwLT2017");
    tauDiscriminators.push_back("byVLooseIsolationMVArun2017v1DBoldDMwLT2017");
    tauDiscriminators.push_back("byLooseIsolationMVArun2017v1DBoldDMwLT2017");
    tauDiscriminators.push_back("byMediumIsolationMVArun2017v1DBoldDMwLT2017");
    tauDiscriminators.push_back("byTightIsolationMVArun2017v1DBoldDMwLT2017");
    tauDiscriminators.push_back("byVTightIsolationMVArun2017v1DBoldDMwLT2017");
    tauDiscriminators.push_back("byVVTightIsolationMVArun2017v1DBoldDMwLT2017");
    tauDiscriminators.push_back("byDeepTau2017v2p1VSjetraw");
    // tauDiscriminators.push_back("byVVVLooseDeepTau2017v2p1VSjet");
    tauDiscriminators.push_back("byVVLooseDeepTau2017v2p1VSjet");
    tauDiscriminators.push_back("byVLooseDeepTau2017v2p1VSjet");
    tauDiscriminators.push_back("byLooseDeepTau2017v2p1VSjet");
    tauDiscriminators.push_back("byMediumDeepTau2017v2p1VSjet");
    tauDiscriminators.push_back("byTightDeepTau2017v2p1VSjet");
    tauDiscriminators.push_back("byVTightDeepTau2017v2p1VSjet");
    tauDiscriminators.push_back("byVVTightDeepTau2017v2p1VSjet");
    tauDiscriminators.push_back("byDeepTau2017v2p1VSeraw");
    // tauDiscriminators.push_back("byVVVLooseDeepTau2017v2p1VSe");
    tauDiscriminators.push_back("byVVLooseDeepTau2017v2p1VSe");
    tauDiscriminators.push_back("byVLooseDeepTau2017v2p1VSe");
    tauDiscriminators.push_back("byLooseDeepTau2017v2p1VSe");
    tauDiscriminators.push_back("byMediumDeepTau2017v2p1VSe");
    tauDiscriminators.push_back("byTightDeepTau2017v2p1VSe");
    tauDiscriminators.push_back("byVTightDeepTau2017v2p1VSe");
    tauDiscriminators.push_back("byVVTightDeepTau2017v2p1VSe");
    tauDiscriminators.push_back("byDeepTau2017v2p1VSmuraw");
    tauDiscriminators.push_back("byVLooseDeepTau2017v2p1VSmu");
    tauDiscriminators.push_back("byLooseDeepTau2017v2p1VSmu");
    tauDiscriminators.push_back("byMediumDeepTau2017v2p1VSmu");
    tauDiscriminators.push_back("byTightDeepTau2017v2p1VSmu");
    tauDiscriminators.push_back("chargedIsoPtSum");
    tauDiscriminators.push_back("decayModeFinding");
    tauDiscriminators.push_back("decayModeFindingNewDMs");
    tauDiscriminators.push_back("neutralIsoPtSum");
    tauDiscriminators.push_back("puCorrPtSum");
    tauDiscriminators.push_back("footprintCorrection");
    tauDiscriminators.push_back("photonPtSumOutsideSignalCone");
    tauDiscriminators.push_back("decayDistX");
    tauDiscriminators.push_back("decayDistY");
    tauDiscriminators.push_back("decayDistZ");
    tauDiscriminators.push_back("decayDistM");
    tauDiscriminators.push_back("nPhoton");
    tauDiscriminators.push_back("ptWeightedDetaStrip");
    tauDiscriminators.push_back("ptWeightedDphiStrip");
    tauDiscriminators.push_back("ptWeightedDrSignal");
    tauDiscriminators.push_back("ptWeightedDrIsolation");
    tauDiscriminators.push_back("leadingTrackChi2");
    tauDiscriminators.push_back("eRatio");


    for (std::string tauDiscriminator : tauDiscriminators)
    {
            std::string quantity = tauDiscriminator + "_tau";
            LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(quantity, [tauDiscriminator](event_type const& event, product_type const& product)
            {
                return (product.m_validTauForTauIDFakeRateMeasurement != nullptr ? product.m_validTauForTauIDFakeRateMeasurement->getDiscriminator(tauDiscriminator, event.m_tauMetadata) : DefaultValues::UndefinedFloat);
            });
    }
    //temporary fix for VVVLoose deep tau ID WP
    LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byVVVLooseDeepTau2017v2p1VSjet_tau", [](event_type const& event, product_type const& product)
    {
            return (product.m_validTauForTauIDFakeRateMeasurement != nullptr ? product.m_validTauForTauIDFakeRateMeasurement->getDiscriminator("byDeepTau2017v2p1VSjetraw", event.m_tauMetadata) > 0.2599605 : DefaultValues::UndefinedFloat);
    });
    LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byVVVLooseDeepTau2017v2p1VSe_tau", [](event_type const& event, product_type const& product)
    {
            return (product.m_validTauForTauIDFakeRateMeasurement != nullptr ? product.m_validTauForTauIDFakeRateMeasurement->getDiscriminator("byDeepTau2017v2p1VSeraw", event.m_tauMetadata) > 0.0630386 : DefaultValues::UndefinedFloat);
    });
    //end of fix
    bool useUWGenMatching = settings.GetUseUWGenMatching();
    LambdaNtupleConsumer<HttTypes>::AddIntQuantity("gen_match_tau", [useUWGenMatching](event_type const& event, product_type const& product)
    {
            if (useUWGenMatching)
            {
                    if (product.m_validTauForTauIDFakeRateMeasurement != nullptr)
                    {
                        KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons,
                                                                                               dynamic_cast<const KLepton*>(product.m_validTauForTauIDFakeRateMeasurement),
                                                                                               dynamic_cast<const KLepton*>(product.m_validTauForTauIDFakeRateMeasurement)));
                        return Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton));
                    }
                    else
                    {
                        return DefaultValues::UndefinedInt;
                    }
            }
            else
            {
                    if (product.m_validTauForTauIDFakeRateMeasurement != nullptr)
                    {
                        KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons,
                                                                                               dynamic_cast<const KLepton*>(product.m_validTauForTauIDFakeRateMeasurement),
                                                                                               dynamic_cast<const KLepton*>(product.m_validTauForTauIDFakeRateMeasurement)));
                        KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(originalLepton,
                                                                                         product.m_genParticleMatchedLeptons,
                                                                                         product.m_genTauMatchedLeptons);
                        if (genParticle)
                        {
                                return Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCode(genParticle));
                        }
                        else
                        {
                                return Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_FAKE);
                        }
                    }
                    else
                    {
                        return DefaultValues::UndefinedInt;
                    }
            }
    });
}

void TauQuantitiesForTauIDFakeRateMeasurementProducer::Produce(event_type const& event, product_type& product,
                                                               setting_type const& settings) const
{
    // Loop over valid taus and find tau lepton with highest pT not overlapping with signal leptons.
    if (product.m_validTaus.size() > 0)
    {
        LOG(DEBUG) << "Found at least one valid tau in event...";
        double maxTauPt = 0.;
        int tauToBeStored = -1;
        for (size_t tauIndex = 0; tauIndex < product.m_validTaus.size(); tauIndex++)
        {
            LOG(DEBUG) << "Checking if tau lepton " << tauIndex << " is overlapping with one of the signal leptons...";
            // Check if tau lepton overlaps with one of the signal leptons.
            KTau* tau = product.m_validTaus.at(tauIndex);
            bool noOverlap = true;
            for (size_t leptonIndex = 0; leptonIndex < 2; leptonIndex++)
            {
                noOverlap = noOverlap && (ROOT::Math::VectorUtil::DeltaR(product.m_flavourOrderedLeptons.at(leptonIndex)->p4, tau->p4) > 0.5);
                LOG(DEBUG) << "Tau lepton overlaps with signal lepton " << leptonIndex << " ? " << !noOverlap;
            }

            if (noOverlap && (tau->p4.pt() > maxTauPt))
            {
                maxTauPt = tau->p4.pt();
                tauToBeStored = tauIndex;
            }
        }
        if (tauToBeStored >= 0)
        {
            LOG(DEBUG) << "Storing quantities of tau lepton " << tauToBeStored << " with pT of " << product.m_validTaus.at(tauToBeStored)->p4.pt();
            product.m_validTauForTauIDFakeRateMeasurement = product.m_validTaus.at(tauToBeStored);
        }
    }
}
