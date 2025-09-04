import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Headphones, Plus, Eye, Clock, AlertTriangle } from 'lucide-react'

export function Chamados() {
  const [chamados, setChamados] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    carregarChamados()
  }, [])

  const carregarChamados = async () => {
    try {
      const response = await fetch('/api/chamados')
      if (response.ok) {
        const data = await response.json()
        setChamados(data)
      }
    } catch (error) {
      console.error('Erro ao carregar chamados:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      aberto: 'bg-red-100 text-red-800',
      em_andamento: 'bg-yellow-100 text-yellow-800',
      aguardando: 'bg-blue-100 text-blue-800',
      resolvido: 'bg-green-100 text-green-800',
      fechado: 'bg-gray-100 text-gray-800'
    }
    return colors[status] || colors.aberto
  }

  const getPrioridadeColor = (prioridade) => {
    const colors = {
      baixa: 'bg-green-100 text-green-800',
      media: 'bg-yellow-100 text-yellow-800',
      alta: 'bg-orange-100 text-orange-800',
      critica: 'bg-red-100 text-red-800'
    }
    return colors[prioridade] || colors.media
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
          <h1 className="text-3xl font-bold text-gray-900">Chamados</h1>
          <p className="text-gray-600">Sistema de atendimento e suporte</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Novo Chamado
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Headphones className="h-5 w-5 mr-2" />
            Lista de Chamados
          </CardTitle>
          <CardDescription>
            {chamados.length} chamado(s) registrado(s)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {chamados.map((chamado) => (
              <div key={chamado.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      {chamado.prioridade === 'critica' ? (
                        <AlertTriangle className="h-5 w-5 text-red-600" />
                      ) : (
                        <Headphones className="h-5 w-5 text-gray-600" />
                      )}
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <h3 className="font-medium">{chamado.numero_chamado}</h3>
                        <Badge className={getPrioridadeColor(chamado.prioridade)}>
                          {chamado.prioridade}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600">{chamado.titulo}</p>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-gray-500">
                        <span className="flex items-center">
                          <Clock className="h-3 w-3 mr-1" />
                          {formatDate(chamado.data_abertura)}
                        </span>
                        {chamado.solicitante && <span>Por: {chamado.solicitante.nome}</span>}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <Badge className={getStatusColor(chamado.status)}>
                    {chamado.status.replace('_', ' ')}
                  </Badge>
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
            {chamados.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                Nenhum chamado registrado
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

