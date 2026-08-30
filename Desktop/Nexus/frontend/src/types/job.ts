export type JobType = 'full_time' | 'part_time' | 'freelance' | 'contract'
export type JobMode = 'remote' | 'hybrid' | 'on_site'

export interface Job {
  id: number
  owner_id: number
  title: string
  company: string
  description: string
  location?: string | null
  type: JobType
  mode: JobMode
  level: string
  salary_range?: string | null
  skills: string
  is_active: boolean
  is_featured: boolean
  views: number
  budget?: number | null
  created_at: string
  updated_at: string
}

export interface JobCreatePayload {
  title: string
  company: string
  description: string
  location?: string
  type?: JobType
  mode?: JobMode
  level?: string
  salary_range?: string
  skills?: string
  budget?: number
}

export interface JobUpdatePayload extends Partial<JobCreatePayload> {
  is_active?: boolean
}

export interface JobApplication {
  id: number
  job_id: number
  candidate_id: number
  status: string
  cover_letter?: string | null
  created_at: string
  updated_at: string
}
