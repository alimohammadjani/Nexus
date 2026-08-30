import { get, post } from './client'
import type { Course, Enrollment, Roadmap } from '../types/roadmap'

export const fetchRoadmaps = (category?: string) =>
  get<Roadmap[]>('/roadmaps', { category })

export const fetchRoadmap = (id: number) => get<Roadmap>(`/roadmaps/${id}`)

export const fetchCourses = (category?: string, freeOnly = false) =>
  get<Course[]>('/learning/courses', { category, free_only: freeOnly })

export const fetchCourse = (id: number) => get<Course>(`/learning/courses/${id}`)

export const enrollCourse = (courseId: number) => post<Enrollment>(`/learning/courses/${courseId}/enroll`)

export const completeLesson = (courseId: number, lessonId: number) =>
  post<{ id: number; lesson_id: number; user_id: number; completed: boolean; completed_at: string | null }>(
    `/learning/courses/${courseId}/lessons/${lessonId}/complete`,
  )
