"""
Overlay an EL Image with the taken Camera image. Example is G1243 Zelle 01.
"""
import glob
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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

    def show(self, colormap='jet', show=False):
        """
        show the el picture as matplotlib.
        :return:
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        im = ax.imshow(self.mat, cmap=colormap, origin='upper', vmin=0, vmax=4095)
        # cmap jet
        # add the mark for the cell
        # Rectangle(xy, width, height, angle=0.0, **kwargs)
        #rect = patches.Rectangle((3, 6), 40, 53, linewidth=2, edgecolor='grey', facecolor='none')
        # Add the patch to the Axes
        #ax.add_patch(rect)
        ax.set_title(self.filename)
        ax.set_xlabel("x (pixel)")
        ax.set_ylabel("y (pixel)")
        # plt.xlim(500, 750)
        # plt.ylim(500, 650)
        # plt.savefig(file_path.strip('.b32')+'.png')
        fig.colorbar(im, cax=cax, orientation='vertical')
        plt.savefig(f'Pictures/EL_{self.filename.split(".")[0]}.svg', transparent=True)
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
P1 = (610,465)
P2 = (680,545)
EL_Image_01 = EL_Image(image_01)
#EL_Image_01.show(show=True)
EL_Image_01.crop_ELImage(Point1=P1, Point2=P2)
#EL_Image_01.show(show=True)
EL_Image_01.show(colormap="gray", show=True)
# same for EL Image
EL_Image_02 = EL_Image(image_02)
EL_Image_02.crop_ELImage(Point1=P1, Point2=P2)
EL_Image_02.show()

EL_Image.overlay_with_other(EL_Image_01, EL_Image_02)






