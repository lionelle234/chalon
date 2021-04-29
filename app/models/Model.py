from flask_login import UserMixin
from sqlalchemy import Column, Numeric, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

from app.database.base import Base, session


class Imoveis(Base):
    __tablename__ = 'Imovel'

    ID_IMOVEL = Column(Integer, primary_key=True)
    NOME = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ENDERECO = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    VALOR_VENDA = Column(Numeric(10, 2), nullable=False)
    VALOR_COMIS = Column(Numeric(10, 2), nullable=False)
    STATUS = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    Pedido = relationship("Pedidos", uselist=False, back_populates="Imovel")

    def read_apt(self):
        return session.query(self) \
            .order_by(self.ID_IMOVEL) \



class Pedidos(Base):
    __tablename__ = 'Pedido'

    ID_PEDIDO = Column(Integer, primary_key=True)
    PAGAMENTO = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    ID_VENDEDOR = Column(Integer, ForeignKey('Vendedor.ID_VENDEDOR'))
    ID_CLIENTE = Column(Integer, ForeignKey('Cliente.ID_CLIENTE'))

    imovel_id = Column(Integer, ForeignKey('Imovel.ID_IMOVEL'))
    Imovel = relationship("Imoveis", back_populates="Pedido")




class Vendedores(UserMixin, Base):
    __tablename__ = 'Vendedor'

    ID_VENDEDOR = Column(Integer, primary_key=True)
    USUARIO = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SENHA = Column(String(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    orders1 = relationship('Pedidos')

    def senha_hash(self, password):
        self.SENHA = generate_password_hash(password)

    def get_id(self):
        return (self.ID_VENDEDOR)

    def get_name(self):
        return self.USUARIO




class Clientes(Base):
    __tablename__ = 'Cliente'

    ID_CLIENTE = Column(Integer, primary_key=True)
    NOME = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CPF = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    EMAIL = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TELEFONE = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    orders2 = relationship('Pedidos')

    def read_client(self):
        return session.query(self.NOME) \
            .order_by(self.ID_CLIENTE) \

    def read_client_all(self):
        return session.query(self) \
            .order_by(self.ID_CLIENTE) \



