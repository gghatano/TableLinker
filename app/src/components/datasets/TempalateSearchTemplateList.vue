<script lang="ts">
  import { defineComponent, SetupContext, reactive, toRefs } from 'vue'
  import { useTemplatesQuery } from '@/modules/graphql'
  import { DatasetTemplateType } from '@/schema/schema'
  import { useResult } from '@vue/apollo-composable'

  export default defineComponent({
    emits: ['select'],
    setup(_, context: SetupContext) {
      const state = reactive({
        keyword: '' as string,
      })

      const variables = reactive({
        keyword: '' as string,
      })

      const { result, refetch } = useTemplatesQuery(variables)

      const templates = useResult(result)

      const onSearch = async () => {
        variables.keyword = state.keyword
        await refetch()
      }

      const onSelect = (template: DatasetTemplateType) => {
        context.emit('select', template)
      }

      return {
        ...toRefs(state),
        onSearch,
        onSelect,
        templates,
      }
    },
  })
</script>

<template>
  <div class="root">
    <div class="p-d-flex p-jc-end">
      <span class="p-input-icon-left">
        <i class="pi pi-search" />
        <InputText
          v-model="keyword"
          type="text"
          placeholder="キーワード"
          class="p-inputtext-sm"
          @change="onSearch"
        />
      </span>
    </div>
    <DataTable :value="templates" responsiveLayout="scroll">
      <Column field="name"></Column>
      <Column width="90px" bodyStyle="text-align: right; padding-right: 0;">
        <template #body="slotProps">
          <Button
            type="button"
            label="変換"
            class="p-button-sm p-button-rounded"
            style="width: 90px"
            @click="onSelect(slotProps.data)"
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
