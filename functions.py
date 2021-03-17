from forex_python.converter import CurrencyRates, CurrencyCodes


def is_currency_code_format(code):
    """User currency code input is in the form of 3 english characters"""

    if len(code) == 3 and code.isalpha():
        return True
    return False


def is_number_format(num_string):
    """User amount input is in the form of a positive, real number"""

    try:
        return float(num_string) >= 0
    except ValueError:
        return False


def is_real_currency_code(code):
    """Error is raised and handled with invalid currency code inputs"""

    rates = CurrencyRates()

    try:
        if rates.get_rates(code):
            return True
    except:
        return False


def convert_currency(fromCode, toCode, amount):
    """Currency is accurately converted and formatted with currency symbol and 2 decimal places"""

    rates = CurrencyRates()
    codes = CurrencyCodes()
    conversion_rate = rates.get_rate(fromCode, toCode)
    currency_symbol = codes.get_symbol(toCode)
    return f'{currency_symbol}{round(conversion_rate*float(amount),2)}'
