'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import api from '@/lib/api'
import toast from 'react-hot-toast'

interface RegisterForm {
  email: string
  password: string
  confirmPassword: string
  full_name?: string
}

export default function RegisterPage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const { register, handleSubmit, watch, formState: { errors } } = useForm<RegisterForm>()

  const password = watch('password')

  const onSubmit = async (data: RegisterForm) => {
    if (data.password !== data.confirmPassword) {
      toast.error('As senhas não coincidem')
      return
    }

    setIsLoading(true)
    try {
      await api.post('/auth/register', {
        email: data.email,
        password: data.password,
        full_name: data.full_name,
      })
      toast.success('Conta criada com sucesso! Faça login para continuar.')
      router.push('/login')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao criar conta')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Criar conta
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4">
            <div>
              <label htmlFor="full_name" className="block text-sm font-medium text-gray-700">
                Nome completo (opcional)
              </label>
              <input
                {...register('full_name')}
                type="text"
                className="input-field mt-1"
                placeholder="Seu nome"
              />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email *
              </label>
              <input
                {...register('email', { required: 'Email é obrigatório' })}
                type="email"
                className="input-field mt-1"
                placeholder="seu@email.com"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Senha *
              </label>
              <input
                {...register('password', {
                  required: 'Senha é obrigatória',
                  minLength: { value: 8, message: 'Senha deve ter no mínimo 8 caracteres' },
                })}
                type="password"
                className="input-field mt-1"
                placeholder="Mínimo 8 caracteres"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirmar senha *
              </label>
              <input
                {...register('confirmPassword', {
                  required: 'Confirmação de senha é obrigatória',
                  validate: (value) => value === password || 'As senhas não coincidem',
                })}
                type="password"
                className="input-field mt-1"
                placeholder="Digite a senha novamente"
              />
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{errors.confirmPassword.message}</p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full"
            >
              {isLoading ? 'Criando conta...' : 'Criar conta'}
            </button>
          </div>

          <div className="text-center">
            <a
              href="/login"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              Já tem conta? Faça login
            </a>
          </div>
        </form>
      </div>
    </div>
  )
}

