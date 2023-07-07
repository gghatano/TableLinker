<script lang="ts">
  import { defineComponent } from 'vue'
  import GlobalNav from '@/components/GlobalNav.vue'
  import DatasetList from '@/components/user/DatasetList.vue'
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
