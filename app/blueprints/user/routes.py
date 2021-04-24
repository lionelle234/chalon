import json

from flask import request, render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, current_user, login_required, logout_user

from app.controllers.ClienteController import criarcliente, deletarcliente, updatecliente, readcliente
from app.controllers.PedidoController import criarpedido, readpedido
from app.models.Model import *
from app.blueprints.user.forms import LoginForm, BuyForm
from app.blueprints.user.forms import ClientForm

from app.database.base import session

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    remember = True
    if current_user.is_authenticated:
        return redirect(url_for('user.imoveis'))

    if request.method == "POST":
        if form.validate_on_submit():
            usero = form.usuario.data
            user = session.query(Vendedores).filter_by(USUARIO=usero).first()

            if not user:
                flash('Verifique seus dados e tente novamente.')
                return redirect(url_for('user.login'))
            else:
                login_user(user, remember=remember)
                return redirect(url_for('user.imoveis'))

    return render_template('login.html', form=form)


@user.route('/imoveis', methods=['GET', 'POST'])
@login_required
def imoveis():
    apt = Imoveis.read_apt(Imoveis)
    return render_template('listaimoveis.html', query=apt)

@user.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    client = Clientes.read_client_all(Clientes)
    return render_template('listaclientes.html', query=client)

@user.route('/clicad', methods=['GET', 'POST'])
@login_required
def clicad():
    form = ClientForm()

    if request.method == "POST":
        if form.validate_on_submit():
                novo = {
                "NOME": form.nome.data,
                "CPF": form.cpf.data,
                "EMAIL": form.email.data,
                "TELEFONE": form.telefone.data
                }

                response = criarcliente(novo)


                if response["status"]:
                    return redirect(url_for('user.clientes'))
                else:
                    flash(response["message"], 'error')
        else:
            message = ''
            for field, errors in form.errors.items():
                message += '' + field + ': ' + json.dumps(errors, ensure_ascii=False)

            flash(message, 'error')

    return render_template('cadastrocli.html', form=form)

@user.route('/delete<client_id>', methods=['GET', 'POST'])
@login_required
def delete(client_id):
    deletarcliente(client_id)
    return redirect(url_for('user.clientes'))

@user.route('/edit<client_id>', methods=['GET', 'POST'])
@login_required
def edit(client_id):
    form = ClientForm()

    if request.method == "POST":
        if form.validate_on_submit():

                updated = {
                    "ID_CLIENTE": client_id,
                    "NOME": form.nome.data,
                    "CPF": form.cpf.data,
                    "EMAIL": form.email.data,
                    "TELEFONE": form.telefone.data

                    }

                response = updatecliente(updated)

                if response["status"]:
                    return redirect(url_for('user.clientes'))
                else:
                    flash(response["message"], 'error')
        else:
            message = ''
            for field, errors in form.errors.items():
                message += '' + field + ': ' + json.dumps(errors, ensure_ascii=False)

            flash(message, 'error')

    return render_template('editar.html', form=form)

@user.route('/view<client_id>', methods=['GET', 'POST'])
@login_required
def view(client_id):
    result=[]
    response = readcliente(client_id)
    result = response['data']

    return render_template('view.html', client=result)

@user.route('/buy<apt_id>', methods=['GET', 'POST'])
@login_required
def buy(apt_id):

    aptid = apt_id

    listacli = Clientes.read_client(Clientes)

    return render_template('buy.html', aptid=aptid, lista=listacli)

@user.route('/buyend<apt_id>', methods=['GET', 'POST'])
@login_required
def buyend(apt_id):
    id_u = current_user.get_id()

    if request.method == 'POST':
        if request.form['bton'] == 'work':
            var = request.form.get("listadd")

            vary = request.form.get("pag")

            order = {

                "PAGAMENTO": vary,
                "ID_VENDEDOR": id_u,
                "NOME": var,
                "imovel_id": apt_id

                }

            response = criarpedido(order)

            pedid = response['data']

            pedidid = pedid.ID_PEDIDO

            result = []
            responsep = readpedido(pedidid)
            result = responsep['data']



    return render_template("vieworder.html", ordered=result)



@user.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    else:
        logout_user()
        return redirect(url_for('user.login'))

