from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

moneda = ('EUR','BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX')




class MiForm(FlaskForm):
    from_currency = SelectField('From:')
    #from_cantidad = FloatField('Cantidad:', validators=[NumberRange (min=0.00000001, max=1000000000, message="La cantidad elegida es demasiado alta")])
    from_cantidad = FloatField('Cantidad:')

    to_currency = SelectField('To:', choices=moneda)
    to_cantidad = FloatField('Cantidad:')

    preciou = FloatField('Precio Unidad:')

    calculator = SubmitField('&#xf1ec;')
    aceptar = SubmitField('Aceptar')


class Status(FlaskForm):
    invertido = FloatField('Invertido:')
    vactual = FloatField('Valor Actual:')

