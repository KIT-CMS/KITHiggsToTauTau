
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <TRandom3.h>
#include <TLorentzVector.h>
#include <TVector3.h>

#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTauCorrectionsProducer.h"

#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"


void HttTauCorrectionsProducer::Init(setting_type const& settings)
{
	TauCorrectionsProducer::Init(settings);

	tauEnergyCorrection = ToTauEnergyCorrection(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(static_cast<HttSettings const&>(settings).GetTauEnergyCorrection())));
}

void HttTauCorrectionsProducer::AdditionalCorrections(KTau* tau, event_type const& event,
                                                      product_type& product, setting_type const& settings) const
{
	bool fes_eta_split = static_cast<HttSettings const&>(settings).GetFESetaSplit(); // todo: move to constr

	TauCorrectionsProducer::AdditionalCorrections(tau, event, product, settings);

	double normalisationFactor = 1.0;

	KappaEnumTypes::GenMatchingCode genMatchingCode = KappaEnumTypes::GenMatchingCode::NONE;
	KLepton* originalLepton = product.m_originalLeptons.find(tau) != product.m_originalLeptons.end() ? const_cast<KLepton*>(product.m_originalLeptons.at(tau)) : tau;
	if (settings.GetUseUWGenMatching())
	{
		genMatchingCode = GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton);
	}
	else
	{
		KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(originalLepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons);
		if (genParticle)
			genMatchingCode = GeneratorInfo::GetGenMatchingCode(genParticle);
		else
			genMatchingCode = KappaEnumTypes::GenMatchingCode::IS_FAKE;
	}

	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#TauES_and_decay_mode_scale_facto
	if (tauEnergyCorrection == TauEnergyCorrection::SUMMER2013)
	{
		// http://cmslxr.fnal.gov/lxr/source/DataFormats/TauReco/interface/PFTau.h#035
		if (tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng0PiZero)
		{
			normalisationFactor = 0.88;
		}
		else if (tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng1PiZero || tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng2PiZero)
		{
			tau->p4 = tau->p4 * (1.012);
			// tau->p4 = tau->p4 * (1.015 + 0.001 * std::min(std::max(tau->p4.Pt() - 45.0, 0.0), 10.0));
		}
		else if (tau->decayMode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero)
		{
			tau->p4 = tau->p4 * (1.012);
			// tau->p4 = tau->p4 * (1.012 + 0.001 * std::min(std::max(tau->p4.Pt() - 32.0, 0.0), 18.0));
		}
	}
	else if (tauEnergyCorrection == TauEnergyCorrection::NEWTAUID)
	{
		tau->p4 = tau->p4 * (1.01);
	}
	else if (tauEnergyCorrection == TauEnergyCorrection::SMHTT2016)
	{
		if (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY) // correct tau->had energy scale
		{
			float tauEnergyCorrectionOneProng = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProng();
			float tauEnergyCorrectionOneProngPiZeros = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZeros();
			float tauEnergyCorrectionThreeProng = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProng();
			float tauEnergyCorrectionThreeProngPiZeros = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngPiZeros();
			std::vector<float> tauEnergyCorrectionOneProngPtDependant = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPtDependant();
			std::vector<float> tauEnergyCorrectionOneProngPiZerosPtDependant = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZerosPtDependant();
			std::vector<float> tauEnergyCorrectionThreeProngPtDependant = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngPtDependant();
			std::vector<float> tauEnergyCorrectionThreeProngPiZerosPtDependant = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngPiZerosPtDependant();

			std::vector<float> tauEnergyCorrectionOneProngPtDependantUncShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPtDependantUncShift();
			std::vector<float> tauEnergyCorrectionOneProngPiZerosPtDependantUncShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZerosPtDependantUncShift();
			std::vector<float> tauEnergyCorrectionThreeProngPtDependantUncShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngPtDependantUncShift();
			std::vector<float> tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngPiZerosPtDependantUncShift();

			bool use_interpolation = 0 < (tauEnergyCorrectionOneProngPtDependant.size() + tauEnergyCorrectionOneProngPiZerosPtDependant.size() + tauEnergyCorrectionThreeProngPtDependant.size() + tauEnergyCorrectionThreeProngPiZerosPtDependant.size());
			bool is_nominal = HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPtDependantUncShift[0], 0.0) && HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPtDependantUncShift[1], 0.0) &&
				HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPiZerosPtDependantUncShift[0], 0.0) && HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPiZerosPtDependantUncShift[1], 0.0) &&
				HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPtDependantUncShift[0], 0.0) && HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPtDependantUncShift[1], 0.0) &&
				HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift[0], 0.0) && HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift[1], 0.0);

			if (! use_interpolation)
			{
				if (tau->decayMode == 0 && tauEnergyCorrectionOneProng != 1.0)
				{
					tau->p4 = tau->p4 * tauEnergyCorrectionOneProng;
				}
				else if ((tau->decayMode == 1 || tau->decayMode == 2) && tauEnergyCorrectionOneProngPiZeros != 1.0)
				{
					tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPiZeros;
				}
				else if (tau->decayMode == 10 && tauEnergyCorrectionThreeProng != 1.0)
				{
					tau->p4 = tau->p4 * tauEnergyCorrectionThreeProng;
				}
				else if (tau->decayMode == 11 && tauEnergyCorrectionThreeProngPiZeros != 1.0)
				{
					tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngPiZeros;
				}
			}
			else
			{
				assert(tauEnergyCorrectionOneProngPtDependant.size() == 2);
				assert(tauEnergyCorrectionOneProngPiZerosPtDependant.size() == 2);
				assert(tauEnergyCorrectionThreeProngPtDependant.size() == 2);
				assert(tauEnergyCorrectionOneProngPtDependantUncShift.size() == 2);
				assert(tauEnergyCorrectionOneProngPiZerosPtDependantUncShift.size() == 2);
				assert(tauEnergyCorrectionThreeProngPtDependantUncShift.size() == 2);

				if (tau->p4.Pt() < 34.0)
				{
					if (tau->decayMode == 0 && tauEnergyCorrectionOneProngPtDependant[0] != 1.0)
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPtDependant[0];
					}
					else if ((tau->decayMode == 1 || tau->decayMode == 2) && tauEnergyCorrectionOneProngPiZerosPtDependant[0] != 1.0)
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPiZerosPtDependant[0];
					}
					else if (tau->decayMode == 10 && tauEnergyCorrectionThreeProngPtDependant[0] != 1.0)
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngPtDependant[0];
					}
					else if (tau->decayMode == 11 && tauEnergyCorrectionThreeProngPiZerosPtDependant[0] != 1.0)
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngPiZerosPtDependant[0];
					}
				}
				else if (tau->p4.Pt() >= 170.0 || is_nominal)
				{

					if (tau->decayMode == 0 && ! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPtDependant[1], 1.0))
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPtDependant[1];
					}
					else if ((tau->decayMode == 1 || tau->decayMode == 2) && ! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPiZerosPtDependant[1], 1.0))
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPiZerosPtDependant[1];
					}
					else if (tau->decayMode == 10 && ! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPtDependant[1], 1.0))
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngPtDependant[1];
					}
					else if (tau->decayMode == 11 && ! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPiZerosPtDependant[1], 1.0))
					{
						assert(tauEnergyCorrectionThreeProngPiZerosPtDependant.size() == 2);
						assert(tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift.size() == 2);
						tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngPiZerosPtDependant[1];
					}

				}
				else if (tau->p4.Pt() >= 34.0)
				{
					float mixing_fraction = (tau->p4.Pt() - 34) / (170 - 34);

					if (tau->decayMode == 0 && (
						! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPtDependantUncShift[1], 0.0) &&
						! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPtDependantUncShift[0], 0.0) ))
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPtDependant[1] * ( 1 + tauEnergyCorrectionOneProngPtDependantUncShift[0] + (tauEnergyCorrectionOneProngPtDependantUncShift[1] - tauEnergyCorrectionOneProngPtDependantUncShift[0]) * mixing_fraction);
					}
					else if ((tau->decayMode == 1 || tau->decayMode == 2) && (
						! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPiZerosPtDependantUncShift[1], 0.0) ||
						! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionOneProngPiZerosPtDependantUncShift[0], 0.0) ))
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPiZerosPtDependant[1] * ( 1 + tauEnergyCorrectionOneProngPiZerosPtDependantUncShift[0] + (tauEnergyCorrectionOneProngPiZerosPtDependantUncShift[1] - tauEnergyCorrectionOneProngPiZerosPtDependantUncShift[0]) * mixing_fraction);
					}
					else if (tau->decayMode == 10 && (
						! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPtDependantUncShift[1], 0.0) ||
						! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPtDependantUncShift[0], 0.0) ))
					{
						tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngPtDependant[1] * ( 1 + tauEnergyCorrectionThreeProngPtDependantUncShift[0] + (tauEnergyCorrectionThreeProngPtDependantUncShift[1] - tauEnergyCorrectionThreeProngPtDependantUncShift[0]) * mixing_fraction);
					}
					else if (tau->decayMode == 11 && (
						! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift[1], 0.0) ||
						! HttTauCorrectionsProducer::areEqual(tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift[0], 0.0) ))
					{
						assert(tauEnergyCorrectionThreeProngPiZerosPtDependant.size() == 2);
						assert(tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift.size() == 2);
						tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngPiZerosPtDependant[1] * ( 1 + tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift[0] + (tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift[1] - tauEnergyCorrectionThreeProngPiZerosPtDependantUncShift[0]) * mixing_fraction);
					}
				}
			}
		}
		else if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)) // correct mu->tau fake energy scale
		{
			float tauMuonFakeEnergyCorrectionOneProng = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProng();
			float tauMuonFakeEnergyCorrectionOneProngPiZeros = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProngPiZeros();
			float tauMuonFakeEnergyCorrectionThreeProng = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionThreeProng();
			if (tau->decayMode == 0 && tauMuonFakeEnergyCorrectionOneProng != 1.0)
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionOneProng;
			}
			else if ((tau->decayMode == 1 || tau->decayMode == 2) && tauMuonFakeEnergyCorrectionOneProngPiZeros != 1.0)
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionOneProngPiZeros;
			}
			else if (tau->decayMode == 10 && tauMuonFakeEnergyCorrectionThreeProng != 1.0)
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionThreeProng;
			}
		}
		else if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)) // correct e->tau fake energy scale
		{
			if (fes_eta_split)
			{
				LOG(DEBUG) << "fes_eta_split: split ";
				float tauElectronFakeEnergyCorrectionOneProngBarrel = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngBarrel();
				float tauElectronFakeEnergyCorrectionOneProngPiZerosBarrel = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngPiZerosBarrel();
				float tauElectronFakeEnergyCorrectionThreeProngBarrel = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionThreeProngBarrel();
				float tauElectronFakeEnergyCorrectionOneProngEndcap = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngEndcap();
				float tauElectronFakeEnergyCorrectionOneProngPiZerosEndcap = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngPiZerosEndcap();
				float tauElectronFakeEnergyCorrectionThreeProngEndcap = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionThreeProngEndcap();
				if (tau->p4.Eta() <= 1.5)
				{
					LOG(DEBUG) << "\t fes_eta_split: barrel ";
					if (tau->decayMode == 0 && tauElectronFakeEnergyCorrectionOneProngBarrel != 1.0)
					{

						LOG(DEBUG) << "\t\t fes_eta_split: barrel : dm 0 " << tauElectronFakeEnergyCorrectionOneProngBarrel;
						tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngBarrel;
					}
					else if ((tau->decayMode == 1 || tau->decayMode == 2) && tauElectronFakeEnergyCorrectionOneProngPiZerosBarrel != 1.0)
					{

						LOG(DEBUG) << "\t\t fes_eta_split: barrel : dm 1 " << tauElectronFakeEnergyCorrectionOneProngPiZerosBarrel;
						tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngPiZerosBarrel;
					}
					else if (tau->decayMode == 10 && tauElectronFakeEnergyCorrectionThreeProngBarrel != 1.0)
					{

						LOG(DEBUG) << "\t\t fes_eta_split: barrel : dm 10 " << tauElectronFakeEnergyCorrectionThreeProngBarrel;
						tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionThreeProngBarrel;
					}
				}
				else
				{
					LOG(DEBUG) << "\t fes_eta_split: endcap ";
					if (tau->decayMode == 0 && tauElectronFakeEnergyCorrectionOneProngEndcap != 1.0)
					{
						LOG(DEBUG) << "\t\t fes_eta_split: endcap : dm 0 " << tauElectronFakeEnergyCorrectionOneProngEndcap;
						tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngEndcap;
					}
					else if ((tau->decayMode == 1 || tau->decayMode == 2) && tauElectronFakeEnergyCorrectionOneProngPiZerosEndcap != 1.0)
					{
						LOG(DEBUG) << "\t\t fes_eta_split: endcap : dm 1 " << tauElectronFakeEnergyCorrectionOneProngPiZerosEndcap;
						tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngPiZerosEndcap;
					}
					else if (tau->decayMode == 10 && tauElectronFakeEnergyCorrectionThreeProngEndcap != 1.0)
					{
						LOG(DEBUG) << "\t\t fes_eta_split: endcap : dm 10 " << tauElectronFakeEnergyCorrectionThreeProngEndcap;
						tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionThreeProngEndcap;
					}
				}
			}
			else
			{
				float tauElectronFakeEnergyCorrectionOneProng = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProng();
				float tauElectronFakeEnergyCorrectionOneProngPiZeros = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngPiZeros();
				float tauElectronFakeEnergyCorrectionThreeProng = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionThreeProng();
				if (tau->decayMode == 0 && tauElectronFakeEnergyCorrectionOneProng != 1.0)
				{
					tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProng;
				}
				else if ((tau->decayMode == 1 || tau->decayMode == 2) && tauElectronFakeEnergyCorrectionOneProngPiZeros != 1.0)
				{
					tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngPiZeros;
				}
				else if (tau->decayMode == 10 && tauElectronFakeEnergyCorrectionThreeProng != 1.0)
				{
					tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionThreeProng;
				}
			}
		}
	}
	else if (tauEnergyCorrection == TauEnergyCorrection::MSSMHTT2016)
	{
		if (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)
		{
			if (tau->decayMode == 0)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProng();
			}
			else if (tau->decayMode == 1)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZeros();
			}
			else if (tau->decayMode == 10)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProng();
			}
		}
		// correct e->tau fake energy scale
		if (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)
		{
			if (tau->decayMode == 0)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProng();
			}
			else if (tau->decayMode == 1)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngPiZeros();
			}
		}
	}
	else if (tauEnergyCorrection != TauEnergyCorrection::NONE)
	{
		LOG(FATAL) << "Tau energy correction of type " << Utility::ToUnderlyingValue(tauEnergyCorrection) << " not yet implemented!";
	}

	// -------------------------------------
	// tau energy scale shifts
	float tauEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionShift();
	float tauEnergyCorrectionOneProngShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngShift();
	float tauEnergyCorrectionOneProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZerosShift();
	float tauEnergyCorrectionOneProngPiZerosShift_ch = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZerosCHShift();
	float tauEnergyCorrectionOneProngPiZerosShift_neu = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZerosNTShift();
	float tauEnergyCorrectionThreeProngShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngShift();
	// inclusive
	if (tauEnergyCorrectionShift != 1.0)
	{
		tau->p4 = tau->p4 * tauEnergyCorrectionShift;

		// settings for (cached) Svfit calculation
		(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ES;
		(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionShift;
	}
	// 1-prongs only
	if (tauEnergyCorrectionOneProngShift != 1.0 && tau->decayMode == 0)
	{
		tau->p4 = tau->p4 * tauEnergyCorrectionOneProngShift;

		// settings for (cached) Svfit calculation
		(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ES_1PRONG;
		(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionOneProngShift;
	}
	// 1-prong+pi0s only
	if ((tau->decayMode == 1 || tau->decayMode == 2))
	{
		if (tauEnergyCorrectionOneProngPiZerosShift != 1.0)
		{
			tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPiZerosShift;
		}
		else if (tau->decayMode == 1 && (tauEnergyCorrectionOneProngPiZerosShift_ch != 1.0 || tauEnergyCorrectionOneProngPiZerosShift_neu != 1.0))
		{
			// Scale the individual components
			for (auto& candidate : tau->chargedHadronCandidates)
				candidate.p4 = candidate.p4 * tauEnergyCorrectionOneProngPiZerosShift_ch;

			for (auto& candidate : tau->piZeroCandidates)
				candidate.p4 = candidate.p4 * tauEnergyCorrectionOneProngPiZerosShift_neu;

			for (auto& candidate : tau->gammaCandidates)
				candidate.p4 = candidate.p4 * tauEnergyCorrectionOneProngPiZerosShift_neu;

			// Recalculate the p4 of the tau candidate
			float mpi0 = 0.1349766;
			float mpi = 0.13957018;
			// pi0 and pi mass constrain
			TVector3 signalGammaCands_v(tau->piZeroMomentum().Px(), tau->piZeroMomentum().Py(), tau->piZeroMomentum().Pz());
			TVector3 signalChargedHadrCands_v(tau->sumChargedHadronCandidates().Px(), tau->sumChargedHadronCandidates().Py(), tau->sumChargedHadronCandidates().Pz());
			TLorentzVector signalGammaCands_p4_new = TLorentzVector(signalGammaCands_v, std::sqrt(std::pow(mpi0, 2) + signalGammaCands_v.Mag2()));
			TLorentzVector signalChargedHadrCands_p4_new = TLorentzVector(signalChargedHadrCands_v, std::sqrt(std::pow(mpi, 2) + signalChargedHadrCands_v.Mag2()));
			TLorentzVector tau_p4 = signalGammaCands_p4_new + signalChargedHadrCands_p4_new;

			tau->p4 = RMFLV(tau_p4.Pt(), tau_p4.Eta(), tau_p4.Phi(), tau_p4.M());
		}

		// settings for (cached) Svfit calculation
		(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ES_1PRONGPI0S;
		(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionOneProngPiZerosShift;
	}

	// 3-prongs only
	if (tauEnergyCorrectionThreeProngShift != 1.0 && tau->decayMode == 10)
	{
		tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngShift;

		// settings for (cached) Svfit calculation
		(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ES_3PRONG;
		(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionThreeProngShift;
	}

	// -------------------------------------
	// electron->tau fake energy scale shifts
	float tauElectronFakeEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionShift();
	float tauElectronFakeEnergyCorrectionOneProngShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngShift();
	float tauElectronFakeEnergyCorrectionOneProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngPiZerosShift();
	float tauElectronFakeEnergyCorrectionThreeProngShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionThreeProngShift();
	if (tauElectronFakeEnergyCorrectionShift != 1.0 ||
		tauElectronFakeEnergyCorrectionOneProngShift != 1.0 ||
		tauElectronFakeEnergyCorrectionOneProngPiZerosShift != 1.0 ||
		tauElectronFakeEnergyCorrectionThreeProngShift != 1.0)
	{
		if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU))
		{
			// inclusive
			if (tauElectronFakeEnergyCorrectionShift != 1.0)
			{
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ELECTRON_FAKE_ES;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionShift;
			}
			// 1-prongs only
			if (tauElectronFakeEnergyCorrectionOneProngShift != 1.0 && tau->decayMode == 0)
			{
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ELECTRON_FAKE_ES_1PRONG;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauElectronFakeEnergyCorrectionOneProngShift;
			}
			// 1-prong+pi0s only
			if (tauElectronFakeEnergyCorrectionOneProngPiZerosShift != 1.0 && (tau->decayMode == 1 || tau->decayMode == 2))
			{
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngPiZerosShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ELECTRON_FAKE_ES_1PRONGPI0S;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauElectronFakeEnergyCorrectionOneProngPiZerosShift;
			}
			// 3-prongs only
			if (tauElectronFakeEnergyCorrectionThreeProngShift != 1.0 && tau->decayMode == 10)
			{
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionThreeProngShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ELECTRON_FAKE_ES_3PRONG;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauElectronFakeEnergyCorrectionThreeProngShift;
			}
		}
	}

	// -------------------------------------
	// muon->tau fake energy scale shifts
	float tauMuonFakeEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionShift();
	float tauMuonFakeEnergyCorrectionOneProngShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProngShift();
	float tauMuonFakeEnergyCorrectionOneProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProngPiZerosShift();
	float tauMuonFakeEnergyCorrectionThreeProngShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionThreeProngShift();
	if (tauMuonFakeEnergyCorrectionShift != 1.0 ||
		tauMuonFakeEnergyCorrectionOneProngShift != 1.0 ||
		tauMuonFakeEnergyCorrectionOneProngPiZerosShift != 1.0 ||
		tauMuonFakeEnergyCorrectionThreeProngShift != 1.0)
	{
		if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU))
		{
			// inclusive
			if (tauMuonFakeEnergyCorrectionShift != 1.0)
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_MUON_FAKE_ES;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionShift;
			}
			// 1-prongs only
			if (tauMuonFakeEnergyCorrectionOneProngShift != 1.0 && tau->decayMode == 0)
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionOneProngShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_MUON_FAKE_ES_1PRONG;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauMuonFakeEnergyCorrectionOneProngShift;
			}
			// 1-prong+pi0s only
			if (tauMuonFakeEnergyCorrectionOneProngPiZerosShift != 1.0 && (tau->decayMode == 1 || tau->decayMode == 2))
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionOneProngPiZerosShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_MUON_FAKE_ES_1PRONGPI0S;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauMuonFakeEnergyCorrectionOneProngPiZerosShift;
			}
			// 3-prongs only
			if (tauMuonFakeEnergyCorrectionThreeProngShift != 1.0 && tau->decayMode == 10)
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionThreeProngShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_MUON_FAKE_ES_3PRONG;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauMuonFakeEnergyCorrectionThreeProngShift;
			}
		}
	}
	// -------------------------------------
	// jet->tau fake energy scale shifts
	float tauJetFakeEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauJetFakeEnergyCorrection();
	if (tauJetFakeEnergyCorrectionShift != 0.0)
	{
		if (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_FAKE)
		{
			// maximum shift of 40% for pt > 200 GeV
			double shift = tau->p4.Pt() < 200. ? 0.2 * tau->p4.Pt() / 100. : 0.4;

			tau->p4 = tau->p4 * (1 - tauJetFakeEnergyCorrectionShift * shift);

			// settings for (cached) Svfit calculation
			(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_JET_FAKE_ES;
			(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauJetFakeEnergyCorrectionShift;
		}
	}
	(static_cast<HttProduct&>(product)).m_tauEnergyScaleWeight[tau] = normalisationFactor;
		float randomTauEnergySmearing = static_cast<HttSettings const&>(settings).GetRandomTauEnergySmearing();

	if (randomTauEnergySmearing != 0.0)
	{
		double r;
		TRandom *r3 = new TRandom3();
		r3->SetSeed(event.m_eventInfo->nEvent);
		r = (1.0+r3->Gaus(0,randomTauEnergySmearing));
		tau->p4 = tau->p4 * r;
	}
}

