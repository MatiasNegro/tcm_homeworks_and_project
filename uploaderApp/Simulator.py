import xml.etree.ElementTree as ET
import random as ran
import string
import datetime
import names
import randomtimestamp
import country_code as cd
import copy

# Base xmls
start_xml = ET.fromstring("<ResultList></ResultList>")
person_result_xml = ET.fromstring("<PersonResult></PersonResult>")
class_result_xml = ET.fromstring("<ClassResult></ClassResult>")

# Files
event_base = ET.parse("xmls/Event.xml")
class_base = ET.parse("xmls/Class.xml")
course_base = ET.parse("xmls/Course.xml")
person_base = ET.parse("xmls/Person.xml")
organisation_base = ET.parse("xmls/Organisation.xml")
result_base = ET.parse("xmls/Result.xml")
split_time_base = ET.parse("xmls/SplitTime.xml")
control_card_base = ET.parse("xmls/ControlCard.xml")
route_base = ET.parse("xmls/Route.xml")
assigned_fee_base = ET.parse("xmls/AssignedFee.xml")
service_request_base = ET.parse("xmls/ServiceRequest.xml")


def date_sim():
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = ran.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return str(random_date)


def id_generator(size=ran.randint(5, 10), chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(ran.choice(chars) for _ in range(size))


def simulation(num):

    f_r_l = []

    for i in range(0, num):

        # Event generation
        event = copy.deepcopy(event_base)
        event.find("Name").text = id_generator()
        event.find("StartTime").find("Date").text = str(date_sim())[0:9]
        event.find("StartTime").find("Time").text = str(
            randomtimestamp.randomtimestamp())[10:]
        event.find("EndTime").find("Date").text = str(date_sim())[0:9]
        event.find("EndTime").find("Time").text = str(
            randomtimestamp.randomtimestamp())[10:]

        classes_list = []
        # Multiple class generation:
        for number in range(0, 5):
            # Class generation
            class_ev = copy.deepcopy(class_base)
            class_ev.find("Id").text = id_generator()
            class_ev.find("Name").text = id_generator()

            # Course generation
            course = copy.deepcopy(course_base)
            course.find("Id").text = id_generator()
            course.find("Name").text = id_generator()
            course.find("Length").text = str(ran.randint(0, 2000))
            course.find("Climb").text = str(ran.randint(0, 1000))

            course_first = copy.deepcopy(course_base)
            c_f_root = course_first.getroot()
            c_f_root.remove(course_first.find("Id"))
            c_f_root.remove(course_first.find("Name"))
            c_f_root.find("Length").text = copy.deepcopy(
                course.find("Length").text)
            c_f_root.find("Climb").text = copy.deepcopy(
                course.find("Climb").text)

            # PersonResult generation
            p_r_b = copy.deepcopy(person_result_xml)
            p_r_l = []
            for i in range(0, ran.randint(1, 5)):
                p_r = copy.deepcopy(p_r_b)

                person = copy.deepcopy(person_base)
                person.find("Id").text = id_generator()
                person.find("Name").find("Family").text = names.get_last_name()
                person.find("Name").find("Given").text = names.get_first_name()

                # Generating Organisation
                organisation = copy.deepcopy(organisation_base)
                organisation.find("Id").text = id_generator()
                organisation.find("Name").text = id_generator()
                organisation.find("Country").text = cd.get_country()[0]

                # Resut generation
                result = copy.deepcopy(result_base)
                result.find("BibNumber").text = str(ran.randint(0, 99))
                result.find("StartTime").text = event.find(
                    "StartTime").find("Date").text
                result.find("FinishTime").text = str(
                    randomtimestamp.randomtimestamp())[10:]
                result.find("Time").text = str(ran.randint(0, 100))
                result.find("TimeBehind").text = str(ran.randint(0, 100))
                result.find("Position").text = str(i)
                result.find("Status").text = "OK"

                # SplitTimes generation
                split_time_list = []
                for j in range(0, 5):
                    split = copy.deepcopy(split_time_base)
                    split.find("ControlCode").text = id_generator()
                    split.find("Time").text = str(
                        randomtimestamp.randomtimestamp())[10:]
                    split_time_list.append(split)

                # Route generation
                route = copy.deepcopy(route_base)
                route.getroot().text = id_generator()
                # ControlCard generation
                control_card = copy.deepcopy(control_card_base)
                control_card.getroot().text = str(ran.randint(10000, 100000))

                # AssignedFee generation
                assigned_fee = copy.deepcopy(assigned_fee_base)
                assigned_fee.find("Fee").find("Id").text = id_generator()
                assigned_fee.find("Fee").find("Name").text = id_generator()
                assigned_fee.find("Fee").find(
                    "Amount").text = str(ran.randint(10, 1000))
                assigned_fee.find("Fee").find(
                    "TaxableAmount").text = str(ran.randint(10, 100))

                # ServiceRequest generation
                service_request = copy.deepcopy(service_request_base)
                service_request.find("Service").find(
                    "Id").text = id_generator()
                service_request.find("Service").find(
                    "Name").text = id_generator()
                service_request.find("RequestedQuantity").text = str(
                    ran.randint(0, 10))
                service_request.find("AssignedFee").find(
                    "Fee").find("Id").text = id_generator()
                service_request.find("AssignedFee").find(
                    "Fee").find("Name").text = id_generator()
                service_request.find("AssignedFee").find("Fee").find(
                    "Amount").text = str(ran.randint(10, 100))

                p_r.append(person.getroot())
                p_r.append(organisation.getroot())
                result = result.getroot()
                result.append(course.getroot())

                for i in split_time_list:
                    result.append(i.getroot())

                result.append(route.getroot())
                test = ET.tostring(result)
                result.append(control_card.getroot())
                result.append(assigned_fee.getroot())
                result.append(service_request.getroot())
                test = ET.tostring(result)
                p_r.append(result)
                test = ET.tostring(p_r)
                p_r_l.append(p_r)

            c_r = copy.deepcopy(class_result_xml)
            c_r.append(class_ev.getroot())
            c_r.append(course_first.getroot())

            for i in p_r_l:
                c_r.append(i)

            classes_list.append(c_r)

        f_r = copy.deepcopy(start_xml)
        f_r.append(event.getroot())
        event.getroot()
        for cl in classes_list:
            f_r.append(cl)
        f_r_l.append(f_r)

    for i in f_r_l:
        el_tree = ET.ElementTree(i)
        name = el_tree.find("Event").find(
            "Name").text + el_tree.find("Event").find("StartTime").find("Date").text + '.xml'
        el_tree.write('Result_of_Simulation/' + name, encoding='utf-8')
