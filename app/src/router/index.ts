import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

import authGuard from './authGuard'

import NotFound from '@/views/NotFound.vue'
import Login from '@/views/auths/Login.vue'
import Loading from '@/views/auths/Loading.vue'
import PasswordConfirm from '@/views/auths/PasswordConfirm.vue'
import PasswordRequest from '@/views/auths/PasswordRequest.vue'

import UserDetail from '@/views/users/Detail.vue'
import UserCreate from '@/views/users/Create.vue'
import UserDatasetList from '@/views/users/DatasetList.vue'

import DatasetList from '@/views/datasets/List.vue'
import DatasetDetail from '@/views/datasets/Detail.vue'
import DatasetEdit from '@/views/datasets/Edit.vue'
import DatasetNew from '@/views/datasets/New.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    //component: Home,
    redirect: {
      name: 'DatasetList',
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { noAuth: true },
  },
  {
    path: '/logout',
    name: 'Logout',
    redirect: {
      name: 'Login',
    },
  },
  {
    path: '/loading',
    name: 'Loading',
    component: Loading,
    meta: { noAuth: true },
  },
  {
    path: '/password/request',
    name: 'PasswordRequest',
    component: PasswordRequest,
    meta: { noAuth: true },
  },
  {
    path: '/password/confirm',
    name: 'PasswordConfirm',
    component: PasswordConfirm,
    meta: { noAuth: true },
  },
  {
    path: '/user',
    name: 'UserDetail',
    component: UserDetail,
  },
  {
    path: '/user/create',
    name: 'UserCreate',
    component: UserCreate,
    meta: { noAuth: true },
  },
  {
    path: '/user/datasets',
    name: 'UserDatasetList',
    component: UserDatasetList,
  },
  {
    path: '/datasets',
    name: 'DatasetList',
    component: DatasetList,
  },
  {
    path: '/datasets/new',
    name: 'DatasetNew',
    component: DatasetNew,
  },
  {
    path: '/datasets/:id',
    name: 'DatasetDetail',
    component: DatasetDetail,
    props: true,
  },
  {
    path: '/datasets/:id/edit',
    name: 'DatasetEdit',
    component: DatasetEdit,
    props: true,
  },
  {
    path: '/datasets/:id/datasetMapping/:targetDatasetGroupId',
    name: 'DatasetMappingDatasetGroup',
    component: DatasetEdit,
    props: true,
  },
  {
    path: '/datasets/:id/templateMapping/:targetDatasetTemplateId',
    name: 'DatasetMappingTemplate',
    component: DatasetEdit,
    props: true,
  },
  {
    path: '/datasets/:id/edit',
    name: 'DatasetEdit',
    component: DatasetEdit,
    props: true,
  },

  {
    path: '/:pathMatch(.*)',
    name: 'NotFound',
    component: NotFound,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.CLIENT_BASE_URL || '/'),
  routes,
})

// AuthGuard
router.beforeEach(authGuard)

export default router
