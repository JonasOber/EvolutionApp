"""
EL files are b32 files. We try to open it and then see what we can do.
Image information:
Image format:	float-4-byte
Image data start:	0
Width:	1376	[px]
Height:	1024	[px]
Rotation:	0	[Degrees]
Endianness:	big
Transposed:	True
"""

# libraries
import glob
import struct
import numpy as np
import matplotlib.pyplot as plt
# file path
dir_path = 'C:/Users/j.oberroehrmann/Documents/Messdaten/P3T_015_Temperaturkontrolle_Koverdampfung/EL/P3T_015_Versuch 2_hohe U/'
file_name = "G718-2_oM_.009-0.900 V-0.400 A-1x1.000 s-0.0 A.EL"
file_path = dir_path + file_name + '.b32'
#for file_path in glob.iglob(dir_path+'*.b32'):

with open(file_path, 'rb') as file:
    bytes = file.read()
byte_array = [bytearray(bytes[i:i+4]) for i in range(0,len(bytes),4)]
# struct does bytes to float with small endiaan <f and big endian >f
floats = np.array([struct.unpack('>f', item) for item in byte_array])

mat = np.array_split(floats, 1376)
# Transpose the matrix
mat, = np.transpose(mat)
print("matrix if of", len(mat), "x", len(mat[0]))
plt.figure(figsize=(6,5), dpi=200)
plt.imshow(mat)

plt.suptitle(file_name, fontsize=8 )
plt.colorbar()
#plt.xlim(500, 750)
#plt.ylim(500, 650)
#plt.savefig(file_path.strip('.b32')+'.png')
plt.show()
#plt.close()

#print(struct.unpack('<f', bytes))
