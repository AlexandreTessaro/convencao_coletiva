'use client'

import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import Link from 'next/link'
import { useEffect, useState } from 'react'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const router = useRouter()
  const { user, logout } = useAuthStore()
  const [mounted, setMounted] = useState(false)

  // Only render after client-side hydration to avoid SSR mismatch
  useEffect(() => {
    setMounted(true)
  }, [])

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  // Get user display name - use empty string during SSR to ensure consistent HTML
  const userDisplayName = mounted ? (user?.full_name || user?.email || '') : ''

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm" suppressHydrationWarning>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <Link href="/dashboard" className="flex items-center">
                <span className="text-xl font-bold text-primary-600">
                  ConvençãoColetiva
                </span>
              </Link>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link
                  href="/dashboard"
                  className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Dashboard
                </Link>
                <Link
                  href="/companies"
                  className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Empresas
                </Link>
                <Link
                  href="/convencoes"
                  className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Convenções
                </Link>
                <Link
                  href="/notifications"
                  className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Notificações
                </Link>
              </div>
            </div>
            <div className="flex items-center">
              <span className="text-sm text-gray-700 mr-4" suppressHydrationWarning>
                {userDisplayName}
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Sair
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  )
}

