<script lang="ts">
  import { defineComponent, PropType, SetupContext } from 'vue'
  import { ParamType } from '@/schema/schema'

  type Props = {
    param: ParamType
    modeleValue: string
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
    emits: ['input', 'update:modelValue'],
    setup(_props: Props, { emit }: SetupContext) {
      const onInput = (event: HTMLInputElement) => {
        const value = event.target.value
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
  <InputText :modeleValue="modeleValue" @input="onInput" />
</template>

<style lang="scss"></style>
