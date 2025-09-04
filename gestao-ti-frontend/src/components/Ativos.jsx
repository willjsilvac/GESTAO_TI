import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Package, Plus, Eye, MapPin, Calendar } from 'lucide-react'

export function Ativos() {
  const [ativos, setAtivos] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    carregarAtivos()
  }, [])

  const carregarAtivos = async () => {
    try {
      const response = await fetch('/api/ativos')
      if (response.ok) {
        const data = await response.json()
        setAtivos(data)
      }
    } catch (error) {
      console.error('Erro ao carregar ativos:', error)
    } finally {
      setLoading(false)
    }
  }

  const getTipoColor = (tipo) => {
    const colors = {
      hardware: 'bg-blue-100 text-blue-800',
      software: 'bg-green-100 text-green-800',
      licenca: 'bg-purple-100 text-purple-800',
      equipamento: 'bg-orange-100 text-orange-800',
      mobiliario: 'bg-gray-100 text-gray-800'
    }
    return colors[tipo] || colors.hardware
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
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Ativos</h1>
          <p className="text-gray-600">Gerenciar ativos da empresa</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Novo Ativo
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Package className="h-5 w-5 mr-2" />
            Lista de Ativos
          </CardTitle>
          <CardDescription>
            {ativos.length} ativo(s) cadastrado(s)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {ativos.map((ativo) => (
              <div key={ativo.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center space-x-4">
                    <div>
                      <h3 className="font-medium">{ativo.nome}</h3>
                      <p className="text-sm text-gray-600">{ativo.descricao}</p>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-gray-500">
                        {ativo.localizacao && (
                          <span className="flex items-center">
                            <MapPin className="h-3 w-3 mr-1" />
                            {ativo.localizacao}
                          </span>
                        )}
                        <span className="flex items-center">
                          <Calendar className="h-3 w-3 mr-1" />
                          {formatDate(ativo.data_aquisicao)}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="font-bold">{formatCurrency(ativo.valor_atual || 0)}</p>
                    <Badge className={getTipoColor(ativo.tipo_ativo)}>
                      {ativo.tipo_ativo}
                    </Badge>
                  </div>
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
            {ativos.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                Nenhum ativo cadastrado
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

