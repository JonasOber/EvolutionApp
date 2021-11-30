import numpy as np
import matplotlib.pyplot as plt
plt.style.use('../PL/plot.mplstyle')
# get the voltages for my lowest measurement range
voltages = np.logspace(-6, -5, 50)
fig = plt.figure()
ax = fig.add_subplot(111)
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

ax.set_box_aspect(1)
ax.errorbar(voltages, voltages, yerr=error_voltage(voltages), color='blue', linestyle='None', marker='.')
ax.set_ylabel("Spannung U (V) with error")
ax.set_xlabel("Spannung U (V)")
ax.spines['left'].set_color('blue')
ax.tick_params(axis='y', colors='blue')
#plt.rc_context({'axes.edgecolor':'orange', 'xtick.color':'red', 'ytick.color':'green', 'figure.facecolor':'white'})
# Question: When can I distinguish one measured voltage from 0 V?
E_N_array = [E_N(0, volt) for volt in voltages]


ax2 = ax.twinx()
ax2.set_box_aspect(1)
ax2.plot(voltages, E_N_array, linestyle='None',color='green', marker='.')
ax2.set_xlabel("Spannung U (V)")
ax2.set_ylabel(r"Kriterium E$_{\mathrm{N}}$ (a. u.)")
ax2.tick_params(axis='y', colors='green')
ax2.spines['left'].set_color('blue')
ax2.spines['right'].set_color('green')
plt.savefig("Messunsicherheit_Spannung.svg")
plt.show()
