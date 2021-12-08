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
k_B = 1.38e-23 # m^2 kg/(s^2 K)
T = 300 #K
hbar = 6.636/(2*np.pi)*1e-34 # Js, 1J = 1kg m^2/s^2
#V_T = k_B * T/hbar # 1V = kg m^2 /(As^3)
V_T = 25.7e-3 #V
V_applied = 0.55 #V 
L_b = 264*1e-4 # cm
S_rear = 600 # cm/s
W_b = 200*1e-4 # cm
# Diffusion coeff for electrons in si
D = 36 # cm^2/s
L_eff = L_b * (L_b * S_rear * np.sinh(W_b/L_b) + D * np.cosh(W_b/L_b))/ (L_b * S_rear * np.cosh(W_b/L_b) + D * np.sinh(W_b/L_b))

# x scale for charge concentration in Silicon
z_analytic = np.linspace(0, 200, 1000)*1E-6
#print(z_analytic)

# Functions
def n1(V_i):
    # returns the boundary condition for an applied voltage in 10**12 cm^3
    return n_i**2 /N_A * np.exp(V_i/V_T)

boundary_charge_left = n1(V_applied)

#def boundary_condition_Wb()
# Srear delta n_Wb = - D * d/dz delta n(z) at z = W_b

# analytic solution
@np.vectorize
def dark_charge_concentration(z):
    return boundary_charge_left * (np.cosh(z/L_b) - L_b/L_eff * np.sinh(z/L_b))

"""
Numerical FD Solution
PDE: -D/L_b**2 * n(z) + D d^2 n(z)/dz^2 = 0
    => - delta n(z)/L_b^2 + d^2 delta n(z)/dz^2 = 0

    mesh n points
    d^2 n/dz^2 = (n_j-1 + n_j+1 - 2*n_j)/h^2
"""
# get the Matrix
N = 30
x_discrete = np.linspace(0, W_b*1e-2, N+2)
h = W_b*1e-2/N # now h is in m
diagonal_element = -( 1/(L_b*1e-2)**2 + 2/h**2)
M = np.zeros((N,N))
np.fill_diagonal(M, diagonal_element)
M = np.pad(M, ((1,1), (1,1)), mode='constant', constant_values=(0))
# add next to diag elements
offdiag_element = 1/h**2
for i in range(1,N+1):
    M[i][i+1] = offdiag_element
    M[i][i-1] = offdiag_element
# add boundary conditions, voltage at z=0
M[0][0] = 1
b = np.zeros(N+2)
b[0] = boundary_charge_left
# right side at z=W_b: Srear*n_N+1 = -D ( n_N+1 - n_N)/h
# => (Srear+D/h) *n_N+1 - D/h * n_N = 0
# DIESE HIER NOCHMAL CHECKEN, das passst noch nicht 
M[N+1][N] = -D/h
M[N+1][N+1] = (S_rear+D/h)
#print(M)
sol = solve(M, b)
#print(sol)
# charge carrier concentraiton
charge_concentration = dark_charge_concentration(z_analytic)
fig = plt.figure()
ax = fig.add_subplot(111)
#print(z_analytic)
#print(x_discrete)
ax.plot(z_analytic*1e6, charge_concentration*1e-12, label='Analytic')
ax.plot(x_discrete*1e6, sol*1e-12, '--', label='FD')
ax.set_ylabel(r"Excess carrier density $\Delta$n 10$^{12}$ (cm$^3$)")
ax.set_xlabel(r"Distance from front ($\mu$m)")
ax.legend()
plt.savefig("pde_silicon.png")






