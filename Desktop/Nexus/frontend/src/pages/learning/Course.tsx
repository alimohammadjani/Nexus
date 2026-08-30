import { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { completeLesson, enrollCourse, fetchCourse, fetchRoadmap } from '../../api/roadmap'
import type { Course as CourseType, Lesson, Roadmap as RoadmapType } from '../../types/roadmap'
import { useAuth } from '../../store/authStore'
import { useUI } from '../../store/uiStore'
import Loading from '../../components/Loading'
import ErrorState from '../../components/ErrorState'

export default function Course() {
  const { id, type } = useParams()
  const { isAuthenticated } = useAuth()
  const { notify } = useUI()
  const [course, setCourse] = useState<CourseType | null>(null)
  const [roadmap, setRoadmap] = useState<RoadmapType | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [enrolled, setEnrolled] = useState(false)

  const load = useCallback(async () => {
    if (!id) return
    setLoading(true)
    setError(null)
    try {
      if (type === 'course') {
        setCourse(await fetchCourse(Number(id)))
      } else {
        setRoadmap(await fetchRoadmap(Number(id)))
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'محتوا پیدا نشد.')
    } finally {
      setLoading(false)
    }
  }, [id, type])

  useEffect(() => {
    void load()
  }, [load])

  async function handleEnroll() {
    if (!course || !isAuthenticated) return
    try {
      await enrollCourse(course.id)
      setEnrolled(true)
      notify('در دوره ثبت‌نام کردید!')
    } catch (err) {
      notify(err instanceof Error ? err.message : 'ثبت‌نام ناموفق بود.', 'error')
    }
  }

  async function handleCompleteLesson(lesson: Lesson) {
    if (!course || !isAuthenticated) return
    try {
      await completeLesson(course.id, lesson.id)
      notify('پیشرفت ذخیره شد!')
    } catch (err) {
      notify(err instanceof Error ? err.message : 'ذخیره پیشرفت ناموفق بود.', 'error')
    }
  }

  if (loading) return <Loading />
  if (error) return <ErrorState message={error} onRetry={load} />

  if (roadmap) {
    return (
      <div className="content-section">
        <Link to="/learning" className="ghost-link">← بازگشت به یادگیری</Link>
        <h1 className="page-title" style={{ marginTop: 18 }}>{roadmap.title}</h1>
        <p className="page-subtitle">{roadmap.subtitle ?? roadmap.description}</p>
        <div className="list-stack">
          {roadmap.stages.map((stage) => (
            <div className="panel list-item" key={stage.id}>
              <div>
                <div className="row-meta">
                  <span className="badge badge-purple">{stage.order}</span>
                </div>
                <h3 style={{ margin: '8px 0 4px' }}>{stage.title}</h3>
                <p>{stage.description}</p>
                {stage.resources && <p className="help-text">منابع: {stage.resources}</p>}
                {stage.project && <p className="help-text">پروژه: {stage.project}</p>}
              </div>
              {stage.checkpoint && <span className="badge badge-amber">{stage.checkpoint}</span>}
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (!course) return <ErrorState message="دوره پیدا نشد." onRetry={load} />

  return (
    <div className="content-section">
      <Link to="/learning" className="ghost-link">← بازگشت به یادگیری</Link>
      <div className="page-heading" style={{ marginTop: 18 }}>
        <div>
          <div className="row-meta">
            <span className="badge badge-purple">{course.category}</span>
            <span className="badge badge-cyan">{course.level}</span>
            <span className={course.is_free ? 'badge badge-green' : 'badge badge-amber'}>
              {course.is_free ? 'رایگان' : `${course.price.toLocaleString('fa-IR')} تومان`}
            </span>
          </div>
          <h1 className="page-title">{course.title}</h1>
          <p className="page-subtitle">{course.description}</p>
        </div>
        <button className="primary-button" onClick={handleEnroll} type="button">
          {enrolled ? 'ثبت‌نام شده' : 'ثبت‌نام در دوره'}
        </button>
      </div>

      <div className="panel">
        <h2 className="panel-title">درس‌ها</h2>
        {course.lessons.map((lesson) => (
          <div className="lesson-row" key={lesson.id}>
            <span className="badge badge-cyan">{lesson.order}</span>
            <div><strong>{lesson.title}</strong>{lesson.content && <p className="help-text">{lesson.content}</p>}</div>
            <button className="secondary-button" type="button" onClick={() => handleCompleteLesson(lesson)}>
              علامت‌گذاری تکمیل
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
