"""
USSD codes for MTN Uganda and Airtel Uganda
"""

MTN_CODES = {
    'mobile_money_balance': '*165*5#',
    'airtime_balance': '*131*5#',
    'data_balance': '*131*5#',
    'mini_statement': '*165*6#',
    'loan_balance': '*165*1*7#',
    'request_loan': '*165*1*2*{amount}#',
    'send_money': '*165*3*{phone}*{amount}#',
    'buy_airtime_self': '*165*2*{amount}#',
    'buy_airtime_other': '*165*2*{phone}*{amount}#',
    'buy_data': '*165*3*{phone}*{amount}#',
    'withdraw_money': '*165*5*{agent_code}*{amount}#',
    'pay_merchant': '*165*6*{merchant_code}*{amount}#',
}

AIRTEL_CODES = {
    'mobile_money_balance': '*185*5#',
    'airtime_balance': '*185#',
    'data_balance': '*185*6#',
    'mini_statement': '*185*2*6#',
    'loan_balance': '*185*1*7#',
    'request_loan': '*185*1*2*{amount}#',
    'send_money': '*185*1*1*{phone}*{amount}#',
    'buy_airtime_self': '*185*1*3*{amount}#',
    'buy_airtime_other': '*185*1*3*{phone}*{amount}#',
    'buy_data': '*185*1*4*{phone}*{amount}#',
    'withdraw_money': '*185*1*5*{agent_code}*{amount}#',
    'pay_merchant': '*185*1*6*{merchant_code}*{amount}#',
}


def get_ussd_code(intent: str, telecom: str, params: dict = None) -> str:
    """Build USSD code for the given intent, telecom, and parameters"""
    params = params or {}
    telecom = telecom.upper()

    if telecom == 'MTN':
        codes = MTN_CODES
    elif telecom == 'AIRTEL':
        codes = AIRTEL_CODES
    else:
        raise ValueError(f"Unknown telecom: {telecom}")

    template = codes.get(intent)
    if not template:
        raise ValueError(f"No USSD code for intent: {intent} on {telecom}")

    # Normalize phone: strip leading 0 and replace with country code or keep as is
    phone = params.get('phone_number', params.get('recipient_phone', ''))
    amount = params.get('amount', '')
    agent_code = params.get('agent_code', '')
    merchant_code = params.get('merchant_code', '')

    return template.format(
        phone=phone,
        amount=amount,
        agent_code=agent_code,
        merchant_code=merchant_code,
    )
