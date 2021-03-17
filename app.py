from flask import Flask, render_template, redirect, request, flash, session
from functions import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"


@app.route('/')
def homepage():
    """Show forex conversion form"""

    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """Take form submission and perform the conversion of the currency"""

    convert_from = request.form.get('convertFrom')
    convert_to = request.form.get('convertTo')
    amount = request.form.get('amount')

    error = False
    if not (is_currency_code_format(convert_from) and is_real_currency_code(convert_from)):
        flash(f'Not a valid code: {convert_from}')
        error = True
    if not (is_currency_code_format(convert_to) and is_real_currency_code(convert_to)):
        flash(f'Not a valid code: {convert_to}')
        error = True
    if not is_number_format(amount):
        flash(f'Not a valid amount: {amount}')
        error = True

    if error:
        return redirect('/')
    else:
        result = convert_currency(convert_from, convert_to, amount)
        session['result'] = result
        return redirect('/result')


@app.route('/result')
def result():
    """Shows the html page with the resulting conversion information"""

    return render_template('result.html')
