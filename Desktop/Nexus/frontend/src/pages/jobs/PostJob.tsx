import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { createJob } from '../../api/jobs'
import type { JobCreatePayload } from '../../types/job'
import { useUI } from '../../store/uiStore'
import { required } from '../../utils/validators'
import ProtectedRoute from '../../components/ProtectedRoute'

function PostJobInner() {
  const { notify } = useUI()
  const navigate = useNavigate()
  const [form, setForm] = useState<JobCreatePayload>({
    title: '',
    company: '',
    description: '',
    location: '',
    type: 'full_time',
    mode: 'remote',
    level: 'mid',
    salary_range: '',
    skills: '',
  })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  function update<K extends keyof JobCreatePayload>(key: K, value: JobCreatePayload[K]) {
    setForm((f) => ({ ...f, [key]: value }))
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    if (!required(form.title) || !required(form.company) || !required(form.description)) {
      return setError('عنوان، شرکت و شرح فرصت الزامی هستند.')
    }
    setSubmitting(true)
    try {
      const job = await createJob(form)
      notify('فرصت با موفقیت ثبت شد!')
      navigate(`/jobs/${job.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'ثبت فرصت ناموفق بود.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="content-section">
      <h1 className="page-title">ثبت فرصت / پروژه</h1>
      <p className="page-subtitle">اطلاعات را کامل وارد کنید تا کارفرما یا توسعه‌دهنده مناسب‌تر پیدا شود.</p>
      <form className="panel" onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="field"><label className="label">عنوان</label><input className="input" value={form.title} onChange={(e) => update('title', e.target.value)} /></div>
          <div className="field"><label className="label">شرکت / کارفرما</label><input className="input" value={form.company} onChange={(e) => update('company', e.target.value)} /></div>
          <div className="field"><label className="label">موقعیت</label><input className="input" value={form.location ?? ''} onChange={(e) => update('location', e.target.value)} /></div>
          <div className="field"><label className="label">بازه حقوق / بودجه</label><input className="input" value={form.salary_range ?? ''} onChange={(e) => update('salary_range', e.target.value)} /></div>
          <div className="field"><label className="label">نوع</label>
            <select className="select" value={form.type} onChange={(e) => update('type', e.target.value as JobCreatePayload['type'])}>
              <option value="full_time">تمام‌وقت</option><option value="part_time">پاره‌وقت</option><option value="freelance">فریلنس</option><option value="contract">قراردادی</option>
            </select>
          </div>
          <div className="field"><label className="label">حالت کاری</label>
            <select className="select" value={form.mode} onChange={(e) => update('mode', e.target.value as JobCreatePayload['mode'])}>
              <option value="remote">ریموت</option><option value="hybrid">هیبرید</option><option value="on_site">حضوری</option>
            </select>
          </div>
          <div className="field"><label className="label">سطح</label>
            <select className="select" value={form.level} onChange={(e) => update('level', e.target.value)}>
              <option value="junior">جونیور</option><option value="mid">میدل</option><option value="senior">سینیور</option>
            </select>
          </div>
          <div className="field"><label className="label">مهارت‌ها (با کاما)</label><input className="input" value={form.skills ?? ''} onChange={(e) => update('skills', e.target.value)} placeholder="React, FastAPI, Docker" /></div>
          <div className="field field-full"><label className="label">شرح کامل</label><textarea className="textarea" value={form.description} onChange={(e) => update('description', e.target.value)} /></div>
        </div>
        {error && <p className="field-error">{error}</p>}
        <button className="primary-button" type="submit" disabled={submitting} style={{ marginTop: 18 }}>
          {submitting ? 'در حال ثبت…' : 'انتشار فرصت'}
        </button>
      </form>
    </div>
  )
}

export default function PostJob() {
  return <ProtectedRoute><PostJobInner /></ProtectedRoute>
}
