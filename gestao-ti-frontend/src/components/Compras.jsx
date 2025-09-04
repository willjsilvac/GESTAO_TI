import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ShoppingCart, Plus, Eye, Calendar, DollarSign } from 'lucide-react'

export function Compras() {
  const [compras, setCompras] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    carregarCompras()
  }, [])

  const carregarCompras = async () => {
    try {
      const response = await fetch('/api/compras')
      if (response.ok) {
        const data = await response.json()
        setCompras(data)
      }
    } catch (error) {
      console.error('Erro ao carregar compras:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      solicitado: 'bg-yellow-100 text-yellow-800',
      aprovado: 'bg-blue-100 text-blue-800',
      em_andamento: 'bg-purple-100 text-purple-800',
      entregue: 'bg-green-100 text-green-800',
      cancelado: 'bg-red-100 text-red-800'
    }
    return colors[status] || colors.solicitado
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Compras</h1>
          <p className="text-gray-600">Gerenciar pedidos de compra</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nova Compra
        </Button>
      </div>

      {/* Estatísticas Rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <ShoppingCart className="h-5 w-5 text-blue-600" />
              <div>
                <p className="text-sm text-gray-600">Total</p>
                <p className="text-xl font-bold">{compras.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Calendar className="h-5 w-5 text-yellow-600" />
              <div>
                <p className="text-sm text-gray-600">Pendentes</p>
                <p className="text-xl font-bold">
                  {compras.filter(c => c.status === 'solicitado').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <DollarSign className="h-5 w-5 text-green-600" />
              <div>
                <p className="text-sm text-gray-600">Valor Total</p>
                <p className="text-xl font-bold">
                  {formatCurrency(compras.reduce((sum, c) => sum + (c.valor_total || 0), 0))}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <ShoppingCart className="h-5 w-5 text-purple-600" />
              <div>
                <p className="text-sm text-gray-600">Em Andamento</p>
                <p className="text-xl font-bold">
                  {compras.filter(c => c.status === 'em_andamento').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Compras */}
      <Card>
        <CardHeader>
          <CardTitle>Lista de Compras</CardTitle>
          <CardDescription>
            Histórico de pedidos de compra
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {compras.map((compra) => (
              <div key={compra.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center space-x-4">
                    <div>
                      <h3 className="font-medium">{compra.numero_pedido}</h3>
                      <p className="text-sm text-gray-600">{compra.descricao}</p>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-gray-500">
                        <span>Solicitado em: {formatDate(compra.data_solicitacao)}</span>
                        {compra.fornecedor && <span>Fornecedor: {compra.fornecedor.nome}</span>}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="font-bold">{formatCurrency(compra.valor_total)}</p>
                    <Badge className={getStatusColor(compra.status)}>
                      {compra.status.replace('_', ' ')}
                    </Badge>
                  </div>
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
            {compras.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                Nenhuma compra cadastrada
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

