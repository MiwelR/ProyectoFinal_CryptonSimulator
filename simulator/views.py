from simulator import app
from flask import render_template, request, url_for, redirect, flash
from simulator import forms
from config import *
from simulator.dataaccess import *
from simulator.api_requests import *
from datetime import datetime
from time import time


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404


@app.context_processor
def monedero():
    try:
        cryptosList = ['BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX']
        cryptos = {}
        cryptos['EUR'] = 'Infinito'
        for i in cryptosList:
            cryptos[i] = round(saldos(i), 8)
            if cryptos[i] <= 0:
                del cryptos[i]
    except Exception as error:
        print("🔧***ERROR***🔧: Acceso a base de datos - Saldos Header: {} - {}". format(type(error).__name__, error))
        cryptos['ERROR'] = "Error en acceso a base de datos. Consulte con el administrador."
        del cryptos['EUR']
        return dict(misaldo=cryptos)

    return dict(misaldo=cryptos)


@app.route('/')
def main():
    msgError = []

    try:
        movimientos = consulta('SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, price FROM movements;')
    except Exception as error:
        print("🔧***ERROR***🔧: Acceso a base de datos - Movimientos: {} - {}". format(type(error).__name__, error))
        msgError.append("Error en acceso a base de datos. Consulte con el administrador.")

        return render_template('index.html', msgError=msgError)

    return render_template('index.html', datos=movimientos, msgError=msgError)


@app.route('/purchase', methods=['GET', 'POST'])
def change():
    form = forms.MiForm()
    msgError = []
    # Selección de monedas disponibles según el saldo:
    try:
        form.from_currency.choices = select_from()
    except Exception as error:
        print("🔧***ERROR***🔧: Acceso a base de datos - Monedas From disponibles: {} - {}". format(type(error).__name__, error))
        msgError.append("Error en acceso a base de datos. Consulte con el administrador.")

        return render_template('purchase.html', form=form, calculo=False, msgError=msgError)

    if request.method == 'POST' and form.validate():
        if form.calculator.data:
            # Consulta a API:
            try:
                from_currency = form.from_currency.data
                from_cantidad = form.from_cantidad.data
                to_currency = form.to_currency.data

                respuesta = peticion(url_api.format(from_cantidad, from_currency, to_currency, API_KEY))
                
                to_cantidad = respuesta['data']['quote'][to_currency]['price']
            except Exception as error:
                print("🔧***ERROR***🔧: Acceso a API - Petición de cálculo a API: {} - {}". format(type(error).__name__, error))
                msgError.append("Error de acceso a API. Consulte con el administrador.")

                return render_template('purchase.html', form=form, calculo=False, msgError=msgError)

            # Redondeo para euros/cryptos en el cálculo (formato para notación científica):
            if 'e' in str(to_cantidad):
                to_cantidad = '{:f}'.format(to_cantidad)
            elif to_currency == 'EUR':
                to_cantidad = round(to_cantidad, 2)
            else:
                to_cantidad = round(to_cantidad, 8)
            # Control del error ZeroDivisionError en caso de división entre 0:
            try:
                if from_currency == 'EUR':
                    preciou = round((from_cantidad / float(to_cantidad)), 2)
                else:
                    preciou = round((from_cantidad / float(to_cantidad)), 8)
                if 'e' in str(preciou):
                    preciou = '{:f}'.format(preciou)
            except ZeroDivisionError:
                try:
                    preciou = peticion(url_api.format(1, to_currency, from_currency, API_KEY))['data']['quote'][from_currency]['price']
                    if from_currency == 'EUR':
                        preciou = round(preciou, 2)
                    else:
                        preciou = round(preciou, 8)
                except Exception as error:
                    print("🔧***ERROR***🔧: Acceso a API - Valor de 1 unidad de Moneda_To en Moneda_From: {} - {}". format(type(error).__name__, error))
                    msgError.append("Error de acceso a API. Consulte con el administrador.")

                    return render_template('purchase.html', form=form, calculo=False, msgError=msgError)

            # Datos para el formulario:
            form.to_cantidad.data = to_cantidad
            form.preciou.data = preciou
            form.time.data = time()

            return render_template('purchase.html', form=form, calculo=True)

        if form.aceptar.data:
            # Caducidad del cálculo en 60seg:
            timeAcept = time()
            if int(timeAcept - form.time.data) > 60:
                msgError.append("Su consulta ha caducado. Por favor, realice la consulta de nuevo")

                return render_template('purchase.html', form=form, calculo=False, msgError=msgError)
            # Fecha/Hora Actual:
            ahora = datetime.now()
            fecha = ahora.date()
            hora = ahora.strftime("%H:%M:%S")
            # Grabando operación en Base de Datos:
            try:
                consulta('INSERT INTO movements (date, time, from_currency, from_quantity, to_currency, to_quantity, price) VALUES (?, ?, ?, ?, ?, ?, ?);', 
                        (fecha, hora, form.from_currency.data, float(form.from_cantidad.data), form.to_currency.data, float(form.to_cantidad.data), float(form.preciou.data)))
            except Exception as error:
                print("🔧***ERROR***🔧: Acceso a base de datos - Grabando operación en Database.db: {} - {}". format(type(error).__name__, error))
                msgError.append("Error en acceso a base de datos. Consulte con el administrador.")

                return render_template('purchase.html', form=form, calculo=False, msgError=msgError)

            return redirect(url_for('main'))

    else:
        return render_template('purchase.html', form=form, calculo=False)


@app.route('/status')
def trade():
    form = forms.Status()
    msgError = []

    # Invertido (Total de Euros invertidos):
    try:
        movimientos = consulta("SELECT from_quantity FROM movements WHERE from_currency ='EUR';")
        euros_invertidos = 0
        for fila in movimientos:
            euros_invertidos += float(fila['from_quantity'])
    except Exception as error:
        print("🔧***ERROR***🔧: Acceso a base de datos - Consultando Euros invertidos: {} - {}". format(type(error).__name__, error))
        msgError.append("Error en acceso a base de datos. Consulte con el administrador.")

        return render_template('status.html', form=form, msgError=msgError)

    # Saldo de euros:
    try:
        saldo_euros = saldos('EUR')
    except Exception as error:
        print("🔧***ERROR***🔧: Acceso a base de datos - Consultando Saldo de Euros: {} - {}". format(type(error).__name__, error))
        msgError.append("Error en acceso a base de datos. Consulte con el administrador.")

        return render_template('status.html', form=form, msgError=msgError)

    # Valor actual de las cryptos (en euros):
    try:
        cryptosList = ('BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX')
        cryptos = {}
        for i in cryptosList:
            cryptos[i] = saldos(i)
    except Exception as error:
        print("🔧***ERROR***🔧: Acceso a base de datos - Consultando Saldo de Cryptos: {} - {}". format(type(error).__name__, error))
        msgError.append("Error en acceso a base de datos. Consulte con el administrador.")

        return render_template('status.html', form=form, msgError=msgError)

    try:
        totalE = 0
        for coin in cryptos:
            conversion = ''
            if float(cryptos[coin]) > 0:
                conversion = peticion(url_api.format(float(cryptos[coin]), coin, 'EUR', API_KEY))['data']['quote']['EUR']['price']
                totalE += float(conversion)
    except Exception as error:
        print("🔧***ERROR***🔧: Acceso a API - Valor actual de Cryptos en Euros: {} - {}". format(type(error).__name__, error))
        msgError.append("Error de acceso a API. Consulte con el administrador.")

        return render_template('status.html', form=form, msgError=msgError)

    # Valor actual (Total de euros invertidos + Saldo de euros invertidos + Valor en euros del saldo de cryptos):
    valor_actual = euros_invertidos + saldo_euros + totalE

    # Datos para el formulario:
    form.invertido.data = str(euros_invertidos) + " €"
    form.vactual.data = str(round(valor_actual, 2)) + " €"
    form.ganancia.data = '{:.2f} €'.format(valor_actual - euros_invertidos)

    return render_template('status.html', form=form)

