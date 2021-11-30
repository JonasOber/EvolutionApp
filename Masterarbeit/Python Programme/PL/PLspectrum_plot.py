import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
plt.style.use('plot.mplstyle')
file = "C:/Users/j.oberroehrmann/Documents/Messdaten/Chargen/Referenzzellen/G1331/G1331_Z1/PL/Referenzzellen_G1331_Zelle1_01.txt"
with open(file, 'r') as data:
    PL_data = data.readlines()
PL_data = [item.strip().split('\t') for item in PL_data]

wavelengths = [float(item[0]) for item in PL_data]
pl_intensity = [float(item[1])*100/750 for item in PL_data]
pl_intensity = pl_intensity#/np.max(pl_intensity[0:4000])
# load the Filterfunctions
path_filter1 = 'C:/Users/j.oberroehrmann/Documents/Masterarbeit/Literatur/Manual_Filterdaten LP 711.csv'
path_filter2 = 'C:/Users/j.oberroehrmann/Documents/Masterarbeit/Literatur/Manual_Filterdaten LP 714.csv'
# read the filter csv to pandas
filter1 = pd.read_csv(path_filter1)
filter2 = pd.read_csv(path_filter2)
# calculate total filter function: F1*F2
filter2["total"] = filter1["%T"]*filter2["%T"]/(100)
print(filter1.head())
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(filter1["Wavelength (nm)"], filter1["%T"], label='Filter 1', color='darkblue')

ax.plot(filter2["Wavelength (nm)"], filter2["%T"], label='Filter 2', color='red')


ax.plot(filter2["Wavelength (nm)"], filter2["total"], label='Filter total', color='orange')
ax.plot(wavelengths, pl_intensity, color='gray', label='PL meas.')
# plot the mean
N = 500
lower = int(N/2 -1)
upper = int(N/2)
ax.plot(wavelengths[lower:-upper], np.convolve(pl_intensity, np.ones(N)/N, mode='valid'), color='black', label='PL smoothed')
ax.set_xlim(650,850)
ax.set_ylim(0, 100)
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Intensity (a.u.), Transmission (%)")
ax.legend()
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
#ax.axis('equal')
plt.savefig("PL_spectrum_MAPIcell_with_filter.svg")
plt.show()