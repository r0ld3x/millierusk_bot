import string
from urllib.request import urlopen
import json
import re
import os
import random
import names
from random_address import real_random_address



class RandUser():
    def __init__(self) -> None:
        self.site = 'https://randomuser.me/api/'
        self.nat = 'us'
        # f = open('datasets/addresses-us-all.json')
        # self.address_json = json.loads(f.read())
        # self.address = {}
        # for a in self.address_json['addresses']:
        #     if 'city' in a:
        #         self.address.update({a['postcode']: a})
          
    def rand_user(self, nat = None):
        x = real_random_address()
        return {
            'street': x['address1'],
            'city': x['city'],
            'state': x['state'],
            'zip': x['postalCode'],
            'name': self.full_name,
            'password': self.get_password,
            'email': self.get_email,
            'username': self.get_username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'name': self.full_name,
            'province': self.get_province(x['state']),
            'phone': self.get_phone
        }
    


    @property
    def full_name(self, gender: str = None):
        return names.get_full_name(gender)
    
    @property
    def first_name(self, gender: str = None):
        return names.get_first_name(gender)
    
    @property
    def last_name(self, gender: str = None):
        return names.get_last_name()

    @property
    def get_password(self, length = 8):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation
        all = lower + upper + num + symbols
        temp = random.sample(all,length)
        password = "".join(temp)
        return password
    
    @property
    def get_phone(self):
        first = str(random.randint(100, 999))
        second = str(random.randint(1, 888)).zfill(3)
        last = (str(random.randint(1, 9998)).zfill(4))
        while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
            last = (str(random.randint(1, 9998)).zfill(4))
        return '{}-{}-{}'.format(first, second, last)
    
    @property
    def get_email(self):
        return str(''.join(random.choices(string.ascii_lowercase + string.digits, k = 15))) + '@gmail.com'

    @property
    def get_random_string(self, length :int = str):
        return random.random_string(length)
    
    @property
    def get_random_integer(self, length :int = str):
        return random.random_integer(length)

    @property
    def get_username(self):
        return str(''.join(random.choices(string.ascii_lowercase + string.digits, k = 8)))
    
    def get_province(self, state_name):
        a= {
"AL": "Alabama",
"AK": "Alaska",
"AZ": "Arizona",
"AR": "Arkansas",
"CA": "California",
"CO": "Colorado",
"CT": "Connecticut",
"DE": "Delaware",
"DC": "District Of Columbia",
"FL": "Florida",
"GA": "Georgia",
"HI": "Hawaii",
"ID": "Idaho",
"IL": "Illinois",
"IN": "Indiana",
"IA": "Iowa",
"KS": "Kansas",
"KY": "Kentucky",
"LA": "Louisiana",
"ME": "Maine",
"MD": "Maryland",
"MA": "Massachusetts",
"MI": "Michigan",
"MN": "Minnesota",
"MS": "Mississippi",
"MO": "Missouri",
"MT": "Montana",
"NE": "Nebraska",
"NV": "Nevada",
"NH": "New Hampshire",
"NJ": "New Jersey",
"NM": "New Mexico",
"NY": "New York",
"NC": "North Carolina",
"ND": "North Dakota",
"OH": "Ohio",
"OK": "Oklahoma",
"OR": "Oregon",
"PA": "Pennsylvania",
"RI": "Rhode Island",
"SC": "South Carolina",
"SD": "South Dakota",
"TN": "Tennessee",
"TX": "Texas",
"UT": "Utah",
"VT": "Vermont",
"VA": "Virginia",
"WA": "Washington",
"WV": "West Virginia",
"WI": "Wisconsin",
"WY": "Wyoming"
}

        for key , val in a.items():
            if val == state_name.title():
                return key
            else:
                return state_name