'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import Layout from '@/components/Layout'
import api from '@/lib/api'
import Link from 'next/link'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import toast from 'react-hot-toast'

interface Convencao {
  id: string
  titulo: string
  tipo: string
  data_publicacao: string
  data_vigencia_inicio: string
  data_vigencia_fim: string
  sindicato_empregador: string
  sindicato_trabalhador: string
  municipio: string
  uf: string
  cnae: string
  status: string
}

export default function ConvencoesPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [convencoes, setConvencoes] = useState<Convencao[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    loadConvencoes()
  }, [isAuthenticated, router])

  const loadConvencoes = async () => {
    setLoading(true)
    try {
      // Try to get convenções from dashboard recent endpoint or search
      const response = await api.get('/convencoes/search?page=1&page_size=50')
      
      // Handle both array response and paginated response
      if (Array.isArray(response.data)) {
        setConvencoes(response.data)
      } else {
        setConvencoes(response.data.items || response.data.results || [])
      }
    } catch (error: any) {
      // If search fails, try to get from dashboard
      try {
        const dashboardResponse = await api.get('/dashboard/recent?limit=50')
        setConvencoes(dashboardResponse.data || [])
      } catch (dashboardError: any) {
        toast.error('Erro ao carregar convenções')
        console.error('Error loading convencoes:', error)
      }
    } finally {
      setLoading(false)
    }
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <Layout>
      <div className="px-4 py-6 sm:px-0">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Convenções Coletivas</h1>
          <Link href="/convencoes/search" className="btn-primary">
            🔍 Buscar Convenções
          </Link>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        )}

        {/* Empty State */}
        {!loading && convencoes.length === 0 && (
          <div className="card text-center py-12">
            <p className="text-gray-500 mb-4">Nenhuma convenção encontrada.</p>
            <Link href="/convencoes/search" className="btn-primary">
              Buscar Convenções
            </Link>
          </div>
        )}

        {/* Convenções List */}
        {!loading && convencoes.length > 0 && (
          <div className="space-y-4">
            {convencoes.map((convencao) => (
              <div key={convencao.id} className="card">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {convencao.titulo || 'Sem título'}
                    </h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600 mb-3">
                      {convencao.tipo && (
                        <div>
                          <span className="font-medium">Tipo:</span> {convencao.tipo}
                        </div>
                      )}
                      {convencao.data_publicacao && (
                        <div>
                          <span className="font-medium">Publicação:</span>{' '}
                          {format(new Date(convencao.data_publicacao), "dd/MM/yyyy", {
                            locale: ptBR,
                          })}
                        </div>
                      )}
                      {convencao.municipio && (
                        <div>
                          <span className="font-medium">Local:</span> {convencao.municipio}
                          {convencao.uf && `, ${convencao.uf}`}
                        </div>
                      )}
                      {convencao.cnae && (
                        <div>
                          <span className="font-medium">CNAE:</span> {convencao.cnae}
                        </div>
                      )}
                      {convencao.data_vigencia_inicio && (
                        <div>
                          <span className="font-medium">Vigência:</span>{' '}
                          {format(new Date(convencao.data_vigencia_inicio), "dd/MM/yyyy", {
                            locale: ptBR,
                          })}
                          {convencao.data_vigencia_fim && (
                            <> até {format(new Date(convencao.data_vigencia_fim), "dd/MM/yyyy", {
                              locale: ptBR,
                            })}</>
                          )}
                        </div>
                      )}
                    </div>

                    {convencao.sindicato_empregador && (
                      <div className="text-sm text-gray-600 mb-1">
                        <span className="font-medium">Sindicato Empregador:</span>{' '}
                        {convencao.sindicato_empregador}
                      </div>
                    )}
                    {convencao.sindicato_trabalhador && (
                      <div className="text-sm text-gray-600">
                        <span className="font-medium">Sindicato Trabalhador:</span>{' '}
                        {convencao.sindicato_trabalhador}
                      </div>
                    )}

                    {convencao.status && (
                      <div className="mt-2">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                          convencao.status === 'PROCESSADO' 
                            ? 'bg-green-100 text-green-800'
                            : convencao.status === 'PROCESSANDO'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {convencao.status}
                        </span>
                      </div>
                    )}
                  </div>
                  
                  <div className="ml-4">
                    <Link
                      href={`/convencoes/${convencao.id}`}
                      className="btn-primary text-sm"
                    >
                      Ver Detalhes
                    </Link>
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



