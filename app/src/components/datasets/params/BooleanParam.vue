<script lang="ts">
  import { defineComponent, PropType } from 'vue'
  import { ParamType } from '@/schema/schema'

  type Props = {
    param: ParamType
    modeleValue: boolean
  }

  export default defineComponent({
    props: {
      param: {
        type: Object as PropType<ParamType>,
        required: true,
      },
      modeleValue: {
        type: Boolean,
        required: false,
        default: (params: Props) => {
          return params.param.defaultValue === 'true' ? true : false
        },
      },
    },
    emits: ['input', 'update:modelValue'],
    setup(props, { emit }) {
      const onInput = (value: boolean) => {
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
  <InputSwitch :modeleValue="modeleValue" @input="onInput" />
</template>

<style lang="scss"></style>
