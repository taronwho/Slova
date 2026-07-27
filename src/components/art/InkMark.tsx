/** Kapka inkoustu — značka měny. Musí být čitelná i v jedenácti pixelech. */

interface Props {
  size?: number
  className?: string
}

export function InkMark({ size = 12, className }: Props) {
  return (
    <svg
      className={`ink-mark ${className ?? ''}`}
      viewBox="0 0 24 24"
      width={size}
      height={size}
      aria-hidden="true"
    >
      <path
        d="M12 2.5c3.9 5 6.4 8.4 6.4 11.2a6.4 6.4 0 0 1-12.8 0C5.6 10.9 8.1 7.5 12 2.5Z"
        fill="currentColor"
      />
      {/* Odlesk. Bez něj vypadá kapka jako plná tečka. */}
      <path
        d="M9.6 14.4a2.6 2.6 0 0 1 1.7-2.7"
        fill="none"
        stroke="var(--surface)"
        strokeWidth="1.6"
        strokeLinecap="round"
        opacity="0.75"
      />
    </svg>
  )
}
