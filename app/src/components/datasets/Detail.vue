<script lang="ts">
  import { defineComponent, unref, computed, reactive, toRefs } from 'vue'
  import {
    useDatasetGroupQuery,
    useDeleteDatasetGroupMutation,
  } from '@/modules/graphql'
  import { DatasetTemplateType, DatasetGroupType } from '@/schema/schema'
  import Nav from './Nav.vue'
  import { useResult } from '@vue/apollo-composable'
  import { useRouter } from 'vue-router'
  import { useConfirm } from 'primevue/useconfirm'
  import DataPreview from './DataPreview.vue'
  import DataVersionList from './DataVersionList.vue'
  import TempalateSearch from './TempalateSearch.vue'

  type Props = {
    datasetGroupId: string
  }

  export default defineComponent({
    components: {
      Nav,
      DataPreview,
      DataVersionList,
      TempalateSearch,
    },
    props: {
      datasetGroupId: {
        type: String,
        required: true,
      },
    },
    setup(props: Props) {
      const router = useRouter()

      const state = reactive({
        visibleSearch: false,
      })

      const { result, loading, refetch } = useDatasetGroupQuery({
        id: props.datasetGroupId,
      })

      const datasetGroup = useResult(result)
      const dataset = computed(() => unref(datasetGroup)?.currentDataset)
      const attrs = computed(() => unref(dataset)?.attrs)

      const useDelete = () => {
        const confirm = useConfirm()
        const { mutate, loading: deleting } = useDeleteDatasetGroupMutation({})

        const onDelete = async () => {
          await mutate({
            datasetGroupId: props.datasetGroupId,
          })
          router.push({ name: 'UserDatasetList' })
        }

        const onDeleteConfirm = async (event: Event) => {
          confirm.require({
            target: event.currentTarget,
            message: '削除します。よろしいですか？',
            icon: 'pi pi-exclamation-triangle',
            accept: async () => {
              await onDeleteConfirm()
            },
          })
        }

        return {
          ...toRefs(state),
          onDelete,
          onDeleteConfirm,
          deleting,
        }
      }

      const onEditDataset = () => {
        state.visibleSearch = true
      }

      const onSelectTemplate = (template: DatasetTemplateType) => {
        state.visibleSearch = false
        router.push({
          name: 'DatasetMappingTemplate',
          params: {
            id: props.datasetGroupId,
            targetDatasetTemplateId: template.id,
          },
        })
      }

      const onSelectDatasetGroup = (datasetGroup: DatasetGroupType) => {
        state.visibleSearch = false
        router.push({
          name: 'DatasetMappingDatasetGroup',
          params: {
            id: props.datasetGroupId,
            targetDatasetGroupId: datasetGroup.id,
          },
        })
      }

      const isOwner = computed(() => true) // TODO

      const onRefetch = async () => {
        await refetch()
      }

      return {
        datasetGroup,
        dataset,
        attrs,
        loading,
        ...useDelete(),
        onEditDataset,
        onSelectTemplate,
        onSelectDatasetGroup,

        onRefetch,
        isOwner,
      }
    },
  })
</script>

<template>
  <div>
    <template v-if="loading">
      <ProgressBar mode="indeterminate" style="height: 0.5em" />
    </template>
    <template v-else-if="!datasetGroup.currentDataset.isAnalyzed">
      <div class="p-d-flex p-flex-column p-jc-center p-ai-center">
        <div>
          <p>アップロードを受け付けました。解析処理に数秒かかります。</p>
          <p>
            画面をリロードするか、他の作業を行った後、ユーザメニューの［アップロード一覧」から再度確認してください。
          </p>
          <div v-if="isOwner" style="margin: 24px 0">
            <Button type="is-primary is-light" @click="onDelete">
              解析処理をキャンセルする
            </Button>
          </div>
        </div>
      </div>
    </template>
    <template
      v-else-if="
        dataset.currentDataset != null && dataset.currentDataset.hasAnnotates
      "
    >
      <p>
        以下のエラー発生した為、データ解析を継続できません。ファイルを再度アップロードしてください。
      </p>
      <ul class="list">
        <li
          v-for="(message, index) in dataset.currentDataset.annotateMessages"
          :key="index"
        >
          {{ message }}
        </li>
      </ul>
      <div v-if="isOwner" style="margin: 24px 0">
        <button type="is-danger" @click="onDeleteConfirm">
          このデータソースを削除する
        </button>
      </div>
    </template>
    <template v-else>
      <Nav v-if="datasetGroup" :datasetGroupId="datasetGroupId">
        <template #backTo>
          <div class="p-d-inline-flex p-ai-center">
            <i class="pi pi-arrow-left p-mr-2"></i>
            <router-link :to="{ name: 'DatasetList' }">
              <span>リストへ戻る</span>
            </router-link>
          </div>
        </template>
      </Nav>
      <div class="content">
        <template v-if="isOwner">
          <div class="edit-button">
            <Button
              type="button"
              icon="pi pi-edit"
              label="データを編集する"
              class="p-button-raised p-button-rounded p-button-sm p-ml-1"
              @click="onEditDataset"
            />
          </div>
        </template>
        <TabView lazy>
          <TabPanel header="データ詳細">
            <div>
              <h3>基本情報</h3>
              <div class="desrcriptions">
                <div class="desrcription-item">
                  <div class="desrcription-item--label">データ件数</div>
                  <div
                    class="desrcription-item--value desrcription-item--value__number"
                  >
                    {{ datasetGroup.currentDataset.numRecords }} 件
                  </div>
                </div>
                <div class="desrcription-item">
                  <div class="desrcription-item--label">データサイズ</div>
                  <div
                    class="desrcription-item--value desrcription-item--value__number"
                  >
                    <span>{{ datasetGroup.currentDataset.fileSize }} byte</span>
                  </div>
                </div>
                <div
                  v-if="datasetGroup?.source.siteUrl"
                  class="desrcription-item"
                >
                  <div class="desrcription-item--label">取得元URL</div>
                  <div class="desrcription-item--value">
                    {{ datasetGroup?.source.siteUrl }}
                  </div>
                </div>
              </div>
            </div>
            <div>
              <h3>カラム情報</h3>
              <DataTable
                :value="attrs"
                dataKey="id"
                :rowHover="true"
                :loading="loading"
                :resizableColumns="true"
                columnResizeMode="expand"
                responsiveLayout="scroll"
              >
                <Column field="index" header="#">
                  <template #body="{ data }">
                    {{ data.index + 1 }}
                  </template>
                </Column>
                <Column field="name" header="名前">
                  <template #body="{ data }">
                    {{ data.name }}
                  </template>
                </Column>
                <Column field="name" header="意味型">
                  <template #body="{ data }">
                    {{ data.attrTypeName }}
                  </template>
                </Column>
                <Column field="name" header="データ型">
                  <template #body="{ data }">
                    {{ data.dataTypeName }}
                  </template>
                </Column>
                <Column field="name" header="サンプル値">
                  <template #body="{ data }">
                    <template v-for="sampleValue in data.sampleValues">
                      {{ sampleValue }},
                    </template>
                  </template>
                </Column>
              </DataTable>
            </div>
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
    </template>

    <Dialog
      v-model:visible="visibleSearch"
      :style="{ width: '70vw', height: '70vh', backgroundColor: '#fff' }"
    >
      <template #header>
        データの形を整えるデータセットを選択してください
      </template>
      <TempalateSearch
        :datasetGroup="datasetGroup"
        @select-template="onSelectTemplate"
        @select-dataset-group="onSelectDatasetGroup"
      ></TempalateSearch>
    </Dialog>
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
    top: 192px;
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
