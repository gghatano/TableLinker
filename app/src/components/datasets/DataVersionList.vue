<script lang="ts">
  import { defineComponent, reactive, toRefs, SetupContext } from 'vue'
  import { DatasetGroupType, DatasetType } from '@/schema/schema'
  import { PropType } from 'vue'
  import { useUpdateDatasetGroupMutation } from '@/modules/graphql'
  import DataPreview from './DataPreview.vue'
  import DatasetDetail from './DatasetDetail.vue'

  type Props = {
    datasetGroup: DatasetGroupType
  }

  export default defineComponent({
    components: {
      DataPreview,
      DatasetDetail,
    },
    props: {
      datasetGroup: {
        type: Object as PropType<DatasetGroupType>,
        required: true,
      },
    },
    emits: ['change'],
    setup(props: Props, context: SetupContext) {
      const state = reactive({
        currentDatset: null as DatasetType | null,
        showDetailDrawer: false,
      })

      const onSelect = ({ data }: { data: DatasetType }) => {
        state.currentDatset = data
        state.showDetailDrawer = true
      }

      const onHide = () => {
        state.currentDatset = null
      }

      const { mutate: update } = useUpdateDatasetGroupMutation({})
      const onSetCurrent = async () => {
        await update({
          input: {
            datasetGroupId: props.datasetGroup.id,
            currentDatasetId: state.currentDatset.id,
          },
        })
        context.emit('change')
      }

      return {
        ...toRefs(state),
        onHide,
        onSelect,
        onSetCurrent,
      }
    },
  })
</script>

<template>
  <div class="data-preview">
    <DataTable
      v-model:selection="currentDatset"
      :value="datasetGroup.datasets"
      selectionMode="single"
      dataKey="id"
      :rowHover="true"
      :loading="loading"
      :resizableColumns="true"
      columnResizeMode="expand"
      responsiveLayout="scroll"
      @row-select="onSelect"
    >
      <Column field="version" header="バージョン">
        <template #body="{ data }">
          {{ data.version }}
        </template>
      </Column>
      <Column field="name" header="変換内容">
        <template #body="{ data }">
          <span>{{ data.name }}</span>
        </template>
      </Column>
      <Column field="isAnalyzed" header="">
        <template #body="{ data }">
          <tempalat v-if="data.id === datasetGroup.currentDataset.id">
            <i v-tooltip="'カレントデータです。'" class="pi pi-star-fill"></i>
          </tempalat>
          <template v-else-if="data.isAnalyzed">
            <i v-tooltip="'成功しました。'" class="pi pi-check"></i>
          </template>
          <template v-else>
            <i v-tooltip="'変換失敗しました'" class="pi pi-times"></i>
          </template>
        </template>
      </Column>
      <!-- <Column field="filterDetail" header="変換詳細">
        <template #body="{ data }">
          {{ data.filterDetail }}
        </template>
      </Column> -->
      <Column field="numRecords" header="件数">
        <template #body="{ data }">
          {{ data.numRecords }}
        </template>
      </Column>
      <Column field="numColumns" header="列数">
        <template #body="{ data }">
          {{ data.numColumns }}
        </template>
      </Column>
      <!-- <Column field="attrs" header="列数">
        <template #body="{ data }">
          {{ data.attrs.map((attr) => attr.name).join(',') }}
        </template>
      </Column> -->
      <Column field="createdAt" header="作成日時">
        <template #body="{ data }">
          {{ data.createdAt }}
        </template>
      </Column>
    </DataTable>
    <Sidebar
      v-model:visible="showDetailDrawer"
      position="right"
      :showCloseIcon="false"
      style="width: 600px"
      @hide="onHide"
    >
      <template v-if="currentDatset != null">
        <template v-if="datasetGroup.currentDataset.id !== currentDatset.id">
          <Button
            type="button"
            icon="pi pi-edit"
            label="カレントに設定"
            class="p-button-sm edit-button"
            @click="onSetCurrent"
          />
        </template>
        <TabView lazy>
          <TabPanel header="詳細">
            <DatasetDetail :datasetId="currentDatset.id" />
          </TabPanel>
          <TabPanel header="データ">
            <DataPreview :url="currentDatset.dataFileUrl" />
          </TabPanel>
        </TabView>
      </template>
    </Sidebar>
  </div>
</template>

<style lang="scss" scoped>
  .data-preview {
    height: calc(100vh - 140px);
  }
  .edit-button {
    position: absolute;
    right: 40px;
    z-index: 1000;
    top: 0;
  }
</style>
