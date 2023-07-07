import { GraphQLError } from 'graphql'
import { ServerError, ServerParseError } from '@apollo/client'

import { setContext } from '@apollo/client/link/context'
import { onError, ErrorResponse } from '@apollo/client/link/error'

import { getAuthToken } from '@/store/session'

export const authLink = () => {
  return setContext((_, { headers }) => {
    const accessToken = getAuthToken()?.token
    return {
      headers: {
        ...headers,
        authorization: accessToken ? `Bearer ${accessToken}` : '',
      },
    }
  })
}

// export const tokenRefreshLink = (parefix: string | null | undefined) => {
//   return new TokenRefreshLink<TokenPayload>({
//     isTokenValidOrUndefined: () => isAccessTokenValidOrUndefined(),
//     fetchAccessToken: () => {
//       const refreshToken = getRefreshToken();
//       return fetch(getEndpoint(SESSIONS_ENDPOINT), {
//         method: 'PUT',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': `Bearer ${getAccessToken()}`,
//         },
//         body: JSON.stringify({
//           token: refreshToken,
//         }),
//       });
//     },
//     handleFetch: (accessTokenPayload: TokenPayload) => {
//       setAuthTokens(accessTokenPayload);
//     },
//     handleError: (err: Error) => {
//       console.warn('Your refresh token is invalid. Try to relogin');
//       console.error(err);
//       // GOTO HOME
//       //router.push({ name: 'Login' });
//     }
//   });
// }

export const errorLink = onError(
  ({ graphQLErrors, networkError }: ErrorResponse) => {
    if (graphQLErrors) {
      graphQLErrors.map(
        ({ message, locations, path, extensions }: GraphQLError) =>
          console.log(
            `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}, extensions: ${extensions}`
          )
      )
    }
    if (networkError) {
      console.log(`[Network error]: ${networkError}`)
      if ((networkError as ServerParseError | ServerError).statusCode === 401) {
        // 認証エラー
        // message.error(
        //   '通信できませんでした。しばらく経ってから、やり直してください'
        // )
        // TODO: どこかへ飛ばす？
      } else {
        // message.error(
        //   '通信できませんでした。しばらく経ってから、やり直してください'
        // )
      }
    }
  }
)
