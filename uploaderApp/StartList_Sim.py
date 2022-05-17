from datetime import datetime
from lxml  import etree
import xml.etree.ElementTree as ET
import copy
import threading
import random as rand
#default variables

start_list_base = ET.fromstring('<StartList></StartList>')
start_list_base.set('xmlns', 'http://www.orienteering.org/datastandard/3.0')
start_list_base.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
start_list_base.set('iofVersion', '3.0')
start_list_base.set('createTime', str(datetime.now))
start_list_base.set('creator', 'SimulationSoftware')

start_classes_base = ET.fromstring('<StartClasses></StartClasses>')
start_class_base = ET.fromstring('<StartClass></StartClass>')
start_name_base = ET.fromstring('<StartName></StartName>')
person_start_base = ET.fromstring('<PersonStart></PersonStart>')
start_base = ET.fromstring('<Start></Start>')
class_start_base = ET.fromstring('<ClassStart></ClassStart>')

def format_validator(root):
    source_file = ET.tostring(root)
    schema_file = 'schema.xsd'
    schema_file_type = 'schema_type.xsd'
    flag = True
    flag_type = True

    with open(schema_file) as f_schema, open(schema_file_type) as f_schema_type:

        schema_doc = etree.parse(f_schema)
        schema_type_doc = etree.parse(f_schema_type)
        schema = etree.XMLSchema(schema_doc)
        schema_type = etree.XMLSchema(schema_type_doc)
        parser = etree.XMLParser(schema=schema)
        parser_type = etree.XMLParser(schema = schema_type)

        try:
            doc = etree.fromstring(source_file, parser)
        except etree.XMLSyntaxError as e:
            # this exception is thrown on schema validation error
            # print(e) è solo per eventuale debugging
            #print("PARSER")
            #print(e)
            flag = False
        
        try:
            doc = etree.fromstring(source_file, parser_type)
        except etree.XMLSyntaxError as e:
            #print("PARSER_TYPE")
            #print(e)
            flag_type = False

    return (flag or flag_type)


def start_list_sim(root):
    my_thread = threading.Thread(target= start_list_parsed(root))
    start_list = copy.deepcopy(start_list_base)
    event = root.find("Event")
    start_list.append(event)
    
    to_iter_class = root.findall("ClassResult")
    index :int = 0

    for c_start in to_iter_class:
        new_class_start = copy.deepcopy(class_start_base)

        new_class = c_start.find("Class")
        new_class_start.append(new_class)

        new_course = c_start.find("Course")
        new_class_start.append(new_course)

        new_start_name = copy.deepcopy(start_name_base)
        new_start_name.text = 'StartName' + str(index)
        new_class_start.append(new_start_name)

        to_iter_person = c_start.findall("PersonResult")

        for p_start in to_iter_person:
            new_start_person = copy.deepcopy(person_start_base)
            new_start_person.append(ET.fromstring('<EntryId>' + str(rand.randint(1000,9999)) + '</EntryId>'))
            new_person = p_start.find("Person")
            new_start_person.append(new_person)
            new_organisation = p_start.find("Organisation")
            new_start_person.append(new_organisation)
            new_start = copy.deepcopy(start_base)
            new_start.append(p_start.find("Result").find("BibNumber"))
            new_start.append(p_start.find("Result").find("StartTime"))
            new_start.append(p_start.find("Result").find("ControlCard"))
            new_start_person.append(new_start)
            new_class_start.append(new_start_person)

        index += 1
        start_list.append(new_class_start)
    
    ET.ElementTree(start_list).write('Result_of_Simulation/start_list_unparsed/' + start_list.find("Event").find("Name").text + start_list.find("Event").find("StartTime").find("Date").text + 'StartList.xml')
    index = 0
    #print("UNPARSED: " + str(format_validator(start_list)))
    pass

def start_list_parsed(root):
    #defining bases
    start_list = copy.deepcopy(start_list_base)
    event = root.find("Event")
    start_list.append(event)

    classes_list = copy.deepcopy(start_classes_base)
    
    to_iter_class = root.findall("ClassResult")
    index :int = 0

    for c_start in to_iter_class:
        new_class_start = copy.deepcopy(class_start_base)
        new_class_start.tag = 'ClassStart' + str(index)

        new_class = c_start.find("Class")
        new_class_start.append(new_class)

        new_course = c_start.find("Course")
        new_class_start.append(new_course)

        new_start_name = copy.deepcopy(start_name_base)
        new_start_name.text = 'StartName' + str(index)
        new_class_start.append(new_start_name)

        to_iter_person = c_start.findall("PersonResult")

        for p_start in to_iter_person:
            new_start_person = copy.deepcopy(person_start_base)
            new_start_person.append(ET.fromstring('<EntryId>' + str(rand.randint(1000,9999)) + '</EntryId>'))
            new_person = p_start.find("Person")
            new_start_person.append(new_person)
            new_organisation = p_start.find("Organisation")
            new_start_person.append(new_organisation)
            new_start = copy.deepcopy(start_base)
            new_start.append(p_start.find("Result").find("BibNumber"))
            new_start.append(p_start.find("Result").find("StartTime"))
            new_start.append(p_start.find("Result").find("ControlCard"))
            new_start_person.append(new_start)
            new_class_start.append(new_start_person)

        index += 1
        classes_list.append(new_class_start)
    start_list.append(classes_list)
    ET.ElementTree(start_list).write('Result_of_Simulation/start_list_parsed/' + start_list.find("Event").find("Name").text + start_list.find("Event").find("StartTime").find("Date").text + 'StartList.xml')
    index = 0
    pass
