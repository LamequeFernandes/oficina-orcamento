-- Migração: adiciona suporte a rastreamento de pagamento via Mercado Pago
-- Execute este script se o banco de dados já existir

USE oficina_orcamento;

-- 1. Adiciona as colunas de pagamento na tabela orcamento
ALTER TABLE `orcamento`
    ADD COLUMN IF NOT EXISTS `url_pagamento`  VARCHAR(255) DEFAULT NULL AFTER `dta_cancelamento`,
    ADD COLUMN IF NOT EXISTS `preference_id`  VARCHAR(255) DEFAULT NULL AFTER `url_pagamento`,
    ADD COLUMN IF NOT EXISTS `mp_payment_id`  VARCHAR(100) DEFAULT NULL AFTER `preference_id`;

-- 2. Adiciona o valor PAGO ao ENUM de status_orcamento
ALTER TABLE `orcamento`
    MODIFY COLUMN `status_orcamento`
        ENUM('AGUARDANDO_APROVACAO', 'APROVADO', 'PAGO') NOT NULL;

-- 3. Torna orcamento_id opcional na tabela servico (serviço pode existir sem orçamento)
ALTER TABLE `servico`
    MODIFY COLUMN `orcamento_id` INT DEFAULT NULL;
