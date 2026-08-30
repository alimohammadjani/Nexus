import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../store/authStore'
import { useUI } from '../store/uiStore'
import './Layout.css'

const navItems = [
  { to: '/', label: 'خانه' },
  { to: '/jobs', label: 'فرصت‌ها' },
  { to: '/learning', label: 'یادگیری' },
  { to: '/market', label: 'مارکت' },
  { to: '/profile', label: 'پروفایل' },
]

export default function Layout() {
  const { user, isAuthenticated, logout } = useAuth()
  const { toasts, notify } = useUI()
  const navigate = useNavigate()

  return (
    <div className="app-shell site-app" dir="rtl">
      <div className="noise-layer" aria-hidden="true" />
      <div className="orb orb-one" aria-hidden="true" />
      <div className="orb orb-two" aria-hidden="true" />

      <header className="site-header">
        <Link className="brand" to="/">
          <span className="brand-mark">D</span>
          <span>
            <strong>DevHub</strong>
            <small>از صفر تا استخدام</small>
          </span>
        </Link>

        <nav className="main-nav site-main-nav" aria-label="ناوبری اصلی">
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.to === '/'} className={({ isActive }) => (isActive ? 'active' : '')}>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="header-actions">
          {isAuthenticated ? (
            <>
              <span className="user-chip">
                <span className="avatar avatar-sm">{user?.full_name?.[0] ?? 'و'}</span>
                <span className="user-chip-name">{user?.full_name?.split(' ')[0]}</span>
              </span>
              {user?.is_employer || user?.role === 'admin' ? (
                <Link className="ghost-link" to="/jobs/new">
                  ثبت فرصت
                </Link>
              ) : null}
              {(user?.is_employer || user?.role === 'admin' || true) && (
                <Link className="ghost-link" to="/market/sell">
                  فروش
                </Link>
              )}
              <button
                className="primary-button small"
                type="button"
                onClick={() => {
                  logout()
                  notify('با موفقیت خارج شدید', 'info')
                  navigate('/')
                }}
              >
                خروج
              </button>
            </>
          ) : (
            <>
              <Link className="ghost-link" to="/login">
                ورود
              </Link>
              <Link className="primary-button small" to="/register">
                شروع رایگان
              </Link>
            </>
          )}
        </div>
      </header>

      <main className="page-content">
        <Outlet />
      </main>

      <footer className="site-footer">
        <strong>DevHub</strong>
        <span>از صفر تا استخدام — همه چیز برای رشد برنامه‌نویس‌ها، یک‌جا.</span>
      </footer>

      <div className="toast-stack" aria-live="polite">
        {toasts.map((toast) => (
          <div key={toast.id} className={`toast toast-${toast.kind}`}>
            {toast.message}
          </div>
        ))}
      </div>
    </div>
  )
}
