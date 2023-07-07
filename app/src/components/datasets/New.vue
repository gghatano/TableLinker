<script lang="ts">
  import { defineComponent, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { useCreateDatasetGroupMutation } from '@/modules/graphql'

  export default defineComponent({
    setup() {
      const router = useRouter()

      const input = reactive({
        originalFile: null as File | null,
        name: null as string | null,
        source: {
          siteName: null as string | null,
          siteUrl: null as string | null,
        },
      })

      const { mutate, loading } = useCreateDatasetGroupMutation({
        variables: {
          input,
        },
      })

      const onFileSelect = (event) => {
        input.originalFile = event.files[0]
        if (input.name == null || input.name.length === 0) {
          input.name = input.originalFile.name
        }
      }

      const onUpload = async () => {
        if (input.name == null || input.name.length === 0) {
          input.name = input.originalFile.name
        }
        try {
          await mutate()
          router.push({ name: 'UserDatasetList' })
        } catch (error) {
          // TODO: if error.
          console.error(error)
        }
      }

      const onCancel = () => {
        router.push({ name: 'UserDatasetList' })
      }

      return {
        input,
        onFileSelect,
        onUpload,
        onCancel,
        loading,
      }
    },
  })
</script>

<template>
  <Card>
    <template #title>ファイルアップロード</template>
    <template #content>
      <div class="p-fluid">
        <div class="p-field">
          <div class="p-d-flex p-jc-start p-ai-center">
            <FileUpload
              mode="basic"
              :previewWidth="0"
              :maxFileSize="100000000"
              chooseLabel="ファイルを選択"
              :uploadLabel="null"
              :showUploadButton="false"
              :showCancelButton="false"
              :auto="true"
              :customUpload="true"
              @uploader="onFileSelect"
            >
            </FileUpload>
            <span class="p-ml-3">
              {{ input.originalFile ? input.originalFile.name : '' }}
            </span>
          </div>
          <div>
            CSVファイル(Shift-JIS or UTF8 or
            UTF8BOM付き,100MB以下)を指定してください。
          </div>
        </div>
        <div class="p-field">
          <label for="name">名前</label>
          <InputText
            id="name"
            v-model:modelValue="input.name"
            type="text"
            :disabled="loading"
          />
        </div>
        <Fieldset legend="詳細" :toggleable="true" :collapsed="true">
          <div class="p-field">
            <label for="siteName">サイト名</label>
            <InputText
              id="siteName"
              v-model:modelValue="input.source.siteName"
              type="text"
              :disabled="loading"
            />
          </div>
          <div class="p-field">
            <label for="siteUrl">サイトURL </label>
            <InputText
              id="siteUrl"
              v-model:modelValue="input.source.siteUrl"
              type="text"
              :disabled="loading"
            />
          </div>
        </Fieldset>
      </div>
    </template>
    <template #footer>
      <div class="p-d-flex p-jc-end">
        <Button
          icon="pi pi-times"
          label="キャンセル"
          class="p-button-secondary p-button-rounded p-button-sm"
          :disabled="loading"
          @click="onCancel"
        />
        <Button
          icon="pi pi-check"
          label="アップロード"
          style="margin-left: 0.5em"
          class="p-button-rounded p-button-sm"
          :loading="loading"
          @click="onUpload"
        />
      </div>
    </template>
  </Card>
</template>

<style lang="scss" scoped></style>
