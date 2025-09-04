# Guia de Instalação Rápida - Sistema de Gestão Integrada TI

## ⚡ Instalação Express (Ubuntu/Debian)

### 1. Preparação do Sistema
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nodejs npm git curl

# Instalar pnpm
npm install -g pnpm
```

### 2. Configurar PostgreSQL
```bash
# Iniciar PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Criar banco e usuário
sudo -u postgres createdb gestao_ti
sudo -u postgres psql -c "CREATE USER gestao_app WITH PASSWORD 'gestao123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE gestao_ti TO gestao_app;"
sudo -u postgres psql -d gestao_ti -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gestao_app;"
sudo -u postgres psql -d gestao_ti -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gestao_app;"
```

### 3. Configurar Backend
```bash
# Navegar para pasta do backend
cd gestao_ti_system

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Aplicar schema do banco
sudo -u postgres psql -d gestao_ti -f ../database_schema.sql

# Corrigir senha do admin
python fix_admin_password.py
```

### 4. Configurar Frontend
```bash
# Navegar para pasta do frontend
cd ../gestao-ti-frontend

# Instalar dependências
pnpm install
```

### 5. Executar Sistema

**Terminal 1 - Backend:**
```bash
cd gestao_ti_system
source venv/bin/activate
python src/main.py
```

**Terminal 2 - Frontend:**
```bash
cd gestao-ti-frontend
pnpm run dev --host
```

### 6. Acessar Sistema

- **URL:** http://localhost:5173
- **Usuário:** admin@empresa.com
- **Senha:** admin123

## 🔧 Configuração de Produção

### Nginx (Frontend)
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        root /caminho/para/gestao-ti-frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Gunicorn (Backend)
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar em produção
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
```

### Systemd Service
```ini
# /etc/systemd/system/gestao-ti.service
[Unit]
Description=Sistema de Gestao TI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/caminho/para/gestao_ti_system
Environment=PATH=/caminho/para/gestao_ti_system/venv/bin
ExecStart=/caminho/para/gestao_ti_system/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🚨 Solução de Problemas

### Erro de Permissão PostgreSQL
```bash
sudo -u postgres psql -d gestao_ti -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gestao_app;"
```

### Erro de Conexão Backend
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar logs
tail -f /var/log/postgresql/postgresql-*.log
```

### Frontend não carrega
```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
pnpm install
pnpm run dev
```

## 📋 Checklist de Instalação

- [ ] Sistema operacional atualizado
- [ ] PostgreSQL instalado e configurado
- [ ] Python 3.11 e dependências instaladas
- [ ] Node.js e pnpm instalados
- [ ] Banco de dados criado e configurado
- [ ] Schema aplicado ao banco
- [ ] Backend executando na porta 5000
- [ ] Frontend executando na porta 5173
- [ ] Login funcionando com admin@empresa.com
- [ ] Todos os módulos acessíveis

## 🔐 Credenciais Padrão

**Administrador:**
- Email: admin@empresa.com
- Senha: admin123
- Perfil: Super Admin

⚠️ **IMPORTANTE:** Altere a senha padrão imediatamente após o primeiro acesso!

## 📞 Suporte

Em caso de problemas:
1. Consulte os logs do sistema
2. Verifique a documentação completa
3. Verifique se todos os serviços estão rodando
4. Confirme as configurações de rede e firewall

---
**Tempo estimado de instalação:** 15-30 minutos

