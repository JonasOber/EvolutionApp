
import xml.etree.ElementTree as ET

tree = ET.parse("C:/Users/j.oberroehrmann/Documents/Messdaten/templates/Voltage_Sweep_ExpTimechange.lcseq")
root = tree.getroot()

xmlstr = ET.tostring(root, encoding='unicode', method='xml')

print(xmlstr)

str_header = """
<ns0:LVData xmlns:ns0="http://www.ni.com/LVData">
<ns0:Version>14.0f1</ns0:Version>
<ns0:Cluster>
<ns0:Name />
<ns0:NumElts>3</ns0:NumElts>
<ns0:String>
<ns0:Name>pattern label</ns0:Name>
<ns0:Val>LCGET3SEQ_V1</ns0:Val>
</ns0:String>
"""

