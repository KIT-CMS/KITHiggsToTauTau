
#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TauPOG/TauIDSFs/interface/TauIDSFTool.h"

/**
   \brief TauIDScaleFactorProducer
   Config tags:
        TauIDSFWorkingPoints
        TauIDSFTypes
        TauIDScaleFactorWeightNames
        Year
        Channel
        UseUWGenMatching

*/

class TauIDScaleFactorProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
                const std::string year = m_yearMap.at(settings.GetYear());
                const bool isTT = settings.GetChannel()=="TT";
                for(auto wp: settings.GetTauIDSFWorkingPoints())
                {
                        for(auto t: settings.GetTauIDSFTypes())
                        {
                                TauIDSFs[wp][t] = new TauIDSFTool(year, t, wp, isTT);
                        }
                }
                m_weightNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap(settings.GetTauIDScaleFactorWeightNames()));
	}

	virtual void Produce(event_type const& event, product_type & product,
	                     setting_type const& settings) const override;
private:
        std::map<std::string,std::map<std::string,TauIDSFTool*>> TauIDSFs;
        std::map<int,std::vector<std::string>> m_weightNames;
        const std::map<int, std::string> m_yearMap = {
            {2016, "2016Legacy"},
            {2017, "2017ReReco"},
            {2018, "2018ReReco"}
        };
};