import { from, ApolloClient, NormalizedCacheObject } from '@apollo/client'
import { DefaultApolloClient, ApolloClients } from '@vue/apollo-composable'
import { authLink } from './link'
import { InMemoryCache } from '@apollo/client'

import { createUploadLink } from 'apollo-upload-client'

const cache = new InMemoryCache()

export const createApolloClient = (
  path: string
): ApolloClient<NormalizedCacheObject> => {
  return new ApolloClient({
    link: from([
      authLink(),
      // @ts-ignore
      createUploadLink({
        uri: path,
      }),
    ]),
    cache,
    connectToDevTools: true,
  })
}

type ClientId = string
type ClientDict<T> = Record<ClientId, ApolloClient<T>>
export const apolloClients = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any,@typescript-eslint/explicit-module-boundary-types
  install: (app: any, options: ClientDict<any>) => {
    // app.config.globalProperties.$translate = key => {
    //   return key.split('.').reduce((o, i) => {
    //     if (o) return o[i]
    //   }, options)
    // }
    app.provide(ApolloClients, options)
    app.provide(DefaultApolloClient, options['default'])
  },
}

export const defaultApolloClient = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any,@typescript-eslint/explicit-module-boundary-types
  install: (app: any, apolloClient: ApolloClient<any>) => {
    app.provide(DefaultApolloClient, apolloClient)
  },
}
