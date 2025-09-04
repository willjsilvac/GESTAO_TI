import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Archive, Plus, Eye, Package, AlertTriangle } from 'lucide-react'

export function Inventario() {
  const [inventario, setInventario] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    carregarInventario()
  }, [])

  const carregarInventario = async () => {
    try {
      const response = await fetch('/api/inventario')
      if (response.ok) {
        const data = await response.json()
        setInventario(data)
      }
    } catch (error) {
      console.error('Erro ao carregar inventário:', error)
    } finally {
      setLoading(false)
    }
  }

  const getTipoColor = (tipo) => {
    const colors = {
      hardware: 'bg-blue-100 text-blue-800',
      licenca_periodica: 'bg-purple-100 text-purple-800',
      licenca_perpetua: 'bg-green-100 text-green-800'
    }
    return colors[tipo] || colors.hardware
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
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
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Inventário</h1>
          <p className="text-gray-600">Controle de estoque e itens</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Novo Item
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Archive className="h-5 w-5 mr-2" />
            Itens do Inventário
          </CardTitle>
          <CardDescription>
            {inventario.length} item(ns) em estoque
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {inventario.map((item) => (
              <div key={item.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      {item.estoque_baixo ? (
                        <AlertTriangle className="h-5 w-5 text-orange-600" />
                      ) : (
                        <Package className="h-5 w-5 text-gray-600" />
                      )}
                    </div>
                    <div>
                      <h3 className="font-medium">{item.nome}</h3>
                      <p className="text-sm text-gray-600">{item.descricao}</p>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-gray-500">
                        <span>Quantidade: {item.quantidade}</span>
                        <span>Mínimo: {item.quantidade_minima}</span>
                        {item.localizacao && <span>Local: {item.localizacao}</span>}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    {item.valor_unitario && (
                      <p className="font-bold">{formatCurrency(item.valor_unitario)}</p>
                    )}
                    <Badge className={getTipoColor(item.tipo_item)}>
                      {item.tipo_item.replace('_', ' ')}
                    </Badge>
                    {item.estoque_baixo && (
                      <Badge variant="destructive" className="ml-1">
                        Estoque Baixo
                      </Badge>
                    )}
                  </div>
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
            {inventario.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                Nenhum item no inventário
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

