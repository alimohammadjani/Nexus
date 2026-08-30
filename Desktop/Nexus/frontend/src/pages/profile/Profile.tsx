import { useState, type FormEvent } from 'react'
import { useAuth } from '../../store/authStore'
import { useUI } from '../../store/uiStore'
import { put } from '../../api/client'
import type { UpdateUserPayload } from '../../types/user'
import { formatDate } from '../../utils/formatters'
import ProtectedRoute from '../../components/ProtectedRoute'

function ProfileInner() {
  const { user, refresh } = useAuth()
  const { notify } = useUI()
  const [form, setForm] = useState<UpdateUserPayload>({
    full_name: user?.full_name ?? '',
    bio: user?.bio ?? '',
    location: user?.location ?? '',
    company: user?.company ?? '',
  })
  const [saving, setSaving] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setSaving(true)
    try {
      await put('/users/me', form)
      await refresh()
      notify('پروفایل به‌روزرسانی شد!')
    } catch (err) {
      notify(err instanceof Error ? err.message : 'ذخیره ناموفق بود.', 'error')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="content-section profile-grid">
      <div className="panel">
        <div className="avatar-large">{user?.full_name?.[0] ?? 'و'}</div>
        <h2 style={{ margin: '18px 0 4px' }}>{user?.full_name}</h2>
        <p className="help-text">{user?.email}</p>
        <div className="row-meta" style={{ marginTop: 14 }}>
          <span className="badge badge-purple">{user?.role}</span>
          {user?.is_verified && <span className="badge badge-green">تأییدشده</span>}
        </div>
        <p className="help-text" style={{ marginTop: 18 }}>عضو از {formatDate(user?.created_at)}</p>
      </div>

      <form className="panel" onSubmit={handleSubmit}>
        <h1 className="panel-title">ویرایش پروفایل</h1>
        <div className="form-grid">
          <div className="field"><label className="label">نام کامل</label><input className="input" value={form.full_name ?? ''} onChange={(e) => setForm((f) => ({ ...f, full_name: e.target.value }))} /></div>
          <div className="field"><label className="label">موقعیت</label><input className="input" value={form.location ?? ''} onChange={(e) => setForm((f) => ({ ...f, location: e.target.value }))} /></div>
          <div className="field field-full"><label className="label">شرکت</label><input className="input" value={form.company ?? ''} onChange={(e) => setForm((f) => ({ ...f, company: e.target.value }))} /></div>
          <div className="field field-full"><label className="label">بیوگرافی</label><textarea className="textarea" value={form.bio ?? ''} onChange={(e) => setForm((f) => ({ ...f, bio: e.target.value }))} /></div>
        </div>
        <button className="primary-button" type="submit" disabled={saving} style={{ marginTop: 18 }}>
          {saving ? 'در حال ذخیره…' : 'ذخیره تغییرات'}
        </button>
      </form>
    </div>
  )
}

export default function Profile() {
  return <ProtectedRoute><ProfileInner /></ProtectedRoute>
}
