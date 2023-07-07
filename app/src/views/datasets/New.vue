<script lang="ts">
  import { defineComponent } from 'vue'
  import GlobalNav from '@/components/GlobalNav.vue'
  import DatasetNew from '@/components/datasets/New.vue'
  export default defineComponent({
    components: {
      GlobalNav,
      DatasetNew,
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
    <div class="p-d-flex p-jc-center">
      <DatasetNew style="width: 600px; margin: 40px" />
    </div>
  </div>
</template>
