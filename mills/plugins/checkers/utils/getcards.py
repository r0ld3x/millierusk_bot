import time
import os , re , sys

from mills import adb , mdb
from mills.plugins.checkers.utils.tools import checkLuhn
from mills.utils.logger import log


from mills.plugins.checkers.utils.userinfo import user_info
from mills.plugins.checkers.utils.bininfo import get_bin_info

def get_cards():
    """get gate info."""
    def inner(func):
        async def wrap(*args, **kwargs):
            m = args[0]
            if m.is_reply:
                m =await m.get_reply_message()
                text = m.text
            else:
                if 'api' in m.text:
                    text = m.text.split('|', maxsplit=1)[1]
                else:
                    text = m.text
                    
            text = text.replace('\n',' ').replace('\r',' ')
            input = re.findall(r"[0-9]+", text)
            if not input or len(input) < 3:
                await m.sod("No Cards Found From Your Input. Try Again With A Valid Input.", time = 5)
                return
            if len(input) == 3:
                cc = input[0]
                if not checkLuhn(cc): return await m.sod("Invalid Card Number. Try Again With A Valid Input.", time = 5)
                if len(input[1]) == 3:
                    mes = input[2][:2]
                    ano = input[2][2:]
                    cvv = input[1]
                else:
                    mes = input[1][:2]
                    ano = input[1][2:]
                    cvv = input[2]
            else:
                cc = input[0]
                if len(input[1]) == 3:
                    mes = input[2]
                    ano = input[3]
                    cvv = input[1]
                else:
                    mes = input[1]
                    ano = input[2]
                    cvv = input[3]
                if  len(mes) == 2 and (mes > '12' or mes < '01'):
                    ano1 = mes
                    mes = ano
                    ano = ano1
            
            if cc[0] == 3 and len(cc) != 15 or len(cc) != 16 or int(cc[0]) not in [3,4,5,6]:
                await m.sod("Invalid Card Number. Try Again With A Valid Card Number.", time = 5)
                return
            if len(mes) not in [2 , 4] or len(mes) == 2 and mes > '12' or len(mes) == 2 and mes < '01':
                await m.sod("Invalid Card Expiry Month. Try Again With A Valid Expiry Month.", time = 5)
                return
            if len(ano) not in [2,4] or len(ano) == 2 and ano < '21' or len(ano)  == 4 and ano < '2021' or len(ano) == 2 and ano > '29' or len(ano)  == 4 and ano > '2029':
                await m.sod("Invalid Card Expiry Year. Try Again With A Valid Expiry Year.", time = 5)
            if cc[0] == 3 and len(cvv) != 4 or len(cvv) != 3:
                await m.sod("Invalid Card CVV. Try Again With A Valid CVV.", time = 5)
                return 
            bin =  get_bin_info(cc[:6])
            if not bin:
                await m.sod("Change your bin i will not check with this bin.", time = 5)
                return
            if (cc,mes,ano ,cvv):
                if len(ano) == 2:
                    ano = "20"+ str(ano)
                await func(*args,(cc, mes, ano, cvv, bin),**kwargs)
        return wrap
    return inner
