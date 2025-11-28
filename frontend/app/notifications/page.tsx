'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import Layout from '@/components/Layout'
import api from '@/lib/api'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import toast from 'react-hot-toast'

interface Notification {
  id: string
  tipo: string
  titulo: string
  mensagem: string
  lida: boolean
  created_at: string
  convencao_id?: string
}

export default function NotificationsPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'unread'>('all')

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    loadNotifications()
  }, [isAuthenticated, router, filter])

  const loadNotifications = async () => {
    setLoading(true)
    try {
      const params = filter === 'unread' ? '?lida=false' : ''
      const response = await api.get(`/notifications${params}`)
      // Handle both array and object responses
      const data = Array.isArray(response.data) ? response.data : (response.data.items || response.data.results || [])
      setNotifications(data)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao carregar notificações')
      console.error('Error loading notifications:', error)
    } finally {
      setLoading(false)
    }
  }

  const markAsRead = async (notificationId: string) => {
    try {
      await api.put(`/notifications/${notificationId}/read`)
      setNotifications(prev =>
        prev.map(n => n.id === notificationId ? { ...n, lida: true } : n)
      )
      toast.success('Notificação marcada como lida')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao marcar notificação')
    }
  }

  const markAllAsRead = async () => {
    try {
      const unreadNotifications = notifications.filter(n => !n.lida)
      await Promise.all(
        unreadNotifications.map(n => api.put(`/notifications/${n.id}/read`))
      )
      setNotifications(prev => prev.map(n => ({ ...n, lida: true })))
      toast.success('Todas as notificações foram marcadas como lidas')
    } catch (error: any) {
      toast.error('Erro ao marcar notificações como lidas')
    }
  }

  if (!isAuthenticated) {
    return null
  }

  const unreadCount = notifications.filter(n => !n.lida).length

  return (
    <Layout>
      <div className="px-4 py-6 sm:px-0">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Notificações</h1>
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
              Todas ({notifications.length})
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
            <Link
              href="/notifications/dissidio"
              className="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
            >
              ⚠️ Dissídio
            </Link>
          </nav>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        )}

        {/* Notifications List */}
        {!loading && notifications.length === 0 && (
          <div className="card text-center py-12">
            <p className="text-gray-500">
              {filter === 'unread'
                ? 'Nenhuma notificação não lida'
                : 'Nenhuma notificação encontrada'}
            </p>
          </div>
        )}

        {!loading && notifications.length > 0 && (
          <div className="space-y-4">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className={`card ${
                  !notification.lida ? 'border-l-4 border-l-primary-600 bg-blue-50' : ''
                }`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      {!notification.lida && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-800">
                          Nova
                        </span>
                      )}
                      <span className="text-xs text-gray-500">
                        {format(new Date(notification.created_at), "dd 'de' MMMM 'de' yyyy 'às' HH:mm", {
                          locale: ptBR,
                        })}
                      </span>
                    </div>
                    
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">
                      {notification.titulo}
                    </h3>
                    
                    <p className="text-gray-700 mb-2">{notification.mensagem}</p>
                    
                    {notification.tipo && (
                      <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800">
                        {notification.tipo}
                      </span>
                    )}
                  </div>
                  
                  <div className="ml-4 flex flex-col gap-2">
                    {!notification.lida && (
                      <button
                        onClick={() => markAsRead(notification.id)}
                        className="btn-secondary text-sm whitespace-nowrap"
                      >
                        Marcar como lida
                      </button>
                    )}
                    {notification.convencao_id && (
                      <a
                        href={`/convencoes/${notification.convencao_id}`}
                        className="btn-primary text-sm whitespace-nowrap"
                      >
                        Ver Convenção
                      </a>
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

