import { App, InjectionKey, inject } from 'vue'
import { createI18n } from 'vue-i18n'
import { underscore } from 'inflected'

const messages = {
  ja: {},
}

export const i18n = createI18n({
  locale: 'ja', // set locale
  fallbackLocale: 'en', // set fallback locale
  messages,
})

export const t = i18n.global.t

export function tr(key: string): string {
  return i18n.global.t(underscore(`activerecord.models.${key}`)) as string
}

export function ta(key: string, namespace: string | null = null): string {
  if (namespace != null) {
    const _key = underscore(`attributes.${namespace}.${key}`)
    let text = _key
    try {
      text = i18n.global.t(_key) as string
    } catch {
      console.log('error')
    }
    if (text !== _key) return text
  }
  const _key = underscore(`attributes.${key}`)
  try {
    return i18n.global.t(_key) as string
  } catch {
    console.log('error')
  }
  return _key
}
export type TaStore = typeof ta
export const TaKey: InjectionKey<TaStore> = Symbol('TaStore')
export const TeKey: InjectionKey<TaStore> = Symbol('TeStore')

export function tu(key: string, namespace: string | null = null): string {
  if (namespace != null) {
    const _key = underscore(`units.${namespace}.${key}`)
    const text = i18n.global.t(_key) as string
    if (text !== _key) return text
  }
  return i18n.global.t(underscore(`units.${key}`)) as string
}

export function te(key: string, enumName: string): string {
  console.log('===te', underscore(`enums.${enumName}.${key}`))
  return i18n.global.t(underscore(`enums.${enumName}.${key}`)) as string
}

export function td(key: string, namespace: string | null = null): string {
  if (namespace != null) {
    const _key = underscore(`descriptions.${namespace}.${key}`)
    const text = i18n.global.t(_key) as string
    if (text !== _key) return text
  }
  return i18n.global.t(underscore(`descriptions.${key}`)) as string
}

export const i18nExtend = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any,@typescript-eslint/explicit-module-boundary-types
  install: (app: App) => {
    console.log('install i18nExtend')

    app.config.globalProperties.$tr = tr
    app.provide('$tr', tr)

    app.config.globalProperties.$ta = ta
    app.provide(TaKey, ta)

    app.config.globalProperties.$tu = tu
    app.provide('$tu', tu)

    app.config.globalProperties.$te = te
    app.provide(TeKey, te)

    app.config.globalProperties.$td = td
    app.provide('$td', td)
  },
}

export const useI18n = () => {
  return {
    t: i18n.global.t,
    ta: inject(TaKey) as TaStore,
    te: inject(TeKey) as TaStore,
  }
}

// function setLang(locale: LocaleType) {
//   if (i18n.mode === 'legacy') {
//     i18n.global.locale = locale
//   } else {
//     i18n.global.locale = locale
//   }
//   // axios.defaults.headers.common['Accept-Language'] = lang
//   // document.querySelector('html').setAttribute('lang', lang)
//   return locale
// }

//const loadedLanguages: LocaleType[] = []

// export async function loadLanguage(locale: LocaleType) {
//   if (i18n.global.locale === locale && loadedLanguages.includes(locale)) {
//     return setLang(locale)
//   }

//   const result = await fetch(`/i18n/ja.json`)
//   const i18nMessages = await result.json()

//   const ja: any = {} // TODO
//   const mergedMessages = Object.assign(i18nMessages, ja)

//   i18n.global.setLocaleMessage(locale, mergedMessages)
//   loadedLanguages.push(locale)

//   return setLang(locale)
// }

export default i18n
