<script lang="ts">
  import { defineComponent, reactive, toRefs } from 'vue'
  import { useRouter } from 'vue-router'
  import { usePasswordResetMutation } from '@/modules/graphql'
  import Logo from '@/components/shared/Logo.vue'
  export default defineComponent({
    components: {
      Logo,
    },
    setup() {
      const router = useRouter()

      const { mutate, loading } = usePasswordResetMutation({})

      const state = reactive({
        passwordResetToken: '',
        password: '',
      })

      const onSubmit = async () => {
        try {
          await mutate({
            password: state.password,
            passwordResetToken: state.passwordResetToken,
          })
        } catch (e) {
          console.log(e)
        }
        router.push({ name: 'Login' })
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
            v-model:modelValue="passwordResetToken"
            type="text"
            placeholder="認証番号"
          />
        </div>
        <div class="p-field">
          <Password v-model:modelValue="password" placeholder="パスワード" />
        </div>
        <div>
          <Button label="パスワードを変更する" @click="onSubmit" />
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
