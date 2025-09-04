import React, { useState, useEffect } from 'react';
import { Settings, Moon, Sun, User, Mail, Server, Image, Shield } from 'lucide-react';

const Configuracoes = () => {
  const [tema, setTema] = useState('claro');
  const [senhaAtual, setSenhaAtual] = useState('');
  const [novaSenha, setNovaSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');
  const [novoEmail, setNovoEmail] = useState('');
  const [senhaEmail, setSenhaEmail] = useState('');
  const [smtpConfig, setSmtpConfig] = useState({
    host: '',
    port: '',
    username: '',
    password: '',
    use_tls: true,
    from_email: ''
  });
  const [logoFile, setLogoFile] = useState(null);
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('geral');

  useEffect(() => {
    // Carregar dados do usuário do localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
    
    // Carregar configurações SMTP se for admin
    if (user && (user.perfil === 'admin' || user.perfil === 'superadmin')) {
      carregarConfigSMTP();
    }
  }, [user]);

  const carregarConfigSMTP = async () => {
    try {
      const response = await fetch('/api/configuracoes/smtp');
      if (response.ok) {
        const config = await response.json();
        setSmtpConfig(prev => ({ ...prev, ...config }));
      }
    } catch (error) {
      console.error('Erro ao carregar configurações SMTP:', error);
    }
  };

  const alterarTema = async (novoTema) => {
    try {
      const response = await fetch('/api/configuracoes/tema', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tema: novoTema }),
      });

      if (response.ok) {
        setTema(novoTema);
        // Aplicar tema ao documento
        document.documentElement.setAttribute('data-theme', novoTema);
        alert('Tema alterado com sucesso!');
      }
    } catch (error) {
      console.error('Erro ao alterar tema:', error);
      alert('Erro ao alterar tema');
    }
  };

  const alterarSenha = async (e) => {
    e.preventDefault();
    
    if (novaSenha !== confirmarSenha) {
      alert('As senhas não coincidem');
      return;
    }

    try {
      const response = await fetch('/api/configuracoes/alterar-senha', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.id,
          senha_atual: senhaAtual,
          nova_senha: novaSenha,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        alert('Senha alterada com sucesso!');
        setSenhaAtual('');
        setNovaSenha('');
        setConfirmarSenha('');
      } else {
        alert(data.erro || 'Erro ao alterar senha');
      }
    } catch (error) {
      console.error('Erro ao alterar senha:', error);
      alert('Erro ao alterar senha');
    }
  };

  const alterarEmail = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/configuracoes/alterar-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.id,
          novo_email: novoEmail,
          senha: senhaEmail,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        alert('Email alterado com sucesso!');
        setNovoEmail('');
        setSenhaEmail('');
        // Atualizar dados do usuário no localStorage
        const updatedUser = { ...user, email: novoEmail };
        localStorage.setItem('user', JSON.stringify(updatedUser));
        setUser(updatedUser);
      } else {
        alert(data.erro || 'Erro ao alterar email');
      }
    } catch (error) {
      console.error('Erro ao alterar email:', error);
      alert('Erro ao alterar email');
    }
  };

  const salvarConfigSMTP = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/configuracoes/smtp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...smtpConfig,
          user_id: user.id,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        alert('Configurações SMTP salvas com sucesso!');
      } else {
        alert(data.erro || 'Erro ao salvar configurações SMTP');
      }
    } catch (error) {
      console.error('Erro ao salvar configurações SMTP:', error);
      alert('Erro ao salvar configurações SMTP');
    }
  };

  const uploadLogo = async (e) => {
    e.preventDefault();

    if (!logoFile) {
      alert('Selecione um arquivo de logo');
      return;
    }

    const formData = new FormData();
    formData.append('logo', logoFile);
    formData.append('user_id', user.id);

    try {
      const response = await fetch('/api/configuracoes/logo', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      if (response.ok) {
        alert('Logo atualizado com sucesso!');
        setLogoFile(null);
      } else {
        alert(data.erro || 'Erro ao atualizar logo');
      }
    } catch (error) {
      console.error('Erro ao atualizar logo:', error);
      alert('Erro ao atualizar logo');
    }
  };

  const isAdmin = user && (user.perfil === 'admin' || user.perfil === 'superadmin');

  return (
    <div className="p-6">
      <div className="flex items-center gap-3 mb-6">
        <Settings className="h-8 w-8 text-blue-600" />
        <h1 className="text-3xl font-bold text-gray-900">Configurações</h1>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('geral')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'geral'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Geral
          </button>
          <button
            onClick={() => setActiveTab('seguranca')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'seguranca'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Segurança
          </button>
          {isAdmin && (
            <button
              onClick={() => setActiveTab('admin')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'admin'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Administração
            </button>
          )}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'geral' && (
        <div className="space-y-6">
          {/* Tema */}
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center gap-3 mb-4">
              {tema === 'claro' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              <h2 className="text-xl font-semibold">Tema</h2>
            </div>
            <div className="flex gap-4">
              <button
                onClick={() => alterarTema('claro')}
                className={`px-4 py-2 rounded-lg border ${
                  tema === 'claro'
                    ? 'bg-blue-500 text-white border-blue-500'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
              >
                <Sun className="h-4 w-4 inline mr-2" />
                Claro
              </button>
              <button
                onClick={() => alterarTema('escuro')}
                className={`px-4 py-2 rounded-lg border ${
                  tema === 'escuro'
                    ? 'bg-blue-500 text-white border-blue-500'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
              >
                <Moon className="h-4 w-4 inline mr-2" />
                Escuro
              </button>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'seguranca' && (
        <div className="space-y-6">
          {/* Alterar Senha */}
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center gap-3 mb-4">
              <Shield className="h-5 w-5" />
              <h2 className="text-xl font-semibold">Alterar Senha</h2>
            </div>
            <form onSubmit={alterarSenha} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Senha Atual
                </label>
                <input
                  type="password"
                  value={senhaAtual}
                  onChange={(e) => setSenhaAtual(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nova Senha
                </label>
                <input
                  type="password"
                  value={novaSenha}
                  onChange={(e) => setNovaSenha(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Confirmar Nova Senha
                </label>
                <input
                  type="password"
                  value={confirmarSenha}
                  onChange={(e) => setConfirmarSenha(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <button
                type="submit"
                className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
              >
                Alterar Senha
              </button>
            </form>
          </div>
        </div>
      )}

      {activeTab === 'admin' && isAdmin && (
        <div className="space-y-6">
          {/* Alterar Email */}
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center gap-3 mb-4">
              <Mail className="h-5 w-5" />
              <h2 className="text-xl font-semibold">Alterar Email</h2>
            </div>
            <form onSubmit={alterarEmail} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Novo Email
                </label>
                <input
                  type="email"
                  value={novoEmail}
                  onChange={(e) => setNovoEmail(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Confirmar com Senha
                </label>
                <input
                  type="password"
                  value={senhaEmail}
                  onChange={(e) => setSenhaEmail(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <button
                type="submit"
                className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
              >
                Alterar Email
              </button>
            </form>
          </div>

          {/* Configuração SMTP */}
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center gap-3 mb-4">
              <Server className="h-5 w-5" />
              <h2 className="text-xl font-semibold">Configuração SMTP</h2>
            </div>
            <form onSubmit={salvarConfigSMTP} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Servidor SMTP
                  </label>
                  <input
                    type="text"
                    value={smtpConfig.host}
                    onChange={(e) => setSmtpConfig(prev => ({ ...prev, host: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="smtp.gmail.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Porta
                  </label>
                  <input
                    type="number"
                    value={smtpConfig.port}
                    onChange={(e) => setSmtpConfig(prev => ({ ...prev, port: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="587"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Usuário
                </label>
                <input
                  type="text"
                  value={smtpConfig.username}
                  onChange={(e) => setSmtpConfig(prev => ({ ...prev, username: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Senha
                </label>
                <input
                  type="password"
                  value={smtpConfig.password}
                  onChange={(e) => setSmtpConfig(prev => ({ ...prev, password: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email de Envio
                </label>
                <input
                  type="email"
                  value={smtpConfig.from_email}
                  onChange={(e) => setSmtpConfig(prev => ({ ...prev, from_email: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={smtpConfig.use_tls}
                  onChange={(e) => setSmtpConfig(prev => ({ ...prev, use_tls: e.target.checked }))}
                  className="mr-2"
                />
                <label className="text-sm text-gray-700">Usar TLS</label>
              </div>
              <button
                type="submit"
                className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
              >
                Salvar Configurações SMTP
              </button>
            </form>
          </div>

          {/* Upload Logo */}
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center gap-3 mb-4">
              <Image className="h-5 w-5" />
              <h2 className="text-xl font-semibold">Logo da Empresa</h2>
            </div>
            <form onSubmit={uploadLogo} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Arquivo do Logo
                </label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setLogoFile(e.target.files[0])}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Formatos aceitos: PNG, JPG, JPEG. Tamanho máximo: 2MB
                </p>
              </div>
              <button
                type="submit"
                className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
              >
                Atualizar Logo
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Configuracoes;

