# Sistema de Gestão Integrada para TI

Um sistema completo de gestão para processos de TI, desenvolvido com Flask (backend) e React (frontend).

## 🚀 Funcionalidades

- **Gestão de Compras**: Controle de fornecedores, pedidos e processos de aquisição
- **Controle de Ativos**: Gerenciamento de patrimônio com depreciação automática
- **Sistema de Chamados**: Atendimento e suporte técnico estruturado
- **Inventário**: Controle de estoque com alertas automáticos
- **Gestão de Usuários**: Controle de acesso com diferentes perfis
- **Contas Mensais**: Controle de despesas recorrentes e orçamento

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.11
- Flask
- SQLAlchemy
- PostgreSQL
- bcrypt

### Frontend
- React 18
- Vite
- Tailwind CSS
- shadcn/ui
- React Router DOM

## 📋 Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- Git

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd sistema-gestao-ti
```

### 2. Configure o Backend

```bash
# Instale o PostgreSQL
sudo apt install postgresql postgresql-contrib

# Crie o banco de dados
sudo -u postgres createdb gestao_ti
sudo -u postgres psql -c "CREATE USER gestao_app WITH PASSWORD 'sua_senha';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE gestao_ti TO gestao_app;"

# Configure o ambiente Python
cd gestao_ti_system
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Inicialize o banco de dados
python -c "from src.main import app, db; app.app_context().push(); db.create_all()"
```

### 3. Configure o Frontend

```bash
# Instale as dependências
cd gestao-ti-frontend
npm install -g pnpm
pnpm install

# Configure as variáveis de ambiente
cp .env.example .env.local
# Edite o arquivo .env.local conforme necessário
```

## 🚀 Executando o Sistema

### Desenvolvimento

**Backend:**
```bash
cd gestao_ti_system
source venv/bin/activate
python src/main.py
```

**Frontend:**
```bash
cd gestao-ti-frontend
pnpm run dev
```

### Produção

**Backend:**
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
```

**Frontend:**
```bash
pnpm run build
# Sirva os arquivos da pasta dist/ com nginx ou outro servidor web
```

## 👤 Acesso Inicial

**Usuário padrão:**
- Email: `admin@empresa.com`
- Senha: `admin123`

⚠️ **Importante**: Altere a senha padrão após o primeiro acesso!

## 📁 Estrutura do Projeto

```
sistema-gestao-ti/
├── gestao_ti_system/          # Backend Flask
│   ├── src/
│   │   ├── models/            # Modelos do banco de dados
│   │   ├── routes/            # Rotas da API
│   │   ├── config.py          # Configurações
│   │   └── main.py            # Aplicação principal
│   ├── requirements.txt       # Dependências Python
│   └── database_schema.sql    # Schema do banco
├── gestao-ti-frontend/        # Frontend React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── App.jsx           # Componente principal
│   │   └── main.jsx          # Ponto de entrada
│   ├── package.json          # Dependências Node.js
│   └── vite.config.js        # Configuração do Vite
└── documentacao_sistema_gestao_ti.md  # Documentação completa
```

## 🔒 Segurança

- Autenticação com hash bcrypt
- Controle de acesso baseado em perfis
- Validação de dados no frontend e backend
- Logs de auditoria para todas as operações
- Proteção contra SQL injection via SQLAlchemy

## 📊 Perfis de Usuário

- **Solicitante**: Acesso básico para abertura de chamados
- **Técnico**: Atendimento de chamados e consultas
- **Admin**: Acesso completo aos módulos
- **Super Admin**: Acesso irrestrito ao sistema

## 🔄 API Endpoints

### Autenticação
- `POST /api/login` - Login de usuário
- `POST /api/logout` - Logout de usuário

### Usuários
- `GET /api/usuarios` - Listar usuários
- `POST /api/usuarios` - Criar usuário
- `PUT /api/usuarios/{id}` - Atualizar usuário
- `DELETE /api/usuarios/{id}` - Desativar usuário

### Compras
- `GET /api/compras` - Listar compras
- `POST /api/compras` - Criar compra
- `GET /api/fornecedores` - Listar fornecedores

### Ativos
- `GET /api/ativos` - Listar ativos
- `POST /api/ativos` - Criar ativo

### Chamados
- `GET /api/chamados` - Listar chamados
- `POST /api/chamados` - Criar chamado

### Inventário
- `GET /api/inventario` - Listar itens
- `POST /api/inventario` - Criar item

### Contas Mensais
- `GET /api/contas-mensais` - Listar contas
- `POST /api/contas-mensais` - Criar conta

### Dashboard
- `GET /api/dashboard/estatisticas` - Estatísticas gerais
- `GET /api/dashboard/alertas` - Alertas do sistema

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema:

- Consulte a documentação completa em `documentacao_sistema_gestao_ti.md`
- Abra uma issue no repositório do projeto
- Entre em contato com a equipe de desenvolvimento

## 🔄 Changelog

### v1.0.0 (12/08/2025)
- Lançamento inicial do sistema
- Implementação de todos os módulos principais
- Interface responsiva e moderna
- Documentação completa
- Testes de integração

---

**Desenvolvido com ❤️ pela equipe Manus AI**

