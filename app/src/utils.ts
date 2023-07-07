import { unref } from 'vue'

export function clone(src: any): any {
  const safeSrc = unref(src)
  return JSON.parse(JSON.stringify(safeSrc))
}
