"""
Overlay an EL Image with the taken Camera image. Example is G1243 Zelle 01.
"""
import glob
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable
import EL_Analysis as EL
plt.style.use('../PL/plot.mplstyle')
"""
This is for G1243 Zelle 1
dir_path = 'C:/Users/j.oberroehrmann/Documents/Messdaten/Ref Charge nach PL/G1243/overview/'
files = glob.glob(dir_path+'*.b32')
filenames = [item.split('\\')[1] for item in files]
# image 01 is the camera image
image_01 = dir_path + filenames[1]
# image 02 is the EL image of the PSC
image_02 = dir_path + filenames[0]
"""
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

image_01 = filedialog.askopenfilename()
image_02 = filedialog.askopenfilename()
# now same for G1331 Zelle 1
#dir_path = "C:/Users/j.oberroehrmann/Documents/Messdaten/Ref Charge nach PL/G1331/G1331_Z1/"
#image_01 = dir_path + "G1331_Z1_Cam.000-0.000 V-0.400 A-3x3.000 s-0.0000 A.EL.b32"
#image_02 = dir_path + "/01 votlage/G1331_Z1_02.009-1.600 V-0.400 A-1x6.000 s-0.0000 A.EL.b32"
# Camera Image
#P(x,y)
#P1 = (600,475)
#P2 = (670,545)
# cell overview
#P1 = (486, 456)
#P2 = (841, 801)
# for image with extender: x0 : x0+150. y0:y0+150
x0 = 740
y0 = 250
x0 = 273
y0 = 48
length = 600
P1 = (x0, y0)
P2 = (x0+length, y0+length)
EL_Image_01 = EL.EL_Image(image_01)
#EL_Image_01.show(show=True)
EL_Image_01.crop_ELImage(Point1=P1, Point2=P2)
#EL_Image_01.show(show=True)
EL_Image_01.show(colormap="gray", show=True)
# same for EL Image
EL_Image_02 = EL.EL_Image(image_02)
EL_Image_02.crop_ELImage(Point1=P1, Point2=P2)
EL_Image_02.show()

#EL.EL_Image.overlay_with_other(EL_Image_01, EL_Image_02)
#xl_0 = 80
#yl_0 = 50
#yl_1 = 180 - 30
#EL.EL_Image.EL_Linescan(EL_Image_02, EL_Image_01, xl_0, xl_0, yl_0, yl_1)






