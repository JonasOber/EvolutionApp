# Gold-Perovskite interface
Created: 2021-12-0914:34
What happens at the gold-perovskite interface?
asdf
Ohmic and Schottky contacts:
![[Ohmic and schottky.png]] 

Contact of Gold with Perovskite:
![[Gold_Pero.png]]
- Schottky contact for electrons
- ohmic for holes?

The I-V curve for a schottky contact:
$\begin{equation}
J = q \frac{v_{th}}{4} Nu_C \, \exp{ - \frac{q\Phi _{Bn}}{kT}} (\exp{\frac{qV}{kT}-1})
\end{equation}$
For the parameters:
				Perovskite
--------------------------
q				1.602E-19		C
v_th			1e7					m/s
N_C				8e18				cm^-3
k				1.38e-23			m^2 kd s^-2 K^-1
T 				300					K
$\Phi_{Bn}$			1.4			eV			

Simulation in Python Programs, but without the HTL and ... so not of much use.

For voltages under 0.9 V, reversible ion diffusion  occurs. At higher voltages electrochemical reactions might occur at the interfaces, leading to the formation of HI, Pb^0_UPD, I^0_UPD [1].

# Dark IV measurement
The dark IV measurement for the ETL defect, then we have a gold-pero interface, with cells 2 and 4 defect, shows: 
![[Dark IV of ETL defect.png]]


##Questions 
- Wieso Kante im EL Bild hohe Intensität?
- Wieso ist die Kante bei der Messung vom 9.12. nicht mehr erkennbar?
- 
##References
1. [[2019 Reactions at noble metal contacts with methylammonium lead triiodide perovskites]]
##Further Reading
1. 