import { useCallback, useEffect, useMemo, useState } from 'react'
import type { CSSProperties } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchRoadmap } from '../../api/roadmap'
import type { Roadmap as RoadmapType, RoadmapStage } from '../../types/roadmap'
import { parseResources, renderContent } from '../../utils/content'
import Loading from '../../components/Loading'
import ErrorState from '../../components/ErrorState'
import './learning.css'

const NODE_W = 270
const NODE_H = 108
const MARGIN = 40
const COL_GAP = 90
const ROW_GAP = 150
const COLS = 2

const CATEGORY_META: Record<string, { icon: string; label: string }> = {
  frontend: { icon: '🎨', label: 'فرانت‌اند' },
  backend: { icon: '⚙️', label: 'بک‌اند' },
  devops: { icon: '🚀', label: 'DevOps' },
  mobile: { icon: '📱', label: 'موبایل' },
}

function progressKey(id: number) {
  return `devhub_rm_progress_${id}`
}

export default function RoadmapView() {
  const { id } = useParams()
  const [roadmap, setRoadmap] = useState<RoadmapType | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selected, setSelected] = useState<RoadmapStage | null>(null)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [viewMode, setViewMode] = useState<'graph' | 'list'>('graph')
  const [completed, setCompleted] = useState<number[]>([])

  const load = useCallback(async () => {
    if (!id) return
    setLoading(true)
    setError(null)
    try {
      const data = await fetchRoadmap(Number(id))
      setRoadmap(data)
      try {
        const stored = localStorage.getItem(progressKey(data.id))
        setCompleted(stored ? JSON.parse(stored) : [])
      } catch {
        setCompleted([])
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'مسیر یافت نشد.')
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    void load()
  }, [load])

  const openStage = useCallback((stage: RoadmapStage) => {
    setSelected(stage)
    setDrawerOpen(true)
  }, [])

  const selectedIndex = selected && roadmap ? roadmap.stages.findIndex((s) => s.id === selected.id) : -1

  const goToStage = useCallback(
    (delta: number) => {
      if (!roadmap || selectedIndex < 0) return
      const next = roadmap.stages[selectedIndex + delta]
      if (next) setSelected(next)
    },
    [roadmap, selectedIndex],
  )

  const closeDrawer = useCallback(() => setDrawerOpen(false), [])

  const toggleDone = useCallback(
    (stageId: number) => {
      if (!roadmap) return
      setCompleted((prev) => {
        const next = prev.includes(stageId) ? prev.filter((x) => x !== stageId) : [...prev, stageId]
        try {
          localStorage.setItem(progressKey(roadmap.id), JSON.stringify(next))
        } catch {
          /* ignore */
        }
        return next
      })
    },
    [roadmap],
  )

  const accent = roadmap?.color ?? '#8b5cf6'
  const meta = roadmap ? CATEGORY_META[roadmap.category] ?? { icon: '🧭', label: roadmap.category } : null

  const progress = useMemo(() => {
    if (!roadmap) return 0
    return Math.round((completed.filter((cid) => roadmap.stages.some((s) => s.id === cid)).length / roadmap.stages.length) * 100)
  }, [roadmap, completed])

  const layout = useMemo(() => {
    if (!roadmap) return null
    const stages = roadmap.stages
    const n = stages.length
    const rows = Math.ceil(n / COLS)
    const canvasWidth = MARGIN * 2 + COLS * NODE_W + (COLS - 1) * COL_GAP
    const canvasHeight = MARGIN * 2 + (rows - 1) * ROW_GAP + NODE_H

    const positions = stages.map((stage, i) => {
      const col = i % COLS
      const row = Math.floor(i / COLS)
      const x = MARGIN + col * (NODE_W + COL_GAP)
      const y = MARGIN + row * ROW_GAP
      return { stage, x, y, cx: x + NODE_W / 2, top: y, bottom: y + NODE_H }
    })

    const connectors = positions.slice(0, -1).map((p, i) => {
      const next = positions[i + 1]
      const midY = (p.bottom + next.top) / 2
      return `M ${p.cx} ${p.bottom} C ${p.cx} ${midY}, ${next.cx} ${midY}, ${next.cx} ${next.top}`
    })

    return { positions, connectors, canvasWidth, canvasHeight }
  }, [roadmap])

  if (loading) return <Loading text="در حال بارگذاری مسیر…" />
  if (error) return <ErrorState message={error} onRetry={load} />
  if (!roadmap || !layout) return <ErrorState message="مسیر یافت نشد." onRetry={load} />

  return (
    <div className="content-section" style={{ '--accent': accent } as CSSProperties}>
      <Link to="/learning" className="ghost-link">
        ← بازگشت به یادگیری
      </Link>

      <div className="roadmap-header" style={{ marginTop: 18 }}>
        <div className="roadmap-title">
          <span className="rm-icon" style={{ background: accent }}>
            {meta?.icon}
          </span>
          <div className="roadmap-title-text">
            <h1>{roadmap.title}</h1>
            <p>{roadmap.subtitle ?? roadmap.description}</p>
          </div>
        </div>
        <div className="roadmap-tools">
          <button
            className={`view-toggle ${viewMode === 'graph' ? 'active' : ''}`}
            type="button"
            onClick={() => setViewMode('graph')}
          >
            نمای گراف
          </button>
          <button
            className={`view-toggle ${viewMode === 'list' ? 'active' : ''}`}
            type="button"
            onClick={() => setViewMode('list')}
          >
            نمای لیست
          </button>
        </div>
      </div>

      <div className="roadmap-progress">
        <div className="roadmap-progress-label">
          پیشرفت شما: <b>{progress}٪</b> ({completed.length} از {roadmap.stages.length} مرحله مطالعه‌شده)
        </div>
        <div className="progress-track">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>
      </div>

      <div className="roadmap-hint">
        <span>💡</span>
        <span>روی هر مرحله کلیک کنید تا آموزش، منابع و پروژهٔ عملی آن باز شود.</span>
      </div>

      {viewMode === 'graph' ? (
        <div className="roadmap-canvas-wrap">
          <div
            className="roadmap-canvas"
            style={{ width: layout.canvasWidth, height: layout.canvasHeight }}
          >
            <svg
              width={layout.canvasWidth}
              height={layout.canvasHeight}
              style={{ position: 'absolute', inset: 0 }}
              aria-hidden="true"
            >
              {layout.connectors.map((d, i) => (
                <path key={i} className="roadmap-connector" d={d} />
              ))}
            </svg>
            {layout.positions.map(({ stage, x, y }) => {
              const done = completed.includes(stage.id)
              const isSelected = selected?.id === stage.id
              return (
                <button
                  key={stage.id}
                  type="button"
                  className={`roadmap-node ${done ? 'done' : ''} ${isSelected ? 'selected' : ''}`}
                  style={{ left: x, top: y }}
                  onClick={() => openStage(stage)}
                >
                  <div className="roadmap-node-top">
                    <span className="roadmap-order">{stage.order}</span>
                    <span className="roadmap-node-title">{stage.title}</span>
                    {done && <span className="roadmap-node-check">✓</span>}
                  </div>
                  <p className="roadmap-node-desc">{stage.description}</p>
                </button>
              )
            })}
          </div>
        </div>
      ) : (
        <div className="roadmap-list">
          {roadmap.stages.map((stage) => {
            const done = completed.includes(stage.id)
            return (
              <button
                key={stage.id}
                type="button"
                className={`roadmap-list-item ${done ? 'done' : ''}`}
                onClick={() => openStage(stage)}
              >
                <span className="roadmap-order">{stage.order}</span>
                <div>
                  <div className="roadmap-node-title">{stage.title}</div>
                  <p className="roadmap-node-desc">{stage.description}</p>
                </div>
                {done && <span className="roadmap-node-check">✓</span>}
              </button>
            )
          })}
        </div>
      )}

      <div className={`drawer-backdrop ${drawerOpen ? 'open' : ''}`} onClick={closeDrawer} />
      <aside className={`training-drawer ${drawerOpen ? 'open' : ''}`} aria-hidden={!drawerOpen}>
        {selected && (
          <>
            <div className="drawer-head">
              <span className="roadmap-order">{selected.order}</span>
              <div>
                <h2>{selected.title}</h2>
                {selected.description && <p className="help-text">{selected.description}</p>}
              </div>
              <button className="drawer-close" type="button" onClick={closeDrawer} aria-label="بستن">
                ✕
              </button>
            </div>

            <div className="drawer-body">
              {selected.content && (
                <div className="training-section">
                  <span className="label">آموزش</span>
                  {renderContent(selected.content)}
                </div>
              )}

              {selected.resources && (
                <div className="training-section">
                  <span className="label">منابع پیشنهادی</span>
                  <div className="resource-links">
                    {parseResources(selected.resources).map((r, i) =>
                      r.url ? (
                        <a
                          key={i}
                          className="resource-link"
                          href={r.url}
                          target="_blank"
                          rel="noreferrer noopener"
                        >
                          <span className="rl-dot" />
                          <span>
                            <span className="rl-text">{r.label}</span>
                            <span className="rl-sub">{r.url}</span>
                          </span>
                        </a>
                      ) : (
                        <div key={i} className="resource-link">
                          <span className="rl-dot" />
                          <span className="rl-text">{r.label}</span>
                        </div>
                      ),
                    )}
                  </div>
                </div>
              )}

              {selected.project && (
                <div className="training-section">
                  <span className="label">پروژه عملی</span>
                  <div className="training-card accent">
                    <p>{selected.project}</p>
                  </div>
                </div>
              )}

              {selected.checkpoint && (
                <div className="training-section">
                  <span className="label">نقطه بازرسی (Checkpoint)</span>
                  <div className="training-card green">
                    <strong>وقتی این را می‌توانید انجام دهید، مرحله تمام است:</strong>
                    <p>{selected.checkpoint}</p>
                  </div>
                </div>
              )}
            </div>

            {selectedIndex >= 0 && (
              <div className="drawer-nav">
                <button
                  type="button"
                  className="nav-btn"
                  onClick={() => goToStage(-1)}
                  disabled={selectedIndex === 0}
                >
                  → مرحله قبلی
                </button>
                <span className="drawer-nav-count">
                  مرحله {selectedIndex + 1} از {roadmap.stages.length}
                </span>
                <button
                  type="button"
                  className="nav-btn"
                  onClick={() => goToStage(1)}
                  disabled={selectedIndex === roadmap.stages.length - 1}
                >
                  مرحله بعدی ←
                </button>
              </div>
            )}

            <div className="drawer-foot">
              <button
                type="button"
                className={`done-btn ${completed.includes(selected.id) ? 'active' : ''}`}
                onClick={() => toggleDone(selected.id)}
              >
                {completed.includes(selected.id) ? '✓ مطالعه شد — برداشتن علامت' : 'علامت‌گذاری به‌عنوان مطالعه‌شده'}
              </button>
            </div>
          </>
        )}
      </aside>
    </div>
  )
}
