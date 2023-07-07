<script lang="ts">
  import { defineComponent, unref, computed, reactive, toRefs } from 'vue'
  import { useResult } from '@vue/apollo-composable'
  import {
    useDatasetGroupQuery,
    useUpdateDatasetGroupMutation,
    useDeleteDatasetGroupMutation,
  } from '@/modules/graphql'
  import { useConfirm } from 'primevue/useconfirm'
  import { useRouter } from 'vue-router'

  type Props = {
    datasetGroupId: string
  }

  export default defineComponent({
    props: {
      datasetGroupId: {
        type: String,
        required: true,
      },
    },
    setup(props: Props) {
      const { result, loading, refetch } = useDatasetGroupQuery(
        {
          id: props.datasetGroupId,
        },
        {
          fetchPolicy: 'cache-only',
        }
      )
      const datasetGroup = useResult(result)

      const useDownload = () => {
        const onDownload = async () => {
          const dataFileUrl = unref(datasetGroup).currentDataset.dataFileUrl
          window.location.href = dataFileUrl
        }
        return {
          onDownload,
        }
      }

      const useUpdate = () => {
        const confirm = useConfirm()
        const { mutate, loading: updating } = useUpdateDatasetGroupMutation({})

        const onTogglePublish = async (publicLevel: number) => {
          confirm.require({
            target: event.currentTarget,
            message: '公開します。よろしいですか？',
            icon: 'pi pi-exclamation-triangle',
            accept: async () => {
              await mutate({
                input: {
                  datasetGroupId: props.datasetGroupId,
                  publicLevel: publicLevel === 10 ? 100 : 10,
                },
              })
              await refetch()
            },
          })
        }

        const state = reactive({
          editableName: null as string | null,
        })

        const onEditName = async () => {
          state.editableName = unref(datasetGroup)?.name
        }

        const activeEditName = computed(() => state.editableName !== null)

        const onUpdateName = async () => {
          await mutate({
            input: {
              datasetGroupId: props.datasetGroupId,
              name: state.editableName,
            },
          })
          state.editableName = null
        }

        return {
          ...toRefs(state),
          onTogglePublish,
          onEditName,
          onUpdateName,
          activeEditName,
          updating,
        }
      }

      const useDelete = () => {
        const router = useRouter()
        const confirm = useConfirm()
        const { mutate, loading: deleting } = useDeleteDatasetGroupMutation({})
        const onDelete = async (event: Event) => {
          confirm.require({
            target: event.currentTarget,
            message: '削除します。よろしいですか？',
            icon: 'pi pi-exclamation-triangle',
            accept: async () => {
              await mutate({
                datasetGroupId: props.datasetGroupId,
              })
              router.push({ name: 'UserDatasetList' })
            },
          })
        }

        return {
          onDelete,
          deleting,
        }
      }

      const isOwner = computed(() => unref(datasetGroup).isOwner) // TODO

      return {
        datasetGroup,
        loading,
        ...useDownload(),
        ...useUpdate(),
        ...useDelete(),
        isOwner,
      }
    },
  })
</script>

<template>
  <Card class="nav">
    <template #content>
      <div class="p-d-inline-flex p-ai-center p-jc-between" style="width: 100%">
        <div class="p-d-inline-flex p-ai-center">
          <slot name="backTo">
            <i class="pi pi-arrow-left p-mr-2"></i>
            <span>Back to datasets</span>
          </slot>
        </div>
        <div class="p-d-inline-flex p-ai-center">
          <span class="p-mr-2">登録者: {{ datasetGroup?.createdBy }}</span>
          <span
            >登録日:
            {{ new Date(datasetGroup?.createdAt).toLocaleString() }}</span
          >
        </div>
      </div>
      <div class="p-d-inline-flex p-ai-center p-jc-between" style="width: 100%">
        <div>
          <Inplace :active="activeEditName" :closable="false">
            <template #display>
              <span @click="onEditName">
                <span>{{ datasetGroup?.name }}</span>
                <i class="pi pi-pencil" style="margin-left: 10px"></i>
              </span>
            </template>
            <template #content>
              <div class="p-inputgroup">
                <InputText
                  v-model="editableName"
                  autoFocus
                  style="width: 400px"
                />
                <Button
                  icon="pi pi-check"
                  class="p-button-success"
                  @click="onUpdateName"
                />
              </div>
            </template>
          </Inplace>
        </div>
        <div>
          <slot name="menu">
            <span v-if="isOwner" class="menu p-buttonset">
              <Button
                label="ダウンロード"
                class="p-button-text"
                @click="onDownload"
              />
              <Button
                :label="datasetGroup.publicLevelName"
                class="p-button-text"
                @click="onTogglePublish(datasetGroup.publicLevel)"
              />
              <Button label="削除" class="p-button-text" @click="onDelete" />
              <ConfirmPopup></ConfirmPopup>
            </span>
          </slot>
        </div>
      </div>
    </template>
  </Card>
</template>

<style lang="scss" scoped>
  .nav {
    .menu {
      ::v-deep(.p-button) {
        padding: 6px;
      }
    }
    ::v-deep(.p-card-body) {
      padding: 0 30px;
    }

    ::v-deep(.p-inplace-display) {
      padding: 0;
    }
  }
</style>
