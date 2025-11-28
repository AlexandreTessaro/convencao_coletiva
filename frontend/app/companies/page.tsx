'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import Layout from '@/components/Layout'
import api from '@/lib/api'
import Link from 'next/link'
import toast from 'react-hot-toast'

interface Company {
  id: string
  cnpj: string
  razao_social?: string
  cnae?: string
  municipio?: string
  uf?: string
}

export default function CompaniesPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [companies, setCompanies] = useState<Company[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    loadCompanies()
  }, [isAuthenticated, router])

  const loadCompanies = async () => {
    try {
      const response = await api.get('/companies')
      setCompanies(response.data)
    } catch (error) {
      toast.error('Erro ao carregar empresas')
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
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Empresas</h1>
          <Link href="/companies/new" className="btn-primary">
            + Adicionar Empresa
          </Link>
        </div>

        {companies.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-500 mb-4">Nenhuma empresa cadastrada</p>
            <Link href="/companies/new" className="btn-primary inline-block">
              Cadastrar primeira empresa
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {companies.map((company) => (
              <div key={company.id} className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {company.razao_social || 'Sem razão social'}
                </h3>
                <p className="text-sm text-gray-600 mb-2">CNPJ: {company.cnpj}</p>
                {company.cnae && (
                  <p className="text-sm text-gray-600 mb-2">CNAE: {company.cnae}</p>
                )}
                {company.municipio && (
                  <p className="text-sm text-gray-600 mb-4">
                    {company.municipio}, {company.uf}
                  </p>
                )}
                <Link
                  href={`/companies/${company.id}`}
                  className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                >
                  Ver detalhes →
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}

