import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchJobs, type JobFilters } from '../../api/jobs'
import type { Job } from '../../types/job'
import { jobModeLabel, jobTypeLabel } from '../../utils/formatters'
import Loading from '../../components/Loading'
import ErrorState from '../../components/ErrorState'

export default function JobList() {
  const [filters, setFilters] = useState<JobFilters>({})
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      setJobs(await fetchJobs(filters))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'خطا در دریافت فرصت‌ها')
    } finally {
      setLoading(false)
    }
  }, [JSON.stringify(filters)])

  useEffect(() => {
    void load()
  }, [load])

  return (
    <div className="content-section">
      <div className="page-heading">
        <div>
          <h1 className="page-title">فرصت‌های پروژه و استخدام</h1>
          <p className="page-subtitle">پروژه‌های رایگان، فریلنسری و آگهی‌های استخدام را با فیلتر مهارت، سطح و حالت کاری ببینید.</p>
        </div>
        <Link className="primary-button" to="/jobs/new">ثبت فرصت</Link>
      </div>

      <div className="filter-bar">
        <input className="input" placeholder="جستجو در عنوان یا شرکت…" value={filters.search ?? ''} onChange={(e) => setFilters((f) => ({ ...f, search: e.target.value }))} />
        <input className="input" placeholder="مهارت، مثلاً React" value={filters.skill ?? ''} onChange={(e) => setFilters((f) => ({ ...f, skill: e.target.value }))} />
        <select className="select" value={filters.mode ?? ''} onChange={(e) => setFilters((f) => ({ ...f, mode: e.target.value || undefined }))}>
          <option value="">همه حالت‌ها</option>
          <option value="remote">ریموت</option>
          <option value="hybrid">هیبرید</option>
          <option value="on_site">حضوری</option>
        </select>
        <select className="select" value={filters.level ?? ''} onChange={(e) => setFilters((f) => ({ ...f, level: e.target.value || undefined }))}>
          <option value="">همه سطح‌ها</option>
          <option value="junior">جونیور</option>
          <option value="mid">میدل</option>
          <option value="senior">سینیور</option>
        </select>
      </div>

      {loading ? <Loading text="در حال دریافت فرصت‌ها…" /> : error ? <ErrorState message={error} onRetry={load} /> : jobs.length === 0 ? (
        <div className="state-block">هنوز فرصتی ثبت نشده است.</div>
      ) : (
        <div className="list-stack">
          {jobs.map((job) => (
            <Link className="panel list-item" to={`/jobs/${job.id}`} key={job.id}>
              <div>
                <div className="row-meta">
                  {job.is_featured && <span className="badge badge-purple">پریمیوم</span>}
                  <span className="badge badge-cyan">{jobTypeLabel(job.type)}</span>
                  <span className="badge badge-green">{jobModeLabel(job.mode)}</span>
                </div>
                <h3 style={{ margin: '8px 0 0' }}>{job.title}</h3>
                <p className="meta">
                  <span>{job.company}</span> • <span>{job.location ?? 'ریموت'}</span> • <span>{job.salary_range ?? 'بودجه توافقی'}</span>
                </p>
              </div>
              <strong style={{ color: '#c4b5fd' }}>{job.level}</strong>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
