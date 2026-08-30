import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchProducts, type ProductFilters } from '../../api/market'
import type { Product } from '../../types/market'
import { formatPrice } from '../../utils/formatters'
import Loading from '../../components/Loading'
import ErrorState from '../../components/ErrorState'

const categories = ['همه', 'template', 'plugin', 'api', 'script', 'course']

export default function MarketList() {
  const [filters, setFilters] = useState<ProductFilters>({})
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

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
  }, [JSON.stringify(filters)])

  useEffect(() => {
    void load()
  }, [load])

  return (
    <div className="content-section">
      <div className="page-heading">
        <div>
          <h1 className="page-title">مارکت ابزار</h1>
          <p className="page-subtitle">قالب، پلاگین، API و اسکریپت را با ریویو و رتبه‌بندی از توسعه‌دهندگان دیگر بخرید یا بفروشید.</p>
        </div>
        <Link className="primary-button" to="/market/sell">فروش محصول</Link>
      </div>

      <div className="filter-bar">
        <input className="input" placeholder="جستجوی محصول…" value={filters.search ?? ''} onChange={(e) => setFilters((f) => ({ ...f, search: e.target.value }))} />
        <select className="select" value={filters.category ?? ''} onChange={(e) => setFilters((f) => ({ ...f, category: e.target.value || undefined }))}>
          {categories.map((category) => <option key={category} value={category === 'همه' ? '' : category}>{category === 'همه' ? 'همه دسته‌ها' : category}</option>)}
        </select>
      </div>

      {loading ? <Loading text="در حال دریافت محصولات…" /> : error ? <ErrorState message={error} onRetry={load} /> : products.length === 0 ? (
        <div className="state-block">محصولی منتشر نشده است.</div>
      ) : (
        <div className="market-grid">
          {products.map((product) => (
            <Link className="product-card" to={`/market/${product.id}`} key={product.id}>
              <div className="product-preview"><span>{product.category}</span></div>
              <div className="product-body">
                <h3>{product.title}</h3>
                <div className="rating-row"><span>★ {product.rating?.toFixed(1) ?? '0'}</span><span>{product.sales} فروش</span></div>
                <strong>{formatPrice(product.price, product.currency)}</strong>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
