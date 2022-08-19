from mills import sdb


def insert_gates(sdb):
    dict = [
    {"_id": "chk", "status": True, "status_logo": "✅", "gate_type": "auth", "cmd_name": "chk", "gate_name": "Stripe Auth", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": False, "date": "2022-05-29"},
    {"_id": "au", "status": True, "status_logo": "✅", "gate_type": "auth", "cmd_name": "au", "gate_name": "Stripe Aut", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": False, "date": "2022-05-29"},
    {"_id": "ad", "status": True, "status_logo": "✅", "gate_type": "charge", "charge_amount": "56", "cmd_name": "ad", "gate_name": "Adyen ", "made_by_id": 1317173146, "made_by_name": "Roldex",         "is_paid": True, "date": "2022-05-29"},
    {"_id": "mass", "status": True, "status_logo": "✅", "gate_type": "mass", "cmd_name": "mass", "gate_name": "Stripe", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": True, "date": "2022-05-29"},
    {"_id": "sho", "status": True, "status_logo": "✅", "gate_type": "charge", "charge_amount": "34", "cmd_name": "sho", "gate_name": "Shopify", "made_by_id": 1317173146, "made_by_name": "𓆩Roldex", "is_paid": True, "date": "2022-05-30"},
    {"_id": "wp", "status": True, "status_logo": "✅", "gate_type": "charge", "charge_amount": "5", "cmd_name": "wp", "gate_name": "Wepay", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": True, "date":         "2022-06-01"},
    {"_id": "mchk", "status": True, "status_logo": "✅", "gate_type": "mass", "cmd_name": "mchk", "gate_name": "Stripe Charge $10", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": True, "date": "2022-06-19"},
    {"_id": "at", "status": True, "status_logo": "✅", "gate_type": "charge", "charge_amount": "36", "cmd_name": "at", "gate_name": "Adyen", "made_by_id": 1317173146, "made_by_name": "𓆩ᯓ𝙍𝙊𝙇𝘿𝙀�      ↯↯𓆪 #lost", "is_paid": True, "date": "2022-07-01"},
    {"_id": "al", "status": True, "status_logo": "✅ ", "gate_type": "charge", "charge_amount": "10", "cmd_name": "al", "gate_name": "Authorize", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": True, "d        ate": "2022-07-02"},
    {"_id": "cc", "status": True, "status_logo": "✅", "gate_type": "charge", "charge_amount": "1", "cmd_name": "cc", "gate_name": "Stripe 0.", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": True, "date": "2022-07-        03"},
    {"_id": "ck", "status": True, "status_logo": "✅", "gate_type": "charge", "charge_amount": "5", "cmd_name": "ck", "gate_name": "Stripe 0.", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": True, "date": "2022-07-03"},
    {"_id": "pf", "status": True, "status_logo": "✅", "gate_type": "charge", "charge_amount": "20", "cmd_name": "pf", "gate_name": "Payflow $", "made_by_id": 1317173146, "made_by_name": "Roldex",         "is_paid": True, "date": "2022-07-03"},
    {"_id": "str", "status": True, "status_logo": "✅", "gate_type": "charge", "charge_amount": "5", "cmd_name": "str", "gate_name": "Stripe", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": True        , "date": "2022-07-03"},
    {"_id": "vbv", "status": True, "status_logo": "✅", "gate_type": "other", "cmd_name": "vbv", "gate_name": "Braintree Vbv Check", "made_by_id": 1317173146, "made_by_name": "Roldex", "is_paid": False, "date": "2022-07-03"}]

    x = sdb["gate"].insert_many(dict)
    return x
