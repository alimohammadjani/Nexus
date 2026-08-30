export const isEmail = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)

export const isStrongPassword = (value: string) => value.length >= 8

export const required = (value: string | undefined | null) => Boolean(value && value.trim())

export function validationMessages(values: Record<string, string>) {
  const errors: Record<string, string> = {}
  Object.entries(values).forEach(([key, value]) => {
    if (!value.trim()) errors[key] = 'این فیلد الزامی است.'
  })
  return errors
}
