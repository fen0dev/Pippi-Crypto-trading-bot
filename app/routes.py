from flask import Blueprint, render_template, request, redirect, url_for
from .utils import fetch_balance, create_order, send_telegram_message
from .models import Order
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    balance = fetch_balance()
    return render_template('index.html', balance=balance)

@main.route('/trade', methods=['POST'])
def trade():
    symbol = request.form['symbol']
    side = request.form['side']
    amount = float(request.form['amount'])
    order = create_order(symbol, 'market', side, amount)
    if order:
        send_telegram_message(f"Order placed: {side} {amount} of {symbol}")
        
        # Save order to the database
        new_order = Order(symbol=symbol, side=side, amount=amount, price=order['price'])
        db.session.add(new_order)
        db.session.commit()
        
    return redirect(url_for('main.index'))
