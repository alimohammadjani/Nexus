import { useCallback, useEffect, useState, type FormEvent } from 'react'
import { Link, useParams } from 'react-router-dom'
import { applyToJob, fetchJob } from '../../api/jobs'
import type { Job } from '../../types/job'
import { formatPrice, jobModeLabel, jobTypeLabel, splitSkills } from '../../utils/formatters'
import { useAuth } from '../../store/authStore'
import { useUI } from '../../store/uiStore'
import Loading from '../../components/Loading'
import ErrorState from '../../components/ErrorState'

export default function JobDetail() {
  const { id } = useParams()
  const { isAuthenticated } = useAuth()
  const { notify } = useUI()
  const [job, setJob] = useState<Job | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [coverLetter, setCoverLetter] = useState('')
  const [applied, setApplied] = useState(false)

  const load = useCallback(async () => {
    if (!id) return
    setLoading(true)
    try {
      setJob(await fetchJob(Number(id)))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فرصت پیدا نشد.')
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    void load()
  }, [load])

  async function handleApply(e: FormEvent) {
    e.preventDefault()
    if (!id) return
    try {
      await applyToJob(Number(id), coverLetter)
      setApplied(true)
      notify('درخواست شما ثبت شد!')
    } catch (err) {
      notify(err instanceof Error ? err.message : 'ثبت درخواست ناموفق بود.', 'error')
    }
  }

  if (loading) return <Loading />
  if (error || !job) return <ErrorState message={error ?? 'فرصت پیدا نشد.'} onRetry={load} />

  return (
    <div className="content-section">
      <Link to="/jobs" className="ghost-link">← بازگشت به فرصت‌ها</Link>
      <div className="page-heading" style={{ marginTop: 18 }}>
        <div>
          <div className="row-meta">
            {job.is_featured && <span className="badge badge-purple">پریمیوم</span>}
            <span className="badge badge-cyan">{jobTypeLabel(job.type)}</span>
            <span className="badge badge-green">{jobModeLabel(job.mode)}</span>
          </div>
          <h1 className="page-title">{job.title}</h1>
          <p className="page-subtitle">{job.company} • {job.location ?? 'ریموت'} • {job.salary_range ?? 'بودجه توافقی'}</p>
        </div>
        {job.budget ? <strong style={{ color: '#86efac', fontSize: '1.2rem' }}>{formatPrice(job.budget, 'T')}</strong> : null}
      </div>

      <div className="panel" style={{ marginBottom: 18 }}>
        <h2 className="panel-title">شرح فرصت</h2>
        <p>{job.description}</p>
        <div className="skill-row" style={{ marginTop: 20 }}>
          {splitSkills(job.skills).map((skill) => <span className="skill-tag" key={skill}>{skill}</span>)}
        </div>
      </div>

      <form className="panel" onSubmit={handleApply}>
        <h2 className="panel-title">درخواست همکاری</h2>
        <div className="form-grid">
          <div className="field field-full">
            <label className="label" htmlFor="cover">پیام / معرفی (اختیاری)</label>
            <textarea className="textarea" id="cover" value={coverLetter} onChange={(e) => setCoverLetter(e.target.value)} placeholder="کوتاه درباره خود و مهارت‌هایتان بنویسید…" />
          </div>
        </div>
        {isAuthenticated ? (
          <button className="primary-button" type="submit" disabled={applied} style={{ marginTop: 16 }}>
            {applied ? 'درخواست ثبت شد' : 'ارسال درخواست'}
          </button>
        ) : (
          <p className="help-text" style={{ marginTop: 16 }}>برای ثبت درخواست ابتدا <Link to="/login">وارد</Link> شوید.</p>
        )}
      </form>
    </div>
  )
}
