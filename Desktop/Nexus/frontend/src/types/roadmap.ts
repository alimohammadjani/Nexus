export interface RoadmapStage {
  id: number
  roadmap_id: number
  order: number
  title: string
  description?: string | null
  content?: string | null
  resources?: string | null
  project?: string | null
  checkpoint?: string | null
}

export interface Roadmap {
  id: number
  title: string
  subtitle?: string | null
  description?: string | null
  category: string
  color?: string | null
  is_published: boolean
  created_at: string
  stages: RoadmapStage[]
}

export interface Lesson {
  id: number
  course_id: number
  order: number
  title: string
  content?: string | null
  video_url?: string | null
  duration_minutes: number
}

export interface Course {
  id: number
  title: string
  description: string
  category: string
  level: string
  instructor_name?: string | null
  cover_url?: string | null
  duration_hours: number
  is_free: boolean
  price: number
  created_at: string
  lessons: Lesson[]
}

export interface Enrollment {
  id: number
  course_id: number
  user_id: number
  progress: number
  completed: boolean
  enrolled_at: string
}
