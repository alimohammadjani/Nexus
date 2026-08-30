import { useCallback, useEffect, useState } from 'react'
import { fetchCourses, fetchRoadmaps } from '../api/roadmap'
import type { Course, Roadmap } from '../types/roadmap'

export function useRoadmap(category?: string) {
  const [roadmaps, setRoadmaps] = useState<Roadmap[]>([])
  const [courses, setCourses] = useState<Course[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [roadmapData, courseData] = await Promise.all([fetchRoadmaps(category), fetchCourses(category)])
      setRoadmaps(roadmapData)
      setCourses(courseData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'خطا در دریافت مسیر آموزشی')
    } finally {
      setLoading(false)
    }
  }, [category])

  useEffect(() => {
    void load()
  }, [load])

  return { roadmaps, courses, loading, error, reload: load }
}
