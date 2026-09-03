import { type ReactNode } from 'react'

/**
 * Minimal content renderer for the real training text stored in the database.
 * Supports:
 *   - paragraph blocks (with **bold** and `code` inline)
 *   - `## ` headings
 *   - bullet lists (`- ` lines)
 *   - ordered/step lists (`1. ` lines)
 *   - fenced code blocks (```lang ... ```)
 *   - tip callouts (`> ` lines)
 *
 * Newlines inside a paragraph are preserved via CSS white-space: pre-line.
 */

const INLINE_RE = /(\*\*([^*]+)\*\*|`([^`]+)`)/g

function renderInline(text: string): ReactNode[] {
  const nodes: ReactNode[] = []
  let lastIndex = 0
  let match: RegExpExecArray | null
  let key = 0
  INLINE_RE.lastIndex = 0
  while ((match = INLINE_RE.exec(text)) !== null) {
    if (match.index > lastIndex) {
      nodes.push(text.slice(lastIndex, match.index))
    }
    if (match[2] !== undefined) {
      nodes.push(<strong key={key++}>{match[2]}</strong>)
    } else if (match[3] !== undefined) {
      nodes.push(
        <code className="code-inline" key={key++}>
          {match[3]}
        </code>,
      )
    }
    lastIndex = INLINE_RE.lastIndex
  }
  if (lastIndex < text.length) nodes.push(text.slice(lastIndex))
  return nodes
}

type Block =
  | { type: 'heading'; text: string }
  | { type: 'list'; ordered: boolean; items: string[] }
  | { type: 'paragraph'; text: string }
  | { type: 'code'; lang: string; code: string }
  | { type: 'tip'; text: string }

function stripFence(line: string): string {
  return line.replace(/^```/, '').trim()
}

function parseBlocks(raw: string): Block[] {
  const chunks = raw.split(/\n{2,}/)
  const blocks: Block[] = []
  let i = 0
  while (i < chunks.length) {
    let chunk = chunks[i].replace(/^\n+|\n+$/g, '')
    if (!chunk.trim()) {
      i++
      continue
    }

    // Fenced code block
    if (chunk.startsWith('```')) {
      const lang = stripFence(chunk.split('\n')[0])
      const lines = chunk.split('\n').slice(1)
      // consume trailing fence if present in same chunk
      if (lines.length && lines[lines.length - 1].trim().startsWith('```')) lines.pop()
      blocks.push({ type: 'code', lang, code: lines.join('\n') })
      i++
      continue
    }

    // Heading
    if (chunk.startsWith('## ')) {
      blocks.push({ type: 'heading', text: chunk.replace(/^##\s*/, '') })
      i++
      continue
    }

    const lines = chunk.split('\n').map((l) => l.replace(/\s+$/, ''))

    // Tip callout
    if (lines.every((l) => l.startsWith('> '))) {
      blocks.push({ type: 'tip', text: lines.map((l) => l.replace(/^>\s?/, '')).join('\n') })
      i++
      continue
    }

    // Ordered list
    const isOrdered = lines.length > 0 && lines.every((l) => /^\d+\.\s/.test(l))
    if (isOrdered) {
      blocks.push({ type: 'list', ordered: true, items: lines.map((l) => l.replace(/^\d+\.\s/, '')) })
      i++
      continue
    }

    // Bullet list
    const isBullet = lines.length > 0 && lines.every((l) => l.startsWith('- '))
    if (isBullet) {
      blocks.push({ type: 'list', ordered: false, items: lines.map((l) => l.replace(/^-\s/, '')) })
      i++
      continue
    }

    blocks.push({ type: 'paragraph', text: lines.join('\n') })
    i++
  }
  return blocks
}

export function renderContent(raw: string | null | undefined): ReactNode {
  if (!raw) return null
  const blocks = parseBlocks(raw)
  return (
    <div className="content-blocks">
      {blocks.map((block, i) => {
        switch (block.type) {
          case 'heading':
            return (
              <h4 className="content-heading" key={i}>
                {renderInline(block.text)}
              </h4>
            )
          case 'list':
            return block.ordered ? (
              <ol className="content-ordered" key={i}>
                {block.items.map((item, j) => (
                  <li key={j}>{renderInline(item)}</li>
                ))}
              </ol>
            ) : (
              <ul className="content-list" key={i}>
                {block.items.map((item, j) => (
                  <li key={j}>{renderInline(item)}</li>
                ))}
              </ul>
            )
          case 'code':
            return (
              <pre className="content-code" key={i}>
                <code>{block.code}</code>
              </pre>
            )
          case 'tip':
            return (
              <div className="content-tip" key={i}>
                {renderInline(block.text)}
              </div>
            )
          case 'paragraph':
          default:
            return (
              <p className="content-paragraph" key={i}>
                {renderInline(block.text)}
              </p>
            )
        }
      })}
    </div>
  )
}

/** Parse a comma-separated resources string into label/url pairs when possible. */
export interface ResourceLink {
  label: string
  url?: string
}

export function parseResources(raw: string | null | undefined): ResourceLink[] {
  if (!raw) return []
  return raw
    .split(',')
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => {
      const match = part.match(/^(.*?)\s*—\s*(https?:\/\/\S+)$/)
      if (match) return { label: match[1].trim(), url: match[2] }
      if (/^https?:\/\//.test(part)) return { label: part, url: part }
      return { label: part, url: undefined }
    })
}
