import xml

import xml.etree.ElementTree as ET

file = "C:/Users/j.oberroehrmann/Documents/Messdaten/templates/Voltage_Sweep_ExpTimechange.lcseq"
tree = ET.parse(file)
root = tree.getroot()

#print(root[1])
for child in root[1]:
    print(child)