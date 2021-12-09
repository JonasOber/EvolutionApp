import numpy as np
import matplotlib.pyplot as plt
plt.style.use('../PL/plot.mplstyle')

file = "../../Auswertungen/MaPbI3 ISFH7TLModel_E2_059_211_nk.csv"

with open(file, 'r') as open_file:
    data = open_file.readlines()

wavelengths = [float(item.strip().split(',')[0]) for item in data]
refraction_index = [float(item.strip().split(',')[1]) for item in data]
extinction_coeff = [float(item.strip().split(',')[2]) for item in data]

#c = 2,9974e8 # m/s
#pi_c = np.pi*c
yticks = np.logspace(1,9,4)
@np.vectorize
def absorption_from_extinction(wavelength, ext_coeff):
    """
    https://de.wikipedia.org/wiki/Absorptionskoeffizient
    alpha = 2*n''*w/c
    w/c = 2pi/lambda
    :param wavelength:
    :param ext_coeff:
    :return: abs [m^-1]
    """
    return 2*ext_coeff*2*np.pi/(wavelength*1e-9)

# calculate the absorption coefficient for the wavelengths
absorption_coeff = absorption_from_extinction(wavelengths, extinction_coeff)

# convert 1/m to 1/nm
absorption_coeff_nm = 1e-9*absorption_coeff
# absorption length
absorption_length = absorption_coeff**(-1)
absorption_length_nm = absorption_coeff_nm**(-1)

fig = plt.figure(figsize=(3 * 11 / 2.54, 11 / 2.54))
ax = fig.add_subplot(131)
ax.plot(wavelengths, refraction_index, linestyle='None', marker='.', markersize=1, label="n")
ax.plot(wavelengths, extinction_coeff, linestyle='None', marker='.', markersize=1,label="k")
ax.set_xlabel("Wellenlänge (nm)")
ax.set_ylabel("n, k")
ax.set_xlim(250,750)
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
ax.legend()

ax2 = fig.add_subplot(132)
ax2.plot(wavelengths, absorption_coeff_nm, linestyle='None', marker='.', markersize=1)
ax2.set_ylabel(r"Absorbtionskoeffizient (nm$^{-1}$)")
ax2.set_xlabel("Wellenlänge (nm)")
ax2.set_yscale('log')
ax2.set_ylim(7e-4,1e-1)
#ax2.set_yticks(yticks)
ax2.set_xlim(250,750)
ax2.set_aspect(1.0/ax2.get_data_ratio(), adjustable='box')

ax3 = fig.add_subplot(133)
ax3.set_xlim(250,750)
ax3.plot(wavelengths, absorption_length_nm, linestyle='None', marker='.', markersize=1)
ax3.set_xlabel("Wellenlänge (nm)")
ax3.set_ylabel("Absorptionslänge (nm)")
ax3.set_ylim(10, 1e4)
ax3.set_yscale('log')
#ax3.set_yticks(yticks)
ax3.set_aspect(1.0/ax3.get_data_ratio(), adjustable='box')
fig.suptitle("Daten für Perowskit MAPbI3")
fig.tight_layout()
plt.savefig("Pero_nk_alpha_Ld.svg")
#plt.show()

print(wavelengths)
PL_index = wavelengths.index(633.37)
absorption_coeff_PL = absorption_coeff_nm[PL_index]
print(f"At {wavelengths[PL_index]} nm , absorption coeff: {absorption_coeff_nm[PL_index]:1.3e} nm^-1, length: {absorption_length_nm[PL_index]:1.2e} nm.")

PL_781_index = wavelengths.index(781.26)
abs_718nm = absorption_coeff_nm[PL_781_index]
print(abs_718nm)

thickness = np.linspace(0, 500, 100) # nm
# I/I0 = exp(-zalpha)
intensity_normed_633 = np.exp(-thickness*absorption_coeff_PL)
intensity_normed_780 = np.exp(-thickness*abs_718nm)

fig = plt.figure(figsize=(1 * 11 / 2.54, 11 / 2.54))
ax = fig.add_subplot(111)
ax.plot(thickness, intensity_normed_633, label="633 nm")
ax.plot(thickness, intensity_normed_780, label="780 nm")
ax.set_ylabel(r"I/I$_0$")
ax.set_xlabel("Abstand zur Oberfläche (nm)")
ax.legend()
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
fig.suptitle("Abfall der PL Anregung in MAPbI3")
plt.savefig("MAPbI3_Intensität.svg")
#plt.show()
