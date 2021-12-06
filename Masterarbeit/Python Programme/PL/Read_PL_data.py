import tkinter as tk
from tkinter import filedialog
import glob
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.style.use('../PL/plot.mplstyle')
root = tk.Tk()
root.withdraw()
import codecs
blockSize = 1048576
#image_01 = filedialog.askopenfilename()
image_01 = "G1963_Zelle4_aufPero_01.txt"

with open(image_01, 'r') as file:
    data = file.readlines()

wavelengths = [float(item.strip().split("\t")[0]) for item in data]
Spectrum = [float(item.strip().split("\t")[1]) for item in data]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(Spectrum)

ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.show()