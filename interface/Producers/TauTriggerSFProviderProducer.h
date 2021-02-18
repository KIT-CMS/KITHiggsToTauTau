
#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TauAnalysisTools/TauTriggerSFs/interface/SFProvider.h"

/**
   \brief TauTriggerEfficiencyProducer
   Config tags:
   - Fill me with something meaningful

*/

class TauTriggerSFProviderProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

        ~TauTriggerSFProviderProducer()
        {
                for (std::map<std::string, tau_trigger::SFProvider*>::iterator wp_map_it = TauSFs.begin(); wp_map_it != TauSFs.end(); wp_map_it++)
                {
                        delete wp_map_it->second;
                }
        }

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
                std::string input = settings.GetTauTriggerSFProviderInput();
                std::string trigger = settings.GetTauTrigger();
                for(auto wp: settings.GetTauTriggerWorkingPoints())
                {
                        TauSFs[wp] = new tau_trigger::SFProvider(input, trigger, wp);
                }
                m_weightNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap(settings.GetTauTriggerSFProviderWeightNames()));
                for(auto weightNames: m_weightNames)
                {
                        for(size_t index = 0; index < weightNames.second.size(); index++)
                        {
                                MCWeight[weightNames.first].resize(weightNames.second.size());
                                MCWeight[weightNames.first].at(index) = (weightNames.second.at(index).find("MC") != std::string::npos);
                                DataWeight[weightNames.first].resize(weightNames.second.size());
                                DataWeight[weightNames.first].at(index) = (weightNames.second.at(index).find("Data") != std::string::npos);
                        }
                }
	}

	virtual void Produce(event_type const& event, product_type & product,
	                     setting_type const& settings) const override;
private:
        std::map<std::string,tau_trigger::SFProvider*> TauSFs;
        std::map<int,std::vector<std::string>> m_weightNames;
        std::map<int,std::vector<bool>> MCWeight;
        std::map<int,std::vector<bool>> DataWeight;

};
