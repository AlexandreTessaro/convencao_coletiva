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
  id?: string
  instrumento_id?: string
  titulo: string
  tipo?: string
  data_publicacao?: string
  data_vigencia_inicio?: string
  data_vigencia_fim?: string
  sindicato_empregador?: string
  sindicato_trabalhador?: string
  municipio?: string
  uf?: string
  cnae?: string
  status?: string
  fonte?: string
}

interface SearchParams {
  q?: string
  cnpj?: string
  cnae?: string
  municipio?: string
  uf?: string
  keyword?: string
  page?: number
  page_size?: number
}

export default function SearchConvencoesPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [convencoes, setConvencoes] = useState<Convencao[]>([])
  const [total, setTotal] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [pageSize] = useState(20)
  const [searchSource, setSearchSource] = useState<'local' | 'live' | 'hybrid'>('local')
  
  const [searchParams, setSearchParams] = useState<SearchParams>({
    q: '',
    cnpj: '',
    cnae: '',
    municipio: '',
    uf: '',
    keyword: '',
  })

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
  }, [isAuthenticated, router])

  const handleSearch = async (page: number = 1) => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      
      if (searchParams.q) params.append('q', searchParams.q)
      if (searchParams.cnpj) params.append('cnpj', searchParams.cnpj)
      if (searchParams.cnae) params.append('cnae', searchParams.cnae)
      if (searchParams.municipio) params.append('municipio', searchParams.municipio)
      if (searchParams.uf) params.append('uf', searchParams.uf)
      if (searchParams.keyword) params.append('keyword', searchParams.keyword)
      
      params.append('page', page.toString())
      params.append('page_size', pageSize.toString())
      
      let response
      let endpoint = '/convencoes/search'
      
      // Escolher endpoint baseado no tipo de busca
      if (searchSource === 'live') {
        // Busca apenas no Mediador MTE em tempo real
        endpoint = '/mediador/search-live'
        params.delete('q')  // Remover parâmetros não suportados pela API live
        params.delete('keyword')
        params.delete('page')
        params.delete('page_size')
        params.append('limit', pageSize.toString())
      } else if (searchSource === 'hybrid') {
        // Busca híbrida: banco local + Mediador MTE
        endpoint = '/mediador/search-hybrid'
        params.append('use_live', 'true')
      }
      
      response = await api.get(`${endpoint}?${params.toString()}`)
      
      // Handle different response formats
      if (Array.isArray(response.data)) {
        setConvencoes(response.data)
        setTotal(response.data.length)
        setSearchSource('local')
      } else if (response.data.results) {
        // Formato paginado ou com results
        const results = response.data.results || []
        setConvencoes(results)
        setTotal(response.data.total || response.data.count || results.length || 0)
        setSearchSource(response.data.source === 'mediador_mte_live' ? 'live' : 'local')
        
        // Mostrar mensagem informativa se não encontrou resultados na busca em tempo real
        if (results.length === 0 && response.data.source === 'mediador_mte_live' && response.data.message) {
          toast.error(response.data.message, { duration: 5000 })
        }
      } else {
        setConvencoes(response.data.items || [])
        setTotal(response.data.total || response.data.count || 0)
      }
      setCurrentPage(page)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao buscar convenções')
      console.error('Error searching convencoes:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    handleSearch(1)
  }

  const handleInputChange = (field: keyof SearchParams, value: string) => {
    setSearchParams(prev => ({ ...prev, [field]: value }))
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <Layout>
      <div className="px-4 py-6 sm:px-0">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Buscar Convenções</h1>

        {/* Search Form */}
        <div className="card mb-6">
          {/* Search Source Selector */}
          <div className="mb-4 p-3 bg-blue-50 rounded-lg">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Fonte de Busca:
            </label>
            <div className="flex gap-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="searchSource"
                  value="local"
                  checked={searchSource === 'local'}
                  onChange={(e) => setSearchSource(e.target.value as 'local' | 'live' | 'hybrid')}
                  className="mr-2"
                />
                <span className="text-sm">Banco Local</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="searchSource"
                  value="live"
                  checked={searchSource === 'live'}
                  onChange={(e) => setSearchSource(e.target.value as 'local' | 'live' | 'hybrid')}
                  className="mr-2"
                />
                <span className="text-sm">Mediador MTE (Tempo Real)</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="searchSource"
                  value="hybrid"
                  checked={searchSource === 'hybrid'}
                  onChange={(e) => setSearchSource(e.target.value as 'local' | 'live' | 'hybrid')}
                  className="mr-2"
                />
                <span className="text-sm">Híbrido (Local + Tempo Real)</span>
              </label>
            </div>
            {searchSource === 'live' && (
              <p className="text-xs text-gray-600 mt-2">
                ⚡ Buscando diretamente do site do Mediador MTE em tempo real
              </p>
            )}
            {searchSource === 'hybrid' && (
              <p className="text-xs text-gray-600 mt-2">
                🔄 Combinando resultados do banco local e busca em tempo real
              </p>
            )}
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Busca Geral
                </label>
                <input
                  type="text"
                  value={searchParams.q || ''}
                  onChange={(e) => handleInputChange('q', e.target.value)}
                  placeholder="Digite palavras-chave..."
                  className="input-field w-full"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  CNPJ
                </label>
                <input
                  type="text"
                  value={searchParams.cnpj || ''}
                  onChange={(e) => handleInputChange('cnpj', e.target.value)}
                  placeholder="00.000.000/0000-00"
                  className="input-field w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  CNAE
                </label>
                <input
                  type="text"
                  value={searchParams.cnae || ''}
                  onChange={(e) => handleInputChange('cnae', e.target.value)}
                  placeholder="0000-0/00"
                  className="input-field w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Município
                </label>
                <input
                  type="text"
                  value={searchParams.municipio || ''}
                  onChange={(e) => handleInputChange('municipio', e.target.value)}
                  placeholder="Nome do município"
                  className="input-field w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  UF
                </label>
                <input
                  type="text"
                  value={searchParams.uf || ''}
                  onChange={(e) => handleInputChange('uf', e.target.value.toUpperCase())}
                  placeholder="SP"
                  maxLength={2}
                  className="input-field w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Palavra-chave
                </label>
                <input
                  type="text"
                  value={searchParams.keyword || ''}
                  onChange={(e) => handleInputChange('keyword', e.target.value)}
                  placeholder="Palavra-chave específica"
                  className="input-field w-full"
                />
              </div>
            </div>

            <div className="flex gap-4">
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Buscando...' : '🔍 Buscar'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setSearchParams({
                    q: '',
                    cnpj: '',
                    cnae: '',
                    municipio: '',
                    uf: '',
                    keyword: '',
                  })
                  setConvencoes([])
                  setTotal(0)
                }}
                className="btn-secondary"
              >
                Limpar
              </button>
            </div>
          </form>
        </div>

        {/* Results */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        )}

        {!loading && convencoes.length > 0 && (
          <>
            <div className="mb-4 text-sm text-gray-600">
              {total} convenção(ões) encontrada(s)
            </div>

            <div className="space-y-4">
              {convencoes.map((convencao, index) => (
                <div key={convencao.id || convencao.instrumento_id || `convencao-${index}`} className="card">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        {convencao.titulo || 'Sem título'}
                      </h3>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600">
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
                        {convencao.sindicato_empregador && (
                          <div>
                            <span className="font-medium">Sindicato Empregador:</span>{' '}
                            {convencao.sindicato_empregador}
                          </div>
                        )}
                        {convencao.sindicato_trabalhador && (
                          <div>
                            <span className="font-medium">Sindicato Trabalhador:</span>{' '}
                            {convencao.sindicato_trabalhador}
                          </div>
                        )}
                      </div>
                    </div>
                    
                    <div className="ml-4">
                      <Link
                        href={`/convencoes/${convencao.id || convencao.instrumento_id || '#'}`}
                        className="btn-primary text-sm"
                      >
                        Ver Detalhes
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            {total > pageSize && (
              <div className="mt-6 flex justify-center gap-2">
                <button
                  onClick={() => handleSearch(currentPage - 1)}
                  disabled={currentPage === 1}
                  className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Anterior
                </button>
                <span className="flex items-center px-4 text-sm text-gray-700">
                  Página {currentPage} de {Math.ceil(total / pageSize)}
                </span>
                <button
                  onClick={() => handleSearch(currentPage + 1)}
                  disabled={currentPage >= Math.ceil(total / pageSize)}
                  className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Próxima
                </button>
              </div>
            )}
          </>
        )}

        {!loading && convencoes.length === 0 && total === 0 && (
          <div className="card text-center py-12">
            <p className="text-gray-500">
              Nenhuma convenção encontrada. Use o formulário acima para buscar.
            </p>
          </div>
        )}
      </div>
    </Layout>
  )
}

