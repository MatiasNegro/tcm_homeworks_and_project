from operator import index
from typing import final
from bitarray import test
from sympy import dict_merge
import xmltodict
import json
import random as ran
import string
import names
import randomtimestamp
import country_code as code
import boto3
import boto3.dynamodb.types as d
from pprint import pprint


def listToDict(lst):
    if not isinstance (lst, list):
        op = {0: "nan"}
    else:
        op = { i : lst[i] for i in range(0, len(lst) ) }
    return op


def merge_dicts(*dict_args):
    """
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def date_sim():
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = ran.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return str(random_date)


def id_generator(size=ran.randint(5,10), chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(ran.choice(chars) for _ in range(size))

#Structure definition
structure = ['Event', {'ClassResoult': [
    'Class', 'Course_half', {'PersoneResult': [
        'Person', 'Organization', {'Result': ['Result_first_half', 'Course_full',
                                              'SplitTime', 'Route', 'ControlCard', 'AssignedFee', 'ServiceRequested']}
    ]}]}]

#Files
event_base = xmltodict.parse(open("xmls/Event.xml").read())
class_base = xmltodict.parse(open("xmls/Class.xml").read())
course_half = xmltodict.parse(open("xmls/Course.xml").read())
course_half = {**{'Length':course_half['Course']['Length']}, **{'Climb': course_half['Course']["Climb"]}}
#PersonResult
person_base = xmltodict.parse(open("xmls/Person.xml").read())
organisation_base = xmltodict.parse(open("xmls/Organisation.xml").read())
result_base = xmltodict.parse(open("xmls/Result_first.xml").read())
course_base = xmltodict.parse(open("xmls/Course.xml").read())
split_time_base = xmltodict.parse(open("xmls/SplitTime.xml").read())
route_base = xmltodict.parse(open("xmls/Route.xml").read())
control_card_base = xmltodict.parse(open("xmls/ControlCard.xml").read())
assigned_fee_base = xmltodict.parse(open("xmls/AssignedFee.xml").read())
service_requested_base = xmltodict.parse(open("xmls/ServiceRequest.xml").read())

#Simulation loop
final_dict = []
test1 = {}
for number in range(1,ran.randint(1,3)):

    #Event generation

    event = event_base
    event["Event"]["Name"] = id_generator()
    datetime = str(randomtimestamp.randomtimestamp())
    event["Event"]["StartTime"]["Date"] = datetime[0:9]
    event["Event"]["StartTime"]["Time"] = datetime[10:]
    event["Event"]["EndTime"]["Date"] = datetime[0:9]
    event["Event"]["EndTime"]["Time"] = str(randomtimestamp.randomtimestamp())[10:]

    #Course generation
    course_h = course_half
    course_h["Length"] = str(ran.randint(1,1500))
    course_h["Climb"] = str(ran.randint(1,1000))
    temp_dict_p = {}
    temp_dict_for_p = []
    temp_dict_for_c = []
    #ClassResult generation:
    for i in range(0,ran.randint(1,1)):
        #Class generation
        class_r = class_base
        class_r["Id"] = str(i)
        class_r["Name"] = id_generator()

        #Person result generation
        person_result_dict = {}
        #Person generation
        for j in range (0, ran.randint(1, 1)):
            
            #Person generation
            person = person_base
            person["Person"]["Id"] = str(j)
            person["Person"]["Name"]["Family"] = names.get_last_name
            person["Person"]["Name"]["Given"] = names.get_first_name

            #Organisation generation
            organisation = organisation_base
            organisation["Organisation"]["Id"] = str(ran.randint(1,100))
            organisation["Organisation"]["Name"] = id_generator()
            organisation["Organisation"]["Country"]["code"] = code.get_country()

            #Result generation
            result = result_base
            result["Result"]["BibNumber"] = str(ran.randint(0,1000))
            result["Result"]["StartTime"] = event["Event"]["StartTime"]["Date"]
            result["Result"]["FinishTime"] = str(randomtimestamp.randomtimestamp())[10:]
            result["Result"]["Time"] = str(ran.randint(10,100))
            result["Result"]["TimeBehind"] = str(ran.randint(10,100))
            result["Result"]["Position"] = str(j)
            result["Result"]["Status"] = 'OK'

            #Full course generatin
            course = course_base
            course["Course"]["Id"] = str(j)
            course["Course"]["Name"] = id_generator()
            course["Course"]["Length"] = course_h["Length"]
            course["Course"]["Climb"] = course_h["Climb"]

            #SplitTime generation
            split_times = {}
            for k in range(0,1):
                split_time = split_time_base
                split_time["SplitTime"]["ControlCode"] = str(ran.randint(0,100))
                split_time["SplitTime"]["Time"] = str(randomtimestamp.randomtimestamp())[10:]
                split_times = {**split_times, **split_time}
            
            #Route generation
            route = route_base
            route["Route"] = id_generator()
            control_card = control_card_base
            control_card["ControlCard"] = id_generator()

            #Assigned fee generation
            assigned_fee = assigned_fee_base
            assigned_fee["AssignedFee"]["Fee"]["Id"] = str(j)
            assigned_fee["AssignedFee"]["Fee"]["Name"] = id_generator()
            assigned_fee["AssignedFee"]["Amount"] = str(ran.randint(1,1000))
            assigned_fee["AssignedFee"]["TaxableAmount"] = str(ran.randint(1,1000))

            #ServiceRequest generation
            service_request = service_requested_base
            service_request["ServiceRequest"]["Service"]["Id"] = str(j)
            service_request["ServiceRequest"]["Service"]["Name"] = id_generator()
            service_request["ServiceRequest"]["AssignedFee"]["Fee"]["Id"] = assigned_fee["AssignedFee"]["Fee"]["Id"]
            service_request["ServiceRequest"]["AssignedFee"]["Fee"]["Name"] = assigned_fee["AssignedFee"]["Fee"]["Name"]
            service_request["ServiceRequest"]["AssignedFee"]["Amount"] = str(ran.randint(1,1000))
            
            p ={'PersonResult': {**result, **course, **split_times, **route, **assigned_fee, ** service_request}}
            temp_dict_for_p.append(p)
        
        dict = listToDict(temp_dict_for_p)
        temp_dict_for_c.append({'ClassResult' : {**class_r, **course_h , **dict}})
        

    dict_1 = listToDict(temp_dict_for_c)
    final_dict.append({'ResultList': {**event , **dict_1}})
    if number == 1:
        test1 = {'ResultList': {**event , **dict_1}}
    
    
print("INIZO")
print("----")
serializer = d.TypeSerializer()
test2 = serializer.serialize(test1)
deserializer = d.TypeDeserializer()
test2 = deserializer.deserialize(test2)
print(json.dumps(test2))
print("----")
print("FINE")
