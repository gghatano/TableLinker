<script lang="ts">
  import { defineComponent, unref, computed, reactive, toRefs } from 'vue'
  import { clone } from '@/utils'
  import {
    useGetManySuggestsByDatasetGroupQuery,
    useGetManySuggestsByDatasetTemplateQuery,
    useGetManyAttrTypeQuery,
    useGetManyDataTypeQuery,
    useCreateConvertJobMutation,
    useUpdateDatasetAttrMutation,
    useGetManyConvertorFiltersQuery,
    useAnalyzeDatasetGroupMutation,
  } from '@/modules/graphql'
  import { useResult } from '@vue/apollo-composable'
  import {
    FilterType,
    DatasetAttrType,
    GetManySuggestsByDatasetGroupQuery,
    GetManySuggestsByDatasetTemplateQuery,
  } from '@/schema/schema'
  import DataConvert from './DataConvert.vue'

  type Props = {
    datasetGroupId: string
    targetDatasetGroupId: string | null | undefined
    targetDatasetTemplateId: string | null | undefined
  }

  export default defineComponent({
    components: {
      DataConvert,
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
      const state = reactive({
        message: '右図の推奨データセットに合わせて、 編集を行ってください',
        selectedAttrs: [] as DatasetAttrType[],
        showConvertDrawer: false,
        currentFilter: null,
        searchQuery: '',
        showTarget: true,
      })

      const selectedAttr = computed(() =>
        state.selectedAttrs.length === 1 ? state.selectedAttrs[0] : null
      )

      const selectedAttrIds = computed(() =>
        state.selectedAttrs.map((attr) => attr.id)
      )

      // 変換ドロワーの表示
      const onShownConvertDrawer = (filter: FilterType) => {
        state.showConvertDrawer = true
        state.currentFilter = filter
      }

      const onCloseConvertDrawer = () => {
        state.showConvertDrawer = false
        state.currentFilter = null
      }

      const useGetItemMappingDatasetGroup = () => {
        const { result, refetch, onResult } =
          useGetManySuggestsByDatasetGroupQuery({
            datasetGroupId: props.datasetGroupId,
            targetDatasetGroupId: props.targetDatasetGroupId,
          })

        const itemMapping = useResult<
          GetManySuggestsByDatasetGroupQuery,
          'suggestByDatasetGroup'
        >(result)

        const datasetGroup = computed(() => unref(itemMapping)?.datasetGroup)
        const dataset = computed(() => {
          return unref(datasetGroup)?.currentDataset
        })
        const attrs = computed(() => unref(dataset)?.attrs)

        const targetDatasetGroup = computed(
          () => unref(itemMapping)?.targetDatasetGroup
        )

        const targetDataset = computed(() => {
          return unref(targetDatasetGroup)?.currentDataset
        })
        const targetAttrs = computed(() => unref(targetDataset)?.attrs)

        const suggests = computed(() => unref(itemMapping)?.suggests || [])

        const suggestsByIndex = computed(() => {
          const suggests = unref(itemMapping)?.suggests || []
          return (
            suggests.reduce((map, obj) => {
              const key = obj['sourceIndex']
              map[key] = [obj]

              return map
            }, {}) || {}
          )
        })

        const selectedSuggests = computed(() => {
          const suggests = unref(itemMapping)?.suggests || []
          if (state.selectedAttrs.length === 0) {
            return suggests
          }
          const _suggestsByIndex = unref(suggestsByIndex)
          return state.selectedAttrs
            .map((attr) => _suggestsByIndex[attr.index])
            .filter((suggets) => suggets !== undefined)
            .flat()
        })

        return {
          itemMapping,
          refetch,
          onResult,
          datasetGroup,
          dataset,
          attrs,
          targetDataset,
          targetAttrs,
          suggests,
          suggestsByIndex,
          selectedSuggests,
        }
      }

      const useGetItemMappingDatasetTemplate = () => {
        const { result, refetch, onResult } =
          useGetManySuggestsByDatasetTemplateQuery({
            datasetGroupId: props.datasetGroupId,
            targetDatasetTemplateId: props.targetDatasetTemplateId,
          })

        const itemMapping = useResult<
          GetManySuggestsByDatasetTemplateQuery,
          'suggestByDatasetTemplate'
        >(result)

        const datasetGroup = computed(() => unref(itemMapping)?.datasetGroup)
        const dataset = computed(() => unref(datasetGroup)?.currentDataset)
        const attrs = computed(() => unref(dataset)?.attrs)

        const targetDataset = computed(() => {
          return unref(itemMapping)?.targetDatasetTemplate
        })
        const targetAttrs = computed(() => unref(targetDataset)?.attrs)

        const suggests = computed(() => unref(itemMapping)?.suggests || [])

        const suggestsByIndex = computed(() => {
          const suggests = unref(itemMapping)?.suggests || []
          return (
            suggests.reduce((map, obj) => {
              const key = obj['sourceIndex']
              map[key] = [obj]

              return map
            }, {}) || {}
          )
        })

        const selectedSuggests = computed(() => {
          const suggests = unref(itemMapping)?.suggests || []
          if (state.selectedAttrs.length === 0) {
            return suggests
          }
          const _suggestsByIndex = unref(suggestsByIndex)
          return state.selectedAttrs
            .map((attr) => _suggestsByIndex[attr.index])
            .filter((suggets) => suggets !== undefined)
            .flat()
        })

        return {
          itemMapping,
          refetch,
          onResult,
          datasetGroup,
          dataset,
          attrs,
          targetDataset,
          targetAttrs,
          suggests,
          suggestsByIndex,
          selectedSuggests,
        }
      }

      const useGetItemMappingDataset =
        props.targetDatasetGroupId == null
          ? useGetItemMappingDatasetTemplate
          : useGetItemMappingDatasetGroup
      const useGetItemMappingDatasetResult = useGetItemMappingDataset()
      const { attrs, onResult } = useGetItemMappingDatasetResult
      const searchedAttrs = computed(() => {
        if (state.searchQuery == '') return unref(attrs)
        return unref(attrs).filter((attr) => {
          return attr.name.indexOf(state.searchQuery) !== -1
        })
      })
      const isSearching = computed(() => state.searchQuery !== '')

      onResult(() => {
        // AttrのIDが変わるので、SelectAttrsを入れ替える必要がある
        // ここでは、名前の変更なので、indexは、変わらない前提で考えている
        const selectedAttrIndexs = state.selectedAttrs.map((attr) => attr.index)
        state.selectedAttrs = unref(attrs).filter((attr) => {
          return selectedAttrIndexs.includes(attr.index)
        })
      })

      // 変換処理
      const useConvert = () => {
        const localState = reactive({
          converting: false,
          currentAttr: null as DatasetAttrType | null,
          editableAttrName: null as string | null,
        })

        const { mutate: convert } = useCreateConvertJobMutation({})

        const onConvert = async (convertData: any) => {
          if (localState.converting) return
          localState.converting = true
          try {
            await convert({
              input: {
                ...convertData,
              },
            })
            state.showConvertDrawer = false
            state.currentFilter = null
          } catch (e) {
            // TODO: 変換に失敗しましました。
            console.error(e)
          } finally {
            try {
              await useGetItemMappingDatasetResult.refetch()
            } finally {
              localState.converting = false
            }
          }
        }

        const onConverted = async () => {
          try {
            state.showConvertDrawer = false
            state.currentFilter = null
            localState.converting = true
            await useGetItemMappingDatasetResult.refetch()
          } finally {
            localState.converting = false
          }
        }

        // 並び替え
        const onRowReorder = async (event) => {
          if (localState.converting) return
          localState.converting = true
          try {
            const input_attr_idx = event.dragIndex
            let output_attr_new_index = event.dropIndex
            if (input_attr_idx < output_attr_new_index) {
              output_attr_new_index = output_attr_new_index + 1
            }

            await convert({
              input: {
                datasetGroupId: props.datasetGroupId,
                filterKey: 'move_col',
                filterParams: JSON.stringify({
                  input_attr_idx: input_attr_idx,
                  output_attr_new_index: output_attr_new_index,
                }),
              },
            })
          } catch (e) {
            // TODO: 変換に失敗しましました。
            console.error(e)
          } finally {
            console.log(useGetItemMappingDatasetResult)
            await useGetItemMappingDatasetResult.refetch()
            localState.converting = false
          }
        }

        const onEditAttr = async (datasetAttr: DatasetAttrType) => {
          if (localState.converting) return
          localState.currentAttr = clone(datasetAttr)
          localState.editableAttrName = localState.currentAttr.name
        }

        const onCancelAttr = () => {
          localState.currentAttr = null
          localState.editableAttrName = null
        }

        const onUpdateAttrName = async () => {
          if (localState.converting) return
          localState.converting = true
          try {
            await convert({
              input: {
                datasetGroupId: props.datasetGroupId,
                filterKey: 'rename_col',
                filterParams: JSON.stringify({
                  new_col_name: localState.editableAttrName,
                  input_attr_idx: localState.currentAttr.index,
                }),
              },
            })
          } catch (e) {
            // TODO: 変換に失敗しましました。
            console.error(e)
          } finally {
            await useGetItemMappingDatasetResult.refetch()
            localState.converting = false
          }
        }

        const onConvertSuggest = async (suggest) => {
          if (localState.converting) return
          localState.converting = true
          try {
            await convert({
              input: {
                datasetGroupId: props.datasetGroupId,
                filterKey: suggest.filterKey,
                filterParams: suggest.filterParams,
              },
            })
          } catch (e) {
            // TODO: 変換に失敗しましました。
            console.error(e)
          } finally {
            console.log(useGetItemMappingDatasetResult)
            await useGetItemMappingDatasetResult.refetch()
            localState.converting = false
          }
        }

        return {
          ...toRefs(localState),
          selectedAttr,
          onConvert,
          onConverted,
          onRowReorder,
          onCancelAttr,
          onEditAttr,
          onUpdateAttrName,
          onConvertSuggest,
        }
      }

      const useUpdateAttr = () => {
        const { mutate, loading: updatingAttr } = useUpdateDatasetAttrMutation(
          {}
        )

        const onUpdateAttr = async (attr: DatasetAttrType) => {
          await mutate({
            input: {
              attrId: attr.id,
              dataType: attr.dataType,
              attrType: attr.attrType,
            },
          })
          await useGetItemMappingDatasetResult.refetch()
        }

        return {
          updatingAttr,
          onUpdateAttr,
        }
      }

      const useDataType = () => {
        const { result, loading: loadingDataTypes } = useGetManyDataTypeQuery(
          {}
        )
        const dataTypes = useResult(result)

        return {
          dataTypes,
          loadingDataTypes,
        }
      }

      const useAttType = () => {
        const { result, loading: loadingAttTypes } = useGetManyAttrTypeQuery({})
        const attrTypes = useResult(result)

        return {
          attrTypes,
          loadingAttTypes,
        }
      }

      const useFilters = () => {
        const { result, loading, refetch } = useGetManyConvertorFiltersQuery({
          datasetAttrIds: unref(selectedAttrIds),
        })
        const convertorFilters = useResult(result)

        const onFilterRefresh = async () => {
          await refetch({
            datasetAttrIds: unref(selectedAttrIds),
          })
        }

        return {
          convertorFilters,
          onFilterRefresh,
          filterloading: loading,
        }
      }

      const useAnalyze = () => {
        const { mutate } = useAnalyzeDatasetGroupMutation({})
        const onAnalyze = async () => {
          await mutate({
            input: {
              datasetGroupId: props.datasetGroupId,
            },
          })
          await useGetItemMappingDatasetResult.refetch()
        }

        return {
          onAnalyze,
        }
      }

      return {
        ...toRefs(state),
        searchedAttrs,
        isSearching,
        onShownConvertDrawer,
        onCloseConvertDrawer,
        ...useGetItemMappingDatasetResult,
        ...useConvert(),
        ...useDataType(),
        ...useAttType(),
        ...useUpdateAttr(),
        ...useFilters(),
        ...useAnalyze(),
      }
    },
  })
</script>

<template>
  <div>
    <div style="min-height: 0.5em">
      <ProgressBar
        v-if="converting"
        showValue="aaa"
        mode="indeterminate"
        style="height: 0.5em"
      />
    </div>

    <div class="content p-d-flex p-jc-between">
      <div class="message">
        <template v-if="message">
          {{ message }}
        </template>
      </div>
      <div>
        <Button
          style="padding: 0; margin-right: 20px"
          label="再解析"
          class="p-button-text p-button-sm"
          @click="onAnalyze"
        />
        <Button
          v-if="showTarget"
          style="padding: 0; margin-right: 20px"
          label="対象を隠す"
          class="p-button-text p-button-sm"
          @click="showTarget = false"
        />
        <Button
          v-else
          style="padding: 0; margin-right: 20px"
          label="対象を表示する"
          class="p-button-text p-button-sm"
          @click="showTarget = true"
        />
      </div>
    </div>
    <div class="content p-d-flex p-jc-between">
      <div class="column column__column">
        <div class="column--title" style="margin-left: 24px">
          現在データ変換箇所
        </div>
        <div class="column--searchbox" style="margin-left: 24px">
          <div class="p-input-icon-right">
            <InputText
              v-model:modelValue="searchQuery"
              type="text"
              placeholder="キーワード"
              class="p-inputtext-sm"
            />
            <i class="pi pi-search" />
          </div>
        </div>
        <ScrollPanel style="width: 100%; height: calc(100vh - 540px)">
          <div class="edit">
            <div class="annotate-icons">
              <template v-for="attr in searchedAttrs" :key="attr.id">
                <div class="annotate-icons--item">
                  <span
                    :style="{
                      visibility:
                        suggestsByIndex[attr.index] == null
                          ? 'hidden'
                          : 'visible',
                    }"
                  >
                    <i class="pi pi-exclamation-circle"></i>
                  </span>
                </div>
              </template>
            </div>
            <DataTable
              v-model:selection="selectedAttrs"
              selectionMode="multiple"
              :value="searchedAttrs"
              class="p-datatable-sm"
              responsiveLayout="scroll"
              :reorderableColumns="false"
              :rowHover="true"
              scrollDirection="both"
              :resizableColumns="true"
              columnResizeMode="expand"
              :metaKeySelection="false"
              dataKey="id"
              @row-reorder="onRowReorder"
              @row-select="onFilterRefresh"
              @row-unselect="onFilterRefresh"
            >
              <Column
                header="並替"
                :rowReorder="!isSearching"
                :reorderableColumn="false"
                :headerStyle="{ width: '60px' }"
                style="flex-grow: 0; flex-basis: 60px"
              ></Column>
              <Column field="no" header="No"></Column>
              <Column
                field="name"
                header="名前"
                :reorderableColumn="false"
                style="flex-grow: 1; flex-basis: 160px"
              >
                <template #body="{ data }">
                  <span style="white-space: nowrap">{{ data.name }}</span>
                </template>
              </Column>
              <Column
                field="attrTypeName"
                header="意味型"
                :reorderableColumn="false"
                style="flex-grow: 0; flex-basis: 160px"
              ></Column>
              <Column
                field="dataTypeName"
                header="データ型"
                :reorderableColumn="false"
                style="flex-grow: 0; flex-basis: 160px"
              ></Column>

              <Column
                field="sampleValues"
                header="サンプル"
                :reorderableColumn="false"
                style="flex-grow: 0; flex-basis: 160px"
              >
                <template #body="{ data }">
                  <template v-for="sampleValue in data.sampleValues">
                    {{ sampleValue }},
                  </template>
                </template>
              </Column>
            </DataTable>
          </div>
        </ScrollPanel>
      </div>
      <div
        v-if="showTarget && targetDataset != null"
        class="column column__target"
      >
        <div class="column--title">推奨データセット</div>
        <div class="column--searchbox">
          {{ targetDataset.name }}
        </div>
        <ScrollPanel style="width: 100%; height: calc(100vh - 540px)">
          <DataTable
            :value="targetAttrs"
            class="p-datatable-sm"
            responsiveLayout="scroll"
            :reorderableColumns="false"
            :rowHover="true"
            :resizableColumns="true"
            columnResizeMode="expand"
            dataKey="id"
          >
            <Column field="no" header="No"></Column>
            <Column
              field="name"
              header="名前"
              :reorderableColumn="false"
              style="flex-grow: 0; flex-basis: 160px"
            >
            </Column>
            <Column
              field="attrTypeName"
              header="意味型"
              :reorderableColumn="false"
              style="flex-grow: 0; flex-basis: 160px"
            ></Column>
            <Column
              field="dataTypeName"
              header="データ型"
              :reorderableColumn="false"
              style="flex-grow: 0; flex-basis: 160px"
            ></Column>
          </DataTable>
        </ScrollPanel>
      </div>

      <div class="column column__annotate">
        <div class="column--title">推奨データセットとの差分内容</div>
        <div class="column--searchbox">
          <template v-if="selectedAttrs != null && selectedAttrs.length > 0">
            <template v-for="attr in selectedAttrs" :key="attr.id">
              {{ attr.name }}
            </template>
          </template>
        </div>
        <div class="column--content">
          <TabView>
            <TabPanel header="提案">
              <ScrollPanel style="width: 100%; height: calc(100vh - 576px)">
                <div class="annotate-messsage">
                  <template
                    v-for="suggest in selectedSuggests"
                    :key="suggest.filterKey"
                  >
                    <div
                      class="annotate-messsage--item"
                      @click="onConvertSuggest(suggest)"
                    >
                      <span><i class="pi pi-exclamation-circle"></i></span>
                      <div>{{ suggest.message }}</div>
                    </div>
                  </template>
                </div>
              </ScrollPanel>
            </TabPanel>
            <TabPanel header="データ編集">
              <ScrollPanel style="width: 100%; height: calc(100vh - 576px)">
                <div :key="convertorFilters" class="annotate-messsage">
                  <template
                    v-for="filter in convertorFilters"
                    :key="filter.key"
                  >
                    <div
                      class="annotate-messsage--item"
                      @click="onShownConvertDrawer(filter)"
                    >
                      <span><i class="pi pi-circle"></i></span>
                      <div>{{ filter.description }}({{ filter.name }})</div>
                    </div>
                  </template>
                </div>
              </ScrollPanel>
            </TabPanel>
            <TabPanel header="列の情報" :disabled="selectedAttr == null">
              <div v-if="selectedAttr != null" class="column-panel">
                <div class="column-panel--actions">
                  <template v-if="currentAttr == null">
                    <Button
                      style="padding: 0"
                      icon="pi pi-pencil"
                      iconPos="right"
                      label="編集する"
                      class="p-button-text p-button-sm"
                      @click="onEditAttr(selectedAttr)"
                    >
                    </Button>
                  </template>
                  <template v-else>
                    <Button
                      style="padding: 0"
                      label="キャンセルする"
                      class="p-button-text p-button-sm"
                      @click="onCancelAttr"
                    >
                    </Button>
                  </template>
                </div>
                <div class="column-panel--colmun">
                  <h5>名前</h5>
                  <Inplace :active="currentAttr != null" :closable="false">
                    <template #display>
                      <span>{{ selectedAttr.name }}</span>
                    </template>
                    <template #content>
                      <div class="p-inputgroup">
                        <InputText
                          v-model:modelValue="editableAttrName"
                          autoFocus
                          style="width: 100px"
                          class="p-inputtext-sm"
                        />
                        <Button
                          v-if="converting"
                          label="保存"
                          icon="pi pi-spin pi-refresh"
                        />
                        <Button
                          v-else
                          label="保存"
                          icon="pi pi-check"
                          @click="onUpdateAttrName"
                        />
                      </div>
                    </template>
                  </Inplace>
                </div>
                <div class="column-panel--colmun">
                  <h5>意味型</h5>
                  <Inplace :active="currentAttr != null" :closable="false">
                    <template #display>
                      {{ selectedAttr.attrTypeName }}
                    </template>
                    <template #content>
                      <Dropdown
                        v-model:modelValue="currentAttr.attrType"
                        :options="attrTypes"
                        optionLabel="name"
                        optionValue="value"
                        @change="onUpdateAttr(currentAttr)"
                      />
                    </template>
                  </Inplace>
                </div>
                <div class="column-panel--colmun">
                  <h5>データ型</h5>
                  <Inplace :active="currentAttr != null" :closable="false">
                    <template #display>
                      {{ selectedAttr.dataTypeName }}
                    </template>
                    <template #content>
                      <Dropdown
                        v-model:modelValue="currentAttr.dataType"
                        :options="dataTypes"
                        optionLabel="name"
                        optionValue="value"
                        @change="onUpdateAttr(currentAttr)"
                      />
                    </template>
                  </Inplace>
                </div>
                <div class="column-panel--colmun">
                  <h5>参考値</h5>
                  <div style="word-break: break-all">
                    {{ selectedAttr.sampleValues.join(',') }}
                  </div>
                </div>
              </div>
            </TabPanel>
          </TabView>
        </div>
      </div>
    </div>
    <Sidebar
      v-model:visible="showConvertDrawer"
      position="right"
      :showCloseIcon="true"
      style="width: 600px"
    >
      <template v-if="datasetGroup != undefined">
        <DataConvert
          :datasetGroup="datasetGroup"
          :targetAttrs="selectedAttrs"
          :filter="currentFilter"
          @converted="onConverted"
          @cancel="onCloseConvertDrawer"
        ></DataConvert>
      </template>
    </Sidebar>
  </div>
</template>

<style lang="scss" scoped>
  .message {
    color: #00a682; // primry color
    padding: 15px;
  }
  .content {
    width: 100%;

    .column {
      width: 33%;
      padding: 25px 15px;
      overflow: auto;

      &--title {
        color: #00a682; // primry color
        margin-bottom: 15px;
      }
      &--searchbox {
        height: 3rem;
        margin-bottom: 10px;
      }

      &--content {
        ::v-deep(.p-tabview) {
          .p-tabview-nav {
            background-color: transparent;
            .p-tabview-nav-link {
              padding: 10px 20px;
              background-color: transparent;

              &:not(.p-disabled):focus {
                box-shadow: none;
              }
            }
          }
          .p-tabview-panels {
            padding: 14px 10px 10px 0;
            background-color: transparent;
          }
        }
      }

      &__column {
        flex-grow: 1;
      }

      &__target {
        border: 1px solid #00a682; // primry color
        border-radius: 5px;
        margin: 0 20px;
      }

      &__annotate {
        border-radius: 5px;
        margin: 0 20px;
        background-color: rgba(0, 166, 130, 0.1); // primry color
      }
    }

    .annotate-messsage {
      &--item {
        cursor: pointer;

        margin-bottom: 5px;

        display: flex;
        justify-content: flex-start;
        align-items: flex-start;

        i.pi {
          margin-right: 5px;
          color: #ff858c;
          margin-top: 2px;
          font-size: 1rem;
        }
      }
    }

    .column-convert {
      &--item {
        margin-bottom: 5px;

        display: flex;
        justify-content: flex-start;
        align-items: flex-start;

        i.pi {
          visibility: hidden;
          margin-right: 5px;
        }

        &__checked {
          i.pi {
            visibility: visible;
            color: #ff858c; // primry color
          }
        }
      }
    }

    .edit {
      display: flex;
    }

    .annotate-icons {
      padding: 36.5px 0 20px;
      &--item {
        margin-right: 10px;
        height: 38px;
        display: flex;
        align-items: center;
        i.pi {
          color: #ff858c;
        }
      }
    }

    .suggest-tabs {
    }

    .column-panel {
      position: relative;
      padding: 20px 0;

      margin-bottom: 10px;

      h5 {
        margin: 0 0 5px;
      }

      &--colmun {
        margin-bottom: 10px;
      }

      ::v-deep(.p-inplace) {
        .p-inplace-display {
          padding: 0;
        }
      }

      &--actions {
        position: absolute;
        top: 0;
        right: 0;
      }
    }
  }
</style>
