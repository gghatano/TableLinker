<script lang="ts">
  import {
    defineComponent,
    reactive,
    toRefs,
    watch,
    PropType,
    computed,
  } from 'vue'
  import { ParamType } from '@/schema/schema'

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

      const enums = computed(() => JSON.parse(props.param.arguments.enums))

      return {
        ...toRefs(state),
        enums,
        onChange,
      }
    },
  })
</script>

<template>
  <Dropdown
    v-model:modelValue="value"
    :options="enums"
    optionLabel="label"
    optionValue="value"
    @change="onChange"
  >
  </Dropdown>
</template>

<style scoped lang="scss"></style>
