import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  ShoppingCart, 
  Package, 
  Headphones, 
  Archive, 
  CreditCard, 
  AlertTriangle,
  CheckCircle,
  Clock,
  TrendingUp
} from 'lucide-react'

export function Dashboard() {
  const [estatisticas, setEstatisticas] = useState(null)
  const [alertas, setAlertas] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    carregarDados()
  }, [])

  const carregarDados = async () => {
    try {
      const [estatisticasRes, alertasRes] = await Promise.all([
        fetch('/api/dashboard/estatisticas'),
        fetch('/api/dashboard/alertas')
      ])

      if (estatisticasRes.ok && alertasRes.ok) {
        const estatisticasData = await estatisticasRes.json()
        const alertasData = await alertasRes.json()
        
        setEstatisticas(estatisticasData)
        setAlertas(alertasData)
      }
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  const estatisticasCards = [
    {
      title: 'Compras',
      icon: ShoppingCart,
      stats: estatisticas?.compras || {},
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Chamados',
      icon: Headphones,
      stats: estatisticas?.chamados || {},
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'Ativos',
      icon: Package,
      stats: estatisticas?.ativos || {},
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      title: 'Inventário',
      icon: Archive,
      stats: estatisticas?.inventario || {},
      color: 'text-orange-600',
      bgColor: 'bg-orange-50'
    }
  ]

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Visão geral do sistema de gestão integrada</p>
      </div>

      {/* Alertas */}
      {alertas.length > 0 && (
        <Card className="border-orange-200 bg-orange-50">
          <CardHeader>
            <CardTitle className="flex items-center text-orange-800">
              <AlertTriangle className="h-5 w-5 mr-2" />
              Alertas Importantes
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {alertas.map((alerta, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-white rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className={`w-2 h-2 rounded-full ${
                      alerta.tipo === 'critico' ? 'bg-red-500' : 'bg-yellow-500'
                    }`}></div>
                    <span className="text-sm font-medium">{alerta.mensagem}</span>
                  </div>
                  <Badge variant={alerta.tipo === 'critico' ? 'destructive' : 'secondary'}>
                    {alerta.modulo}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Estatísticas Principais */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {estatisticasCards.map((card) => {
          const Icon = card.icon
          return (
            <Card key={card.title}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{card.title}</CardTitle>
                <div className={`p-2 rounded-lg ${card.bgColor}`}>
                  <Icon className={`h-4 w-4 ${card.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="text-2xl font-bold">
                    {card.stats.total || 0}
                  </div>
                  <div className="space-y-1">
                    {Object.entries(card.stats).map(([key, value]) => {
                      if (key === 'total') return null
                      return (
                        <div key={key} className="flex justify-between text-sm">
                          <span className="text-gray-600 capitalize">
                            {key.replace('_', ' ')}:
                          </span>
                          <span className="font-medium">{value}</span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Cards de Resumo */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Contas Mensais */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <CreditCard className="h-5 w-5 mr-2 text-red-600" />
              Contas Mensais
            </CardTitle>
            <CardDescription>Status dos pagamentos</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="h-4 w-4 text-red-600" />
                  <span className="text-sm font-medium">Contas Vencidas</span>
                </div>
                <Badge variant="destructive">
                  {estatisticas?.contas_mensais?.vencidas || 0}
                </Badge>
              </div>
              <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Clock className="h-4 w-4 text-yellow-600" />
                  <span className="text-sm font-medium">Vencendo em 7 dias</span>
                </div>
                <Badge variant="secondary">
                  {estatisticas?.contas_mensais?.vencendo || 0}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Resumo Geral */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-green-600" />
              Resumo Geral
            </CardTitle>
            <CardDescription>Indicadores principais</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <span className="text-sm font-medium">Ativos Ativos</span>
                </div>
                <span className="font-bold text-green-600">
                  {estatisticas?.ativos?.total || 0}
                </span>
              </div>
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Archive className="h-4 w-4 text-blue-600" />
                  <span className="text-sm font-medium">Itens em Estoque</span>
                </div>
                <span className="font-bold text-blue-600">
                  {estatisticas?.inventario?.total_itens || 0}
                </span>
              </div>
              {estatisticas?.inventario?.estoque_baixo > 0 && (
                <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <AlertTriangle className="h-4 w-4 text-orange-600" />
                    <span className="text-sm font-medium">Estoque Baixo</span>
                  </div>
                  <Badge variant="secondary">
                    {estatisticas.inventario.estoque_baixo}
                  </Badge>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

