-- Sistema de Gestão Integrada de TI
-- Esquema do Banco de Dados PostgreSQL

-- Tabela de Usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    perfil VARCHAR(20) NOT NULL CHECK (perfil IN ('solicitante', 'tecnico', 'admin', 'superadmin')),
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Centros de Custo
CREATE TABLE centros_custo (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Fornecedores
CREATE TABLE fornecedores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) UNIQUE,
    email VARCHAR(255),
    telefone VARCHAR(20),
    endereco TEXT,
    contato_responsavel VARCHAR(255),
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Compras
CREATE TABLE compras (
    id SERIAL PRIMARY KEY,
    fornecedor_id INTEGER REFERENCES fornecedores(id),
    centro_custo_id INTEGER REFERENCES centros_custo(id),
    usuario_solicitante_id INTEGER REFERENCES usuarios(id),
    numero_pedido VARCHAR(100) UNIQUE,
    descricao TEXT NOT NULL,
    valor_total DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('solicitado', 'aprovado', 'em_andamento', 'entregue', 'cancelado')),
    data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_aquisicao DATE,
    anexo_pedido VARCHAR(500),
    anexo_nota_fiscal VARCHAR(500),
    anexo_boleto VARCHAR(500),
    observacoes TEXT
);

-- Tabela de Produtos Adquiridos
CREATE TABLE produtos_adquiridos (
    id SERIAL PRIMARY KEY,
    compra_id INTEGER REFERENCES compras(id),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    quantidade INTEGER NOT NULL DEFAULT 1,
    valor_unitario DECIMAL(15,2) NOT NULL,
    valor_total DECIMAL(15,2) NOT NULL
);

-- Tabela de Rateio de Compras
CREATE TABLE rateio_compras (
    id SERIAL PRIMARY KEY,
    compra_id INTEGER REFERENCES compras(id),
    centro_custo_id INTEGER REFERENCES centros_custo(id),
    percentual DECIMAL(5,2) NOT NULL,
    valor DECIMAL(15,2) NOT NULL
);

-- Tabela de Ativos
CREATE TABLE ativos (
    id SERIAL PRIMARY KEY,
    tipo_ativo VARCHAR(50) NOT NULL CHECK (tipo_ativo IN ('hardware', 'software', 'licenca', 'equipamento', 'mobiliario')),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    numero_serie VARCHAR(100),
    localizacao VARCHAR(255),
    responsavel_id INTEGER REFERENCES usuarios(id),
    centro_custo_id INTEGER REFERENCES centros_custo(id),
    data_aquisicao DATE NOT NULL,
    valor_aquisicao DECIMAL(15,2),
    valor_atual DECIMAL(15,2),
    percentual_depreciacao DECIMAL(5,2) DEFAULT 30.00,
    data_vencimento_licenca DATE,
    status VARCHAR(20) DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'manutencao', 'descartado')),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Chamados
CREATE TABLE chamados (
    id SERIAL PRIMARY KEY,
    numero_chamado VARCHAR(20) UNIQUE NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    solicitante_id INTEGER REFERENCES usuarios(id),
    tecnico_atribuido_id INTEGER REFERENCES usuarios(id),
    prioridade VARCHAR(10) NOT NULL CHECK (prioridade IN ('baixa', 'media', 'alta', 'critica')),
    status VARCHAR(20) NOT NULL DEFAULT 'aberto' CHECK (status IN ('aberto', 'em_andamento', 'aguardando', 'resolvido', 'fechado')),
    categoria VARCHAR(50),
    anexo_evidencia VARCHAR(500),
    data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atribuicao TIMESTAMP,
    data_resolucao TIMESTAMP,
    data_fechamento TIMESTAMP,
    solucao TEXT
);

-- Tabela de Histórico de Chamados
CREATE TABLE historico_chamados (
    id SERIAL PRIMARY KEY,
    chamado_id INTEGER REFERENCES chamados(id),
    usuario_id INTEGER REFERENCES usuarios(id),
    acao VARCHAR(100) NOT NULL,
    descricao TEXT,
    status_anterior VARCHAR(20),
    status_novo VARCHAR(20),
    data_acao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Inventário
CREATE TABLE inventario (
    id SERIAL PRIMARY KEY,
    tipo_item VARCHAR(50) NOT NULL CHECK (tipo_item IN ('hardware', 'licenca_periodica', 'licenca_perpetua')),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    quantidade INTEGER NOT NULL DEFAULT 0,
    quantidade_minima INTEGER DEFAULT 0,
    localizacao VARCHAR(255),
    centro_custo_id INTEGER REFERENCES centros_custo(id),
    fornecedor_id INTEGER REFERENCES fornecedores(id),
    valor_unitario DECIMAL(15,2),
    data_vencimento_licenca DATE,
    observacoes TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Movimentação de Inventário
CREATE TABLE movimentacao_inventario (
    id SERIAL PRIMARY KEY,
    inventario_id INTEGER REFERENCES inventario(id),
    usuario_id INTEGER REFERENCES usuarios(id),
    tipo_movimentacao VARCHAR(20) NOT NULL CHECK (tipo_movimentacao IN ('entrada', 'saida', 'transferencia', 'ajuste')),
    quantidade INTEGER NOT NULL,
    quantidade_anterior INTEGER NOT NULL,
    quantidade_nova INTEGER NOT NULL,
    motivo TEXT,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Contas Mensais
CREATE TABLE contas_mensais (
    id SERIAL PRIMARY KEY,
    tipo_conta VARCHAR(100) NOT NULL,
    fornecedor_id INTEGER REFERENCES fornecedores(id),
    centro_custo_id INTEGER REFERENCES centros_custo(id),
    valor DECIMAL(15,2) NOT NULL,
    data_vencimento DATE NOT NULL,
    status_pagamento VARCHAR(20) NOT NULL DEFAULT 'pendente' CHECK (status_pagamento IN ('pendente', 'pago', 'vencido', 'cancelado')),
    recorrencia VARCHAR(20) CHECK (recorrencia IN ('mensal', 'bimestral', 'trimestral', 'semestral', 'anual', 'unica')),
    data_contratacao DATE,
    descricao TEXT,
    anexo_contrato VARCHAR(500),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_pagamento TIMESTAMP
);

-- Índices para melhor performance
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_compras_status ON compras(status);
CREATE INDEX idx_compras_data_solicitacao ON compras(data_solicitacao);
CREATE INDEX idx_ativos_tipo ON ativos(tipo_ativo);
CREATE INDEX idx_ativos_status ON ativos(status);
CREATE INDEX idx_chamados_status ON chamados(status);
CREATE INDEX idx_chamados_prioridade ON chamados(prioridade);
CREATE INDEX idx_chamados_data_abertura ON chamados(data_abertura);
CREATE INDEX idx_inventario_tipo ON inventario(tipo_item);
CREATE INDEX idx_contas_vencimento ON contas_mensais(data_vencimento);
CREATE INDEX idx_contas_status ON contas_mensais(status_pagamento);

-- Triggers para atualização automática de timestamps
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_usuarios_update
    BEFORE UPDATE ON usuarios
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_ativos_update
    BEFORE UPDATE ON ativos
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_inventario_update
    BEFORE UPDATE ON inventario
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

-- Função para calcular depreciação automática
CREATE OR REPLACE FUNCTION calcular_depreciacao(
    valor_aquisicao DECIMAL,
    data_aquisicao DATE,
    percentual_depreciacao DECIMAL DEFAULT 30.00
)
RETURNS DECIMAL AS $$
DECLARE
    anos_decorridos DECIMAL;
    valor_depreciado DECIMAL;
BEGIN
    anos_decorridos := EXTRACT(YEAR FROM AGE(CURRENT_DATE, data_aquisicao));
    valor_depreciado := valor_aquisicao * (percentual_depreciacao / 100) * anos_decorridos;
    
    IF valor_depreciado > valor_aquisicao THEN
        valor_depreciado := valor_aquisicao;
    END IF;
    
    RETURN valor_aquisicao - valor_depreciado;
END;
$$ LANGUAGE plpgsql;

-- Trigger para atualizar valor atual dos ativos automaticamente
CREATE OR REPLACE FUNCTION atualizar_valor_ativo()
RETURNS TRIGGER AS $$
BEGIN
    NEW.valor_atual := calcular_depreciacao(NEW.valor_aquisicao, NEW.data_aquisicao, NEW.percentual_depreciacao);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_ativos_depreciacao
    BEFORE INSERT OR UPDATE ON ativos
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_valor_ativo();

-- Inserção de dados iniciais
INSERT INTO centros_custo (codigo, nome, descricao) VALUES
('TI001', 'Tecnologia da Informação', 'Centro de custo para área de TI'),
('ADM001', 'Administrativo', 'Centro de custo administrativo'),
('FIN001', 'Financeiro', 'Centro de custo financeiro');

INSERT INTO usuarios (nome, email, senha, perfil) VALUES
('Administrador', 'admin@empresa.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5S/kS', 'superadmin');
-- Senha padrão: admin123

