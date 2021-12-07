"""
PDE solution and test with FD numerical solution.
PDE from D. Hinken Diss
Charge carrier profile in silicon
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

# Constants
n_i = 0.99e10 # cm^-3
N_A = 1e16 # cm^-3
k_B = 
T = 300 #K
hbar = 6.636e-34 # Js
V_T = k_B * T/hbar
V_applied = 1 #V
L_b = 264 # um
S_rear = 600 # cm/s
W_b = 200 # um
L_eff = L_b * (L_b * S_rear * np.sinh(W_b/L_b) + D * np.cosh(W_b/L_b))/ (L_b * S_rear * np.cosh(W_b/L_b) + D * np.sinh(W_b/L_b))

# mobility in Silicon

# Diffusion coeff
D = 36 # cm^2/s
# Functions
def n1(V_i):
    # returns the boundary condition for an applied voltage
    return n_i**2 /N_A * np.exp(V_i/V_T)

boundary_charge = n1(V_applied)

#def boundary_condition_Wb()
# Srear delta n_Wb = - D * d/dz delta n(z) at z = W_b

# analytic solution
def dark_charge_concentration(z):
    return boundary_charge * (np.cosh(z/L_b) - L_b/L_eff * np.sinh(z/L_b))






