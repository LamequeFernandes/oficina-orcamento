-- Primeiro verifica se o usuário já existe antes de criar
DROP USER IF EXISTS 'lameque'@'localhost';
DROP USER IF EXISTS 'lameque'@'%';

CREATE USER 'lameque'@'localhost' IDENTIFIED BY 'lameque123';

GRANT ALL PRIVILEGES ON *.* TO 'lameque'@'localhost' WITH GRANT OPTION;

CREATE USER 'lameque'@'%' IDENTIFIED BY 'lameque123';

GRANT ALL PRIVILEGES ON *.* TO 'lameque'@'%' WITH GRANT OPTION;


FLUSH PRIVILEGES;

-- Cria o banco de dados se não existir
CREATE DATABASE IF NOT EXISTS oficina_orcamento;
USE oficina_orcamento;

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = 'utf8mb4_unicode_ci';

CREATE TABLE `tipo_peca` (
  `tipo_peca_id` int NOT NULL AUTO_INCREMENT,
  `nome_peca` varchar(255) NOT NULL,
  `peca_critica` tinyint(1) NOT NULL,
  PRIMARY KEY (`tipo_peca_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- oficina_orcamento.tipo_servico definição
CREATE TABLE `tipo_servico` (
  `tipo_servico_id` int NOT NULL AUTO_INCREMENT,
  `nome_servico` varchar(255) NOT NULL,
  `descricao` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`tipo_servico_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- oficina_orcamento.orcamento definição
CREATE TABLE `orcamento` (
  `orcamento_id` int NOT NULL AUTO_INCREMENT,
  `status_orcamento` enum('AGUARDANDO_APROVACAO','APROVADO') NOT NULL,
  -- TODO
  `ordem_servico_id` int NOT NULL,
  `dta_criacao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dta_cancelamento` datetime DEFAULT NULL,
  PRIMARY KEY (`orcamento_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- oficina_orcamento.peca definição
CREATE TABLE `peca` (
  `peca_id` int NOT NULL AUTO_INCREMENT,
  `tipo_peca_id` int NOT NULL,
  `valor_peca` decimal(8,2) NOT NULL,
  `marca` varchar(255) NOT NULL,
  `orcamento_id` int DEFAULT NULL,
  PRIMARY KEY (`peca_id`),
  KEY `tipo_peca_id` (`tipo_peca_id`),
  KEY `orcamento_id` (`orcamento_id`),
  CONSTRAINT `peca_ibfk_1` FOREIGN KEY (`tipo_peca_id`) 
      REFERENCES `tipo_peca` (`tipo_peca_id`) ON DELETE CASCADE,
  CONSTRAINT `peca_ibfk_2` FOREIGN KEY (`orcamento_id`) 
      REFERENCES `orcamento` (`orcamento_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- oficina_orcamento.servico definição
CREATE TABLE `servico` (
  `servico_id` int NOT NULL AUTO_INCREMENT,
  `tipo_servico_id` int NOT NULL,
  `valor_servico` decimal(8,2) NOT NULL,
  `orcamento_id` int NOT NULL,
  PRIMARY KEY (`servico_id`),
  KEY `tipo_servico_id` (`tipo_servico_id`),
  KEY `orcamento_id` (`orcamento_id`),
  CONSTRAINT `servico_ibfk_1` FOREIGN KEY (`tipo_servico_id`) 
      REFERENCES `tipo_servico` (`tipo_servico_id`) ON DELETE CASCADE,
  CONSTRAINT `servico_ibfk_2` FOREIGN KEY (`orcamento_id`) 
      REFERENCES `orcamento` (`orcamento_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Inserts para tipo_servico
INSERT INTO tipo_servico (nome_servico, descricao) VALUES
('Troca de óleo', 'Substituição do óleo do motor e filtro de óleo'),
('Alinhamento e balanceamento', 'Ajuste do alinhamento das rodas e balanceamento dos pneus'),
('Revisão de freios', 'Inspeção e substituição de pastilhas, discos ou fluido de freio'),
('Troca de correia dentada', 'Substituição da correia dentada e inspeção dos tensores'),
('Troca de bateria', 'Substituição da bateria e teste do sistema de carga'),
('Revisão geral', 'Verificação completa do veículo conforme checklist'),
('Troca de velas de ignição', 'Substituição das velas para melhor desempenho do motor'),
('Troca de amortecedores', 'Substituição dos amortecedores e verificação da suspensão'),
('Troca de embreagem', 'Substituição do kit de embreagem completo'),
('Limpeza de bicos injetores', 'Limpeza ultrassônica dos bicos injetores de combustível'),
('Troca de filtro de ar', 'Substituição do filtro de ar do motor'),
('Troca de filtro de combustível', 'Substituição do filtro de combustível'),
('Troca de filtro de cabine', 'Substituição do filtro de ar-condicionado'),
('Regulagem de motor', 'Ajustes finos para melhorar desempenho e consumo'),
('Troca de radiador', 'Substituição do radiador e verificação do sistema de arrefecimento'),
('Troca de líquido de arrefecimento', 'Substituição do fluido de arrefecimento do motor'),
('Troca de junta do cabeçote', 'Substituição da junta e retífica do cabeçote'),
('Troca de escapamento', 'Substituição de componentes do sistema de escapamento'),
('Troca de faróis', 'Substituição e alinhamento dos faróis'),
('Revisão elétrica', 'Inspeção e reparo de componentes elétricos do veículo');


-- Inserts para tipo_peca
INSERT INTO tipo_peca (nome_peca, peca_critica) VALUES
('Filtro de óleo', 1),
('Filtro de ar', 1),
('Filtro de combustível', 1),
('Filtro de cabine', 0),
('Pastilha de freio', 1),
('Disco de freio', 1),
('Correia dentada', 1),
('Correia auxiliar', 1),
('Velas de ignição', 1),
('Amortecedor', 1),
('Kit de embreagem', 1),
('Bateria', 1),
('Radiador', 1),
('Mangueira do radiador', 1),
('Termostato', 1),
('Junta do cabeçote', 1),
('Silencioso do escapamento', 0),
('Farol', 0),
('Lâmpada do farol', 0),
('Sensor de temperatura', 1);
