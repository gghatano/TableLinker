const prefix = 'tablelinker.'

let inited = false
let loggined = false

export const onInited = (): void => {
  inited = true
}
export const onLoggined = () => {
  inited = true
  loggined = true
}
export const offInited = (): void => {
  inited = false
  loggined = false
}
export const offLoggined = () => {
  loggined = false
}
export const isInited = () => inited
export const isLoggined = () => loggined

export type AuthToken = {
  token: string
  refreshToken: string
}

export const setAuthToken = (authToken: AuthToken) => {
  localStorage.setItem(prefix + 'accessToken', authToken.token)
  localStorage.setItem(prefix + 'refreshToken', authToken.refreshToken)
  onLoggined()
}

export const getAuthToken = (): AuthToken => {
  return {
    token: localStorage.getItem(prefix + 'accessToken') as string,
    refreshToken: localStorage.getItem(prefix + 'refreshToken') as string,
  }
}

export const clearAuthToken = () => {
  localStorage.removeItem(prefix + 'accessToken')
  localStorage.removeItem(prefix + 'refreshToken')
  localStorage.removeItem(prefix + 'refreshToken')
  localStorage.removeItem(prefix + 'refreshTokenExpiredAt')
  offLoggined()
}
