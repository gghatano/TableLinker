<script lang="ts">
  import {
    defineComponent,
    reactive,
    toRefs,
    watch,
    PropType,
    unref,
    computed,
  } from 'vue'
  import { ParamType } from '@/schema/schema'
  import { useDatasetGroupsQuery } from '@/modules/graphql'
  import { useResult } from '@vue/apollo-composable'

  type Props = {
    param: ParamType
    modeleValue: number
  }

  export default defineComponent({
    props: {
      param: {
        type: Object as PropType<ParamType>,
        required: true,
      },
      modeleValue: {
        type: String,
        required: false,
        default: (params: Props) => {
          return params.param.defaultValue
        },
      },
    },
    emits: ['change', 'update:modelValue'],
    setup(props: Props, { emit }) {
      const state = reactive({
        value: props.modeleValue,
      })

      watch(
        () => props.modeleValue,
        () => {
          state.value = props.modeleValue
        }
      )

      const onChange = () => {
        emit('update:modelValue', state.value)
        emit('change', state.value)
      }

      const queryArguments = reactive({
        keyword: null as string | null,
        page: 0,
        pageSize: 20,
        published: false,
      })

      const { result, loading, fetchMore } =
        useDatasetGroupsQuery(queryArguments)

      const datasetGroupResult = useResult(result)

      const datasetGroups = computed(
        () => unref(datasetGroupResult)?.datasetGroups
      )
      const itemSize = computed(() => unref(datasetGroupResult)?.totalRecords)

      const onLazyLoad = async (event) => {
        const { first } = event
        const page = Math.floor(first / queryArguments.pageSize)
        await fetchMore({
          variables: {
            page,
          },
        })
      }

      return {
        ...toRefs(state),
        datasetGroups,
        itemSize,
        loading,
        onChange,
        onLazyLoad,
        ...toRefs(queryArguments),
      }
    },
  })
</script>

<template>
  <Dropdown
    v-model:modelValue="value"
    :options="datasetGroups"
    optionLabel="name"
    opionValue="id"
    :virtualScrollerOptions="{
      lazy: true,
      onLazyLoad: onLazyLoad,
      itemSize: itemSize,
      showLoader: true,
      loading: loading,
      delay: 250,
    }"
    :loading="loading"
    @change="onChange"
  >
    <template #header>
      <div style="padding: 10px; background-color: #eee">
        <InputText v-model:modelValue="keyword" />
      </div>
    </template>
  </Dropdown>
</template>

<style scoped lang="scss"></style>
