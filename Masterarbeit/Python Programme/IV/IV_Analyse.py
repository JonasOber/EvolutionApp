import glob
from os import path
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable
import tkinter as tk
from tkinter import filedialog
import matplotlib as mpl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

plt.rcParams['font.family'] = "Arial"
plt.rcParams['font.size'] = 14
root = tk.Tk()
root.withdraw()

class IV_Analyse():
    def __init__(self, path):
        self.path = path 
        self.cellsize = 0.12 # cm^2
        self.get_IV_data()
       

    def get_IV_data(self):
        with open(self.path, encoding='latin-1') as file:
            for line in file:
                if line.strip() == "**Data**":
                    data_array = file.readlines()
        
        self.voltage = [float(item.strip().split('\t')[0]) for item in data_array]
        self.current = [float(item.strip().split('\t')[1]) for item in data_array]
        self.current = np.array(self.current)*1e3/self.cellsize
        self.temp = [float(item.strip().split('\t')[2]) for item in data_array]
        
    def show_IV(self):
        return [self.voltage, self.current]

    def return_label(self):
        # split path at "-""
        cell_number = self.path.split('-')[-1]
        # split path at last "."
        cell_number = cell_number.split('.')[0]
        return str(cell_number)

#image_01 = filedialog.askopenfilename()
#print(image_01)
#IV_directory = "/".join(image_01.split("/")[:-2])
#print("current working on:",IV_directory)
List_Substrates = [
    "G1963",
    "G1965",
    "G1967",
    "G1968",
    "G1971",
    "G1974"
]

for substrate in ["G1963", "G1974"]:
    IV_directory = "C:/Users/j.oberroehrmann/Documents/Messdaten/Loana_Lukas/P3T_063/"+substrate
    # create the figure
    width = 14/2.54
    fig = plt.figure(figsize=(2*width, width))
    ax = fig.add_subplot(121)
    ax_inset = inset_axes(ax, width="30%", height="30%", loc=(9))
    ax2 = fig.add_subplot(122)
    ax2_inset = inset_axes(ax2, width="30%", height="30%", loc=(9))

    #ax.set_aspect("equal")
    #ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    ax.set_xlabel(r"Spannung $\mathit{U}$ (V)")
    ax.set_ylabel(r"Stromdichte $\mathit{J}$ (mA/cm$^2$)")
    ax_inset.set_xlabel(r"$\mathit{U}$ (V)")
    ax_inset.set_ylabel(r"$\mathit{J}$ (mA/cm$^2$)")
    ax2.set_xlabel(r"Spannung $\mathit{U}$ (V)")
    ax2.set_ylabel(r"Stromdichte $\mathit{J}$ (mA/cm$^2$)")
    ax2_inset.set_xlabel(r"$\mathit{U}$ (V)")
    ax2_inset.set_ylabel(r"$\mathit{J}$ (mA/cm$^2$)")
    
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax2.yaxis.set_ticks_position('both')
    ax2.xaxis.set_ticks_position('both')
    #ax.set_yscale('log')
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax2.axhline(0, color='black', linewidth=1)
    ax2.axvline(0, color='black', linewidth=1)
    print(IV_directory)
    Substrate_name = IV_directory.split('/')[-1]
    print("Substrate name:", Substrate_name)
    Mode = IV_directory.split('/')[-1]
    dict_mode = {"Hell":'lgt', "Dunkel":'drk'}
    for path in glob.iglob(IV_directory+"/Dunkel"+"/*.drk"):#+dict_mode[Mode]):
        print(path)
        IV_plt = IV_Analyse(path)
        volt, curr = IV_plt.show_IV()
        ax.plot(volt, curr, linestyle='None', marker='.', markersize=5, label="Zelle "+IV_plt.return_label())
        ax_inset.plot(volt, curr, linestyle='None', marker='.', markersize=5, label="Zelle "+IV_plt.return_label())
    for path in glob.iglob(IV_directory+"/Hell"+"/*.lgt"):#+dict_mode[Mode]):
        print(path)
        IV_plt = IV_Analyse(path)
        volt, curr = IV_plt.show_IV()
        ax2_inset.plot(volt, curr, linestyle='None', marker='.', markersize=5, label="Zelle " + IV_plt.return_label())
        ax2.plot(volt, curr, linestyle='None', marker='.', markersize=5, label="Zelle "+IV_plt.return_label())

    ax.set_yscale('log')
    ax2.set_ylim(-3, 1)
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    ax2.set_aspect(1.0/ax2.get_data_ratio(), adjustable='box')
    #lgnd = plt.legend(loc="upper left", scatterpoints=1, fontsize=10)
    ax.set_title("Dunkelkennlinie")
    ax2.set_title("Hellkennlinie")

    #ax_inset.set_ylim(-0.01,0.01)
    #ax_inset.set_yscale('log')


    ax2.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(IV_directory+"/"+Substrate_name+".svg", transparent='true')
    #plt.show()
