from simulator import app
import sqlite3

DBFILE = app.config['DBFILE']


# Función consulta a base de datos:
def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    c.execute(query, params)
    conn.commit()

    filas = c.fetchall()

    conn.close()

    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios


# Función consulta saldo actual de criptomonedas:
def saldos(moneda):
        datos = consulta('SELECT from_currency, from_quantity, to_currency, to_quantity FROM movements;')
        cantidad_to = 0
        cantidad_from = 0
        for i in datos:
            if i['to_currency'] == moneda:
                cantidad_to += float(i['to_quantity'])
            elif i['from_currency'] == moneda:
                cantidad_from += float(i['from_quantity'])
        saldo = cantidad_to - cantidad_from
        return saldo


# Función para lista de monedas "From":
def select_from():
    # Cálculo de cryptos para el SelectField "From":
    cryptosList = ['BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX']
    cryptos = {}
    for i in cryptosList:
        cryptos[i] = saldos(i)
    
    for coin in cryptos:
        if float(cryptos[coin]) <= 0:
            cryptosList.remove(coin)

    # Añadiendo Euros por defecto en primera posición:
    cryptosList.insert(0, 'EUR')
    return cryptosList