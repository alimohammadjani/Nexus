import { useCallback, useEffect, useState } from 'react'
import { fetchProducts, type ProductFilters } from '../api/market'
import type { Product } from '../types/market'

export function useMarket(filters: ProductFilters = {}) {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const filterKey = JSON.stringify(filters)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      setProducts(await fetchProducts(filters))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'خطا در دریافت محصولات')
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterKey])

  useEffect(() => {
    void load()
  }, [load])

  return { products, loading, error, reload: load }
}
