import { useCallback, useEffect, useState } from 'react'
import type { CSSProperties } from 'react'
import { Link, useParams } from 'react-router-dom'
import { completeLesson, enrollCourse, fetchCourse } from '../../api/roadmap'
import type { Course as CourseType, Lesson } from '../../types/roadmap'
import { renderContent } from '../../utils/content'
import { useAuth } from '../../store/authStore'
import { useUI } from '../../store/uiStore'
import Loading from '../../components/Loading'
import ErrorState from '../../components/ErrorState'
import './learning.css'

export default function Course() {
  const { id } = useParams()
  const { isAuthenticated } = useAuth()
  const { notify } = useUI()
  const [course, setCourse] = useState<CourseType | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [enrolled, setEnrolled] = useState(false)
  const [selected, setSelected] = useState<Lesson | null>(null)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [doneLessons, setDoneLessons] = useState<number[]>([])

  const load = useCallback(async () => {
    if (!id) return
    setLoading(true)
    setError(null)
    try {
      const data = await fetchCourse(Number(id))
      setCourse(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'دوره پیدا نشد.')
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    void load()
  }, [load])

  function openLesson(lesson: Lesson) {
    setSelected(lesson)
    setDrawerOpen(true)
  }

  const selectedIndex = selected && course ? course.lessons.findIndex((l) => l.id === selected.id) : -1

  function goToLesson(delta: number) {
    if (!course || selectedIndex < 0) return
    const next = course.lessons[selectedIndex + delta]
    if (next) setSelected(next)
  }

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
      setDoneLessons((prev) => (prev.includes(lesson.id) ? prev : [...prev, lesson.id]))
      notify('پیشرفت ذخیره شد!')
    } catch (err) {
      notify(err instanceof Error ? err.message : 'ذخیره پیشرفت ناموفق بود.', 'error')
    }
  }

  if (loading) return <Loading />
  if (error) return <ErrorState message={error} onRetry={load} />
  if (!course) return <ErrorState message="دوره پیدا نشد." onRetry={load} />

  return (
    <div className="content-section" style={{ '--accent': '#06b6d4' } as CSSProperties}>
      <Link to="/learning" className="ghost-link">
        ← بازگشت به یادگیری
      </Link>

      <div className="roadmap-header" style={{ marginTop: 18 }}>
        <div className="roadmap-title">
          <span className="rm-icon" style={{ background: '#06b6d4' }}>
            📚
          </span>
          <div className="roadmap-title-text">
            <h1>{course.title}</h1>
            <p>{course.description}</p>
          </div>
        </div>
        <div className="roadmap-tools">
          <span className="badge badge-purple">{course.category}</span>
          <span className="badge badge-cyan">{course.level}</span>
          <span className={course.is_free ? 'badge badge-green' : 'badge badge-amber'}>
            {course.is_free ? 'رایگان' : `${course.price.toLocaleString('fa-IR')} تومان`}
          </span>
        </div>
      </div>

      <div className="roadmap-progress">
        <div className="roadmap-progress-label">
          {course.duration_hours} ساعت آموزش • {course.lessons.length} درس • مدرس: {course.instructor_name ?? 'تیم DevHub'}
        </div>
      </div>

      <div style={{ marginBottom: 20 }}>
        <button className="primary-button" type="button" onClick={handleEnroll}>
          {enrolled ? 'ثبت‌نام شده ✓' : 'ثبت‌نام در دوره'}
        </button>
      </div>

      <div className="panel">
        <h2 className="panel-title">درس‌ها</h2>
        <div className="lesson-list">
          {course.lessons.map((lesson, i) => {
            const done = doneLessons.includes(lesson.id)
            return (
              <div className="lesson-row-item" key={lesson.id} style={{ animationDelay: `${i * 60}ms` }}>
                <button type="button" className="lesson-main" onClick={() => openLesson(lesson)}>
                  <span className={`roadmap-order ${done ? 'done' : ''}`}>{lesson.order}</span>
                  <span className="lesson-info">
                    <strong>{lesson.title}</strong>
                    {lesson.content && <span className="help-text">کلیک کنید تا آموزش باز شود</span>}
                  </span>
                  <span className="help-text">{lesson.duration_minutes} دقیقه</span>
                </button>
                <button
                  className="secondary-button"
                  type="button"
                  onClick={() => handleCompleteLesson(lesson)}
                >
                  {done ? 'تکمیل شد ✓' : 'علامت‌گذاری تکمیل'}
                </button>
              </div>
            )
          })}
        </div>
      </div>

      <div className={`drawer-backdrop ${drawerOpen ? 'open' : ''}`} onClick={() => setDrawerOpen(false)} />
      <aside className={`training-drawer ${drawerOpen ? 'open' : ''}`} aria-hidden={!drawerOpen}>
        {selected && (
          <>
            <div key={selected.id} className="drawer-head drawerAnim">
              <div>
                <h2>{selected.title}</h2>
                <p className="help-text">{selected.duration_minutes} دقیقه مطالعه</p>
              </div>
              <button className="drawer-close" type="button" onClick={() => setDrawerOpen(false)} aria-label="بستن">
                ✕
              </button>
            </div>
            <div key={selected.id} className="drawer-body drawerAnim">
              {selected.content ? (
                <div className="training-section">
                  <span className="label">آموزش درس</span>
                  {renderContent(selected.content)}
                </div>
              ) : (
                <div className="training-section">
                  <div className="training-card">
                    <p>برای این درس محتوای متنی ثبت نشده است.</p>
                  </div>
                </div>
              )}
              {selected.video_url && (
                <div className="training-section">
                  <span className="label">ویدیو</span>
                  <a className="resource-link" href={selected.video_url} target="_blank" rel="noreferrer noopener">
                    <span className="rl-dot" />
                    <span className="rl-text">مشاهده ویدیو آموزشی</span>
                  </a>
                </div>
              )}
            </div>

            {selectedIndex >= 0 && (
              <div key={selected.id} className="drawer-nav drawerAnim">
                <button
                  type="button"
                  className="nav-btn"
                  onClick={() => goToLesson(-1)}
                  disabled={selectedIndex === 0}
                >
                  → درس قبلی
                </button>
                <span className="drawer-nav-count">
                  درس {selectedIndex + 1} از {course.lessons.length}
                </span>
                <button
                  type="button"
                  className="nav-btn"
                  onClick={() => goToLesson(1)}
                  disabled={selectedIndex === course.lessons.length - 1}
                >
                  درس بعدی ←
                </button>
              </div>
            )}

            <div className="drawer-foot">
              <button
                type="button"
                className={`done-btn ${doneLessons.includes(selected.id) ? 'active' : ''}`}
                onClick={() => handleCompleteLesson(selected)}
              >
                {doneLessons.includes(selected.id) ? '✓ تکمیل شد — برداشتن علامت' : 'علامت‌گذاری به‌عنوان تکمیل‌شده'}
              </button>
            </div>
          </>
        )}
      </aside>
    </div>
  )
}
