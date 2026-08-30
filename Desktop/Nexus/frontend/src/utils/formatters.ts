export function formatPrice(value: number, currency = 'IRR', locale = 'fa-IR') {
  if (currency === 'IRR' || currency === 'T') return new Intl.NumberFormat(locale).format(value) + ' تومان'
  return new Intl.NumberFormat(locale, { style: 'currency', currency }).format(value)
}

export function formatDate(value?: string | null) {
  if (!value) return '—'
  return new Intl.DateTimeFormat('fa-IR', { year: 'numeric', month: 'long', day: 'numeric' }).format(new Date(value))
}

export function formatRelative(value?: string | null) {
  if (!value) return '—'
  const seconds = Math.round((new Date(value).getTime() - Date.now()) / 1000)
  const abs = Math.abs(seconds)
  const formatter = new Intl.RelativeTimeFormat('fa-IR', { numeric: 'auto' })
  if (abs < 60) return formatter.format(Math.trunc(seconds), 'second')
  if (abs < 3600) return formatter.format(Math.trunc(seconds / 60), 'minute')
  if (abs < 86400) return formatter.format(Math.trunc(seconds / 3600), 'hour')
  return formatter.format(Math.trunc(seconds / 86400), 'day')
}

export function splitSkills(skills?: string | null): string[] {
  return (skills ?? '').split(',').map((s) => s.trim()).filter(Boolean)
}

export function jobTypeLabel(type?: string) {
  const labels: Record<string, string> = {
    full_time: 'تمام‌وقت',
    part_time: 'پاره‌وقت',
    freelance: 'فریلنس',
    contract: 'قراردادی',
  }
  return labels[type ?? ''] ?? type ?? '—'
}

export function jobModeLabel(mode?: string) {
  const labels: Record<string, string> = {
    remote: 'ریموت',
    hybrid: 'هیبرید',
    on_site: 'حضوری',
  }
  return labels[mode ?? ''] ?? mode ?? '—'
}
