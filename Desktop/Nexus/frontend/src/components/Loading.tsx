export default function Loading({ text = 'در حال بارگذاری…' }: { text?: string }) {
  return <div className="state-block">{text}</div>
}
