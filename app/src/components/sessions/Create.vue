<script lang="ts">
  import { defineComponent, reactive, toRefs, inject } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { UseSessionKey, UseSessionStore } from '@/modules/session'
  import Logo from '@/components/shared/Logo.vue'

  export default defineComponent({
    components: {
      Logo,
    },
    setup() {
      const router = useRouter()
      const route = useRoute()

      const state = reactive({
        email: null,
        password: null,
        errorMessage: null as string | null,
      })

      const { tokenAuth, loadingAuthToken } = inject(
        UseSessionKey
      ) as UseSessionStore

      const onLogin = async () => {
        state.errorMessage = null
        if (!(await tokenAuth(state.email, state.password))) {
          state.errorMessage = 'ログインに失敗しました。'
          return
        }
        const redirect = route.query['redirect'] as string | null
        if (redirect == null) {
          router.push({ name: 'Home' })
        } else {
          router.push({ path: redirect })
        }
      }

      return {
        ...toRefs(state),
        onLogin,
        loadingAuthToken,
      }
    },
  })
</script>

<template>
  <div class="sessions-create p-d-flex p-jc-center">
    <div class="form">
      <div class="logo p-d-flex p-jc-center">
        <Logo></Logo>
      </div>
      <form class="p-fluid" @submit.prevent="onLogin">
        <template v-if="errorMessage">
          <Message severity="error">{{ errorMessage }}</Message>
        </template>
        <div class="p-field">
          <InputText
            v-model:modelValue="email"
            type="text"
            placeholder="メールアドレス"
          />
        </div>
        <div class="p-field">
          <Password
            v-model:modelValue="password"
            placeholder="パスワード"
            :feedback="false"
            toggleMask
          />
        </div>
        <div>
          <Button label="ログイン" @click="onLogin" />
        </div>
      </form>
      <div class="links p-d-flex p-flex-column p-ai-center">
        <router-link :to="{ name: 'PasswordRequest' }">
          パスワードを忘れた場合はこちら
        </router-link>
        <router-link :to="{ name: 'UserCreate' }">
          アカウントを作成する
        </router-link>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .sessions-create {
    width: 100%;
  }
  .form {
    margin: 80px 0;

    border: 1px solid #b4b4b4;
    background-color: #ffffff;
    padding: 28px 24px 24px 24px;

    .logo {
      width: 260px;
      margin: 0 0 40px;
    }

    .p-field {
      margin-bottom: 30px;
    }
  }
</style>
