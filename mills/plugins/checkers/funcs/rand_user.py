from urllib.request import urlopen
import json
import string
import random




class random_user_api(object):
    """
    This is for the random user api genrator
    author: Roldex
    date: 12 DEC 2021
    """
    
    arr = ['AU', 'BR', 'CA', 'CH', 'DE', 'DK', 'ES', 'FI', 'FR', 'GB', 'IE', 'IR', 'NO', 'NL', 'NZ', 'TR', 'US']
    
    def __init__(self, country_code = None, *args):
        super(random_user_api, self).__init__(*args)
        characters = list(string.ascii_letters + string.digits + "!@#$%&*()")
        self.password = str(''.join(random.choices(characters, k = 10)))
        self.email = str(''.join(random.choices(string.ascii_lowercase + string.digits, k = 15))) + '@gmail.com'
        # self.password = random.choice(string.ascii_letters + string.digits + "!@#$%^&*()", k=15)
        if country_code is not None:
            if country_code.upper() in self.arr:
                self.nat = country_code
            else:
                self.nat = 'US'
        else: self.nat = 'US'
    def get_state(self):
        states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }
        for i in states:
            if self.state.title() in states[i]:
                return i.upper()
    
    
    def get_phone_number(self):
        first = str(random.randint(100,999))
        second = str(random.randint(1,888)).zfill(3)

        last = (str(random.randint(1,9998)).zfill(4))
        while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
            last = (str(random.randint(1,9998)).zfill(4))
        return '{}-{}-{}'.format(first,second, last)
    
    def get_random_string(self,length):
        letters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
    
    
    def find_between( data, first, last ):
        """Get middle text from  full text

        Args:
            data (str): data
            first (any): [First text]
            last (any): [last text]

        Returns:
            [str]: [return middle text of first and last text]
        """
        try:
            start = data.index( first ) + len( first )
            end = data.index( last, start )
            return data[start:end]
        except ValueError:
            return False
    
    def get_random_user_info(self) -> object:
        self.url = 'https://randomuser.me/api/?password=special,lower,upper,number,1-20'
        if self.nat:
            url = self.url + "&nat={}".format(self.nat)
        else:
            url = self.url
        result = urlopen(url)
        data = result.read().decode('utf-8')
        data = json.loads(data)
        self.latitude = data['results'][0]['location']['coordinates']['latitude']
        self.longitude = data['results'][0]['location']['coordinates']['longitude']
        self.age = data['results'][0]['dob']['age']
        self.picture = data['results'][0]['picture']['medium']
        self.title =  data['results'][0]['name']['title']
        self.first_name =  data['results'][0]['name']['first']
        self.last_name =  data['results'][0]['name']['last']
        self.name_with_title = self.title + " "+ self.first_name + " "+ self.last_name
        self.name = self.first_name + " "+ self.last_name
        self.street_number =  data['results'][0]['location']['street']['number']
        self.street_name =  data['results'][0]['location']['street']['name']
        self.street = str(self.street_number) + " " + self.street_name
        self.city =  data['results'][0]['location']['city']
        self.state =  data['results'][0]['location']['state']
        self.country =  data['results'][0]['location']['country']
        self.postcode =  data['results'][0]['location']['postcode']
        # self.ex_email =  data['results'][0]['email']
        # self.email = self.ex_email.replace('@example', f'{self.password}@gmail')
        self.username =  data['results'][0]['login']['username']
        # self.password =  data['results'][0]['login']['password']
        self.state_iso = self.get_state()
        self.phone = self.get_phone_number()
        return self

    def get_radnom_card(self) -> object:
        res = urlopen('https://random-data-api.com/api/stripe/random_stripe')
        data = res.read().decode('utf-8')
        data = json.loads(data)
        self.cc =  data['valid_card']
        self.month = data['month']
        self.year =  data['year']
        self.cvv = data['ccv']
        return self


    def get_random_bank(self) -> object:
        res = urlopen('https://random-data-api.com/api/bank/random_bank')
        data = res.read().decode('utf-8')
        data = json.loads(data)
        self.account_number =  data['account_number']
        self.iban = data['iban']
        self.bank_name =  data['bank_name']
        self.routing_number = data['routing_number']
        self.swift_bic = data['swift_bic']
        return self

