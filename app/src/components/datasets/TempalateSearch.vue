<script lang="ts">
  import { defineComponent, SetupContext, PropType } from 'vue'
  import { DatasetTemplateType, DatasetGroupType } from '@/schema/schema'
  import TempalateSearchTemplateList from './TempalateSearchTemplateList.vue'
  import TempalateSearchDatasetGroup from './TempalateSearchDatasetGroup.vue'
  import { useRouter } from 'vue-router'

  type Props = {
    datasetGroup: DatasetGroupType
  }

  export default defineComponent({
    components: {
      TempalateSearchDatasetGroup,
      TempalateSearchTemplateList,
    },
    props: {
      datasetGroup: {
        type: Object as PropType<DatasetGroupType>,
        required: true,
      },
    },
    emits: ['selectTemplate', 'selectDatasetGroup'],
    setup(props: Props, context: SetupContext) {
      const router = useRouter()
      const onSelectTemplate = (template: DatasetTemplateType) => {
        context.emit('selectTemplate', template)
      }

      const onSelectDatasetGroup = (datasetGroup: DatasetGroupType) => {
        context.emit('selectDatasetGroup', datasetGroup)
      }

      const onTabClick = ({ index }: { index: number }) => {
        if (index === 2) {
          router.push({
            name: 'DatasetEdit',
            params: {
              id: props.datasetGroup.id,
            },
          })
        }
      }

      return {
        onSelectTemplate,
        onSelectDatasetGroup,
        onTabClick,
      }
    },
  })
</script>

<template>
  <TabView class="root" @tab-click="onTabClick">
    <TabPanel header="推奨データセット">
      <TempalateSearchTemplateList
        @select="onSelectTemplate"
      ></TempalateSearchTemplateList>
    </TabPanel>
    <TabPanel header="類似データセット">
      <TempalateSearchDatasetGroup
        :datasetGroup="datasetGroup"
        @select="onSelectDatasetGroup"
      ></TempalateSearchDatasetGroup>
    </TabPanel>
    <TabPanel header="直接編集する"></TabPanel>
  </TabView>
</template>

<style lang="scss" scoped>
  .root {
    //height: 100%;
    ::v-deep(.p-tabview-panels) {
      padding: 0;
    }
  }
</style>
