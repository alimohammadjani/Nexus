import { get, post, setToken } from './client'
import type { LoginPayload, RegisterPayload, User } from '../types/user'

export async function login(payload: LoginPayload) {
  const result = await post<{ access_token: string; token_type: string; user: User }>('/auth/login', payload)
  setToken(result.access_token)
  return result
}

export async function register(payload: RegisterPayload) {
  const user = await post<User>('/auth/register', payload)
  return user
}

export async function fetchMe() {
  return get<User>('/users/me')
}

export async function logout() {
  setToken(null)
}
