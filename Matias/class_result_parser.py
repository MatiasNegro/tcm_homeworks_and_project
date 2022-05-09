import xml.etree.ElementTree as ET
import copy

def class_result_parser(xml_doc): 
    '''
    Prende in ingresso una root del documento xml e restituisce le classi dentro un unico tag <ClassResults> per garantire la compatibilità con dynamodb ed evitare la sovrascrittura dei <ClassResult>
    '''
    class_results_base = ET.fromstring('<ClassResults></ClassResults>')
    result_list = ET.fromstring('<ResultList></ResultList>')
    root = xml_doc.getroot()
    event = root.find("Event")
    c_r_s = copy.deepcopy(class_results_base) 
    result_list.append(event)
    for i in root.findall("ClassResult"):
        c_r_s.append(i)
    result_list.append(c_r_s)
    return result_list
