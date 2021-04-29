import json

from flask import request, render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, current_user, login_required, logout_user

from app.controllers.ClienteController import criarcliente, deletarcliente, updatecliente, readcliente
from app.controllers.ImovelController import updateimovel

from app.controllers.PedidoController import criarpedido, readpedido
from app.models.Model import *
from app.blueprints.user.forms import LoginForm
from app.blueprints.user.forms import ClientForm
from passlib.hash import sha256_crypt

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
            userp = form.senha.data
            usero = form.usuario.data
            user = session.query(Vendedores).filter_by(USUARIO=usero).first()
            users = session.query(Vendedores.SENHA).filter_by(USUARIO=usero).first()
            if users:
                users0 = users[0]


            if not user or not sha256_crypt.verify(userp, users0):
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
    status = "Livre"
    return render_template('listaimoveis.html', query=apt, status=status)

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


    listacli = session.query(Clientes.NOME).all()

    strings = [str(y[0]) for y in listacli]

    return render_template('buy.html', aptid=aptid, lista=strings)

@user.route('/buyend<apt_id>', methods=['GET', 'POST'])
@login_required
def buyend(apt_id):
    id_u = current_user.get_id()
    vend_nome = session.query(Vendedores.USUARIO).filter_by(ID_VENDEDOR=id_u).first()
    nome_vend = vend_nome[0]

    imv_nome = session.query(Imoveis.NOME).filter_by(ID_IMOVEL=apt_id).first()
    nome_imv = imv_nome[0]

    if request.method == 'POST':
        if request.form['bton'] == 'work':

            varpag = request.form.get("pag")

            varcli = request.form.get("listadd")


            clinome = session.query(Clientes.ID_CLIENTE).filter_by(NOME=varcli).first()

            clid = clinome[0]



            order = {

                "PAGAMENTO": varpag,
                "ID_VENDEDOR": id_u,
                "ID_CLIENTE": clid,
                "imovel_id": apt_id

                }

            response = criarpedido(order)


            if response["status"]:
                updateimovel(apt_id)
            else:
                flash(response["message"], 'error')




    return render_template("vieworder.html", nome_vend=nome_vend, nome_imv=nome_imv, varcli=varcli, varpag=varpag)



@user.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    else:
        logout_user()
        return redirect(url_for('user.login'))

