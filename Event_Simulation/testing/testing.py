from unicodedata import name
import xml.etree.ElementTree as ET
import xml.etree as xe
from pprint import pprint
import json
import random as ran
import string
import datetime
import names
import randomtimestamp
from sqlalchemy import null
import country_code as cd

#Base xmls
start_xml = ET.fromstring("<ResultList></ResultList>")
person_result_xml = ET.fromstring("<PersonResult></PersonResult>")
class_result_xml = ET.fromstring("<ClassResult></ClassResult>")

#Files
event_base = ET.parse("Event_Simulation/xmls/Event.xml")
class_base = ET.parse("Event_Simulation/xmls/Class.xml")
course_base = ET.parse("Event_Simulation/xmls/Course.xml")
person_base = ET.parse("Event_Simulation/xmls/Person.xml")
organisation_base = ET.parse("Event_Simulation/xmls/Organisation.xml")
result_base = ET.parse("Event_Simulation/xmls/Result.xml")
split_time_base = ET.parse("Event_Simulation/xmls/SplitTime.xml")
control_card_base = ET.parse("Event_Simulation/xmls/ControlCard.xml")
route_base = ET.parse("Event_Simulation/xmls/Route.xml")
assigned_fee_base = ET.parse("Event_Simulation/xmls/AssignedFee.xml")
service_request_base = ET.parse("Event_Simulation/xmls/ServiceRequest.xml")

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


def main():
    
    num_events = input("Number of events to simulate: ")
    num_events = int(num_events)
    f_r_l = []

    for i in range(0,num_events):
        
        #Event generation
        event = event_base
        event.find("Name").text = id_generator()
        event.find("StartTime").find("Date").text = str(date_sim())[0:9]
        event.find("StartTime").find("Time").text = str(date_sim())[10:]
        event.find("EndTime").find("Date").text = str(date_sim())[0:9]
        event.find("EndTime").find("Time").text = str(date_sim())[10:]

        #Class generation
        class_ev = class_base
        class_ev.find("Id").text = id_generator()
        class_ev.find("Name").text = id_generator()
        
        #Course generation
        course = course_base
        course.find("Id").text = id_generator()
        course.find("Name").text = id_generator()
        course.find("Length").text = str(ran.randint(0,2000))
        course.find("Climb").text = str(ran.randint(0,1000))

        course_first = course
        c_f_root = course_first.getroot()
        c_f_root.remove(course_first.find("Id"))
        c_f_root.remove(course_first.find("Name"))

        #PersonResult generation
        p_r_b = person_result_xml
        p_r_l = []
        for i in range(0,ran.randint(1,5)):
            p_r = p_r_b

            person = person_base
            person.find("Id").text = id_generator()
            person.find("Name").find("Family").text = names.get_last_name()
            person.find("Name").find("Given").text = names.get_first_name()

            #Generating Organisation
            organisation = organisation_base
            organisation.find("Id").text = id_generator()
            organisation.find("Name").text = id_generator()
            organisation.find("Country").text = cd.get_country()[0]

            #Resut generation
            result = result_base
            result.find("BibNumber").text = str(ran.randint(0,99))
            result.find("StartTime").text = event.find("StartTime").find("Date").text
            result.find("FinishTime").text = str(date_sim())[10:]
            result.find("Time").text = str(ran.randint(0,100))
            result.find("TimeBehind").text = str(ran.randint(0,100))
            result.find("Position").text = str(i)
            result.find("Status").text = "OK"

            #SplitTimes generation
            split_time_list = []
            for j in range(1,5):
                split = split_time_base
                split.find("ControlCode").text = id_generator()
                split.find("Time").text = str(date_sim())[10:]
                split_time_list.append(split)

            #Route generation
            route = route_base
            route.text = id_generator()
            #ControlCard generation
            control_card = control_card_base
            control_card.text = str(ran.randint(10000,100000))

            #AssignedFee generation
            assigned_fee = assigned_fee_base
            assigned_fee.find("Fee").find("Id").text = id_generator()
            assigned_fee.find("Fee").find("Name").text = id_generator()
            assigned_fee.find("Fee").find("Amount").text = str(ran.randint(10,1000))
            assigned_fee.find("Fee").find("TaxableAmount").text = str(ran.randint(10,100))

            #ServiceRequest generation
            service_request = service_request_base
            service_request.find("Service").find("Id").text = id_generator()
            service_request.find("Service").find("Name").text = id_generator()
            service_request.find("RequestedQuantity").text = str(ran.randint(0,10))
            service_request.find("AssignedFee").find("Fee").find("Id").text = id_generator()
            service_request.find("AssignedFee").find("Fee").find("Name").text = id_generator()
            service_request.find("AssignedFee").find("Fee").find("Amount").text = str(ran.randint(10,100))

            
            p_r.insert(organisation)
            p_r.insert(result)
            p_r.insert(course)
            for i in split_time_list:
                p_r.insert(i)
            p_r.append(route)
            p_r.append(control_card)
            p_r.append(assigned_fee)
            p_r.append(service_request)
            p_r_l.append(p_r)
        
        c_r = class_result_xml
        c_r.append(class_ev)
        c_r.append(course_first)
        for i in p_r_l:
            c_r.append(i)
        f_r = start_xml
        f_r.append(event)
        f_r.append(c_r)
        f_r_l.append(f_r)

    print(f_r_l[0])
        

main()