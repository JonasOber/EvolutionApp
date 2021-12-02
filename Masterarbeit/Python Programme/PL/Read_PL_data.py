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
image_01 = "C:/Users/j.oberroehrmann/Documents/Messdaten/PL/P3T_063/20211202_G1963/G1963_Zelle4_aufPero_oben_01.l6s"
with codecs.open(image_01,"r",encoding="mbcs") as sourceFile:
    with codecs.open("PL_data.txt","w",encoding="UTF-8") as targetFile:
        while True:
            contents = sourceFile.read(blockSize)
            if not contents:
                break
            targetFile.write(contents)
# mbcs for ansi

#print(unicoded_file)

#with open("PL_data.txt", 'w') as data:
#    data.write(unicoded_file)