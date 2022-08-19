import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from userinfo import RandUser

def find_between( data, first, last ):
    try:
        start = data.index( first ) + len( first )
        end = data.index( last, start )
        return data[start:end]
    except ValueError:
        return None



def auto_shopify(cc: str or int, mes: str or int, ano: str or int, cvv: str or int):
    link = 'https://thursdayboots.com/products/gift-cards'
    r = requests.Session()
    r.proxies = {'http': 'http://user-sp40477779:R0ld3x0p@all.dc.smartproxy.com:10001'}
    a = r.get(link)
    variantId = find_between(a.text, 'variantId":',',')
    if not variantId:
        return 
    soup = BeautifulSoup(a.text, 'html.parser')
    hidden_tags = soup.find_all("input", type="hidden")
    a2c_data = {
    'id': variantId,
    'quantity': 1,
    'add': ''
    }
    for x in hidden_tags:
        if 'properties' in  x.get('name'):
            a2c_data[x.get('name')] =  x.get('value')
    webname = urlparse(link).netloc
    if 'add.js' in a.text:
        b = r.post(f'https://{webname}/cart/add.js', data=a2c_data)
        if not b:
            return
    else:
        b = r.post(f'https://{webname}/cart/add', data=a2c_data)
        if not b:
            return
        
    c = r.post(f'https://{webname}/cart', 'updates%5B%5D=1&note=&checkout=Check+Out')

    if 'checkouts/c/' in c.url:
        c = r.get(c.url)
    if not c:
        return
    auth_token = find_between(c.text, 'type="hidden" name="authenticity_token" value="','"')
    if not auth_token:
        return
    d_data = {
'checkout[shipping_address][country]': 'United States',
'checkout[client_details][browser_width]': '1351',
'checkout[client_details][browser_height]': '658',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
}
    rand_sho = RandUser().get_sho_auto()
    soup = BeautifulSoup(c.text,"html.parser")
    inputs = soup.findAll('input', attrs={'type': 'text'})
    finded = soup.find_all("input", type="hidden")
    for x in inputs:
        if x.get('data-autocomplete-field'):
            if x.get('data-autocomplete-field') in rand_sho:
                d_data[x.get('name')] =  rand_sho[x.get('data-autocomplete-field')]
    for x in finded:
        if x.get('name') not in d_data:
            d_data.update({x.get('name'): x.get('value')})
    if 'buyer_accepts_marketing' in c.text:
        d_data.update({'checkout[buyer_accepts_marketing]': 0})
    if 'checkout_email' in c.text:
        d_data.update({'checkout[email]': rand_sho['email']})
    d = r.post(c.url, d_data)
    if 'Calculating taxes' in d.text:
        d = r.get(d.url)
        
    # with open('d.html', 'w') as w: w.write(d.text)
    if not d:
        return
    soup = BeautifulSoup(d.text, 'html.parser')
    hidden_tags = soup.find_all("p",{'class': 'field__message field__message--error'})
    if hidden_tags:
        for x in hidden_tags:
            return hidden_tags
    if 'step=shipping_method' in d.url:
        if 'Shipping Method' in d.text or 'Shipping method' in d.text:
            d = r.get(c.url + '/shipping_rates?step=shipping_method')
        ship_tag = find_between(d.text, '<div class="radio-wrapper" data-shipping-method="', '"')
        if not ship_tag:
            return
        e_data = {
'checkout[client_details][browser_width]': '1351',
'checkout[client_details][browser_height]': '658',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
        }
        soup = BeautifulSoup(d.text,"html.parser")
        finded = soup.find_all("input", type="hidden")
        for x in finded:
            if x.get('name') not in e_data:
                e_data.update({x.get('name'): x.get('value')})
        e_data = {
'_method': 'patch',
'authenticity_token': auth_token,
'previous_step': 'shipping_method',
'step': 'payment_method',
'checkout[shipping_rate][id]': ship_tag,
'checkout[client_details][browser_width]': '674',
'checkout[client_details][browser_height]': '662',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
}
        e = r.post(c.url, e_data)
        with open('e.html', 'w') as w: w.write(e.text)
        
        if not e: return
        price = find_between(e.text,'data-checkout-payment-due-target="','"')
        if price:
            price = int(price) / 100
        if not (price):
            return   
        check_url = e.url
    else:
        price = find_between(d.text,'data-checkout-payment-due-target="','"')
        if price:
            price = int(price) / 100
        if not (price):
            return 
        check_url = d.url
    check_url = r.get(check_url)
    check_url = check_url.text
    json_four = {'credit_card': {'number': cc, 'name': 'Shirley', 'month': mes, 'year': ano, 'verification_value': cvv}, 'payment_session_scope': 'thursdayboots.com'}
    # json_four = {
    #     "credit_card": {
    #         "number": cc,
    #         "name": rand_sho['first_name'],
    #         "month": mes,
    #         "year": ano,
    #         "verification_value": cvv
    #     },
    #     "payment_session_scope": webname
    # }
    
    four = r.post('https://deposit.us.shopifycs.com/sessions', json = json_four)
    if not four or  not 'id' in four.json():
        return 
    f_data = {
'checkout[client_details][browser_width]': '1351',
'checkout[client_details][browser_height]': '658',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
    }    
    soup = BeautifulSoup(check_url,"html.parser")
    inputs = soup.findAll('input', attrs={'type': 'hidden'})
    radios = soup.findAll('input', attrs={'checked': 'checked'})
    for x in radios:
        f_data[x.get('name')] = x.get('value')
    for x in inputs:
        if x.get('name') not in f_data:
            f_data.update({x.get('name') : x.get('value')})
    f_data.update({'s': four.json()['id']})
    if 'checkout_vault_phone' in check_url:
        f_data.update({'checkout[vault_phone]': rand_sho['phone']})
    f = r.post(c.url, f_data)
    soup = BeautifulSoup(f.text, 'html.parser')
    hidden_tags = soup.find_all("p",{'class': 'field__message field__message--error'})
    with open('f.html', 'w') as w: w.write(f.text)
    if hidden_tags:
        for x in hidden_tags:
            return hidden_tags
    hidden_tags = soup.find_all("p",{'class': 'notice__text'})
    if hidden_tags:
        for x in hidden_tags:
            return hidden_tags
    if 'hosted_fields_forward' in f.url:
        g = r.get(f.url)
        g_data = {}
        soup = BeautifulSoup(g.text,"html.parser")
        inputs = soup.findAll('input', attrs={'type': 'hidden'})
        for x in inputs:
            g_data[x.get('name')] = x.get('value')
        
        h = r.post('https://checkout.shopifycs.com/pay', g_data)
        d_val = g_data.get('d')
        if not d_val: return
        i_data = {
'd': d_val,
'checkout[credit_card][number]': cc,
'checkout[credit_card][name]': rand_sho['first_name'],
'checkout[credit_card][month]': mes,
'checkout[credit_card][year]': ano,
'checkout[credit_card][verification_value]': cvv,
'complete': '1',
        }
        f = r.post('https://deposit.us.shopifycs.com/sessions', i_data)

    if 'processing' not in f.url:
        return
    time.sleep(4)
    g = r.get(c.url + '/processing?from_processing_page=1')
    
    time.sleep(5)
    with open('g.html', 'w') as w: w.write(g.text)
    text1 = find_between(g.text, '<p class="notice__text">','</p></div></div>')
    return text1
        
        

# x= auto_shopify('https://www.slimeball.world/collections/all/products/slimeball-rolling-papers',cc,mes,ano,cvv)
# x = auto_shopify('https://thursdayboots.com/products/gift-cards',cc,mes,ano,cvv)
# x= auto_shopify('https://a1bakerysupplies.myshopify.com/products/a1bs-cake-decoration-toys-favors-figurine-toys-barney-kit',cc,mes,ano,cvv)

# print(x)