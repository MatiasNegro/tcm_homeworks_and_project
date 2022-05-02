import xmltodict
import json
import math
from pprint import pprint

#Structure definition
structure = ['Event', {'ClassResoult': [
    'Class', 'Course_half', {'PersoneResult': [
        'Person', 'Organization', {'Result': ['Result_first_half', 'Course_full',
                                              'SplitTime', 'Route', 'ControlCard', 'AssignedFee', 'ServiceRequested']}
    ]}]}]

#Files
event_base = xmltodict.parse(open("Event_Simulation/xmls/Class.xml").read())
class_base = xmltodict.parse(open("Event_Simulation/xmls/Class.xml").read())
course_half = xmltodict.parse(open("Event_Simulation/xmls/Course.xml").read())
course_half = {**{'Length':course_half['Course']['Length']}, **{'Climb': course_half['Course']["Climb"]}}
print(course_half)
