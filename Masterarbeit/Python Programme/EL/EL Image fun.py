# libraries
import glob
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable

# file path
dir_path = 'C:/Users/j.oberroehrmann/Documents/Messdaten/Ref Charge nach PL/G1243/overview/'
files = glob.glob(dir_path+'*.b32')
filenames = [item.split('\\')[1] for item in files]
print(filenames)
#file_name = "G1243_Z3_03.004-1.600 V-0.400 A-1x0.010 s-0.0000 A.EL"
index = 5
file_path = dir_path + filenames[index]
#for file_path in glob.iglob(dir_path+'*.b32'):
file_name = filenames[index]
with open(file_path, 'rb') as file:
    bytes = file.read()
byte_array = [bytearray(bytes[i:i+4]) for i in range(0,len(bytes),4)]
# struct does bytes to float with small endiaan <f and big endian >f
floats = np.array([struct.unpack('>f', item) for item in byte_array])

#split the array into our image matrix
mat = np.array_split(floats, 1376)
# Transpose the matrix
mat, = np.transpose(mat)

# take smaller matrix with just the cell [y + dy, x + dx] 614,516 - 658,463
mat_small = mat[445:510, 591:640]
print("matrix if of", len(mat), "x", len(mat[0]))
fig = plt.figure()
ax = fig.add_subplot(111)
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.05)
im = ax.imshow(mat_small, cmap='jet', origin='lower', vmin=0, vmax=4095)
# cmap jet
# add the mark for the cell
# Rectangle(xy, width, height, angle=0.0, **kwargs)
rect = patches.Rectangle((3, 6), 40, 53, linewidth=2, edgecolor='grey', facecolor='none')
# Add the patch to the Axes
ax.add_patch(rect)

ax.set_title(file_name)
ax.set_xlabel("x (pixel)")
ax.set_ylabel("y (pixel)")
#plt.xlim(500, 750)
#plt.ylim(500, 650)
#plt.savefig(file_path.strip('.b32')+'.png')
fig.colorbar(im, cax=cax, orientation='vertical')
plt.savefig('nicepic.svg', transparent=True)
mat_mean = np.mean(mat_small)
print("mean of solar image:", mat_mean)
print("std dev of solar image:", np.std(mat_small))
print("sum over solar image:", np.sum(mat_small))
"""
Can we extract a line plot?
"""
"""
For further image processing we have different libraries: scipy, 
"""
#from scipy import misc
#import imageio
#image = ndimage.median_filter(mat_small)
#plt.figure()
#plt.imshow(image)
#plt.show()

"""
I can add a new button then do coordinates and plot the line: https://matplotlib.org/stable/gallery/widgets/buttons.html
"""
