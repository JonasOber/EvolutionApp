"""
Simulation for the IV characteristic of the Au- Pero interface, assuming a schottky barrier


"""
# libraries
import numpy as np
import matplotlib.pyplot as plt

# Konstanten
q = 1.6e-19 # C
v_th = 1e7 # m/s
N_C = 8e18 # cm^-3
N_C_m = 8e18 * 1e6 # m^3
k = 1.38e-23 # m^2 kg s^-2 K^-1
k_eV = k/q # eV/k
T = 300 # K
Phi_Bn = 1.4 # eV
# saturation current density
J_s = q * v_th/4 * N_C_m * np.exp(-Phi_Bn/(k_eV*T))

# Voltages
V = np.linspace(0, 1.27, 10000)
@np.vectorize
def J_schottky(voltage):
    return J_s * (np.exp(voltage/(k_eV*T)) -1 )

Current_Schottky = J_schottky(V)
print(Current_Schottky)
fig = plt.figure(figsize=(1 * 11 / 2.54, 11 / 2.54))
ax = fig.add_subplot(111)
ax.plot(V, Current_Schottky)
ax.set_xlabel("Spannung U (V)")
ax.set_ylabel("Strom I (A)")
ax.set_yscale('log')
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.savefig("schottky.png")
plt.show()