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

plt.rcParams['font.family'] = "Arial"
plt.rcParams['font.size'] = 14
root = tk.Tk()
root.withdraw()

image_01 = filedialog.askopenfilename()
#print(image_01)
IV_directory = "/".join(image_01.split("/")[:-1])
#print(IV_directory)

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

# create the figure
width = 12/2.54
fig = plt.figure(figsize=(width, width))
ax = fig.add_subplot(111)
#ax.set_aspect("equal")
#ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
ax.set_xlabel(r"Spannung $\mathit{U}$ (V)")
ax.set_ylabel(r"Stromdichte $\mathit{J}$ (mA/cm$^2$)")
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
#ax.set_yscale('log')
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
print(IV_directory)
Substrate_name = IV_directory.split('/')[-1]
mode = 'lgt'
for path in glob.iglob(IV_directory+"/*."+mode):
    #print(path)
    IV_plt = IV_Analyse(path)
    volt, curr = IV_plt.show_IV()
    ax.plot(volt, curr, linestyle='None', marker='.', markersize=5, label="Z "+IV_plt.return_label())
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
lgnd = plt.legend(loc="upper left", scatterpoints=1, fontsize=10)



plt.tight_layout()
plt.savefig("C:/Users/bomml/Documents/Python/IV/Pictures/"+Substrate_name+"_"+mode+".svg", transparent='true')
#plt.show()
