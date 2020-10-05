from datetime import datetime


class Person:
    def __init__(self, f_name, l_name, date_of_birth, email, country, phone, address, cpr):
        self.FirstName = f_name
        self.LastName = l_name
        self.DateOfBirth = date_of_birth
        self.Email = email
        self.Country = country
        self.Phone = phone
        self.Address = address
        self.CprNumber = cpr

    def validate_date_of_birth(self):
        try:
            datetime.strptime(self.DateOfBirth, '%d-%m-%Y')
        except:
            raise ValueError("Incorrect data format...")

    def is_valid(self):
        if self.FirstName == "" or self.LastName == "" or self.Email == "" or self.Address == "" or self.Phone == "" or self.Country == "" or self.DateOfBirth == "":
            raise ValueError
        return True

    def __str__(self):
        return f"'FirstName': {self.FirstName}, 'LastName': {self.LastName}, 'DateOfBirth': {self.DateOfBirth}, 'Email': {self.Email}, 'Phone': {self.Phone}, 'Address': {self.Address}, 'Country': {self.Country},'CPR': {self.CprNumber}"
