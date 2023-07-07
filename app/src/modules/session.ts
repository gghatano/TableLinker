import { InjectionKey } from 'vue'
import { useResult } from '@vue/apollo-composable'
import {
  setAuthToken,
  clearAuthToken,
  isInited,
  onInited,
  getAuthToken,
  AuthToken,
} from '@/store/session'
import {
  useTokenAuthMutation,
  useVerifyTokenMutation,
  useRefreshTokenMutation,
  useGetOwnUserQuery,
} from '@/modules/graphql'

export function useGetSession() {
  const { result } = useGetOwnUserQuery()
  const currentUser = useResult(result)
  return {
    currentUser,
  }
}

export function useSession() {
  // // ログイン
  const { mutate: tokenAuthMutate, loading: loadingAuthToken } =
    useTokenAuthMutation({})
  const tokenAuth = async (
    email: string,
    password: string
  ): Promise<boolean> => {
    try {
      const result = await tokenAuthMutate({ email, password })

      //const authToken = useResult(result)
      const authToken = result?.data?.tokenAuth
      if (authToken == null) throw new Error('authToken is null')
      setAuthToken({
        token: authToken.token,
        refreshToken: authToken.refreshToken,
      } as AuthToken)

      return true
    } catch (e) {
      console.error('tokenAuth error.', e)
      clearAuthToken()
      return false
    }
  }

  // トークンチェック
  const { mutate: verifyTokenMutate } = useVerifyTokenMutation({})
  const verifyToken = async (token: string): Promise<boolean> => {
    try {
      const result = await verifyTokenMutate({ token })
      const verifyToken = result?.data
      if (verifyToken == null) throw new Error('verifyToken is null')
      return true
    } catch (e) {
      console.error('verifyToken error.', e)
      clearAuthToken()
      return false
    }
  }

  // ログアウト
  const removeToken = async () => {
    clearAuthToken()
  }

  // セッションの復帰
  const { mutate: refreshTokenMutate } = useRefreshTokenMutation({})
  const refreshToken = async (): Promise<boolean> => {
    if (isInited()) return true

    try {
      const authToken = getAuthToken()
      const refreshToken = authToken?.refreshToken
      if (refreshToken == null) {
        clearAuthToken()
        return false
      }
      const result = await refreshTokenMutate({ refreshToken })
      const refreshTokenResult = result?.data?.refreshToken
      if (refreshTokenResult == null)
        throw new Error('refreshTokenResult is null')

      console.log('refreshTokenResult', refreshTokenResult)
      setAuthToken({
        token: refreshTokenResult.token,
        refreshToken: refreshTokenResult.refreshToken,
      } as AuthToken)
      onInited()
      return true
    } catch (e) {
      console.error('error', e)
      clearAuthToken()
      return false
    }
  }

  return {
    tokenAuth,
    loadingAuthToken,
    verifyToken,
    refreshToken,
    removeToken,
  }
}

export type UseGetSessionStore = ReturnType<typeof useGetSession>
export const UseGetSessionKey: InjectionKey<UseGetSessionStore> =
  Symbol('UseGetSessionStore')
export type UseSessionStore = ReturnType<typeof useSession>
export const UseSessionKey: InjectionKey<UseSessionStore> =
  Symbol('UseSessionStore')
