from sqlalchemy.exc import SQLAlchemyError

from app.database.base import Session
from app.models.Model import Pedidos


def criarpedido(data):
    session = Session(expire_on_commit=False)
    try:
        pedido = Pedidos()

        pedido.PAGAMENTO = data["PAGAMENTO"]
        pedido.ID_VENDEDOR = data["ID_VENDEDOR"]
        pedido.ID_CLIENTE = data["ID_CLIENTE"]
        pedido.imovel_id = data["imovel_id"]


        session.add(pedido)
        session.commit()
        session.close()

        response = {
            'status': True,
            'data': pedido,
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

def readpedido(data):
    session = Session()
    try:

        result = session.query(Pedidos).filter(Pedidos.ID_PEDIDO == data).one()

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