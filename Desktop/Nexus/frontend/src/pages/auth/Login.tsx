import { useState, type FormEvent } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../store/authStore'
import { useUI } from '../../store/uiStore'
import { isEmail, isStrongPassword } from '../../utils/validators'

export default function Login() {
  const { login } = useAuth()
  const { notify } = useUI()
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const from = (location.state as { from?: string })?.from ?? '/'

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    if (!isEmail(email)) return setError('ایمیل معتبر نیست.')
    if (!isStrongPassword(password)) return setError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
    setSubmitting(true)
    try {
      await login({ email, password })
      notify('خوش آمدید!')
      navigate(from, { replace: true })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'ورود ناموفق بود.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth-wrap">
      <form className="panel" onSubmit={handleSubmit}>
        <h1 className="panel-title">ورود به DevHub</h1>
        <p className="page-subtitle">به حساب کاربری خود وارد شوید و ادامه مسیر را دنبال کنید.</p>
        <div className="form-grid">
          <div className="field field-full">
            <label className="label" htmlFor="email">ایمیل</label>
            <input className="input" id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
          </div>
          <div className="field field-full">
            <label className="label" htmlFor="password">رمز عبور</label>
            <input className="input" id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
          </div>
        </div>
        {error && <p className="field-error">{error}</p>}
        <button className="primary-button" type="submit" disabled={submitting} style={{ width: '100%', marginTop: 20 }}>
          {submitting ? 'در حال ورود…' : 'ورود'}
        </button>
        <p className="help-text" style={{ textAlign: 'center', marginTop: 16 }}>
          حساب ندارید؟ <Link to="/register">ثبت‌نام کنید</Link>
        </p>
        <p className="help-text" style={{ textAlign: 'center' }}>حساب دمو: demo@devhub.app / demo12345</p>
      </form>
      <div className="auth-visual panel">
        <h2 className="panel-title">چه چیز در انتظار شماست؟</h2>
        <div className="list-stack">
          <div className="list-item"><span className="badge badge-purple">۱</span><p>مسیر یادگیری شخصی‌سازی‌شده با checkpoint</p></div>
          <div className="list-item"><span className="badge badge-green">۲</span><p>پورتفولیوی خودکار از پروژه‌های واقعی</p></div>
          <div className="list-item"><span className="badge badge-amber">۳</span><p>درآمد از فروش ابزار و اجرای پروژه</p></div>
        </div>
      </div>
    </div>
  )
}
