<script lang="ts">
  import { defineComponent, inject } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { UseSessionKey, UseSessionStore } from '@/modules/session'
  export default defineComponent({
    setup() {
      const router = useRouter()
      const route = useRoute()

      const { refreshToken } = inject(UseSessionKey) as UseSessionStore
      refreshToken().then((success) => {
        // 初期化失敗の場合は、ログイン画面ヘ
        if (!success) {
          router.push({ name: 'Login' })
          return {}
        }
        // 成功時の画面遷移
        const redirect = route.query['redirect'] as string | null
        if (redirect == null) {
          router.push({ name: 'Home' })
        } else {
          router.push({ path: redirect })
        }
      })
      return {}
    },
  })
</script>

<template>
  <div class="loading">
    <ProgressSpinner style="width: 50px; height: 50px" />
  </div>
</template>

<style lang="scss" scoped>
  .loading {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
