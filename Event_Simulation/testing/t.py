import xml.etree.ElementTree as ET

xml_f = ET.parse("Event_Simulation/xmls/Event.xml")

print(xml_f.find("StartTime").find("Date").text)