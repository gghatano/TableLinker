<script lang="ts">
  import { defineComponent, reactive, toRefs, unref, computed } from 'vue'

  import {
    useOwnDatasetGroupsQuery,
    useDeleteDatasetGroupMutation,
  } from '@/modules/graphql'
  import { DatasetGroupType } from '@/schema/schema'
  import { useResult } from '@vue/apollo-composable'

  export default defineComponent({
    setup() {
      const state = reactive({
        inputKeyword: null as string | null,
      })

      const variables = reactive({
        keyword: null as string | null,
        page: 0,
        pageSize: 20,
      })
      const { result, loading, refetch } = useOwnDatasetGroupsQuery(variables, {
        fetchPolicy: 'network-only',
      })

      const datasetGroupResult = useResult(result)

      const datasetGroups = computed(
        () => unref(datasetGroupResult)?.datasetGroups
      )

      const totalRecords = computed(
        () => unref(datasetGroupResult)?.totalRecords
      )

      const onSearch = () => {
        variables.keyword = state.inputKeyword
      }

      const onPage = ({ page, rows }: { page: number; rows: number }) => {
        variables.page = page
        variables.pageSize = rows
      }

      const formatDateTime = (date: string) => {
        return new Date(date).toLocaleString()
      }

      const useDelete = () => {
        const { mutate } = useDeleteDatasetGroupMutation({})
        const onDelete = async (datasetGroup: DatasetGroupType) => {
          await mutate({
            datasetGroupId: datasetGroup.id,
          })
          await refetch()
        }

        return {
          onDelete,
        }
      }

      return {
        ...toRefs(state),
        ...toRefs(variables),
        datasetGroups,
        totalRecords,
        loading,
        ...useDelete(),
        onSearch,
        onPage,
        formatDateTime,
      }
    },
  })
</script>

<template>
  <div class="ownDataset">
    <div class="p-d-flex p-jc-center p-mb-5">
      <div class="p-inputgroup" style="width: 1023px">
        <InputText
          v-model:modelValue="inputKeyword"
          placeholder="検索キーワードを入力してください"
        />
        <Button label="検索" class="p-button-secondary" @click="onSearch" />
      </div>
    </div>
    <div style="height: calc(100vh - 280px)">
      <DataTable
        class="p-datatable-sm"
        :value="datasetGroups"
        :resizableColumns="true"
        columnResizeMode="fit"
        showGridlines
        responsiveLayout="scroll"
        :scrollable="true"
        scrollHeight="flex"
      >
        <Column field="name" header="名前" headerStyle="width: 20%">
          <template #body="slotProps">
            <template
              v-if="
                slotProps.data.currentDataset.isAnalyzed &&
                !slotProps.data.currentDataset.hasAnnotates
              "
            >
              <router-link
                :to="{
                  name: 'DatasetDetail',
                  params: { id: slotProps.data.id },
                }"
              >
                {{ slotProps.data.name }}
              </router-link>
            </template>
            <template v-else>
              {{ slotProps.data.name }}
            </template>
          </template>
        </Column>
        <Column field="status" header="ステータス" headerStyle="width: 20%">
          <template #body="slotProps">
            <template v-if="slotProps.data.currentDataset">
              <template v-if="slotProps.data.currentDataset.isAnalyzed">
                <template v-if="slotProps.data.currentDataset.hasAnnotates">
                  <i
                    v-tooltip="
                      'アップロードされたファイルに問題があります。\n' +
                      slotProps.data.currentDataset.annotateMessages.join('\n')
                    "
                    class="pi pi-times"
                  ></i>
                  <Button
                    label="削除する"
                    class="p-button-danger p-button-text p-button-sm"
                    style="padding: 0 10px"
                    @click="onDelete(slotProps.data)"
                  />
                </template>
                <template v-else>
                  <i
                    v-tooltip="
                      'アップロードされたファイルの解析に成功しました。'
                    "
                    class="pi pi-check"
                  ></i>
                </template>
              </template>
              <template v-else>
                <i
                  v-tooltip="'アップロードされたファイルを解析中です。'"
                  class="pi pi-sync"
                ></i>
              </template>
            </template>
          </template>
        </Column>
        <Column field="numRecords" header="データ件数" headerStyle="width: 20%">
          <template #body="slotProps">
            <template v-if="slotProps.data.currentDataset">
              {{ slotProps.data.currentDataset.numRecords }}
            </template>
          </template>
        </Column>
        <Column
          field="publicLevel"
          header="公開レベル"
          headerStyle="width: 20%"
        >
          <template #body="slotProps">
            {{ slotProps.data.publicLevelName }}
          </template>
        </Column>
        <Column field="createdAt" header="登録日時" headerStyle="width: 20%">
          <template #body="slotProps">
            <template v-if="slotProps.data.createdAt">
              {{ formatDateTime(slotProps.data.createdAt) }}
            </template>
          </template>
        </Column>
        <template #footer>
          <Paginator
            :rows="pageSize"
            :totalRecords="totalRecords"
            template="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
            @page="onPage"
          >
          </Paginator>
        </template>
      </DataTable>
    </div>
  </div>
</template>

<style scoped>
  .ownDataset {
    padding: 40px;

    ::v-deep(.p-datatable-footer) {
      padding: 0;
    }
  }
</style>
