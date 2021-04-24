from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    usuario = StringField(validators=[DataRequired()])
    senha = PasswordField(validators=[DataRequired()])


class ClientForm(FlaskForm):
    nome = StringField(validators=[DataRequired()])
    cpf = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    telefone = StringField(validators=[DataRequired()])


class BuyForm(FlaskForm):
    pagamento = StringField(validators=[DataRequired()])
    id_v = IntegerField(validators=[DataRequired()])
    id_c = IntegerField(validators=[DataRequired()])
    imovel_id = IntegerField(validators=[DataRequired()])