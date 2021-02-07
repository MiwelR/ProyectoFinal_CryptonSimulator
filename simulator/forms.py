from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from simulator.dataaccess import *

moneda = ('EUR','BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX')

# VALIDACIONES:

# Validación para distintas monedas:
def validatorSelect(form, field):
    if field.data == form.from_currency.data:
        mensaje = field.gettext('La moneda de compra y de venta son la misma: {}')
        raise ValidationError(mensaje.format(field.data))

# Validación para el saldo de la moneda FROM:
class SaldoDisponible:
    def __init__(self, fieldFrom, message=None):
        self.fieldFrom = fieldFrom
        self.message = message

    def __call__(self, form, field):
        # Cálculo saldo de cryptos disponible:
        try:
            currencyData = form[self.fieldFrom]
            cryptosList = ['BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX']
            cryptos = {}
            for i in cryptosList:
                cryptos[i] = round(saldos(i), 8)
        except Exception as error:
            print("🔧***ERROR***🔧: Acceso a base de datos - Consultando Saldo de Cryptos disponibles en forms.py: {} - {}". format(type(error).__name__, error))
            raise ValidationError(field.gettext("Error en base de datos al consultar saldo en {}. Consulte con el administrador.".format(currencyData.data)))

        if currencyData.data == 'EUR':
            pass
        elif cryptos[currencyData.data] < field.data:
            if self.message is None:
                self.message = field.gettext('No dispone de saldo suficiente en {}')
            
            raise ValidationError(self.message.format(currencyData.data))


# FORMULARIOS:
class MiForm(FlaskForm):
    from_currency = SelectField('Divisa (Venta):')
    to_currency = SelectField('Divisa (Compra):', choices=moneda, validators=[validatorSelect])
    from_cantidad = FloatField('Cantidad:', validators=[DataRequired(message='Debe introducir una cantidad correcta (Use "." para decimales en lugar de ",").'), 
                                    NumberRange (min=0.00000001, max=1000000000, message="Debe elegir una cantidad entre 0.00000001 y %(max)s"),
                                    SaldoDisponible('from_currency')])
    to_cantidad = FloatField('Cantidad:')
    preciou = FloatField('Precio/Unidad:')
    time = FloatField('')
    calculator = SubmitField('')
    aceptar = SubmitField('Aceptar')


class Status(FlaskForm):
    invertido = FloatField('Invertido:')
    vactual = FloatField('Valor Actual:')
    ganancia = FloatField('Ganancia:')
