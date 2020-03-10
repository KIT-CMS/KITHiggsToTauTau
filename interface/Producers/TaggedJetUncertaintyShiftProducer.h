
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "Artus/KappaAnalysis/interface/Utility/BTagSF.h"

/**
   \brief Producer for jet energy scale corrections (Htt version).

   Mostly copied from https://github.com/truggles/FinalStateAnalysis/blob/miniAOD_8_0_25/PatTools/plugins/MiniAODJetFullSystematicsEmbedder.cc

   Required config tags
   - JetEnergyCorrectionSplitUncertaintyParameters (file location)
   - JetEnergyCorrectionSplitUncertaintyParameterNames (list of names)
*/
class TaggedJetUncertaintyShiftProducer: public ProducerBase<HttTypes>
{
	public:
		typedef typename HttTypes::event_type event_type;
		typedef typename HttTypes::product_type product_type;
		typedef typename HttTypes::setting_type setting_type;

		virtual void Init(setting_type const& settings) override;
		std::string GetProducerId() const override;
		virtual void Produce(event_type const& event, product_type& product, setting_type const& settings) const override;

		~TaggedJetUncertaintyShiftProducer()
		{
			JetUncMap.clear();
		}

	private:
		std::string uncertaintyFile;
		std::vector<std::string> individualUncertainties;
		std::vector<HttEnumTypes::JetEnergyUncertaintyShiftName> individualUncertaintyEnums;

		std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::unique_ptr<JetCorrectionUncertainty>> JetUncMap;
		bool jec_shifts_applied;

		KappaEnumTypes::JetIDVersion jetIDVersion;
		KappaEnumTypes::JetID jetID;

		std::map<std::string, std::vector<float> > lowerPtCuts;
		std::map<std::string, std::vector<float> > upperAbsEtaCuts;

		KappaEnumTypes::BTagScaleFactorMethod m_bTagSFMethod;
		float m_bTagWorkingPoint;
		BTagSF m_bTagSf;
};
