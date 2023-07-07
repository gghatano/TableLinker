<script lang="ts">
  import { defineComponent, reactive, toRefs } from 'vue'
  import { usePasswordResetRequestMutation } from '@/modules/graphql'
  import { useRouter } from 'vue-router'
  import Logo from '@/components/shared/Logo.vue'
  export default defineComponent({
    components: {
      Logo,
    },
    setup() {
      const router = useRouter()

      const { mutate, loading } = usePasswordResetRequestMutation({})

      const state = reactive({
        email: '',
      })

      const onSubmit = async () => {
        try {
          await mutate({ email: state.email })
        } catch (e) {
          console.log(e)
        }
        router.push({ name: 'PasswordConfirm' })
      }

      return {
        ...toRefs(state),
        onSubmit,
        loading,
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
      <div class="p-fluid p-mb5">
        <div class="p-field">
          <InputText
            v-model:modelValue="email"
            type="text"
            placeholder="メールアドレス"
          />
        </div>
        <div>
          <Button label="リクエストを送信する" @click="onSubmit" />
        </div>
      </div>
      <div class="links p-d-flex p-flex-column p-ai-center">
        <router-link :to="{ name: 'Login' }">ログイン画面に戻る</router-link>
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
  }
</style>
