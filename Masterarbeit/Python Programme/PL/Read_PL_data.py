import tkinter as tk
from tkinter import filedialog
import glob
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
from pathlib import Path

plt.style.use('../PL/plot.mplstyle')
figsize = 14/2.54 # 14 cm in inches
root = tk.Tk()
root.withdraw()
import codecs
#image_01 = filedialog.askopenfilename()
#image_01 = "G1963_Zelle4_aufPero_01.txt"

class PL_Spectrum():
    def __init__(self, path):
        print(f"Now working with file: {path}.")
        self.path = str(path)
        self.get_filename()
        self.get_labelname()
        # read the data from the file to the dataframe
        self.read_data()
        # get characteristics from spectrum
        self.get_characteristics()

    def read_data(self):
        with open(self.path, 'r') as file:
            data = file.readlines()

        Energies = [float(item.strip().split("\t")[0]) for item in data]
        Spectrum = [float(item.strip().split("\t")[1]) for item in data]
        # create a dict of both arrays
        dict_spectrum = {"Energie (eV)": Energies, "Intensity (counts)": Spectrum}
        # dict to DataFrame
        dataframe_spectrum = pd.DataFrame()
        dataframe_spectrum = dataframe_spectrum.from_dict(dict_spectrum)
        dataframe_spectrum["Intensity rolling mean (counts)"] = dataframe_spectrum["Intensity (counts)"].rolling(200,center=True).mean()
        self.dataframe_spectrum = dataframe_spectrum.set_index(dataframe_spectrum["Energie (eV)"])

    def get_filename(self):
        #print(self.path)
        name = self.path.split("\\")[-1].strip('.txt')
        #print(name)
        self.name = name

    def get_labelname(self):
        #print(self.path)
        label = self.path.strip('.txt').split("\\")[-1].split("_")[-2:]
        #print(name)
        self.label_name = " ".join(label)

    def set_name(self, manual_name):
        self.name = manual_name

    def get_characteristics(self):
        # make Dataframe with characteristics: Maximum_Energie, Maximum_Intensity, FWHM
        df_index = {"Cell": ["Maximum Energie (eV)", "Maximum Intensity (counts)"]}
        Maximum_index = self.dataframe_spectrum["Intensity rolling mean (counts)"].idxmax()
        Maximum_spectrum = self.dataframe_spectrum.loc[Maximum_index]
        #print(Maximum_spectrum)
        self.Maximum_spectrum = Maximum_spectrum

    def set_linestyle(self):
        """
        check if the filename has an "auf Defekt", if yes set linestyle to dotted, else set to solid
        :return:
        """
        if self.path.find("aufDefekt")==-1:
            return "solid"
        else:
            return "dashed"
    def plot_spectrum_smoothed(self, ax):
        linestyle = self.set_linestyle()
        ax.plot(self.dataframe_spectrum["Intensity rolling mean (counts)"], linestyle=linestyle, label=self.label_name)

    def plot_spectrum_raw(self, ax):
        ax.plot(self.dataframe_spectrum["Intensity (counts)"], label=self.label_name+" raw")

    def add_char_to_dataframe(self, df):
        """
        gets a dataframe df and adds the PL characteristics to it.
        :return: dataframe df with characs

        """
        dict = {self.label_name : self.Maximum_spectrum}
        frame = pd.DataFrame.from_dict(dict)
        return pd.concat([df, frame],axis=1)
dir = "C:/Users/j.oberroehrmann/Documents/Messdaten/PL/P3T_063/20211206_G1967/"
dir_add = "G1967_Zelle1"
PL_files = []
# search directory and subdirectories with: for path in Path(dir).rglob("*.txt"):
for path in glob.iglob(dir+dir_add+"*.txt"):
    PL_files.append(path)

print(PL_files)
fig = plt.figure(figsize=(figsize, 0.5*figsize))
ax = fig.add_subplot(111)

PL_characteristics = pd.DataFrame()

for file in PL_files:
    # init object
    PL_01 = PL_Spectrum(file)
    # add smoothed line to plot
    PL_01.plot_spectrum_smoothed(ax)
    # add characteristics to the dataframe
    PL_characteristics = PL_01.add_char_to_dataframe(PL_characteristics)
ax.set_ylabel("PL Intensität (counts)")
ax.set_xlabel("Energie (eV)")
ax.set_xlim(1.3, 1.9)
#ax.set_yscale('log')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.tight_layout()
plt.savefig(dir+"/PL_spectrum.svg", transparent = True)
#plt.show()
PL_characteristics = PL_characteristics.transpose()
PL_characteristics.to_excel(dir+"/PL_characteristics.xlsx")
fig = plt.figure(figsize=(figsize, 0.6*figsize))
ax = fig.add_subplot(121)
ax.plot(PL_characteristics["Energie (eV)"], linestyle="None", marker=".")
ax.set_ylabel("Energie (eV)")
plt.xticks(rotation=45, ha='right')
xlabel = ax.xaxis.get_label()
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
ax = fig.add_subplot(122)
ax.plot(PL_characteristics["Intensity rolling mean (counts)"], linestyle="None", marker=".")
ax.set_ylabel("Intensity (counts)")
xlabel = ax.xaxis.get_label()
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(dir+ "/PL_Characteristics.svg", transparent=True)
#plt.show()