import { del, get, post, put } from './client'
import type { Job, JobApplication, JobCreatePayload, JobUpdatePayload } from '../types/job'

export interface JobFilters {
  search?: string
  skill?: string
  type?: string
  mode?: string
  level?: string
}

export const fetchJobs = (filters: JobFilters = {}) =>
  get<Job[]>('/jobs', {
    search: filters.search,
    skill: filters.skill,
    type: filters.type,
    mode: filters.mode,
    level: filters.level,
  })

export const fetchJob = (id: number) => get<Job>(`/jobs/${id}`)

export const createJob = (payload: JobCreatePayload) => post<Job>('/jobs', payload)

export const updateJob = (id: number, payload: JobUpdatePayload) => put<Job>(`/jobs/${id}`, payload)

export const deleteJob = (id: number) => del<void>(`/jobs/${id}`)

export const applyToJob = (id: number, coverLetter?: string) =>
  post<JobApplication>(`/jobs/${id}/apply`, { cover_letter: coverLetter })

export const fetchApplications = (jobId: number) => get<JobApplication[]>(`/jobs/${jobId}/applications`)
