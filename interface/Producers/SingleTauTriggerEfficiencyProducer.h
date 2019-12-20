#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TauAnalysisTools/TauTriggerSFs/interface/TauTriggerSFsSingleTau.h"

/**
   \brief TauTriggerEfficiencyProducer
   Config tags:
   - Fill me with something meaningful

*/

class SingleTauTriggerEfficiencyProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

        ~SingleTauTriggerEfficiencyProducer()
        {
                for (std::map<std::string, std::map<std::string, TauTriggerSFsSingleTau*>>::iterator wp_map_it = TauSFs.begin(); wp_map_it != TauSFs.end(); wp_map_it++)
                {
                        for (std::map<std::string, TauTriggerSFsSingleTau*>::iterator trig_map_it = wp_map_it->second.begin(); trig_map_it != wp_map_it->second.end(); trig_map_it++)
                        {
                                delete trig_map_it->second;
                        }
                }
        }

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
                std::string input = settings.GetSingleTauTriggerInput();
                std::string year = std::to_string(settings.GetYear());
                for(auto wp: settings.GetSingleTauTriggerWorkingPoints())
                {
                        for(auto t: settings.GetSingleTauTriggerIDTypes())
                        {
                                TauSFs[wp][t] = new TauTriggerSFsSingleTau(input, year, wp, t);
                        }
                }
                m_weightNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap(settings.GetSingleTauTriggerEfficiencyWeightNames()));
                for(auto weightNames: m_weightNames)
                {
                        for(size_t index = 0; index < weightNames.second.size(); index++)
                        {
                                MCWeight[weightNames.first].resize(weightNames.second.size());
                                MCWeight[weightNames.first].at(index) = (weightNames.second.at(index).find("MC") != std::string::npos);
                        }
                }
	}

	virtual void Produce(event_type const& event, product_type & product,
	                     setting_type const& settings) const override;
private:
        std::map<std::string,std::map<std::string,TauTriggerSFsSingleTau*>> TauSFs;
        std::map<int,std::vector<std::string>> m_weightNames;
        std::map<int,std::vector<bool>> MCWeight;

};
