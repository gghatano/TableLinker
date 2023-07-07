<script lang="ts">
  import { defineComponent } from 'vue'
  import GlobalNav from '@/components/GlobalNav.vue'
  import DatasetDetail from '@/components/datasets/Detail.vue'
  export default defineComponent({
    components: {
      GlobalNav,
      DatasetDetail,
    },
    props: {
      id: {
        type: String,
        required: true,
      },
    },
  })
</script>

<template>
  <div>
    <GlobalNav />
    <DatasetDetail :datasetGroupId="id"></DatasetDetail>
  </div>
</template>
