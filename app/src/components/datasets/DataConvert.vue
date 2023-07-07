<script lang="ts">
  import { parse } from 'papaparse'
  import {
    defineComponent,
    reactive,
    toRefs,
    SetupContext,
    PropType,
    computed,
    unref,
  } from 'vue'

  import {
    DatasetGroupType,
    DatasetAttrType,
    FilterType,
    ParamType,
  } from '@/schema/schema'
  import {
    useConvertPreviewMutation,
    useCreateConvertJobMutation,
  } from '@/modules/graphql'

  import BooleanParam from './params/BooleanParam.vue'
  import StringParam from './params/StringParam.vue'
  import StringListParam from './params/StringListParam.vue'
  import TextParam from './params/TextParam.vue'
  import IntegerParam from './params/IntegerParam.vue'
  import EnumsParam from './params/EnumsParam.vue'
  import CollectionParam from './params/CollectionParam.vue'
  import AttributeParam from './params/AttributeParam.vue'
  import AttributeListParam from './params/AttributeListParam.vue'
  import AttributeNameParam from './params/AttributeNameParam.vue'
  import DataPreview from './DataPreview.vue'

  type Props = {
    datasetGroup: DatasetGroupType
    targetAttrs: DatasetAttrType[]
    filter: FilterType
  }

  export default defineComponent({
    components: {
      BooleanParam,
      StringParam,
      StringListParam,
      TextParam,
      IntegerParam,
      EnumsParam,
      CollectionParam,
      AttributeParam,
      AttributeListParam,
      AttributeNameParam,
      DataPreview,
    },
    props: {
      datasetGroup: {
        type: Object as PropType<DatasetGroupType>,
        required: true,
      },
      targetAttrs: {
        type: Array as PropType<DatasetAttrType[]>,
        required: true,
      },
      filter: {
        type: Array as PropType<FilterType>,
        required: true,
      },
      newAttrName: {
        type: String,
        required: false,
        default: null,
      },
    },
    emits: ['cancel', 'converted'],
    setup(props: Props, context: SetupContext) {
      const onCacnel = () => {
        context.emit('cancel')
      }

      const useConvert = () => {
        const state = reactive({
          converting: false,
          paramValues: {} as { [key: string]: any },
          showPreviewModal: false,
          previewData: null as any,
          previewAttrNames: null as any,
          errors: null as { [key: string]: string },
        })

        props.filter.params.forEach((param) => {
          if (
            param.type == 'input-attribute' &&
            props.targetAttrs.length === 1
          ) {
            // 入力列のデフォルト
            state.paramValues[param.name] = props.targetAttrs[0]
          } else if (
            param.type == 'input-attribute-list' &&
            props.targetAttrs.length > 0
          ) {
            state.paramValues[param.name] = [
              ...props.targetAttrs.map((attr) => attr.name),
            ]
          } else if (
            param.type == 'output-attribute' &&
            props.targetAttrs.length > 0
          ) {
            state.paramValues[param.name] = `${props.targetAttrs[0].name}`
          } else if (
            param.type == 'attribute' &&
            param.name == 'output_attr_new_index' &&
            props.targetAttrs.length > 0
          ) {
            // 出力位置のデフォルト
            state.paramValues[param.name] =
              props.targetAttrs[props.targetAttrs.length - 1]
          } else if (param.defaultValue != null) {
            state.paramValues[param.name] = unref(param.defaultValue)
          }
        })

        const { mutate: preview } = useConvertPreviewMutation({})

        const attributeIdParams = ['collection']

        const attributeIndexParams = ['attribute', 'input-attribute']

        const attributeListIndexParams = [
          'attribute-list',
          'input-attribute-list',
          'output-attribute-list',
        ]

        const convertJson = computed(() => {
          const params = {}
          props.filter.params.forEach((param) => {
            if (attributeIdParams.includes(param.type)) {
              params[param.name] = state.paramValues[param.name]?.id
            } else if (attributeIndexParams.includes(param.type)) {
              params[param.name] = state.paramValues[param.name]?.index
            } else if (attributeListIndexParams.includes(param.type)) {
              params[param.name] = state.paramValues[param.name]?.map(
                (value) => value.index
              )
            } else {
              params[param.name] = state.paramValues[param.name]
            }
          })

          return {
            datasetGroupId: props.datasetGroup.id,
            filterKey: props.filter.key,
            filterParams: JSON.stringify(params),
          }
        })

        const { mutate: convert } = useCreateConvertJobMutation({})

        const onConvert = async () => {
          if (state.converting == true) return
          state.converting = true
          state.errors = null
          try {
            await convert({
              input: {
                ...unref(convertJson),
              },
            })
            context.emit('converted', unref(convertJson))
          } catch (e) {
            if (e.graphQLErrors.length > 0) {
              state.errors = e.graphQLErrors[0]?.extensions
            } else {
              console.error(e)
            }
          } finally {
            state.converting = false
          }
        }

        const getTargetCollectionId = (param: ParamType) => {
          const targetCollectionName = param.arguments.collection_param_name
          if (targetCollectionName != null) {
            return state.paramValues[targetCollectionName]?.id
          } else {
            return props.datasetGroup?.id
          }
        }

        const selectedTargetCollection = (param: ParamType) => {
          const targetCollectionName = param.arguments.collection_param_name
          if (targetCollectionName != null) {
            return state.paramValues[targetCollectionName] != null
          } else {
            return props.datasetGroup?.id != null
          }
        }

        const onTogglePreviewModal = () => {
          if (state.previewData == null) {
            state.showPreviewModal = false
          } else {
            state.showPreviewModal = !state.showPreviewModal
          }
        }

        const visiblePreviewAll = computed(() => {
          return (
            state.previewData != null &&
            outputAttrParams.value.length > 0 &&
            ['left_join'].includes(props.filter.key) // 特別扱い
          )
        })

        const onPreview = async () => {
          if (state.converting) return
          state.converting = true
          state.errors = null
          state.previewData = null
          try {
            const result = await preview({
              input: {
                ...unref(convertJson),
              },
            })
            state.previewData = JSON.parse(
              result.data?.createConvertPreview?.datasetPreview?.result
            )
            state.previewAttrNames = state.previewData.shift()

            if (visiblePreviewAll.value === false) {
              state.showPreviewModal = true
            }
          } catch (e) {
            if (e.graphQLErrors.length > 0) {
              state.errors = e.graphQLErrors[0]?.extensions
            } else {
              console.error(e)
            }
          } finally {
            state.converting = false
          }
        }

        const datasetAttrNames = computed(() => {
          return props.datasetGroup.currentDataset.attrNames
        })

        const inputAttrParams = computed(() => {
          if (props.filter == null) return null
          return props.filter.params.filter(
            (param) =>
              param?.type === 'input-attribute' ||
              param?.type === 'input-attribute-list'
          )
        })

        const outputAttrParams = computed(() => {
          if (props.filter == null) return null
          return props.filter.params.filter(
            (param) =>
              param?.type === 'output-attribute' ||
              param?.type === 'output-attribute-list'
          )
        })

        const inputAttrs = computed(() => {
          if (props.filter == null) return []
          const paramValues = state.paramValues
          const attrNames = datasetAttrNames.value
          const names = []
          inputAttrParams.value.forEach((param) => {
            const value = paramValues[param.name]
            if (value == null) return
            if (param.type === 'input-attribute-list') {
              value
                .map((props) => props.index)
                .forEach((index) => {
                  names.push({
                    index: index,
                    name: attrNames[index],
                  })
                })
            } else {
              names.push({
                index: value.index,
                name: attrNames[value.index],
              })
            }
          })
          return names
        })

        const outputAttrs = computed(() => {
          const filter = props.filter
          const paramValues = state.paramValues
          if (filter == null) return []

          const names = []
          unref(
            outputAttrParams.value.map((param) => {
              const value = paramValues[param.name]
              if (value == null) return null

              if (param.type === 'output-attribute-list') {
                value
                  .map((props) => props.name)
                  .forEach((name) => {
                    names.push({
                      index: state.previewAttrNames.indexOf(name),
                      name: name,
                    })
                  })
              } else if (param.arguments.prefix === 'True') {
                const prefix = value
                state.previewAttrNames
                  .filter((name) => name.startsWith(prefix))
                  .forEach((name) =>
                    names.push({
                      index: state.previewAttrNames.indexOf(name),
                      name,
                    })
                  )
              } else {
                console.log(value)
                names.push({
                  index: state.previewAttrNames.indexOf(value),
                  name: value,
                })
              }
            })
          )
          return names
        })

        const canAttrPreview = computed(() => {
          if (props.filter == null) return false
          return unref(outputAttrParams).length > 0
        })

        return {
          ...toRefs(state),
          convertJson,
          onConvert,
          visiblePreviewAll,
          onPreview,
          onTogglePreviewModal,
          getTargetCollectionId,
          selectedTargetCollection,
          inputAttrParams,
          outputAttrParams,
          inputAttrs,
          outputAttrs,
          canAttrPreview,
        }
      }

      const useDatasetGroupData = () => {
        const state = reactive({
          originalHeaders: null as { key: string; value: string[] }[] | null,
          originalData: null as { key: string; value: string[] }[] | null,
        })
        const url = props.datasetGroup.currentDataset.dataFileUrl
        parse(url, {
          header: true,
          download: true,
          complete: function (results) {
            state.originalData = results.data
            state.originalHeaders = results.meta.fields
          },
        })

        return {
          ...toRefs(state),
        }
      }

      return {
        ...useConvert(),
        ...useDatasetGroupData(),
        onCacnel,
      }
    },
  })
</script>

<template>
  <div class="root">
    <div class="root--title">
      <h4>{{ filter.name }}</h4>
    </div>
    <div class="root--content">
      <div class="convert-panel">
        <span>{{ filter.description }}</span>
        <ScrollPanel style="width: 100%; height: calc(100vh - 480px)">
          <template v-if="filter">
            <h5 v-if="filter.helpText">{{ filter.helpText }}</h5>

            <template v-for="param in filter.params" :key="param.name">
              <h5 v-tooltip="param.description">
                {{ param.label }}
                <template v-if="param.required">*</template>
              </h5>

              <template v-if="param.type === 'string'">
                <StringParam
                  v-model:modelValue="paramValues[param.name]"
                  :param="param"
                />
              </template>
              <template v-else-if="param.type === 'string_list'">
                <StringListParam
                  v-model:modelValue="paramValues[param.name]"
                  :param="param"
                />
              </template>
              <template v-else-if="param.type === 'text'">
                <TextParam
                  v-model:modelValue="paramValues[param.name]"
                  :param="param"
                />
              </template>
              <template v-else-if="param.type === 'integer'">
                <IntegerParam
                  v-model:modelValue="paramValues[param.name]"
                  :param="param"
                />
              </template>
              <template v-else-if="param.type === 'enums'">
                <EnumsParam
                  v-model:modelValue="paramValues[param.name]"
                  :param="param"
                />
              </template>
              <template v-else-if="param.type === 'boolean'">
                <BooleanParam
                  v-model:modelValue="paramValues[param.name]"
                  :param="param"
                />
              </template>
              <template v-else-if="param.type === 'collection'">
                <CollectionParam
                  v-model:modelValue="paramValues[param.name]"
                  :param="param"
                  style="width: 80%"
                />
              </template>
              <template v-else-if="param.type === 'attribute'">
                <template v-if="selectedTargetCollection(param) != null">
                  <AttributeParam
                    :key="getTargetCollectionId(param)"
                    v-model:modelValue="paramValues[param.name]"
                    :param="param"
                    :targetCollectionId="getTargetCollectionId(param)"
                    style="width: 80%"
                  />
                </template>
              </template>
              <template v-else-if="param.type === 'attribute-list'">
                <template v-if="selectedTargetCollection(param) != null">
                  <AttributeListParam
                    v-model:modelValue="paramValues[param.name]"
                    :param="param"
                    :targetCollectionId="getTargetCollectionId(param)"
                  />
                </template>
              </template>
              <template v-else-if="param.type === 'input-attribute'">
                <template v-if="datasetGroup != null">
                  <AttributeParam
                    v-model:modelValue="paramValues[param.name]"
                    :param="param"
                    :targetCollectionId="datasetGroup.id"
                    style="width: 80%"
                  />
                </template>
              </template>
              <template v-else-if="param.type === 'input-attribute-list'">
                <template v-if="datasetGroup != null">
                  <AttributeListParam
                    v-model:modelValue="paramValues[param.name]"
                    :param="param"
                    :targetCollectionId="datasetGroup.id"
                    style="width: 80%"
                  />
                </template>
              </template>
              <template v-else-if="param.type === 'output-attribute'">
                <template v-if="datasetGroup != null">
                  <AttributeNameParam
                    :key="param.name"
                    v-model:modelValue="paramValues[param.name]"
                    :param="param"
                    :targetCollectionId="datasetGroup.id"
                    style="width: 80%"
                  />
                </template>
              </template>
              <template v-else-if="param.type === 'output-attribute-list'">
                <template v-if="datasetGroup != null">
                  <AttributeListParam
                    :key="param.name"
                    v-model:modelValue="paramValues[param.name]"
                    :param="param"
                    :targetCollectionId="datasetGroup.id"
                    style="width: 80%"
                  />
                </template>
              </template>
              <template v-else> unknown: ({{ param.type }}) </template>
              <div>
                <small v-if="param.helpText" class="p-info">{{
                  param.helpText
                }}</small>
                <template v-if="errors != null && errors[param.name] != null">
                  <small class="p-error">{{ errors[param.name][0] }}</small>
                </template>
              </div>
            </template>
          </template>
        </ScrollPanel>

        <div class="button-bar p-d-flex p-jc-between p-ai-center">
          <Button
            class="p-button-rounded p-button-sm"
            label="プレビュー"
            :disabled="converting"
            @click="onPreview()"
          />

          <template v-if="visiblePreviewAll">
            <Button
              icon="pi pi-external-link"
              iconPos="right"
              label="全体を表示"
              :disabled="converting"
              class="p-button-rounded p-button-text p-button-sm"
              @click="onTogglePreviewModal()"
            />
          </template>
        </div>

        <div>
          <template v-if="visiblePreviewAll">
            <DataTable
              :value="previewData"
              class="p-datatable-sm"
              responsiveLayout="scroll"
              :reorderableColumns="false"
              :rowHover="true"
              :resizableColumns="true"
              :scrollable="true"
              scrollHeight="180px"
              columnResizeMode="expand"
              dataKey="index"
            >
              <template v-for="(inputAttr, index) in inputAttrs" :key="index">
                <Column :header="inputAttr.name">
                  <template #body="{ data, index }">
                    {{ originalData[index][inputAttr.name] }}
                  </template>
                </Column>
              </template>
              <Column v-if="inputAttrs.length > 0" header="">
                <template #body>▶</template>
              </Column>
              <template v-for="(outputAttr, index) in outputAttrs" :key="index">
                <Column :header="outputAttr.name">
                  <template #body="{ data }">
                    {{ data[outputAttr.index] }}
                  </template>
                </Column>
              </template>
            </DataTable>
          </template>
        </div>
      </div>
    </div>

    <div class="root--button-bar button-bar">
      <Button
        class="p-button-rounded p-button-sm"
        label="キャンセル"
        :disabled="converting"
        @click="onCacnel"
      />
      <Button
        class="p-button-rounded p-button-sm"
        label="変換"
        :loading="converting"
        @click="onConvert"
      />
    </div>

    <Dialog
      v-model:visible="showPreviewModal"
      appendTo="body"
      :style="{ width: 'calc(100vw - 640px)', height: '80vh' }"
      :maximizable="true"
      :modal="false"
      position="left"
      header="プレビュー"
      :dismissableMask="true"
    >
      <template v-if="previewData != null">
        <DataPreview
          :arrayHeaders="previewAttrNames"
          :array="previewData"
          style="height: 100%"
          :rows="5"
        ></DataPreview>
      </template>
      <template v-else>
        <div style="height: 480px"></div>
      </template>
    </Dialog>
  </div>
</template>

<style lang="scss" scoped>
  .root {
    height: calc(100vh - 60px);
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    &--content {
      flex-grow: 1;
      overflow-y: auto;
    }
  }

  .convert-panel {
    //height: 200vh;
  }

  .button-bar {
    padding: 10px 0;
    button {
      margin-right: 10px;
    }
  }
</style>
