<script lang="ts">
  import { defineComponent, SetupContext, reactive, toRefs } from 'vue'
  import { useSimilarDatasetsQuery } from '@/modules/graphql'
  import { DatasetGroupType } from '@/schema/schema'
  import { useResult } from '@vue/apollo-composable'
  import { PropType } from 'vue'

  type Props = {
    datasetGroup: DatasetGroupType
  }

  export default defineComponent({
    props: {
      datasetGroup: {
        type: Object as PropType<DatasetGroupType>,
        required: true,
      },
    },
    emits: ['select'],
    setup(props: Props, context: SetupContext) {
      const state = reactive({
        keyword: '' as string,
      })

      const variables = reactive({
        keyword: '' as string,
        datasetGroupId: props.datasetGroup.id,
      })

      const { result, refetch } = useSimilarDatasetsQuery(variables)

      const similarDatasetGroups = useResult(result)

      const onSearch = async () => {
        variables.keyword = state.keyword
        await refetch()
        console.log('search')
      }

      const onSelect = (datasetGroup: DatasetGroupType) => {
        context.emit('select', datasetGroup)
      }

      return {
        ...toRefs(state),
        onSearch,
        onSelect,
        similarDatasetGroups,
      }
    },
  })
</script>

<template>
  <div class="root">
    <div class="p-d-flex p-jc-end">
      <span class="p-input-icon-left">
        <InputText
          v-model="keyword"
          type="text"
          placeholder="キーワード"
          class="p-inputtext-sm"
          @change="onSearch"
        />
        <i class="pi pi-search" />
      </span>
    </div>
    <DataTable :value="similarDatasetGroups" responsiveLayout="scroll">
      <Column field="name">
        <template #body="slotProps">
          {{ slotProps.data.datasetGroup.name }}
        </template>
      </Column>
      <Column width="90px" bodyStyle="text-align: right; padding-right: 0;">
        <template #body="slotProps">
          <Button
            type="button"
            label="変換"
            class="p-button-sm p-button-rounded"
            style="width: 90px"
            @click="onSelect(slotProps.data.datasetGroup)"
          ></Button>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<style lang="scss" scoped>
  .root {
    padding: 10px 0;
    ::v-deep(.p-datatable-thead) {
      display: none;
    }
    //height: 100%;
  }
</style>
