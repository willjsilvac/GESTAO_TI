import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Sidebar } from '@/components/Sidebar.jsx'
import { Dashboard } from '@/components/Dashboard.jsx'
import { Usuarios } from '@/components/Usuarios.jsx'
import { Compras } from '@/components/Compras.jsx'
import { Ativos } from '@/components/Ativos.jsx'
import { Chamados } from '@/components/Chamados.jsx'
import { Inventario } from '@/components/Inventario.jsx'
import { ContasMensais } from '@/components/ContasMensais.jsx'
import { Building2, LogIn } from 'lucide-react'
import './App.css'

function App() {
  const [usuario, setUsuario] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Verificar se há usuário logado no localStorage
    const usuarioSalvo = localStorage.getItem('usuario')
    if (usuarioSalvo) {
      setUsuario(JSON.parse(usuarioSalvo))
    }
    setLoading(false)
  }, [])

  const handleLogin = async (email, senha) => {
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, senha }),
      })

      if (response.ok) {
        const data = await response.json()
        setUsuario(data.usuario)
        localStorage.setItem('usuario', JSON.stringify(data.usuario))
        return { success: true }
      } else {
        const error = await response.json()
        return { success: false, error: error.erro }
      }
    } catch (error) {
      return { success: false, error: 'Erro de conexão' }
    }
  }

  const handleLogout = () => {
    setUsuario(null)
    localStorage.removeItem('usuario')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!usuario) {
    return <LoginForm onLogin={handleLogin} />
  }

  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Sidebar usuario={usuario} onLogout={handleLogout} />
        <main className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/usuarios" element={<Usuarios />} />
            <Route path="/compras" element={<Compras />} />
            <Route path="/ativos" element={<Ativos />} />
            <Route path="/chamados" element={<Chamados />} />
            <Route path="/inventario" element={<Inventario />} />
            <Route path="/contas-mensais" element={<ContasMensais />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function LoginForm({ onLogin }) {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const result = await onLogin(email, senha)
    
    if (!result.success) {
      setError(result.error)
    }
    
    setLoading(false)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <Building2 className="h-12 w-12 text-primary" />
          </div>
          <CardTitle className="text-2xl">Sistema de Gestão Integrada</CardTitle>
          <CardDescription>Faça login para acessar o sistema</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="seu@email.com"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="senha">Senha</Label>
              <Input
                id="senha"
                type="password"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                required
                placeholder="••••••••"
              />
            </div>
            {error && (
              <div className="text-red-600 text-sm text-center">{error}</div>
            )}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              ) : (
                <LogIn className="h-4 w-4 mr-2" />
              )}
              {loading ? 'Entrando...' : 'Entrar'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default App
