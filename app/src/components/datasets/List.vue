<script lang="ts">
  import { defineComponent, reactive, toRefs, unref, computed } from 'vue'

  import { useDatasetGroupsQuery } from '@/modules/graphql'
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
      const { result, loading } = useDatasetGroupsQuery(variables)

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

      return {
        ...toRefs(state),
        ...toRefs(variables),
        datasetGroups,
        totalRecords,
        loading,
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
        <Button label="検索" class="p-button-sm" @click="onSearch" />
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
            <router-link
              :to="{ name: 'DatasetDetail', params: { id: slotProps.data.id } }"
            >
              {{ slotProps.data.name }}
            </router-link>
          </template>
        </Column>

        <Column field="numRecords" header="データ件数" headerStyle="width: 20%">
          <template #body="slotProps">
            <template v-if="slotProps.data.currentDataset">
              {{ slotProps.data.currentDataset.numRecords }}
            </template>
          </template>
        </Column>
        <Column field="createdAt" header="列名" headerStyle="width: 20%">
          <template #body="slotProps">
            <template v-if="slotProps.data.currentDataset">
              {{ slotProps.data.currentDataset.attrNames.join(',') }}
            </template>
          </template>
        </Column>
        <Column field="createdAt" header="登録日時" headerStyle="width: 20%">
          <template #body="slotProps">
            <template v-if="slotProps.data.createdAt">
              {{ formatDateTime(slotProps.data.createdAt) }}
            </template>
          </template>
        </Column>
        <Column field="createdAt" header="登録ユーザ" headerStyle="width: 20%">
          <template #body="slotProps">
            <template v-if="slotProps.data.createdAt">
              {{ slotProps.data.createdBy }}
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
