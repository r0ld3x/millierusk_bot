

import random
import re

import requests


def checkLuhn(cardNo):
     
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False
     
    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
     
        if (isSecond == True):
            d = d * 2
  
        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10
  
        isSecond = not isSecond
     
    if (nSum % 10 == 0):
        return True
    else:
        return False



def cc_gen(cc, mes = 'x', ano = 'x', cvv = 'x',amount = 'x',): 
    if amount != 'x':
        amount = int(amount)
    else:
        amount = 15
    genrated = 0
    ccs = []
    while(genrated < amount):
        genrated += 1
        s="0123456789"
        l = list(s)
        random.shuffle(l)
        result = ''.join(l)
        result = cc + result
        if cc[0] == "3":
            ccgen = result[0:15]
        else:
            ccgen = result[0:16]
        if mes == 'x':
            mesgen = random.randint(1,12)
            if len(str(mesgen)) == 1:
                mesgen = "0" + str(mesgen)
        else:
            mesgen = mes
        if ano == 'x':
            anogen = random.randint(2021,2029)
        else:
            anogen = ano
        if cvv == 'x':
            if cc[0] == "3":
                cvvgen = random.randint(1000,9999) 
            else:
                cvvgen = random.randint(100,999)
        else:
            cvvgen = cvv   
        # if not x: continue
        lista = "<code>" + str(ccgen) +"|" + str(mesgen) + "|"+ str(anogen) + "|" + str(cvvgen) + "</code>"
        ccs.append(lista)
    return ccs


def getUrl(string):
      
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string) 
    if not url: return None     
    return [x[0] for x in url]






def getcards(text:str):
    text = text.replace('\n', ' ').replace('\r', '')
    card = re.findall(r"[0-9]+", text)
    if not card or len(card) < 3:
        return
    if len(card) == 3:
        cc = card[0]
        if len(card[1]) == 3:
            mes = card[2][:2]
            ano = card[2][2:]
            cvv = card[1]
        else:
            mes = card[1][:2]
            ano = card[1][2:]
            cvv = card[2]
    else:
        cc = card[0]
        if len(card[1]) == 3:
            mes = card[2]
            ano = card[3]
            cvv = card[1]
        else:
            mes = card[1]
            ano = card[2]
            cvv = card[3]
        if  len(mes) == 2 and (mes > '12' or mes < '01'):
            ano1 = mes
            mes = ano
            ano = ano1
    if cc[0] == 3 and len(cc) != 15 or len(cc) != 16 or int(cc[0]) not in [3,4,5,6]:
        return
    if len(mes) not in [2 , 4] or len(mes) == 2 and mes > '12' or len(mes) == 2 and mes < '01':
        return
    if len(ano) not in [2,4] or len(ano) == 2 and ano < '21' or len(ano)  == 4 and ano < '2021' or len(ano) == 2 and ano > '29' or len(ano)  == 4 and ano > '2029':
        return
    if cc[0] == 3 and len(cvv) != 4 or len(cvv) != 3:
        return
    if (cc,mes,ano,cvv):
        return cc,mes,ano,cvv
    


def check_sk(key):
    data = 'card[number]=4512238502012742&card[exp_month]=12&card[exp_year]=2022&card[cvc]=354'
    first = requests.post('https://api.stripe.com/v1/tokens', data = data, auth = (key, ' '))
    status = first.status_code
    f_json = first.json()
    if 'error'in f_json:
        if 'type' in f_json['error']:
            type = f_json['error']['type']
        else:
            type = ''
    else:
        type = ''
    if status == 200 or type == 'card_error':
        r_text, r_logo, r_respo = 'VALID API KEY', '✅', 'VALID API KEY'
    else:
        if 'error' in first.json():
            if 'code' in first.json()['error']:
                r_res = first.json()['error']['code'].replace('_',' ').strip()
            else:
                r_res = 'INVALID API KEY'
        else:
            r_res = 'INVALID API KEY'
            
        r_text, r_logo, r_respo = 'INVALID API KEY', '❌', r_res
    return r_text, r_logo, r_respo
