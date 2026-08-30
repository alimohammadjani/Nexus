import { useState, type FormEvent } from 'react'
import { useAuth } from '../../store/authStore'
import { useUI } from '../../store/uiStore'
import { del, post } from '../../api/client'
import type { Skill } from '../../types/user'
import ProtectedRoute from '../../components/ProtectedRoute'
import { formatDate } from '../../utils/formatters'

function PortfolioInner() {
  const { user } = useAuth()
  const { notify } = useUI()
  const [name, setName] = useState('')
  const [level, setLevel] = useState('beginner')
  const [skills, setSkills] = useState<Skill[]>(user?.skills ?? [])
  const [adding, setAdding] = useState(false)

  async function handleAdd(e: FormEvent) {
    e.preventDefault()
    if (!name.trim()) return
    setAdding(true)
    try {
      const skill = await post<Skill>('/users/me/skills', { name: name.trim(), level })
      setSkills((s) => [...s, skill])
      setName('')
      notify('مهارت اضافه شد!')
    } catch (err) {
      notify(err instanceof Error ? err.message : 'افزودن مهارت ناموفق بود.', 'error')
    } finally {
      setAdding(false)
    }
  }

  async function removeSkill(id: number) {
    try {
      await del(`/users/me/skills/${id}`)
      setSkills((s) => s.filter((skill) => skill.id !== id))
      notify('مهارت حذف شد.')
    } catch (err) {
      notify(err instanceof Error ? err.message : 'حذف مهارت ناموفق بود.', 'error')
    }
  }

  return (
    <div className="content-section">
      <h1 className="page-title">پورتفولیو و مهارت‌ها</h1>
      <p className="page-subtitle">مهارت‌های خود را ثبت کنید تا پروفایل شما در فرصت‌ها و مارکت بهتر نمایش داده شود.</p>

      <form className="panel" onSubmit={handleAdd}>
        <h2 className="panel-title">افزودن مهارت</h2>
        <div className="form-grid">
          <div className="field"><label className="label">نام مهارت</label><input className="input" value={name} onChange={(e) => setName(e.target.value)} placeholder="React, Docker, FastAPI…" /></div>
          <div className="field"><label className="label">سطح</label>
            <select className="select" value={level} onChange={(e) => setLevel(e.target.value)}>
              <option value="beginner">مبتدی</option><option value="intermediate">متوسط</option><option value="expert">حرفه‌ای</option>
            </select>
          </div>
        </div>
        <button className="primary-button" type="submit" disabled={adding} style={{ marginTop: 16 }}>
          {adding ? 'در حال افزودن…' : 'افزودن مهارت'}
        </button>
      </form>

      <div className="panel" style={{ marginTop: 18 }}>
        <h2 className="panel-title">مهارت‌های شما</h2>
        {skills.length === 0 ? (
          <div className="state-block">هنوز مهارتی ثبت نکرده‌اید.</div>
        ) : (
          <div className="list-stack">
            {skills.map((skill) => (
              <div className="list-item" key={skill.id}>
                <div><strong>{skill.name}</strong><span className="help-text">• {skill.level}</span></div>
                <button className="ghost-link" type="button" onClick={() => removeSkill(skill.id)}>حذف</button>
              </div>
            ))}
          </div>
        )}
        <p className="help-text" style={{ marginTop: 18 }}>آخرین به‌روزرسانی: {formatDate(new Date().toISOString())}</p>
      </div>
    </div>
  )
}

export default function Portfolio() {
  return <ProtectedRoute><PortfolioInner /></ProtectedRoute>
}
