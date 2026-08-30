import { del, get, post, put } from './client'
import type { Order, Product, ProductCreatePayload, Review } from '../types/market'

export interface ProductFilters {
  category?: string
  search?: string
  min_price?: number
  max_price?: number
}

export const fetchProducts = (filters: ProductFilters = {}) =>
  get<Product[]>('/market/products', {
    category: filters.category,
    search: filters.search,
    min_price: filters.min_price,
    max_price: filters.max_price,
  })

export const fetchProduct = (id: number) => get<Product>(`/market/products/${id}`)

export const createProduct = (payload: ProductCreatePayload) => post<Product>('/market/products', payload)

export const updateProduct = (id: number, payload: Partial<ProductCreatePayload>) =>
  put<Product>(`/market/products/${id}`, payload)

export const deleteProduct = (id: number) => del<void>(`/market/products/${id}`)

export const addReview = (productId: number, rating: number, comment?: string) =>
  post<Review>(`/market/products/${productId}/reviews`, { rating, comment })

export const fetchReviews = (productId: number) => get<Review[]>(`/market/products/${productId}/reviews`)

export const createOrder = (productId: number) => post<Order>('/market/orders', { product_id: productId })
