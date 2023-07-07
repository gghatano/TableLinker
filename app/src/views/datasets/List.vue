<script lang="ts">
  import { defineComponent } from 'vue'
  import DatasetList from '@/components/datasets/List.vue'
  import GlobalNav from '@/components/GlobalNav.vue'
  export default defineComponent({
    components: {
      GlobalNav,
      DatasetList,
    },
  })
</script>

<template>
  <div>
    <GlobalNav />
    <DatasetList />
  </div>
</template>
