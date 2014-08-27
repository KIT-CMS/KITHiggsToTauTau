
#pragma once

#include <utility>

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Artus/Utility/interface/ArtusLogging.h"

/**
   \brief Place to collect functions calculating CP quantities
   -Phi* : this is a variable, with which one can say, whether the considered boson is a scalar (CP even) or a pseudoscalar (CP odd)
   -Psi*CP : this is a variable, with which one can figure out, whether the have a CP-mixture or not
   -Zs : this is a variable, with which one can figure out, wether the considered boson is a scalar (CP even) or a pseudoscalar (CP odd)
*/

class CPQuantities
{
public:
	static float CalculatePhiStarCP(RMDataLV tau1, RMDataLV tau2, RMDataLV chargPart1, RMDataLV chargPart2,float& ABS_n1, float& ABS_n2, double& phiStar);
	static float CalculatePhiStarCP(KDataVertex pv , KDataTrack track1, KDataTrack track2, RMDataLV chargPart1,RMDataLV chargPart2, float& abs_n1, float& abs_n2);
	static float CalculateChargedHadronEnergy(RMDataLV diTauMomentum, RMDataLV chargHad);
	static float CalculatePhiCP(RMDataLV boson, RMDataLV tau1, RMDataLV tau2, RMDataLV pion1, RMDataLV pion2, double& phi);
	static float CalculateChargedProngEnergy(RMDataLV tau, RMDataLV chargedProng);
	static float CalculateChargedProngEnergyApprox(RMDataLV tau, RMDataLV chargedProng);
	static float CalculateThetaNuHadron(RMDataLV tau, RMDataLV nuTau, RMDataLV hadron);
	static float CalculateAlphaTauNeutrinos(RMDataLV tauM, RMDataLV nuTauM, RMDataLV tauP, RMDataLV nuTauP);
	static float CalculateTrackReferenceError(KDataTrack track);
	static float CalculateZPlusMinus(RMDataLV higgs, RMDataLV chargedPart);
	static float CalculateZs(float zPlus, float zMinus);
	static float PhiTransform(float phi);
};
