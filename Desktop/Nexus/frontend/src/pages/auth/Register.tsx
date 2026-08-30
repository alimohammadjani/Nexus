import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../store/authStore'
import { useUI } from '../../store/uiStore'
import { isEmail, isStrongPassword, required } from '../../utils/validators'

export default function Register() {
  const { register } = useAuth()
  const { notify } = useUI()
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('developer')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    if (!required(fullName)) return setError('نام کامل الزامی است.')
    if (!isEmail(email)) return setError('ایمیل معتبر نیست.')
    if (!isStrongPassword(password)) return setError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
    setSubmitting(true)
    try {
      await register({ email, full_name: fullName, password, role })
      notify('ثبت‌نام با موفقیت انجام شد!')
      navigate('/profile')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'ثبت‌نام ناموفق بود.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth-wrap">
      <form className="panel" onSubmit={handleSubmit}>
        <h1 className="panel-title">ساخت حساب DevHub</h1>
        <p className="page-subtitle">از همین امروز مسیر یادگیری، کار و درآمد خود را شروع کنید.</p>
        <div className="form-grid">
          <div className="field field-full">
            <label className="label" htmlFor="full_name">نام و نام خانوادگی</label>
            <input className="input" id="full_name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
          </div>
          <div className="field field-full">
            <label className="label" htmlFor="email">ایمیل</label>
            <input className="input" id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="field field-full">
            <label className="label" htmlFor="password">رمز عبور</label>
            <input className="input" id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className="field field-full">
            <label className="label" htmlFor="role">نقش</label>
            <select className="select" id="role" value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="developer">توسعه‌دهنده</option>
              <option value="employer">کارفرما / شرکت</option>
            </select>
          </div>
        </div>
        {error && <p className="field-error">{error}</p>}
        <button className="primary-button" type="submit" disabled={submitting} style={{ width: '100%', marginTop: 20 }}>
          {submitting ? 'در حال ساخت حساب…' : 'ثبت‌نام'}
        </button>
        <p className="help-text" style={{ textAlign: 'center', marginTop: 16 }}>
          قبلاً حساب ساخته‌اید؟ <Link to="/login">ورود</Link>
        </p>
      </form>
      <div className="auth-visual panel">
        <h2 className="panel-title">یک حساب، چند مسیر</h2>
        <p>به‌عنوان توسعه‌دهنده می‌توانید یاد بگیرید، کار پیدا کنید و ابزار بفروشید. به‌عنوان کارفرما می‌توانید متخصص واقعی پیدا کنید.</p>
      </div>
    </div>
  )
}
