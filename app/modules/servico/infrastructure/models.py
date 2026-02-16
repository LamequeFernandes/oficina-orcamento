from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base


class TipoServicoModel(Base):
    __tablename__ = 'tipo_servico'

    tipo_servico_id = Column(Integer, primary_key=True, autoincrement=True)
    nome_servico = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=True)


class ServicoModel(Base):
    __tablename__ = 'servico'

    servico_id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_servico_id = Column(
        Integer, ForeignKey('tipo_servico.tipo_servico_id', ondelete="CASCADE"), nullable=False
    )
    valor_servico = Column(Numeric(8, 2), nullable=False)
    orcamento_id = Column(
        Integer, ForeignKey('orcamento.orcamento_id', ondelete="CASCADE"), nullable=False
    )

    tipo_servico = relationship('TipoServicoModel')
    orcamento = relationship('OrcamentoModel', back_populates='servicos')
