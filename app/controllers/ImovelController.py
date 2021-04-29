from sqlalchemy.exc import SQLAlchemyError

from app.database.base import Session
from app.models.Model import Imoveis


def updateimovel(data):
    session = Session(expire_on_commit=False)
    try:

        session.query(Imoveis).filter(Imoveis.ID_IMOVEL == data).update({
            'STATUS': 'Reservado'
        })

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