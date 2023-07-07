<script lang="ts">
  import { defineComponent, reactive, toRefs, unref } from 'vue'
  import { useOwnUserQuery, useUpdateUserMutation } from '@/modules/graphql'
  import { useResult } from '@vue/apollo-composable'
  export default defineComponent({
    setup() {
      const { result } = useOwnUserQuery({})

      const { mutate, loading } = useUpdateUserMutation({})

      const user = useResult(result)

      const state = reactive({
        editAttrName: null as string | null,
        editValue: null as string | null,
      })

      const onEdit = (attrName: string) => {
        state.editAttrName = attrName
        state.editValue = unref(user)[attrName]
      }

      const onUpdate = async () => {
        if (!state.editAttrName || !state.editValue) {
          state.editAttrName = null
          state.editValue = null
          return
        }
        await mutate({
          input: {
            [state.editAttrName]: state.editValue,
          },
        })
        state.editAttrName = null
        state.editValue = null
      }

      return {
        ...toRefs(state),
        user,
        onEdit,
        onUpdate,
        loading,
      }
    },
  })
</script>

<template>
  <Card v-if="user">
    <template #title>ユーザ編集</template>
    <template #content>
      <div>
        <h5>名前</h5>
        <Inplace :active="editAttrName === 'name'" :closable="false">
          <template #display>
            <div class="p-d-inline-flex p-flex-column p-flex-md-row">
              <div>{{ user.name }}</div>
              <i class="pi pi-pencil p-ml-1" @click="onEdit('name')" />
            </div>
          </template>
          <template #content>
            <div class="p-inputgroup">
              <InputText v-model:modelValue="editValue" autoFocus />
              <Button icon="pi pi-check" @click="onUpdate" />
            </div>
          </template>
        </Inplace>
      </div>

      <div>
        <h5>メールアドレス</h5>
        <Inplace :active="editAttrName === 'email'" :closable="false">
          <template #display>
            <div class="p-d-inline-flex p-flex-column p-flex-md-row">
              <div>{{ user.email }}</div>
              <i class="pi pi-pencil p-ml-1" @click="onEdit('email')" />
            </div>
          </template>
          <template #content>
            <div class="p-inputgroup">
              <InputText v-model:modelValue="editValue" autoFocus />
              <Button icon="pi pi-check" @click="onUpdate" />
            </div>
          </template>
        </Inplace>
      </div>

      <div>
        <h5>パスワード</h5>
        <Inplace :active="editAttrName === 'password'" :closable="false">
          <template #display>
            <div class="p-d-inline-flex p-flex-column p-flex-md-row">
              <div>*******</div>
              <i class="pi pi-pencil p-ml-1" @click="onEdit('password')" />
            </div>
          </template>
          <template #content>
            <div class="p-inputgroup">
              <Password
                v-model:modelValue="editValue"
                autoFocus
                class="p-input-sm"
              />
              <Button icon="pi pi-check" @click="onUpdate" />
            </div>
          </template>
        </Inplace>
      </div>
    </template>
  </Card>
</template>

<style scoped></style>
