<script lang="ts">
  import { defineComponent, reactive, toRefs, watch, PropType } from 'vue'
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
        type: Number,
        required: false,
        default: (params: Props) => {
          return params.param.defaultValue
        },
      },
    },
    emits: ['input', 'update:modelValue'],
    setup(_, { emit }) {
      const onInput = (event: HTMLInputElement) => {
        const value = event.value
        emit('update:modelValue', value)
        emit('input', value)
      }

      return {
        onInput,
      }
    },
  })
</script>

<template>
  <InputNumber :modelValue="modelValue" @input="onInput" />
</template>

<style scoped lang="scss"></style>
