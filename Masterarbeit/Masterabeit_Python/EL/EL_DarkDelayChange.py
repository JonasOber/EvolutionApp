
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

    def crop_ELImage(self, Point1=(610,460), Point2=(670, 530)):
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
        im = ax.imshow(self.mat, cmap='Greys', origin='upper', vmin=0, vmax=4095)

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

    def mean(self):
        return np.mean(self.mat)
    def stddev(self):
        return np.std(self.mat)

measurement_counter = 1
plt.figure()
for measurement_counter in range(1,6):
    path = "C:/Users/j.oberroehrmann/Documents/Messdaten/2021_11_05/Ref_Charge/G1331/Zelle 02/dark_delay_check/with subtract dark/"
    files = []
    for file in glob.iglob(path+f"G1331_Z2_0{measurement_counter}.*.EL.b32"):
        files.append(file.split("\\")[-1])

    Dark_Delays = []
    Average_Signal = []
    Settings = {}
    for j in range(len(files)):
        path_setup = path + files[j].strip(".EL.b32") + '.ELPL'
        with open(path_setup) as setupdata:
            Lines  = setupdata.readlines()
        for lineindex in range(len(Lines)):
            if Lines[lineindex].strip() == '[Settings]':
                lineindex += 1
                while Lines[lineindex]!="\n":
                    line = Lines[lineindex].strip()
                    setting = line.split("\t")[0]
                    try:
                        val = float(line.split("\t")[1])
                    except ValueError:
                        val = bool(line.split("\t")[1])
                    setting = setting.strip(":")
                    Settings[setting] = val
                    lineindex += 1
            else:
                pass
        Dark_Delays.append(Settings["Dark Delay"])
        EL_Measurement = EL_Image(path+files[j])
        P1 = (600, 455)
        P2 = (680, 560)
        EL_Measurement.crop_ELImage(Point1=P1, Point2=P2)
        Average_Signal.append(EL_Measurement.mean())
    print(Dark_Delays)
    print(Average_Signal)
    Delta_Signal = []
    for i in range(1,len(Average_Signal)):
        Delta_Signal.append(Average_Signal[i]- Average_Signal[i-1])
    print(Delta_Signal)
    plt.plot(Dark_Delays[:-1], Delta_Signal, linestyle='None', marker='.', markersize=8, label=f"{measurement_counter}")
plt.xlabel("Dark Delay Time (s)")
plt.ylabel("Difference to measurement before (counts)")
plt.legend()
plt.show()