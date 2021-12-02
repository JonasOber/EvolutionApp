"""
Here we look at animating a series of EL images. These Images should be in the same directory.
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
import matplotlib.animation as animation
plt.rcParams['animation.ffmpeg_path'] = 'C:/Program Files/ffmpeg-n4.4.1-2-gcc33e73618-win64-gpl-4.4/bin/ffmpeg'
class Rectangle():
    def __init__(self, coords):
        xinterval, yinterval = self.coords
        self.x0, self.x1 = xinterval
        self.y0, self.y1 = yinterval

    def Rectangle_mean(self, Matrix):
        self.Mean = np.mean(Matrix[self.y0:self.y1][self.x0, self.x1])
        return Mean

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

class EL_Animation(EL_Image):
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.files = self.load_ELfiles()

    def load_ELfiles(self):
        """
        Loads the EL file names for the given directory. These are later used for the animation
        :return:
        """
        files = []
        for file in glob.iglob(self.directory_path + '/*.b32'):
            files.append(file)
        return files
    def return_filename(self, index):
        return self.files[i]
    def print_filenames(self):
        for file in self.files:
            print(file)

    @property
    def run_animation(self):
        # First set up the figure, the axis, and the plot element we want to animate

        fig = plt.figure()
        ax = plt.axes()
        # line, = ax.plot([], [], lw=2)
        a = np.zeros((80, 80))
        im = plt.imshow(a, interpolation='none')
        EL_matrices = []
        #Exposure_Times = []
        for file_index in range(len(self.files)):
            path = self.files[file_index]
            print("now at file index:", file_index)
            super().__init__(path)
            #print(float(self.filename.split('x')[-1].split('s')[0]))
            #Exposure_Time = float(self.filename.split('x')[-1].split('s')[0])
            # crop the EL image
            # P(x,y)
            P1 = (600, 475)
            P2 = (670, 545)
            self.crop_ELImage(Point1=P1, Point2=P2)
            EL_matrices.append(self.mat)#/Exposure_Time)
            #
        fps = 8
        nSeconds = 12.5

        # First set up the figure, the axis, and the plot element we want to animate
        ax.set_ylabel('y (pixels)')
        ax.set_xlabel('x (pixels)')
        Exposure_Time = float(self.filename.split('x')[-1].split('s')[0])
        print(Exposure_Time)
        a = EL_matrices[0]#/self.filename.split('x')

        im = plt.imshow(a, interpolation='none', aspect='auto', cmap='jet', vmin=1, vmax=4095)
        #im = plt.imshow(a, interpolation='none', aspect='auto', cmap='jet', norm=colors.LogNorm(vmin=1, vmax=1000))
        cbar = plt.colorbar(im)
        cbar.ax.set_ylabel('Counts')
       # time_template = 'Time = %.1fs'
       # time_text = plt.text(6, 6, '', transform=ax.transAxes, color='yellow')

        def animate_func(i):
            if i % fps == 0:
                print('.', end='')

            print("index i:", i)
            im.set_array(EL_matrices[i])
            ax.set_title(f"{i} s")
            return [im]

        anim = animation.FuncAnimation(
            fig,
            animate_func,
            frames=len(self.files),
            interval=1000 / fps,  # in ms
        )

        FFwriter = animation.FFMpegWriter(fps=fps, extra_args=['-vcodec', 'libx264'])
        anim.save('Pictures/EL_animation.mp4', writer=FFwriter)

        print('Done!')
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

image_01 = filedialog.askopenfilename()
animation_path = "/".join(image_01.split('/')[:-1])+"/"

#animation_path = 'C:/Users/j.oberroehrmann/Documents/Messdaten/Chargen/Referenzzellen/G1331/G1331_Z3/2021_11_09/02/'
Animation = EL_Animation(animation_path)
Animation.run_animation