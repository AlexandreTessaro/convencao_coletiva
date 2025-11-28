'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import Layout from '@/components/Layout'
import api from '@/lib/api'
import Link from 'next/link'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'

interface Stats {
  total_companies: number
  total_convencoes: number
  novas_convencoes: number
  unread_notifications: number
  dissidio_alerts_count?: number
}

interface DissidioAlert {
  id: string
  tipo: string
  titulo: string
  mensagem: string
  lida: boolean
  created_at: string
  convencao_id?: string
}

interface Convencao {
  id: string
  titulo: string
  data_publicacao: string
  data_vigencia_inicio: string
  municipio: string
  uf: string
}

export default function DashboardPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [stats, setStats] = useState<Stats | null>(null)
  const [recentConvencoes, setRecentConvencoes] = useState<Convencao[]>([])
  const [dissidioAlerts, setDissidioAlerts] = useState<DissidioAlert[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    loadDashboard()
  }, [isAuthenticated, router])

  const loadDashboard = async () => {
    try {
      const [statsRes, convencoesRes, alertsRes] = await Promise.all([
        api.get('/dashboard/stats'),
        api.get('/dashboard/recent?limit=5'),
        api.get('/notifications/dissidio?lida=false').catch(() => ({ data: [] })),
      ])

      setStats(statsRes.data)
      setRecentConvencoes(convencoesRes.data)
      setDissidioAlerts(Array.isArray(alertsRes.data) ? alertsRes.data : [])
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (!isAuthenticated || loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="px-4 py-6 sm:px-0">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div className="card">
            <div className="text-sm font-medium text-gray-500">Empresas</div>
            <div className="mt-2 text-3xl font-semibold text-gray-900">
              {stats?.total_companies || 0}
            </div>
          </div>
          <div className="card">
            <div className="text-sm font-medium text-gray-500">Convenções</div>
            <div className="mt-2 text-3xl font-semibold text-gray-900">
              {stats?.total_convencoes || 0}
            </div>
          </div>
          <div className="card">
            <div className="text-sm font-medium text-gray-500">Novas (7 dias)</div>
            <div className="mt-2 text-3xl font-semibold text-green-600">
              {stats?.novas_convencoes || 0}
            </div>
          </div>
          <div className="card">
            <div className="text-sm font-medium text-gray-500">Notificações</div>
            <div className="mt-2 text-3xl font-semibold text-primary-600">
              {stats?.unread_notifications || 0}
            </div>
          </div>
        </div>

        {/* Dissidio Alerts */}
        {dissidioAlerts.length > 0 && (
          <div className="mb-8">
            <div className="card border-l-4 border-l-red-500 bg-red-50">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold text-red-900">
                  ⚠️ Alertas de Dissídio ({dissidioAlerts.length})
                </h2>
                <Link href="/notifications/dissidio" className="text-red-600 hover:text-red-700 text-sm font-medium">
                  Ver todos →
                </Link>
              </div>
              <div className="space-y-3">
                {dissidioAlerts.slice(0, 3).map((alert) => (
                  <div
                    key={alert.id}
                    className="bg-white p-3 rounded border border-red-200"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="font-medium text-gray-900 mb-1">{alert.titulo}</h3>
                        <p className="text-sm text-gray-700">{alert.mensagem}</p>
                      </div>
                      {alert.convencao_id && (
                        <Link
                          href={`/convencoes/${alert.convencao_id}`}
                          className="ml-4 text-red-600 hover:text-red-700 text-sm font-medium"
                        >
                          Ver →
                        </Link>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="mb-8">
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Ações Rápidas</h2>
            <div className="flex flex-wrap gap-4">
              <Link href="/companies/new" className="btn-primary">
                + Adicionar Empresa
              </Link>
              <Link href="/convencoes/search" className="btn-secondary">
                🔍 Buscar Convenções
              </Link>
              <Link href="/notifications" className="btn-secondary">
                🔔 Ver Notificações
              </Link>
              {dissidioAlerts.length > 0 && (
                <Link href="/notifications/dissidio" className="btn-secondary bg-red-600 hover:bg-red-700 text-white">
                  ⚠️ Alertas de Dissídio ({dissidioAlerts.length})
                </Link>
              )}
            </div>
          </div>
        </div>

        {/* Recent Convenções */}
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Convenções Recentes</h2>
            <Link href="/convencoes" className="text-primary-600 hover:text-primary-700">
              Ver todas →
            </Link>
          </div>
          {recentConvencoes.length === 0 ? (
            <p className="text-gray-500">Nenhuma convenção recente</p>
          ) : (
            <div className="space-y-4">
              {recentConvencoes.map((convencao) => (
                <div
                  key={convencao.id}
                  className="border-b border-gray-200 pb-4 last:border-b-0"
                >
                  <h3 className="font-medium text-gray-900">{convencao.titulo || 'Sem título'}</h3>
                  <p className="text-sm text-gray-500">
                    {convencao.municipio}, {convencao.uf} • Publicada em{' '}
                    {format(new Date(convencao.data_publicacao), "dd 'de' MMMM 'de' yyyy", {
                      locale: ptBR,
                    })}
                  </p>
                  <Link
                    href={`/convencoes/${convencao.id}`}
                    className="text-primary-600 hover:text-primary-700 text-sm"
                  >
                    Ver detalhes →
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}

