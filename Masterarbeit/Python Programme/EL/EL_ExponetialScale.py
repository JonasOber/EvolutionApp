"""
Show an EL image with an exponential scale

"""
import glob
import struct

import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors
import matplotlib.cbook as cbook
from mpl_toolkits.axes_grid1 import make_axes_locatable

class EL_Image():
    def __init__(self, path):
        #self.file_path = path
        self.EL_mat = self.read_file(path)
        self.filename = path.split('/')[-1]
    def read_file(self, path):
        """
        Takes the file path for the EL .b32 file and reads this to an array.

        :return:
        """
        with open(path, 'rb') as file:
            bytes = file.read()

        byte_array = [bytearray(bytes[i:i + 4]) for i in range(0, len(bytes), 4)]
        # struct does bytes to float with small endiaan <f and big endian >f
        floats = np.array([struct.unpack('>f', item) for item in byte_array])

        # split the array into our image matrix
        mat = np.array_split(floats, 1376)
        # Transpose the matrix
        self.mat, = np.transpose(mat)

    def crop_ELImage(self, Point1=(0,0), Point2=(0, 0)):
        #Point1 = (610, 460), Point2 = (670, 530)
        """
        Crop EL Image to the wanted format.
        :return:
        """
        x1, y1 = Point1#input("Gib x,y ein (0-1000):").split(',')
        x2, y2 = Point2#input("Gib x,y ein (0-1000):").split(',')
        self.mat = self.mat[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]

    def show(self, colormap='jet', show=False, my_scale='Norm'):
        """
        show the el picture as matplotlib.
        :return:
        """
        fig, ax = plt.subplots(1,1)
        if my_scale=='Norm':
            pcm = ax.imshow(self.mat, cmap='jet')
            ax.set_title('Lineare Skalierung')
        elif my_scale=='LogNorm':
            ax.set_title('Logarithmische Skalierung')
            pcm = ax.imshow(self.mat, norm=colors.LogNorm(vmin=1, vmax=4095), cmap='jet')
        cbar = plt.colorbar(pcm)
        cbar.ax.set_ylabel('Counts')
        # add the mark for the cell
        # Rectangle(xy, width, height, angle=0.0, **kwargs)
        #rect = patches.Rectangle((3, 6), 40, 53, linewidth=2, edgecolor='grey', facecolor='none')
        # Add the patch to the Axes
        #ax.add_patch(rect)

        ax.set_xlabel("x (pixel)")
        ax.set_ylabel("y (pixel)")
        plt.savefig(f'Pictures/EL_{self.filename.split(".")[0]}_scale_{my_scale}.svg', transparent=True)
        if show:
            plt.show()

    def overlay_with_other(self, other):
        """
        overlays two identical images
        :param other:
        :return:
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        im = ax.imshow(self.mat, cmap='gray', origin='upper', vmin=0, vmax=4095)

        im = ax.imshow(other.mat, cmap='jet', alpha=0.5, origin='upper', vmin=0, vmax=4095)
        # cmap jet
        # add the mark for the cell
        # Rectangle(xy, width, height, angle=0.0, **kwargs)
        # rect = patches.Rectangle((3, 6), 40, 53, linewidth=2, edgecolor='grey', facecolor='none')
        # Add the patch to the Axes
        # ax.add_patch(rect)
        ax.set_title(other.filename)
        ax.set_xlabel("x (pixel)")
        ax.set_ylabel("y (pixel)")
        # plt.xlim(500, 750)
        # plt.ylim(500, 650)
        # plt.savefig(file_path.strip('.b32')+'.png')
        fig.colorbar(im, cax=cax, orientation='vertical')
        plt.savefig(f'Pictures/Overlay.svg', transparent=True)
        plt.show()

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

image_01 = filedialog.askopenfilename()
# both 80 pixels wide
#P(x,y)
P1 = (645,515)
P2 = (725,605)
EL_Image_01 = EL_Image(image_01)
EL_Image_01.crop_ELImage(Point1=P1, Point2=P2)
EL_Image_01.show(show=True)
EL_Image_01.show(show=True, my_scale='LogNorm')