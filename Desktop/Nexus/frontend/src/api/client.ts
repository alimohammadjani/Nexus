const API_BASE = import.meta.env.VITE_API_URL ?? '/api/v1'

const TOKEN_KEY = 'devhub_token'

export const setToken = (token: string | null) => {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token)
  } else {
    localStorage.removeItem(TOKEN_KEY)
  }
}

export const getToken = () => localStorage.getItem(TOKEN_KEY)

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function api<T>(
  path: string,
  options: RequestInit & { query?: Record<string, string | number | boolean | undefined> } = {},
): Promise<T> {
  const url = new URL(`${API_BASE}${path}`, window.location.origin)
  if (options.query) {
    Object.entries(options.query).forEach(([key, value]) => {
      if (value !== undefined && value !== '') url.searchParams.set(key, String(value))
    })
  }

  const headers = new Headers(options.headers)
  const token = getToken()
  if (token) headers.set('Authorization', `Bearer ${token}`)
  if (options.body && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json')
  }

  const response = await fetch(url.toString(), { ...options, headers })
  if (response.status === 204) return undefined as T

  const text = await response.text()
  let data: unknown = null
  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = text
  }

  if (!response.ok) {
    const message =
      (data as { detail?: string } | undefined)?.detail ||
      `Request failed with status ${response.status}`
    if (response.status === 401) setToken(null)
    throw new ApiError(message, response.status)
  }

  return data as T
}

export const get = <T>(
  path: string,
  query?: Record<string, string | number | boolean | undefined>,
) => api<T>(path, { method: 'GET', query })

export const post = <T>(path: string, body?: unknown, query?: Record<string, string | number | boolean | undefined>) =>
  api<T>(path, { method: 'POST', body: body ? JSON.stringify(body) : undefined, query })

export const put = <T>(path: string, body?: unknown) =>
  api<T>(path, { method: 'PUT', body: body ? JSON.stringify(body) : undefined })

export const del = <T>(path: string) => api<T>(path, { method: 'DELETE' })
