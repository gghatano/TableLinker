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
  import { ParamType, DatasetGroupQuery } from '@/schema/schema'
  import { useDatasetGroupQuery } from '@/modules/graphql'
  import { useResult } from '@vue/apollo-composable'

  type Props = {
    param: ParamType
    modeleValue: string
    targetCollectionId: string
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
      targetCollectionId: {
        type: String,
        required: true,
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
        console.log('onChange', state.value)
        emit('update:modelValue', state.value)
        emit('change', state.value)
      }

      const onInput = () => {
        emit('update:modelValue', state.value)
        emit('change', state.value)
      }

      const { result, loading } = useDatasetGroupQuery({
        id: props.targetCollectionId,
      })

      const datasetGroup = useResult<DatasetGroupQuery, 'datasetGroup'>(result)
      const attrs = computed(() => unref(datasetGroup)?.currentDataset?.attrs)

      return {
        ...toRefs(state),
        attrs,
        loading,
        onChange,
        onInput,
      }
    },
  })
</script>

<template>
  <Dropdown
    v-model:modelValue="value"
    :options="attrs"
    optionLabel="name"
    optionValue="name"
    :loading="loading"
    :editable="true"
    @input="onInput"
    @change="onChange"
  >
  </Dropdown>
</template>

<style scoped lang="scss"></style>
