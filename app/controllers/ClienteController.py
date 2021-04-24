from sqlalchemy.exc import SQLAlchemyError

from app.database.base import Session
from app.models.Model import Clientes

def criarcliente(data):
    session = Session(expire_on_commit=False)
    try:
        cliente = Clientes()

        cliente.NOME = data["NOME"]
        cliente.CPF = data["CPF"]
        cliente.EMAIL = data["EMAIL"]
        cliente.TELEFONE = data["TELEFONE"]


        session.add(cliente)
        session.commit()
        session.close()

        response = {
            'status': True,
            'data': cliente,
            'message': None
        }

    except SQLAlchemyError as sql_e:
        session.rollback()
        response = {
            'status': False,
            'data': None,
            'message': str(sql_e)
        }
    except Exception as e:
        response = {
            'status': False,
            'data': None,
            'message': str(e)
        }

    return response

def deletarcliente(data):
    session = Session(expire_on_commit=False)
    try:

        data_entered = session.query(Clientes).filter(Clientes.ID_CLIENTE == data).one()
        session.delete(data_entered)

        session.commit()
        session.close()


        response = {
            'status': True,
            'data': data,
            'message': None
        }
    except SQLAlchemyError as sql_e:
        session.rollback()

        response = {
            'status': False,
            'data': None,
            'message': str(sql_e)
        }
    except Exception as e:
        response = {
            'status': False,
            'data': None,
            'message': str(e)
        }
    return response


def updatecliente(data):
    session = Session(expire_on_commit=False)
    try:

        session.query(Clientes).filter(Clientes.ID_CLIENTE == data["ID_CLIENTE"]).update({
            'NOME': data["NOME"],
            'CPF': data["CPF"],
            'EMAIL': data["EMAIL"],
            'TELEFONE': data["TELEFONE"]})

        session.commit()

        response = {
            'status': True,
            'data': data,
            'message': None
            }

    except SQLAlchemyError as sql_e:

        session.rollback()

        response = {
            'status': False,
            'data': None,
            'message': str(sql_e)
        }

    except Exception as e:
        response = {
            'status': False,
            'data': None,
            'message': str(e)
        }

    return response


def readcliente(data):
    session = Session()
    try:

        result = session.query(Clientes).filter(Clientes.ID_CLIENTE == data).one()

        response = {
            'status': True,
            'data': result,
            'message': None
        }
        session.close()

    except SQLAlchemyError as sql_e:
        response = {
            'status': False,
            'data': None,
            'message': str(sql_e)
        }

    except Exception as e:
        response = {
            'status': False,
            'data': None,
            'message': str(e)
        }
    return response

