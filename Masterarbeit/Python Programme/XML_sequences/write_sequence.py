from lxml import etree
tree = etree.parse("XML_ELParams.xml")
#ET.register_namespace((ns0, "http://www.ni.com/LVData"))
root = tree.getroot()
#namespaces = {'ns0': "http://www.ni.com/LVData"}
textsearch = root.iter('ns0:Name')
print(textsearch)
print(textsearch.tag)
for found in textsearch:
    print(found.items(), found.text)

