import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { createProduct } from '../../api/market'
import type { ProductCreatePayload } from '../../types/market'
import { useUI } from '../../store/uiStore'
import { required } from '../../utils/validators'
import ProtectedRoute from '../../components/ProtectedRoute'

function SellProductInner() {
  const { notify } = useUI()
  const navigate = useNavigate()
  const [form, setForm] = useState<ProductCreatePayload>({
    title: '',
    description: '',
    category: 'template',
    price: 0,
    currency: 'IRR',
    tags: '',
    demo_url: '',
  })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  function update<K extends keyof ProductCreatePayload>(key: K, value: ProductCreatePayload[K]) {
    setForm((f) => ({ ...f, [key]: value }))
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    if (!required(form.title) || !required(form.description)) return setError('عنوان و توضیحات الزامی هستند.')
    if (Number(form.price) < 0) return setError('قیمت نمی‌تواند منفی باشد.')
    setSubmitting(true)
    try {
      const product = await createProduct({ ...form, price: Number(form.price) })
      notify('محصول با موفقیت منتشر شد!')
      navigate(`/market/${product.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'انتشار محصول ناموفق بود.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="content-section">
      <h1 className="page-title">فروش محصول</h1>
      <p className="page-subtitle">محصول دیجیتال خود را با توضیح کامل، دسته، قیمت و تگ‌ها منتشر کنید.</p>
      <form className="panel" onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="field field-full"><label className="label">عنوان</label><input className="input" value={form.title} onChange={(e) => update('title', e.target.value)} /></div>
          <div className="field field-full"><label className="label">توضیح کامل</label><textarea className="textarea" value={form.description} onChange={(e) => update('description', e.target.value)} /></div>
          <div className="field"><label className="label">دسته</label>
            <select className="select" value={form.category} onChange={(e) => update('category', e.target.value)}>
              <option value="template">Template</option><option value="plugin">Plugin</option><option value="api">API</option><option value="script">Script</option><option value="course">Course</option>
            </select>
          </div>
          <div className="field"><label className="label">قیمت</label><input className="input" type="number" value={form.price} onChange={(e) => update('price', Number(e.target.value))} /></div>
          <div className="field"><label className="label">ارز</label>
            <select className="select" value={form.currency} onChange={(e) => update('currency', e.target.value)}>
              <option value="IRR">تومان</option><option value="USD">دلار</option>
            </select>
          </div>
          <div className="field"><label className="label">وب‌سایت / دمو</label><input className="input" value={form.demo_url ?? ''} onChange={(e) => update('demo_url', e.target.value)} /></div>
          <div className="field"><label className="label">تگ‌ها (با کاما)</label><input className="input" value={form.tags ?? ''} onChange={(e) => update('tags', e.target.value)} /></div>
        </div>
        {error && <p className="field-error">{error}</p>}
        <button className="primary-button" type="submit" disabled={submitting} style={{ marginTop: 18 }}>
          {submitting ? 'در حال انتشار…' : 'انتشار محصول'}
        </button>
      </form>
    </div>
  )
}

export default function SellProduct() {
  return <ProtectedRoute><SellProductInner /></ProtectedRoute>
}
