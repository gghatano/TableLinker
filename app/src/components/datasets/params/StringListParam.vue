<script lang="ts">
  import { defineComponent, PropType, watch, toRefs, reactive } from 'vue'
  import { ParamType } from '@/schema/schema'

  type Props = {
    param: ParamType
    modeleValue: string[]
  }

  export default defineComponent({
    props: {
      param: {
        type: Object as PropType<ParamType>,
        required: true,
      },
      modeleValue: {
        type: Array as PropType<string[]>,
        required: false,
        default: (params: Props) => {
          return params.param.defaultValue || []
        },
      },
    },
    emits: ['input', 'update:modelValue'],
    setup(props, { emit }) {
      const state = reactive({
        value: props.modeleValue == null ? [] : props.modeleValue.join('\n'),
      })

      watch(
        () => {
          return props.modeleValue
        },
        () => {
          state.value =
            props.modeleValue == null ? [] : props.modeleValue.join('\n')
        }
      )

      const onInput = (event: any) => {
        const value = event.target.value.split('\n')
        emit('update:modelValue', value)
        emit('input', value)
      }

      onInput({ target: { value: state.value } })

      return {
        ...toRefs(state),
        onInput,
      }
    },
  })
</script>

<template>
  <Textarea
    v-model:modeleValue="value"
    :autoResize="true"
    rows="5"
    @input="onInput"
  />
</template>

<style lang="scss"></style>
