'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { useAuthStore } from '@/store/authStore'
import Layout from '@/components/Layout'
import api from '@/lib/api'
import toast from 'react-hot-toast'

interface CompanyForm {
  cnpj: string
  razao_social?: string
  cnae?: string
  municipio?: string
  uf?: string
}

export default function NewCompanyPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)
  const { register, handleSubmit, formState: { errors } } = useForm<CompanyForm>()

  if (!isAuthenticated) {
    router.push('/login')
    return null
  }

  const onSubmit = async (data: CompanyForm) => {
    setIsLoading(true)
    try {
      await api.post('/companies', data)
      toast.success('Empresa cadastrada com sucesso!')
      router.push('/companies')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao cadastrar empresa')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Layout>
      <div className="px-4 py-6 sm:px-0 max-w-2xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Cadastrar Nova Empresa</h1>

        <form onSubmit={handleSubmit(onSubmit)} className="card space-y-6">
          <div>
            <label htmlFor="cnpj" className="block text-sm font-medium text-gray-700 mb-1">
              CNPJ *
            </label>
            <input
              {...register('cnpj', {
                required: 'CNPJ é obrigatório',
                pattern: {
                  value: /^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$|^\d{14}$/,
                  message: 'CNPJ inválido',
                },
              })}
              type="text"
              className="input-field"
              placeholder="00.000.000/0000-00"
            />
            {errors.cnpj && (
              <p className="mt-1 text-sm text-red-600">{errors.cnpj.message}</p>
            )}
          </div>

          <div>
            <label htmlFor="razao_social" className="block text-sm font-medium text-gray-700 mb-1">
              Razão Social
            </label>
            <input
              {...register('razao_social')}
              type="text"
              className="input-field"
              placeholder="Nome da empresa"
            />
          </div>

          <div>
            <label htmlFor="cnae" className="block text-sm font-medium text-gray-700 mb-1">
              CNAE Principal
            </label>
            <input
              {...register('cnae', {
                pattern: {
                  value: /^\d{4}-\d{1}\/\d{2}$|^\d{7}$/,
                  message: 'CNAE inválido (formato: 0000-0/00)',
                },
              })}
              type="text"
              className="input-field"
              placeholder="0000-0/00"
            />
            {errors.cnae && (
              <p className="mt-1 text-sm text-red-600">{errors.cnae.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="municipio" className="block text-sm font-medium text-gray-700 mb-1">
                Município
              </label>
              <input
                {...register('municipio')}
                type="text"
                className="input-field"
                placeholder="São Paulo"
              />
            </div>
            <div>
              <label htmlFor="uf" className="block text-sm font-medium text-gray-700 mb-1">
                UF
              </label>
              <input
                {...register('uf', {
                  maxLength: { value: 2, message: 'UF deve ter 2 caracteres' },
                })}
                type="text"
                className="input-field"
                placeholder="SP"
                maxLength={2}
              />
              {errors.uf && (
                <p className="mt-1 text-sm text-red-600">{errors.uf.message}</p>
              )}
            </div>
          </div>

          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => router.back()}
              className="btn-secondary flex-1"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary flex-1"
            >
              {isLoading ? 'Cadastrando...' : 'Cadastrar Empresa'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  )
}

