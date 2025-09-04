import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { CreditCard, Plus, Eye, Calendar, AlertTriangle, CheckCircle } from 'lucide-react'

export function ContasMensais() {
  const [contas, setContas] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    carregarContas()
  }, [])

  const carregarContas = async () => {
    try {
      const response = await fetch('/api/contas-mensais')
      if (response.ok) {
        const data = await response.json()
        setContas(data)
      }
    } catch (error) {
      console.error('Erro ao carregar contas mensais:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      pendente: 'bg-yellow-100 text-yellow-800',
      pago: 'bg-green-100 text-green-800',
      vencido: 'bg-red-100 text-red-800',
      cancelado: 'bg-gray-100 text-gray-800'
    }
    return colors[status] || colors.pendente
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

  const isVencida = (conta) => {
    const hoje = new Date()
    const vencimento = new Date(conta.data_vencimento)
    return vencimento < hoje && conta.status_pagamento === 'pendente'
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
          <h1 className="text-3xl font-bold text-gray-900">Contas Mensais</h1>
          <p className="text-gray-600">Controle de pagamentos recorrentes</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nova Conta
        </Button>
      </div>

      {/* Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5 text-red-600" />
              <div>
                <p className="text-sm text-gray-600">Vencidas</p>
                <p className="text-xl font-bold text-red-600">
                  {contas.filter(c => isVencida(c)).length}
                </p>
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
                <p className="text-xl font-bold text-yellow-600">
                  {contas.filter(c => c.status_pagamento === 'pendente').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <div>
                <p className="text-sm text-gray-600">Pagas</p>
                <p className="text-xl font-bold text-green-600">
                  {contas.filter(c => c.status_pagamento === 'pago').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <CreditCard className="h-5 w-5 mr-2" />
            Lista de Contas
          </CardTitle>
          <CardDescription>
            {contas.length} conta(s) cadastrada(s)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {contas.map((conta) => (
              <div key={conta.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      {isVencida(conta) ? (
                        <AlertTriangle className="h-5 w-5 text-red-600" />
                      ) : conta.status_pagamento === 'pago' ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <CreditCard className="h-5 w-5 text-gray-600" />
                      )}
                    </div>
                    <div>
                      <h3 className="font-medium">{conta.tipo_conta}</h3>
                      <p className="text-sm text-gray-600">{conta.descricao}</p>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-gray-500">
                        <span className="flex items-center">
                          <Calendar className="h-3 w-3 mr-1" />
                          Vence em: {formatDate(conta.data_vencimento)}
                        </span>
                        {conta.fornecedor && <span>Fornecedor: {conta.fornecedor.nome}</span>}
                        {conta.recorrencia && <span>Recorrência: {conta.recorrencia}</span>}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="font-bold">{formatCurrency(conta.valor)}</p>
                    <Badge className={getStatusColor(conta.status_pagamento)}>
                      {conta.status_pagamento}
                    </Badge>
                    {isVencida(conta) && (
                      <Badge variant="destructive" className="ml-1">
                        Vencida
                      </Badge>
                    )}
                  </div>
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
            {contas.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                Nenhuma conta cadastrada
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

