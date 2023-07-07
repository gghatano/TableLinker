<script lang="ts">
  import { defineComponent, provide } from 'vue'
  import { useSession, UseSessionKey } from '@/modules/session'

  export default defineComponent({
    setup() {
      provide(UseSessionKey, useSession())
      return {}
    },
  })
</script>

<template>
  <router-view></router-view>
</template>

<style>
  body {
    background-color: #f6f6f6;
    margin: 0;
  }
</style>
