import { Fragment, useState } from 'react'
import type { CSSProperties } from 'react'
import { Link } from 'react-router-dom'
import { useRoadmap } from '../../hooks/useRoadmap'
import type { Course, Roadmap as RoadmapType } from '../../types/roadmap'
import Loading from '../../components/Loading'
import ErrorState from '../../components/ErrorState'
import './learning.css'

const TRACKS = [
  { value: '', label: 'همه' },
  { value: 'frontend', label: 'فرانت‌اند' },
  { value: 'backend', label: 'بک‌اند' },
  { value: 'devops', label: 'DevOps' },
  { value: 'mobile', label: 'موبایل' },
]

const CATEGORY_ICON: Record<string, string> = {
  frontend: '🎨',
  backend: '⚙️',
  devops: '🚀',
  mobile: '📱',
}

export default function Roadmap() {
  const [category, setCategory] = useState<string | undefined>()
  const { roadmaps, courses, loading, error, reload } = useRoadmap(category)

  return (
    <div className="content-section" style={{ '--accent': '#8b5cf6' } as CSSProperties}>
      <div className="learning-hero">
        <div>
          <h1>یادگیری رایگان</h1>
          <p className="page-subtitle" style={{ marginTop: 8 }}>
            مسیرهای شغلی تعاملی با آموزش واقعی، منابع معتبر و پروژه‌های عملی — دقیقاً مثل نقشه‌راه‌های حرفه‌ای.
          </p>
        </div>
      </div>

      <div className="track-filter">
        {TRACKS.map((t) => (
          <button
            key={t.value}
            type="button"
            className={category === t.value ? 'active' : ''}
            onClick={() => setCategory(t.value || undefined)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {loading ? (
        <Loading text="در حال دریافت مسیرها…" />
      ) : error ? (
        <ErrorState message={error} onRetry={reload} />
      ) : (
        <>
          <h2 className="section-title">Roadmap ها</h2>
          <div className="rm-grid" style={{ marginBottom: 12 }}>
            {roadmaps.length === 0 && <div className="state-block">Roadmap یافت نشد.</div>}
            {roadmaps.map((roadmap) => (
              <RoadmapCard key={roadmap.id} roadmap={roadmap} />
            ))}
          </div>

          <h2 className="section-title">دوره‌های رایگان / پولی</h2>
          <div className="rm-grid">
            {courses.length === 0 && <div className="state-block">دوره‌ای یافت نشد.</div>}
            {courses.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function RoadmapCard({ roadmap }: { roadmap: RoadmapType }) {
  const accent = roadmap.color ?? '#8b5cf6'
  const icon = CATEGORY_ICON[roadmap.category] ?? '🧭'
  const preview = roadmap.stages.slice(0, 6)
  return (
    <Link
      className="rm-card"
      to={`/learning/roadmap/${roadmap.id}`}
      style={{ '--accent': accent } as CSSProperties}
    >
      <div className="rm-card-head">
        <span className="rm-icon" style={{ background: accent }}>
          {icon}
        </span>
        <span className="badge badge-cyan">{roadmap.category}</span>
      </div>
      <h3>{roadmap.title}</h3>
      <p>{roadmap.subtitle ?? roadmap.description}</p>

      <div className="rm-preview">
        <div className="rm-preview-col">
          {preview.map((stage, i) => (
            <Fragment key={stage.id}>
              <span className="rm-preview-node">{stage.order}</span>
              {i < preview.length - 1 && <span className="rm-preview-line" />}
            </Fragment>
          ))}
        </div>
        <div className="rm-preview-text">
          <span className="help-text">{roadmap.stages.length} مرحله آموزشی تعاملی</span>
        </div>
      </div>

      <div className="rm-meta">
        <span className="help-text">روی نقشه کلیک کنید</span>
        <span className="badge" style={{ background: 'rgba(255,255,255,0.08)', color: 'var(--text)' }}>
          مشاهده →
        </span>
      </div>
    </Link>
  )
}

function CourseCard({ course }: { course: Course }) {
  return (
    <Link
      className="rm-card"
      to={`/learning/course/${course.id}`}
      style={{ '--accent': '#06b6d4' } as CSSProperties}
    >
      <div className="rm-card-head">
        <span className="rm-icon" style={{ background: '#06b6d4' }}>
          📚
        </span>
        <span className={course.is_free ? 'badge badge-green' : 'badge badge-amber'}>
          {course.is_free ? 'رایگان' : `${course.price.toLocaleString('fa-IR')} تومان`}
        </span>
      </div>
      <h3>{course.title}</h3>
      <p>{course.description}</p>
      <div className="rm-meta">
        <span className="help-text">
          {course.level} • {course.duration_hours} ساعت • {course.lessons.length} درس
        </span>
        <span className="badge" style={{ background: 'rgba(255,255,255,0.08)', color: 'var(--text)' }}>
          شروع →
        </span>
      </div>
    </Link>
  )
}
