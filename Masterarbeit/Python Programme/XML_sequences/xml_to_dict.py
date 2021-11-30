#import xmltodict
#import xml.etree.ElementTree as ET
#tree = ET.parse("C:/Users/j.oberroehrmann/Documents/Messdaten/templates/Voltage_Sweep_ExpTimechange.lcseq")
#root = tree.getroot()
#file = "C:/Users/j.oberroehrmann/Documents/Messdaten/templates/Voltage_Sweep_ExpTimechange.lcseq"
#xmljson = xmltodict.parse(str(root))

import xml.etree.ElementTree as ET
import xmltodict
import json


tree = ET.parse('C:/Users/j.oberroehrmann/Documents/Messdaten/templates/Voltage_Sweep_ExpTimechange.lcseq')
xml_data = tree.getroot()
#here you can change the encoding type to be able to set it to the one you need
xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')

data_dict = dict(xmltodict.parse(xmlstr))
#for item in data_dict["ns0:LVData"]["ns0:Cluster"]:
    #print(item)

print(data_dict["ns0:LVData"]["ns0:Cluster"]["ns0:Array"][0]["ns0:Name"])
ELPL_Params = data_dict["ns0:LVData"]["ns0:Cluster"]["ns0:Array"][0]["ns0:Cluster"][0]
print(ELPL_Params)
# now all i need to do is add the ELPL_Params to my xml file