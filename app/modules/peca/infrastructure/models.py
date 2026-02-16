from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base


class TipoPecaModel(Base):
    __tablename__ = 'tipo_peca'

    tipo_peca_id = Column(Integer, primary_key=True, autoincrement=True)
    nome_peca = Column(String(255), nullable=False)
    peca_critica = Column(Boolean, default=False, nullable=False)


class PecaModel(Base):
    __tablename__ = 'peca'

    peca_id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_peca_id = Column(
        Integer, ForeignKey('tipo_peca.tipo_peca_id', ondelete="CASCADE"), nullable=False
    )
    valor_peca = Column(Numeric(8, 2), nullable=False)
    marca = Column(String(255), nullable=False)
    orcamento_id = Column(
        Integer, ForeignKey('orcamento.orcamento_id', ondelete="CASCADE"), nullable=True
    )

    tipo_peca = relationship('TipoPecaModel')
    orcamento = relationship(
        'OrcamentoModel', back_populates='pecas', uselist=False
    )
