import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useRoadmap } from '../../hooks/useRoadmap'
import type { Course, Roadmap as RoadmapType } from '../../types/roadmap'
import Loading from '../../components/Loading'
import ErrorState from '../../components/ErrorState'

export default function Roadmap() {
  const [category, setCategory] = useState<string | undefined>()
  const { roadmaps, courses, loading, error, reload } = useRoadmap(category)

  return (
    <div className="content-section">
      <div className="page-heading">
        <div>
          <h1 className="page-title">یادگیری رایگان</h1>
          <p className="page-subtitle">مسیرهای شغلی با پروژه عملی، منابع رایگان و checkpoint برای اندازه‌گیری پیشرفت.</p>
        </div>
        <select className="select" value={category ?? ''} onChange={(e) => setCategory(e.target.value || undefined)}>
          <option value="">همه دسته‌ها</option>
          <option value="frontend">Frontend</option>
          <option value="backend">Backend</option>
          <option value="devops">DevOps</option>
          <option value="mobile">Mobile</option>
        </select>
      </div>

      {loading ? <Loading text="در حال دریافت مسیرها…" /> : error ? <ErrorState message={error} onRetry={reload} /> : (
        <>
          <h2 className="section-label">Roadmap ها</h2>
          <div className="grid-3" style={{ marginBottom: 28 }}>
            {roadmaps.length === 0 && <div className="state-block">Roadmap یافت نشد.</div>}
            {roadmaps.map((roadmap) => <RoadmapCard roadmap={roadmap} key={roadmap.id} />)}
          </div>

          <h2 className="section-label">دوره‌های رایگان / پولی</h2>
          <div className="grid-3">
            {courses.length === 0 && <div className="state-block">دوره‌ای یافت نشد.</div>}
            {courses.map((course) => <CourseCard course={course} key={course.id} />)}
          </div>
        </>
      )}
    </div>
  )
}

function RoadmapCard({ roadmap }: { roadmap: RoadmapType }) {
  return (
    <Link className="panel" to={`/learning/${roadmap.id}`}>
      <div className="row-meta"><span className="badge badge-cyan">{roadmap.category}</span></div>
      <h3 style={{ margin: '12px 0 8px' }}>{roadmap.title}</h3>
      <p className="help-text">{roadmap.subtitle ?? roadmap.description}</p>
      <div className="progress-track" style={{ marginTop: 18 }}><div className="progress-fill" style={{ width: `${Math.min(100, roadmap.stages.length * 25)}%` }} /></div>
      <p className="help-text" style={{ marginTop: 12 }}>{roadmap.stages.length} مرحله</p>
    </Link>
  )
}

function CourseCard({ course }: { course: Course }) {
  return (
    <Link className="panel" to={`/learning/course/${course.id}`}>
      <div className="row-meta">
        <span className="badge badge-purple">{course.category}</span>
        <span className={course.is_free ? 'badge badge-green' : 'badge badge-amber'}>
          {course.is_free ? 'رایگان' : `${course.price.toLocaleString('fa-IR')} تومان`}
        </span>
      </div>
      <h3 style={{ margin: '12px 0 8px' }}>{course.title}</h3>
      <p className="help-text">{course.level} • {course.duration_hours} ساعت • {course.lessons.length} درس</p>
    </Link>
  )
}
