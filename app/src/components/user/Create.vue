<script lang="ts">
  import { defineComponent, reactive, toRefs } from 'vue'
  import { useRouter } from 'vue-router'
  import { useCreateUserMutation } from '@/modules/graphql'

  import Logo from '@/components/shared/Logo.vue'

  export default defineComponent({
    components: {
      Logo,
    },
    setup() {
      const router = useRouter()

      const state = reactive({
        email: null,
        name: null,
        password: null,
        errorMessages: [] as string[],
      })

      const { mutate } = useCreateUserMutation({})

      const onCreate = async () => {
        state.errorMessages = []
        try {
          await mutate({
            input: {
              email: state.email,
              name: state.name,
              password: state.password,
            },
          })
          router.push({ name: 'UserDatasetList' })
        } catch (e) {
          state.errorMessages = ['ユーザ登録に失敗しました。']
        }
      }

      return {
        ...toRefs(state),
        onCreate,
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
        <template v-if="errorMessages.length > 0">
          <Message severity="error">
            <template
              v-for="(errorMessage, index) in errorMessages"
              :key="index"
            >
              <div>{{ errorMessage }}</div>
            </template>
          </Message>
        </template>
        <div class="p-field">
          <InputText
            v-model:modelValue="email"
            type="text"
            placeholder="メールアドレス"
          />
        </div>
        <div class="p-field">
          <InputText v-model:modelValue="name" type="text" placeholder="名前" />
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
          <Button label="新規作成" @click="onCreate" />
        </div>
      </form>
      <div class="links p-d-flex p-flex-column p-ai-center">
        <router-link :to="{ name: 'Login' }">ログインする</router-link>
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
