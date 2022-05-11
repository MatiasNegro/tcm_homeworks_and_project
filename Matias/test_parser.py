import copy
import xml.etree.ElementTree as ET

def class_result_parser(root): 
    '''
    Prende in ingresso una root del documento xml e restituisce le classi dentro un unico tag <ClassResults> per garantire la compatibilità con dynamodb ed evitare la sovrascrittura dei <ClassResult>
    '''
    class_results_base = ET.fromstring('<ClassResults></ClassResults>')
    result_list = ET.fromstring('<ResultList></ResultList>')
    c_r_s = copy.deepcopy(class_results_base)
    r_l = copy.deepcopy(result_list)
    event = copy.deepcopy(ET.ElementTree(root.find("Event"))).getroot()
    r_l.append(event)
    index : int = 0
    for i in root.findall("ClassResult"):
        i.tag = "ClassResult" + str(index)
        c_r_s.append(i)
    r_l.append(c_r_s)
    return r_l

class_result_parser(ET.parse('20227.xml').getroot())