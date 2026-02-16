from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class OrcamentoModel(Base):
    __tablename__ = 'orcamento'

    orcamento_id = Column(Integer, primary_key=True, autoincrement=True)
    status_orcamento = Column(
        Enum('AGUARDANDO_APROVACAO', 'APROVADO', name='status_orcamento'),
        nullable=False,
    )
    ordem_servico_id = Column((Integer), nullable=True)
    dta_criacao = Column(DateTime, default=datetime.now)
    dta_cancelamento = Column(DateTime, nullable=True)
    # funcionario_id = Column(
    #     Integer, ForeignKey('funcionario.funcionario_id', ondelete="CASCADE"), nullable=False
    # )

    # Relacionamentos
    # ordem_servico = relationship(
    #     'OrdemServicoModel', back_populates='orcamento', uselist=False
    # )
    # funcionario = relationship(
    #     'FuncionarioModel', back_populates='orcamentos', uselist=False
    # )
    servicos = relationship('ServicoModel', back_populates='orcamento')
    pecas = relationship('PecaModel', back_populates='orcamento')
