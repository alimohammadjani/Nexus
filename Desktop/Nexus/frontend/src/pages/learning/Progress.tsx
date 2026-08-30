import { useCallback, useEffect, useState } from 'react'
import { fetchCourses } from '../../api/roadmap'
import type { Course } from '../../types/roadmap'
import { useAuth } from '../../store/authStore'
import Loading from '../../components/Loading'

export default function Progress() {
  const { user } = useAuth()
  const [courses, setCourses] = useState<Course[]>([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      setCourses(await fetchCourses())
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void load()
  }, [load])

  return (
    <div className="content-section">
      <h1 className="page-title">پیشرفت یادگیری</h1>
      <p className="page-subtitle">وضعیت دوره‌ها و مسیرهای در حال یادگیری شما.</p>
      {loading ? <Loading /> : (
        <div className="panel">
          <div className="profile-strip">
            <div className="avatar">{user?.full_name?.[0] ?? 'و'}</div>
            <div><strong>{user?.full_name}</strong><span>{courses.length} دوره فعال در DevHub</span></div>
          </div>
          <div className="list-stack" style={{ marginTop: 22 }}>
            <div className="list-item">
              <div><strong>تکمیل پروفایل</strong><span className="help-text">مهارت‌ها و پروژه‌ها را تکمیل کنید</span></div>
              <b>۰٪</b>
            </div>
            {courses.map((course) => (
              <div className="list-item" key={course.id}>
                <div><strong>{course.title}</strong><span className="help-text">{course.lessons.length} درس</span></div>
                <b>۰٪</b>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
