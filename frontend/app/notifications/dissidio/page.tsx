'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import Layout from '@/components/Layout'
import api from '@/lib/api'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import toast from 'react-hot-toast'
import Link from 'next/link'

interface DissidioAlert {
  id: string
  tipo: string
  titulo: string
  mensagem: string
  lida: boolean
  created_at: string
  convencao_id?: string
}

const getAlertColor = (tipo: string) => {
  if (tipo.includes('URGENTE')) return 'bg-red-100 text-red-800 border-red-300'
  if (tipo.includes('PROXIMO_30')) return 'bg-orange-100 text-orange-800 border-orange-300'
  if (tipo.includes('PROXIMO_60')) return 'bg-yellow-100 text-yellow-800 border-yellow-300'
  if (tipo.includes('PROXIMO_90')) return 'bg-blue-100 text-blue-800 border-blue-300'
  if (tipo === 'VENCIDO') return 'bg-red-200 text-red-900 border-red-400'
  return 'bg-gray-100 text-gray-800 border-gray-300'
}

const getAlertIcon = (tipo: string) => {
  if (tipo.includes('URGENTE')) return '⚠️'
  if (tipo === 'VENCIDO') return '❌'
  if (tipo.includes('PROXIMO_30')) return '🔔'
  if (tipo.includes('PROXIMO_60')) return '📅'
  if (tipo.includes('PROXIMO_90')) return '📋'
  return '📌'
}

export default function DissidioAlertsPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [alerts, setAlerts] = useState<DissidioAlert[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'unread'>('all')

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    loadAlerts()
  }, [isAuthenticated, router, filter])

  const loadAlerts = async () => {
    setLoading(true)
    try {
      const params = filter === 'unread' ? '?lida=false' : ''
      const response = await api.get(`/notifications/dissidio${params}`)
      const data = Array.isArray(response.data) ? response.data : []
      // Ordenar por prioridade: URGENTE primeiro, depois por data
      const sorted = data.sort((a: DissidioAlert, b: DissidioAlert) => {
        const priorityOrder: { [key: string]: number } = {
          'VENCIMENTO_URGENTE_7': 1,
          'VENCIMENTO_URGENTE_15': 2,
          'VENCIDO': 3,
          'VENCIMENTO_PROXIMO_30': 4,
          'VENCIMENTO_PROXIMO_60': 5,
          'VENCIMENTO_PROXIMO_90': 6,
        }
        const aPriority = priorityOrder[a.tipo] || 99
        const bPriority = priorityOrder[b.tipo] || 99
        if (aPriority !== bPriority) return aPriority - bPriority
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      })
      setAlerts(sorted)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao carregar alertas de dissídio')
      console.error('Error loading dissidio alerts:', error)
    } finally {
      setLoading(false)
    }
  }

  const markAsRead = async (alertId: string) => {
    try {
      await api.put(`/notifications/${alertId}/read`)
      setAlerts(prev =>
        prev.map(a => a.id === alertId ? { ...a, lida: true } : a)
      )
      toast.success('Alerta marcado como lido')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao marcar alerta')
    }
  }

  const markAllAsRead = async () => {
    try {
      const unreadAlerts = alerts.filter(a => !a.lida)
      await Promise.all(
        unreadAlerts.map(a => api.put(`/notifications/${a.id}/read`))
      )
      setAlerts(prev => prev.map(a => ({ ...a, lida: true })))
      toast.success('Todos os alertas foram marcados como lidos')
    } catch (error: any) {
      toast.error('Erro ao marcar alertas como lidos')
    }
  }

  if (!isAuthenticated) {
    return null
  }

  const unreadCount = alerts.filter(a => !a.lida).length

  return (
    <Layout>
      <div className="px-4 py-6 sm:px-0">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Alertas de Dissídio</h1>
            <p className="text-gray-600 mt-1">
              Acompanhe o vencimento das convenções coletivas das suas empresas
            </p>
          </div>
          {unreadCount > 0 && (
            <button
              onClick={markAllAsRead}
              className="btn-secondary text-sm"
            >
              Marcar todas como lidas
            </button>
          )}
        </div>

        {/* Filter Tabs */}
        <div className="mb-6 border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setFilter('all')}
              className={`${
                filter === 'all'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Todas ({alerts.length})
            </button>
            <button
              onClick={() => setFilter('unread')}
              className={`${
                filter === 'unread'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Não lidas ({unreadCount})
            </button>
          </nav>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        )}

        {/* Alerts List */}
        {!loading && alerts.length === 0 && (
          <div className="card text-center py-12">
            <p className="text-gray-500">
              {filter === 'unread'
                ? 'Nenhum alerta de dissídio não lido'
                : 'Nenhum alerta de dissídio encontrado'}
            </p>
            <p className="text-sm text-gray-400 mt-2">
              Os alertas são gerados automaticamente quando convenções estão próximas do vencimento
            </p>
          </div>
        )}

        {!loading && alerts.length > 0 && (
          <div className="space-y-4">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`card border-l-4 ${
                  !alert.lida 
                    ? getAlertColor(alert.tipo).split(' ')[0] + ' ' + getAlertColor(alert.tipo).split(' ')[1]
                    : 'border-gray-300'
                } ${!alert.lida ? 'bg-opacity-50' : ''}`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xl">{getAlertIcon(alert.tipo)}</span>
                      {!alert.lida && (
                        <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getAlertColor(alert.tipo)}`}>
                          Nova
                        </span>
                      )}
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${getAlertColor(alert.tipo)}`}>
                        {alert.tipo.replace(/_/g, ' ')}
                      </span>
                      <span className="text-xs text-gray-500">
                        {format(new Date(alert.created_at), "dd 'de' MMMM 'de' yyyy 'às' HH:mm", {
                          locale: ptBR,
                        })}
                      </span>
                    </div>
                    
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">
                      {alert.titulo}
                    </h3>
                    
                    <p className="text-gray-700 mb-2">{alert.mensagem}</p>
                  </div>
                  
                  <div className="ml-4 flex flex-col gap-2">
                    {!alert.lida && (
                      <button
                        onClick={() => markAsRead(alert.id)}
                        className="btn-secondary text-sm whitespace-nowrap"
                      >
                        Marcar como lida
                      </button>
                    )}
                    {alert.convencao_id && (
                      <Link
                        href={`/convencoes/${alert.convencao_id}`}
                        className="btn-primary text-sm whitespace-nowrap text-center"
                      >
                        Ver Convenção
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}

