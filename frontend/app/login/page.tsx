'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { useAuthStore } from '@/store/authStore'
import api from '@/lib/api'
import toast from 'react-hot-toast'

interface LoginForm {
  email: string
  password: string
}

export default function LoginPage() {
  const router = useRouter()
  const { setAuth } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)
  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>()

  const onSubmit = async (data: LoginForm) => {
    setIsLoading(true)
    try {
      // Try JSON endpoint first
      const response = await api.post('/auth/login-json', {
        email: data.email,
        password: data.password,
      })

      const { access_token } = response.data

      // Save token to localStorage FIRST
      localStorage.setItem('token', access_token)

      // Get user info (token is now in localStorage, so interceptor will add it)
      const userResponse = await api.get('/auth/me')

      setAuth(userResponse.data, access_token)
      toast.success('Login realizado com sucesso!')
      
      // Use window.location for immediate redirect to ensure state is updated
      setTimeout(() => {
        window.location.href = '/dashboard'
      }, 100)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao fazer login')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            ConvençãoColetiva
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Plataforma de Convenções Coletivas
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email" className="sr-only">
                Email
              </label>
              <input
                {...register('email', { required: 'Email é obrigatório' })}
                type="email"
                className="input-field rounded-t-md"
                placeholder="Email"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Senha
              </label>
              <input
                {...register('password', { required: 'Senha é obrigatória' })}
                type="password"
                className="input-field rounded-b-md"
                placeholder="Senha"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                Lembrar-me
              </label>
            </div>

            <div className="text-sm">
              <a href="#" className="font-medium text-primary-600 hover:text-primary-500">
                Esqueci minha senha
              </a>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full"
            >
              {isLoading ? 'Entrando...' : 'Entrar'}
            </button>
          </div>

          <div className="text-center">
            <a
              href="/register"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              Não tem conta? Cadastre-se
            </a>
          </div>
        </form>
      </div>
    </div>
  )
}

