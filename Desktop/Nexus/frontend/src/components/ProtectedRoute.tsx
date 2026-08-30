import { Navigate, useLocation } from 'react-router-dom'
import type { ReactNode } from 'react'
import { useAuth } from '../store/authStore'

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return <div className="state-block">در حال بارگذاری…</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />
  }

  return <>{children}</>
}
