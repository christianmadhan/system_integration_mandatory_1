import csv
from person import Person
import random
import xml.etree.ElementTree as ET
import requests
import msgpack


URL = 'http://localhost:8080/nemID'
ROOT = ET.Element('root')
HEADERS = {'Content-Type': 'application/xml'}

# Will generate CPR number based on date of birth. 
# Returns one combined number (CPR) made from birth day, birth month, last two numbers of the birth year and 4 random digits
def generate_cpr(date_of_birth):
    date = date_of_birth.split('-')
    random_4_digits = random.randint(1000, 9999)
    cpr_number = date[0] + date[1] + date[-1][-2:]
    return ''.join(cpr_number) + str(random_4_digits)



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

    ROOT.append(person_obj)

    ### Storing data as msgpack ###
    data = {
        "FirstName": p.FirstName,
        "LastName": p.LastName,
        "CprNumber": p.CprNumber,
        "Email": p.Email
    }

    with open("data.msgpack", "wb") as outfile:
        packed = msgpack.packb(data)
        outfile.write(packed)


# convert each person from CSV file into XML structure
with open('people.csv', newline='') as csvfile:
    peopleReader = csv.DictReader(csvfile)
    for row in peopleReader:
        add_people(row['FirstName'], row['LastName'], row['DateOfBirth'],
                   row['Email'], row['Phone'], row['Address'], row['Country'])

# send a post request with XML data to the specified URL
x = requests.post(url=URL, data=ET.tostring(ROOT[0]), headers=HEADERS)
print(x)
