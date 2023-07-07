import { isLoggined, isInited } from '@/store/session'
export const authGuard = async (to: any, from: any, next: any) => {
  if (to.matched.some((record: any) => record.meta.noAuth)) {
    // 認証なし
    next()
  } else if (isLoggined()) {
    // ログイン済み
    next()
  } else if (!isInited()) {
    // 初期化前
    if (to.fullPath === '/') {
      next({ name: 'Loading' })
    } else {
      next({ name: 'Loading', query: { redirect: to.fullPath } })
    }
  } else {
    if (to.fullPath === '/') {
      next({ name: 'Login' })
    } else {
      next({ name: 'Login', query: { redirect: to.fullPath } })
    }
  }
}

export default authGuard
