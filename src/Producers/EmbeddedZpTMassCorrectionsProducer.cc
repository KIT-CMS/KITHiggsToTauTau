#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EmbeddedZpTMassCorrectionsProducer.h"

void EmbeddedZpTMassCorrectionsProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("embedZpTMassWeight", [](event_type const& event, product_type const& product) {
		return (product.m_embed_zpt_mass_weight);
	});
	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);
	TFile root_file(settings.GetEmbeddedZpTMassCorrectionFile().c_str());
        m_input_hist = (TH2F*)root_file.Get(settings.GetEmbeddedZpTMassCorrectionHistogram().c_str());
        m_input_hist->SetDirectory(0);
        root_file.Close();
	gDirectory = savedir;
	gFile = savefile;
}

void EmbeddedZpTMassCorrectionsProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings) const
{
    int binx = m_input_hist->GetXaxis()->FindFixBin(product.m_genBosonLV.M());
    binx = std::clamp(binx, 1, m_input_hist->GetXaxis()->GetNbins());
    int biny = m_input_hist->GetYaxis()->FindFixBin(product.m_genBosonLV.Pt());
    biny = std::clamp(biny, 1, m_input_hist->GetYaxis()->GetNbins());

    product.m_embed_zpt_mass_weight = m_input_hist->GetBinContent(binx, biny);
}
