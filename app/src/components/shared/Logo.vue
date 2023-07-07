<script lang="ts">
  import { defineComponent } from 'vue'
  export default defineComponent({
    props: {
      width: {
        type: String,
        default: '180px',
      },
    },
  })
</script>

<template>
  <img src="@/assets/logo.png" :style="{ width: width }" />
</template>

<style scoped></style>
