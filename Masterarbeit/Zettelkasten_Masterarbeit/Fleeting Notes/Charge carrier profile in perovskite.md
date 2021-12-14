# Charge carrier profile in perovskite
Created: 2021-12-1412:43
Task: Model the charge carrier profile in the perovskite, using only the drift equation.

## Basis
Charge carrier concentrations in semiconductors are calculated by:
$
n(x) = n_i \, \exp{\frac{E-E_{C}}{kT}}
$
$
p(x) = n_i \, \exp{{E_V - E}}
$
and with applied Voltages, Fermi Level splits into quasi Fermi Levels EFp, EFn:
$
n(x) = n_i \exp{\frac{E_{Fn}-E_i}{kT}} = n_i \exp{U_F - U}
$
$
p(x) = n_i \exp{\frac{E_i - E_{Fp}}{kT}} = n_i \exp{U-U_F}
$
This shows that applying a positive voltage increases electron concentration, while a negative voltage increases hole concentration.
The potential is then calculated by Poisson's equation:
$
\nabla^2 \,U = - \frac{q}{kT} \frac{\rho}{\epsilon_s}
$
with $\rho$ being:
$
\rho = q *(p-n).
$

##Questions 
Wenn mir die Poissongleichung meinen Ladungsträgerverlauf gibt, wieso brauche ich dann Drift und Diffusionsgleichung?

##References
1. 
##Further Reading
1. 