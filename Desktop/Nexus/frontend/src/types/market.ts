export interface Product {
  id: number
  seller_id: number
  title: string
  description: string
  category: string
  price: number
  currency: string
  cover_url?: string | null
  demo_url?: string | null
  tags: string
  rating: number
  sales: number
  is_published: boolean
  created_at: string
  updated_at: string
}

export interface ProductCreatePayload {
  title: string
  description: string
  category: string
  price: number
  currency?: string
  cover_url?: string
  demo_url?: string
  tags?: string
}

export interface Review {
  id: number
  product_id: number
  user_id: number
  rating: number
  comment?: string | null
  created_at: string
}

export interface Order {
  id: number
  product_id: number
  buyer_id: number
  amount: number
  currency: string
  status: string
  created_at: string
}
