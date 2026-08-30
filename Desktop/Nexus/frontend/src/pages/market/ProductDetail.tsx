import { useCallback, useEffect, useState, type FormEvent } from 'react'
import { Link, useParams } from 'react-router-dom'
import { addReview, createOrder, fetchProduct, fetchReviews } from '../../api/market'
import type { Product, Review } from '../../types/market'
import { formatDate, formatPrice, splitSkills } from '../../utils/formatters'
import { useAuth } from '../../store/authStore'
import { useUI } from '../../store/uiStore'
import Loading from '../../components/Loading'
import ErrorState from '../../components/ErrorState'

export default function ProductDetail() {
  const { id } = useParams()
  const { isAuthenticated } = useAuth()
  const { notify } = useUI()
  const [product, setProduct] = useState<Product | null>(null)
  const [reviews, setReviews] = useState<Review[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [rating, setRating] = useState(5)
  const [comment, setComment] = useState('')
  const [buying, setBuying] = useState(false)

  const load = useCallback(async () => {
    if (!id) return
    setLoading(true)
    try {
      const [productData, reviewData] = await Promise.all([
        fetchProduct(Number(id)),
        fetchReviews(Number(id)).catch(() => []),
      ])
      setProduct(productData)
      setReviews(reviewData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'محصول پیدا نشد.')
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    void load()
  }, [load])

  async function handleBuy() {
    if (!product) return
    setBuying(true)
    try {
      await createOrder(product.id)
      notify('خرید با موفقیت انجام شد!')
      await load()
    } catch (err) {
      notify(err instanceof Error ? err.message : 'خرید ناموفق بود.', 'error')
    } finally {
      setBuying(false)
    }
  }

  async function handleReview(e: FormEvent) {
    e.preventDefault()
    if (!product) return
    try {
      await addReview(product.id, rating, comment)
      notify('نظر شما ثبت شد!')
      setComment('')
      await load()
    } catch (err) {
      notify(err instanceof Error ? err.message : 'ثبت نظر ناموفق بود.', 'error')
    }
  }

  if (loading) return <Loading />
  if (error || !product) return <ErrorState message={error ?? 'محصول پیدا نشد.'} onRetry={load} />

  return (
    <div className="content-section">
      <Link to="/market" className="ghost-link">← بازگشت به مارکت</Link>
      <div className="grid-2" style={{ marginTop: 18 }}>
        <div className="panel">
          <div className="product-preview" style={{ height: 220 }}>
            <span>{product.category}</span>
          </div>
          <h1 style={{ margin: '18px 0 8px' }}>{product.title}</h1>
          <p>{product.description}</p>
          <div className="skill-row" style={{ marginTop: 16 }}>
            {splitSkills(product.tags).map((tag) => <span className="skill-tag" key={tag}>{tag}</span>)}
          </div>
        </div>
        <div className="panel">
          <div className="row-meta">
            <span className="badge badge-green">★ {product.rating?.toFixed(1) ?? '0'}</span>
            <span className="badge badge-amber">{product.sales} فروش</span>
          </div>
          <h2 className="panel-title">{formatPrice(product.price, product.currency)}</h2>
          {product.demo_url && <a className="ghost-link" href={product.demo_url} target="_blank" rel="noreferrer">دمو / پیش‌نمایش</a>}
          <div style={{ marginTop: 20 }}>
            {isAuthenticated ? (
              <button className="primary-button" onClick={handleBuy} disabled={buying} type="button">
                {buying ? 'در حال خرید…' : 'خرید محصول'}
              </button>
            ) : (
              <p className="help-text">برای خرید ابتدا <Link to="/login">وارد</Link> شوید.</p>
            )}
          </div>
          <p className="help-text" style={{ marginTop: 16 }}>انتشار: {formatDate(product.created_at)}</p>
        </div>
      </div>

      <form className="panel" onSubmit={handleReview}>
        <h2 className="panel-title">نظر بگذارید</h2>
        <div className="form-grid">
          <div className="field"><label className="label">امتیاز</label>
            <select className="select" value={rating} onChange={(e) => setRating(Number(e.target.value))}>
              <option value="5">۵ — عالی</option><option value="4">۴ — خوب</option><option value="3">۳ — متوسط</option><option value="2">۲ — ضعیف</option><option value="1">۱ — خیلی ضعیف</option>
            </select>
          </div>
          <div className="field"><label className="label">نظر</label><input className="input" value={comment} onChange={(e) => setComment(e.target.value)} /></div>
        </div>
        <button className="secondary-button" type="submit" style={{ marginTop: 16 }}>ثبت نظر</button>
      </form>

      <div className="panel">
        <h2 className="panel-title">نظرات ({reviews.length})</h2>
        {reviews.length === 0 ? <p className="help-text">هنوز نظری ثبت نشده است.</p> : (
          <div className="list-stack">
            {reviews.map((review) => (
              <div className="list-item" key={review.id}>
                <div><span className="badge badge-green">★ {review.rating}</span>{review.comment && <p style={{ marginTop: 8 }}>{review.comment}</p>}</div>
                <small className="help-text">{formatDate(review.created_at)}</small>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
