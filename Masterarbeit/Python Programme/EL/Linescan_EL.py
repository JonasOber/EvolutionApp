"""
Do a linescan on an EL Image and show the linescan in the EL image and an extra plot.

Drag and drop: https://stackoverflow.com/questions/7878398/how-to-extract-an-arbitrary-line-of-values-from-a-numpy-array
"""
import glob
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable
#import scipy.ndimage
import tkinter as tk
from tkinter import filedialog
plt.rcParams['font.family'] = "Arial"
plt.rcParams['font.size'] = 14
#from scipy.ndimage.measurements import label

root = tk.Tk()
root.withdraw()

class Linescan():
    """
    creates an Object linescan which scans over a matrix and has begin and end (-points)
    """
    def __init__(self, coords, matrix, line_index):
        # coords are [(x0,x1), (y0, y1)]
        self.coords = coords
        # this is the matrix to do the linescan on
        self.mat = matrix
        self.do_linescan()
        self.index = line_index

    def do_linescan(self):
        # extract x and y, beginning and endpoints from coords
        xinterval, yinterval = self.coords
        x0, x1 = xinterval
        y0, y1 = yinterval

        # calculate linescan length
        num = int(np.hypot(x1-x0, y1-y0))
        # get xy pair values for matrix
        x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)
        
       # Extract the values along the line
       # mat[y, x]
        self.zi = self.mat[y.astype(int), x.astype(int)]

    def plot_linescan(self, ax):
        """
        Plot the linescan on a given axis.
        """
        y = np.arange(0, len(self.zi), 1)
        if self.index==2:
            linescan_label = "Kamera"
        elif self.index == 1:
            linescan_label = "EL"
        ax.step(y, self.zi, label=linescan_label, where='mid')
    def imshow_linescan(self, ax):
        xinterval, yinterval = self.coords
        x0, x1 = xinterval
        y0, y1 = yinterval
        text_color = "white"
        if self.index == 2:
            text_color="black"
        ax.plot([x0, x1], [y0, y1], 'k.-')
        ax.text(x0+2, y0-2, str(self.index), color=text_color)
        return ax

        
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

        # -- Prepare the figure
        fig = plt.figure(figsize=(3 * 11 / 2.54, 11 / 2.54))

        # axes for camera picture
        ax0 = fig.add_subplot(131)
        ax0.axis('equal')
        divider = make_axes_locatable(ax0)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        # imshow the matrix
        im = ax.imshow(self.mat, cmap='gray', origin='upper', vmin=0, vmax=4095)
        # plot the linescan on imshow
        line02.imshow_linescan(ax0)

        # ax.set_title(self.filename)
        ax0.set_xlabel("x (pixel)")
        ax0.set_ylabel("y (pixel)")
        # set y ticks
        ax0.set_yticks(EL_ticks)
        ax0.set_xticks(EL_ticks)
        # add the colorbar
        fig.colorbar(im, cax=cax, orientation='vertical', label='Counts')

        ax = fig.add_subplot(132)
        ax.axis('equal')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        # imshow the matrix
        im = ax.imshow(other.mat, cmap='jet', origin='upper', vmin=0, vmax=4095)
        # plot the linescan on imshow
        line01.imshow_linescan(ax)

        # ax.set_title(self.filename)
        ax.set_xlabel("x (pixel)")
        ax.set_ylabel("y (pixel)")
        # set y ticks
        EL_ticks = np.arange(0, 160, 40)
        ax.set_yticks(EL_ticks)
        ax.set_xticks(EL_ticks)
        # add the colorbar
        fig.colorbar(im, cax=cax, orientation='vertical', label='Counts')
        # add axes for the linescan: intensity(position) plot
        ax2 = fig.add_subplot(133)
        # plot the linescan intensity values along it's path
        im = ax2.imshow(self.mat, cmap='gray', origin='upper', vmin=0, vmax=4095)

        im = ax2.imshow(other.mat, cmap='jet', alpha=0.5, origin='upper', vmin=0, vmax=4095)
        # ax2.set_ylim(0, 3000)
        # square plot
        ax2.set_aspect(1.0 / ax2.get_data_ratio(), adjustable='box')
        # label
        ax2.set_ylabel("Intensität (counts)")
        ax2.set_xlabel("Koordinate y (Pixel)")
        # ticks on both sides of plot
        ax2.yaxis.set_ticks_position('both')
        ax2.xaxis.set_ticks_position('both')

        ax2.legend()
        plt.tight_layout()
        # save the figure

        plt.savefig(f'Pictures/Overlay.svg', transparent=True)
        plt.show()

    def EL_Linescan(self,other, x0, x1, y0, y1, colormap='jet'):
        """
        Enter start and end coordinates in pixel-coordinates. spacing is x0 to x1 and number(x,y) linescans in x
        """
        # set coordinates for our linescans
        coords = ((x0, x1), (y0, y1))
        
        line01 = Linescan(coords, self.mat, 1)
        line02 = Linescan(coords,other.mat, 2)
        
        #-- Prepare the figure
        fig = plt.figure(figsize=(3*11/2.54, 11/2.54))

        # axes for camera picture
        ax0 = fig.add_subplot(131)
        ax0.axis('equal')
        divider = make_axes_locatable(ax0)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        # imshow the matrix
        im = ax0.imshow(other.mat, cmap='gray', origin='upper', vmin=0, vmax=4095)
        # plot the linescan on imshow
        line02.imshow_linescan(ax0)
        
        #ax.set_title(self.filename)
        ax0.set_xlabel("x (pixel)")
        ax0.set_ylabel("y (pixel)")
        # set y ticks
        ax0.set_yticks(EL_ticks)
        ax0.set_xticks(EL_ticks)
        # add the colorbar
        fig.colorbar(im, cax=cax, orientation='vertical', label='Counts')

        ax = fig.add_subplot(132)
        ax.axis('equal')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        # imshow the matrix
        im = ax.imshow(self.mat, cmap=colormap, origin='upper', vmin=0, vmax=4095)
        # plot the linescan on imshow
        line01.imshow_linescan(ax)

        #ax.set_title(self.filename)
        ax.set_xlabel("x (pixel)")
        ax.set_ylabel("y (pixel)")
        # set y ticks
        EL_ticks = np.arange(0, 160, 40)
        ax.set_yticks(EL_ticks)
        ax.set_xticks(EL_ticks)
        # add the colorbar
        fig.colorbar(im, cax=cax, orientation='vertical', label='Counts')
        # add axes for the linescan: intensity(position) plot
        ax2 = fig.add_subplot(133)
        # plot the linescan intensity values along it's path
        line01.plot_linescan(ax2)
        line02.plot_linescan(ax2)
        #ax2.set_ylim(0, 3000)
        # square plot
        ax2.set_aspect(1.0/ax2.get_data_ratio(), adjustable='box')
        # label
        ax2.set_ylabel("Intensität (counts)")
        ax2.set_xlabel("Koordinate y (Pixel)")
        # ticks on both sides of plot
        ax2.yaxis.set_ticks_position('both')
        ax2.xaxis.set_ticks_position('both')
        
        ax2.legend()
        plt.tight_layout()
        # save the figure
        plt.savefig("Pictures/Linescan.svg", transparent='true')
        plt.show()

        




root = tk.Tk()
root.withdraw()
# pick first EL then camera
image_01 = filedialog.askopenfilename()

image_02 = filedialog.askopenfilename()
#P(x,y)
# Extender
#P1 = (520,400)
#P2 = (670,550)
# ohne Extender

P1 = (590,470)
P2 = (670,550)

EL_01 = EL_Image(image_01)
EL_01.crop_ELImage(Point1=P1, Point2=P2)
EL_02 = EL_Image(image_02)
EL_02.crop_ELImage(Point1=P1, Point2=P2)

#EL_01.EL_Linescan(EL_02, 110, 110, 40, 110)

EL_01.EL_Linescan(EL_02, 45, 45, 20, 70)
