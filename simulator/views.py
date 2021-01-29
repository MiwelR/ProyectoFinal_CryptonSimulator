from simulator import app
from flask import render_template, request, url_for, redirect
from simulator import forms
from config import *
from simulator.dataaccess import *
import requests
from datetime import datetime

url_api = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'

def peticion(url):
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos
    else: 
        pass


@app.route('/')
def main():
    form = forms.MiForm()

    movimientos = consulta('SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, price FROM movements;')

    return render_template('index.html', form=form, datos=movimientos)


@app.route('/purchase', methods=['GET', 'POST'])
def change():
    form = forms.MiForm()
    calculo = False

    if request.method == 'POST':
        if form.validate():
            if form.aceptar.data == False:
                # Consulta a API:
                respuesta = peticion(url_api.format(form.from_cantidad.data, form.from_currency.data, form.to_currency.data, API_KEY))

                from_currency = respuesta['data']['symbol']
                from_cantidad = respuesta['data']['amount']
                to_currency = form.to_currency.data
                to_cantidad = respuesta['data']['quote'][to_currency]['price']
                if to_currency == 'EUR':
                    to_cantidad = round(to_cantidad, 2)
                else:
                    to_cantidad = round(to_cantidad, 8)
                if from_currency == 'EUR':
                    preciou = round((from_cantidad / to_cantidad), 2)
                else:
                    preciou = round((from_cantidad / to_cantidad), 8)

                form.from_currency.choices = [from_currency]
                datos = [from_currency, from_cantidad, to_currency, to_cantidad, preciou]

                return render_template('purchase.html', form=form, consulta=datos, calculo=True)
            if form.aceptar.data == True:
                # Fecha/Hora Actual:
                ahora = datetime.now()
                fecha = ahora.date()
                hora = ahora.strftime("%H:%M:%S")
                # Grabando operación en Base de Datos:
                consulta('INSERT INTO movements (date, time, from_currency, from_quantity, to_currency, to_quantity, price) VALUES (?, ?, ?, ?, ?, ?, ?);', 
                        (fecha, hora, form.from_currency.data, float(form.from_cantidad.data), form.to_currency.data, float(form.to_cantidad.data), float(form.preciou.data)))
                return redirect(url_for('main'))
        else:
            return render_template('purchase.html', form=form, calculo=False)

    else:
        # Cálculo de cryptos para el SelectField "From":
        cryptosList = ['BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX']
        cryptos = {}
        for i in cryptosList:
            cryptos[i] = saldos(i)
        
        for coin in cryptos:
            if float(cryptos[coin]) <= 0:
                cryptosList.remove(coin)

        # Valores para el SelectField "From":
        cryptosList.insert(0, 'EUR')
        form.from_currency.choices = cryptosList

        return render_template('purchase.html', form=form, calculo=False)


@app.route('/status')
def trade():
    form = forms.Status()

    # Invertido (Total de Euros invertidos):
    movimientos = consulta("SELECT from_quantity FROM movements WHERE from_currency ='EUR';")
    euros_invertidos = 0
    for fila in movimientos:
        euros_invertidos += float(fila['from_quantity'])

    # Saldo de euros:
    saldo_euros = saldos('EUR')

    # Valor actual de las cryptos (en euros):
    cryptosList = ('BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX')
    cryptos = {}
    for i in cryptosList:
        cryptos[i] = saldos(i)
    totalE = 0
    for coin in cryptos:
        conversion = ''
        if float(cryptos[coin]) > 0:
            conversion = peticion(url_api.format(float(cryptos[coin]), coin, 'EUR', API_KEY))['data']['quote']['EUR']['price']
            totalE += float(conversion)

    # Valor actual (Total de euros invertidos + Saldo de euros invertidos + Valor en euros del saldo de cryptos):
    valor_actual = euros_invertidos + saldo_euros + totalE

    datos = (euros_invertidos, round(valor_actual, 2))

    return render_template('status.html', form=form, inversion=datos)

