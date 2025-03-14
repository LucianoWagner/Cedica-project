// src/filters/index.js
export function formatDate(value) {
  if (!value) return ''
  const date = new Date(value)
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
