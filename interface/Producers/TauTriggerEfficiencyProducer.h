
#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TauAnalysisTools/TauTriggerSFs/interface/TauTriggerSFs2017.h"

/**
   \brief TauTriggerEfficiencyProducer
   Config tags:
   - Fill me with something meaningful

*/

class TauTriggerEfficiencyProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

        ~TauTriggerEfficiencyProducer()
        {
                for (std::map<std::string, std::map<std::string, TauTriggerSFs2017*>>::iterator wp_map_it = TauSFs.begin(); wp_map_it != TauSFs.end(); wp_map_it++)
                {
                        for (std::map<std::string, TauTriggerSFs2017*>::iterator trig_map_it = wp_map_it->second.begin(); trig_map_it != wp_map_it->second.end(); trig_map_it++)
                        {
                                delete trig_map_it->second;
                        }
                }
        }

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
                std::string input = settings.GetTauTriggerInput();
                std::string inputEMB = settings.GetTauTriggerInputKIT();
                std::string year = std::to_string(settings.GetYear());
                std::string trigger = settings.GetTauTrigger();
                for(auto wp: settings.GetTauTriggerWorkingPoints())
                {
                        for(auto t: settings.GetTauTriggerIDTypes())
                        {
                                TauSFs[wp][t] = new TauTriggerSFs2017(input, inputEMB, trigger, year, wp, t);
                        }
                }
                m_weightNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap(settings.GetTauTriggerEfficiencyWeightNames()));
                for(auto weightNames: m_weightNames)
                {
                        for(size_t index = 0; index < weightNames.second.size(); index++)
                        {                               
                                MCWeight[weightNames.first].resize(weightNames.second.size());
                                MCWeight[weightNames.first].at(index) = (weightNames.second.at(index).find("MC") != std::string::npos);
                                EMBWeight[weightNames.first].resize(weightNames.second.size());
                                EMBWeight[weightNames.first].at(index) = (weightNames.second.at(index).find("EMB") != std::string::npos);
                                KITDataWeight[weightNames.first].resize(weightNames.second.size());
                                KITDataWeight[weightNames.first].at(index) = (weightNames.second.at(index).find("KITData") != std::string::npos);
                        }
                }
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;
private:
        std::map<std::string,std::map<std::string,TauTriggerSFs2017*>> TauSFs;
        std::map<int,std::vector<std::string>> m_weightNames;
        std::map<int,std::vector<bool>> MCWeight;
        std::map<int,std::vector<bool>> EMBWeight;
        std::map<int,std::vector<bool>> KITDataWeight;

};
