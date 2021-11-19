import numpy as np
import matplotlib.pyplot as plt

# get the voltages for my lowest measurement range
voltages = np.logspace(-6, -1, 10)

# define the functions
@np.vectorize
def error_voltage(V):
    """
    Calculates the measurement accuracy of the Keithley 2000 in lowest range. For data see the manual.
    :param V:
    :return:
    """
    return (50*V + 35 * 0.1)*1e-6

def E_N(y1, y2):
    """
    Calculates the E_N criteria to distinguish to voltages V1, V2 with uncertainties u(y1), u(y2). Voltages accepted as different,
    if E_N << 1.
    :param y1:
    :param y2:
    :return:
    """
    u_y1 = error_voltage(y1)
    u_y2 = error_voltage(y2)

    return 1/2 * np.abs(y1-y2)/np.sqrt(u_y1**2 + u_y2**2)

x = np.linspace(0, len(voltages), len(voltages))
print(len(voltages),"x:", len(x))
plt.errorbar(voltages, voltages, yerr=error_voltage(voltages), linestyle=None, marker='.')
plt.ylabel("Spannung U (V)")
#plt.show()

# Question: When can I distinguish one measured voltage from 0 V?
E_N_array = []
for i in range(len(voltages)):
    E_N_value = E_N(0, voltages[i])
    E_N_array.append(E_N_value)
    print(f"Voltage: {voltages[i]}, u(U): {error_voltage(voltages[i])}, E_N: {E_N_value}.")
plt.plot(voltages, E_N_array)
plt.show()
print()