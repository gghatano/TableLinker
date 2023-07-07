import { createApp } from 'vue'
import App from './App.vue'

import primeVue from './plugins/primevue'
import { createApolloClient, defaultApolloClient } from '@/plugins/apollo'
import { default as i18n, i18nExtend } from '@/plugins/i18n'

import './style/all.scss'

import router from './router'

const apolloClient = createApolloClient('/graphql')
const app = createApp(App)

app.use(primeVue)
app.use(router)
app.use(i18n)
app.use(i18nExtend)
app.use(defaultApolloClient, apolloClient)
app.mount('#app')
