<script lang="ts">
  import { defineComponent, unref, computed } from 'vue'
  import {
    useDatasetGroupQuery,
    useUpdateDatasetGroupMutation,
  } from '@/modules/graphql'
  import Nav from './Nav.vue'
  import { useResult } from '@vue/apollo-composable'
  import DataPreview from './DataPreview.vue'
  import DataEdit from './DataEdit.vue'
  import DataVersionList from './DataVersionList.vue'
  type Props = {
    datasetGroupId: string
  }

  export default defineComponent({
    components: {
      Nav,
      DataPreview,
      DataEdit,
      DataVersionList,
    },
    props: {
      datasetGroupId: {
        type: String,
        required: true,
      },
      targetDatasetGroupId: {
        type: String,
        required: false,
        default: null,
      },
      targetDatasetTemplateId: {
        type: String,
        required: false,
        default: null,
      },
    },
    setup(props: Props) {
      const { result, loading, refetch } = useDatasetGroupQuery({
        id: props.datasetGroupId,
      })

      const datasetGroup = useResult(result)
      const dataset = computed(() => unref(datasetGroup)?.currentDataset)
      const attrs = computed(() => unref(dataset)?.attrs)

      const useUpdate = () => {
        const { mutate, loading: updating } = useUpdateDatasetGroupMutation({})

        const onUpdate = async (publicLevel: number) => {
          await mutate({
            input: {
              datasetGroupId: props.datasetGroupId,
              publicLevel,
            },
          })
          await refetch()
        }

        return {
          updating,
          onUpdate,
        }
      }

      const onRefetch = async () => {
        await refetch()
      }

      return {
        datasetGroup,
        dataset,
        attrs,
        loading,
        onRefetch,
        ...useUpdate(),
      }
    },
  })
</script>

<template>
  <div>
    <template v-if="loading">
      <ProgressBar mode="indeterminate" style="height: 0.5em" />
    </template>
    <Nav v-if="datasetGroup" :datasetGroupId="datasetGroupId">
      <template #backTo>
        <div class="p-d-inline-flex p-ai-center">
          <i class="pi pi-arrow-left p-mr-2"></i>
          <router-link
            :to="{ name: 'DatasetDetail', props: { id: datasetGroupId } }"
          >
            <span>データセット詳細へ戻る</span>
          </router-link>
        </div>
      </template>
    </Nav>
    <div class="content">
      <TabView lazy>
        <TabPanel header="マッピング">
          <DataEdit
            :datasetGroupId="datasetGroupId"
            :targetDatasetGroupId="targetDatasetGroupId"
            :targetDatasetTemplateId="targetDatasetTemplateId"
          ></DataEdit>
        </TabPanel>
        <TabPanel header="データ">
          <DataPreview :url="datasetGroup.currentDataset.dataFileUrl" />
        </TabPanel>
        <TabPanel header="履歴">
          <DataVersionList
            :datasetGroup="datasetGroup"
            @change="onRefetch"
          ></DataVersionList>
        </TabPanel>
      </TabView>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .content {
    padding: 30px;
  }

  .edit-button {
    position: absolute;
    right: 40px;
    z-index: 1000;
    top: 222px;
  }

  .desrcriptions {
    display: flex;
    flex-direction: row;
    margin-bottom: 30px;

    .desrcription-item {
      display: flex;
      flex-direction: row;
      margin-bottom: 30px;
      border: #dbdbdb 1px solid;

      &--label {
        background-color: #dbdbdb;
        padding: 8px;
        width: 180px;
      }

      &--value {
        min-width: 180px;
        padding: 5px;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        &__number {
          justify-content: flex-end;
        }
        //text-align: right;
      }
    }
  }
</style>
