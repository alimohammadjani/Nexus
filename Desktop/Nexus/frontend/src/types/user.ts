export type UserRole = 'developer' | 'employer' | 'admin'

export interface Skill {
  id: number
  name: string
  level: 'beginner' | 'intermediate' | 'expert' | string
}

export interface User {
  id: number
  email: string
  full_name: string
  role: UserRole
  bio?: string | null
  avatar_url?: string | null
  location?: string | null
  is_active: boolean
  is_verified: boolean
  is_employer: boolean
  company?: string | null
  skills: Skill[]
  created_at: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  full_name: string
  password: string
  role?: string
}

export interface UpdateUserPayload {
  full_name?: string
  bio?: string
  avatar_url?: string
  location?: string
  is_employer?: boolean
  company?: string
  password?: string
}
