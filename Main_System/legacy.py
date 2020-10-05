import csv
from person import Person
import random
import xml.etree.ElementTree as ET
import requests


people = []
url = 'http://localhost:8080/nemID'
root = ET.Element('root')


def generate_cpr(date_of_birth):
    date = date_of_birth.split('-')
    random_4_digits = random.randint(1000, 9999)
    return ''.join(date) + str(random_4_digits)


def add_people(f_name, l_name, date_of_birth, email, country, phone, address):
    cpr = generate_cpr(date_of_birth)
    p = Person(f_name, l_name, date_of_birth,
               email, country, phone, address, cpr)
    p.is_valid()
    # create the file structure
    person_obj = ET.Element('Person')
    first_name = ET.SubElement(person_obj, 'FirstName')
    last_name = ET.SubElement(person_obj, 'LastName')
    cpr_number = ET.SubElement(person_obj, 'CprNumber')
    email_ = ET.SubElement(person_obj, 'Email')

    first_name.text = p.FirstName
    last_name.text = p.LastName
    cpr_number.text = p.CprNumber
    email_.text = p.Email
    root.append(person_obj)
    people.append(p)


with open('people.csv', newline='') as csvfile:
    peopleReader = csv.DictReader(csvfile)
    for row in peopleReader:
        add_people(row['FirstName'], row['LastName'], row['DateOfBirth'],
                   row['Email'], row['Phone'], row['Address'], row['Country'])

tree = ET.ElementTree(root)
tree.write('data.xml')


def postnemid():
    tree = ET.parse('data.xml')
    root = tree.getroot()
    ps = root.findall('Person')
    headers = {'Content-Type': 'application/xml'}
    x = requests.post(url, data=ps[0], headers=headers)
    print(x)


postnemid()
