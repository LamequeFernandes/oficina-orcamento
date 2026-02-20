# from app.modules.usuario.infrastructure.models import (
#     UsuarioModel, ClienteModel, FuncionarioModel
# )  # noqa: F401
# from app.modules.veiculo.infrastructure.models import VeiculoModel  # noqa: F401
# from app.modules.ordem_servico.infrastructure.models import OrdemServicoModel  # noqa: F401
from app.modules.orcamento.infrastructure.models import OrcamentoModel  # noqa: F401
from app.modules.peca.infrastructure.models import TipoPecaModel, PecaModel  # noqa: F401
from app.modules.servico.infrastructure.models import TipoServicoModel, ServicoModel  # noqa: F401

from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


servicos = [
    TipoServicoModel(nome_servico='Troca de óleo', descricao='Substituição do óleo do motor e filtro de óleo'),
    TipoServicoModel(nome_servico='Alinhamento e balanceamento', descricao='Ajuste do alinhamento das rodas e balanceamento dos pneus'),
    TipoServicoModel(nome_servico='Revisão de freios', descricao='Inspeção e substituição de pastilhas, discos ou fluido de freio'),
    TipoServicoModel(nome_servico='Troca de correia dentada', descricao='Substituição da correia dentada e inspeção dos tensores'),
    TipoServicoModel(nome_servico='Troca de bateria', descricao='Substituição da bateria e teste do sistema de carga'),
    TipoServicoModel(nome_servico='Revisão geral', descricao='Verificação completa do veículo conforme checklist'),
    TipoServicoModel(nome_servico='Troca de velas de ignição', descricao='Substituição das velas para melhor desempenho do motor'),
    TipoServicoModel(nome_servico='Troca de amortecedores', descricao='Substituição dos amortecedores e verificação da suspensão'),
    TipoServicoModel(nome_servico='Troca de embreagem', descricao='Substituição do kit de embreagem completo'),
    TipoServicoModel(nome_servico='Limpeza de bicos injetores', descricao='Limpeza ultrassônica dos bicos injetores de combustível'),
    TipoServicoModel(nome_servico='Troca de filtro de ar', descricao='Substituição do filtro de ar do motor'),
    TipoServicoModel(nome_servico='Troca de filtro de combustível', descricao='Substituição do filtro de combustível'),
    TipoServicoModel(nome_servico='Troca de filtro de cabine', descricao='Substituição do filtro de ar-condicionado'),
    TipoServicoModel(nome_servico='Regulagem de motor', descricao='Ajustes finos para melhorar desempenho e consumo'),
    TipoServicoModel(nome_servico='Troca de radiador', descricao='Substituição do radiador e verificação do sistema de arrefecimento'),
    TipoServicoModel(nome_servico='Troca de líquido de arrefecimento', descricao='Substituição do fluido de arrefecimento do motor'),
    TipoServicoModel(nome_servico='Troca de junta do cabeçote', descricao='Substituição da junta e retífica do cabeçote'),
    TipoServicoModel(nome_servico='Troca de escapamento', descricao='Substituição de componentes do sistema de escapamento'),
    TipoServicoModel(nome_servico='Troca de faróis', descricao='Substituição e alinhamento dos faróis'),
    TipoServicoModel(nome_servico='Revisão elétrica', descricao='Inspeção e reparo de componentes elétricos do veículo')
]

# Inserir dados na tabela tipo_peca
pecas = [
    TipoPecaModel(nome_peca='Filtro de óleo', peca_critica=True),
    TipoPecaModel(nome_peca='Filtro de ar', peca_critica=True),
    TipoPecaModel(nome_peca='Filtro de combustível', peca_critica=True),
    TipoPecaModel(nome_peca='Filtro de cabine', peca_critica=False),
    TipoPecaModel(nome_peca='Pastilha de freio', peca_critica=True),
    TipoPecaModel(nome_peca='Disco de freio', peca_critica=True),
    TipoPecaModel(nome_peca='Correia dentada', peca_critica=True),
    TipoPecaModel(nome_peca='Correia auxiliar', peca_critica=True),
    TipoPecaModel(nome_peca='Velas de ignição', peca_critica=True),
    TipoPecaModel(nome_peca='Amortecedor', peca_critica=True),
    TipoPecaModel(nome_peca='Kit de embreagem', peca_critica=True),
    TipoPecaModel(nome_peca='Bateria', peca_critica=True),
    TipoPecaModel(nome_peca='Radiador', peca_critica=True),
    TipoPecaModel(nome_peca='Mangueira do radiador', peca_critica=True),
    TipoPecaModel(nome_peca='Termostato', peca_critica=True),
    TipoPecaModel(nome_peca='Junta do cabeçote', peca_critica=True),
    TipoPecaModel(nome_peca='Silencioso do escapamento', peca_critica=False),
    TipoPecaModel(nome_peca='Farol', peca_critica=False),
    TipoPecaModel(nome_peca='Lâmpada do farol', peca_critica=False),
    TipoPecaModel(nome_peca='Sensor de temperatura', peca_critica=True)
]

