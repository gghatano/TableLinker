<script lang="ts">
  import { defineComponent } from 'vue'
  import GlobalNav from '@/components/GlobalNav.vue'
  import DatasetEdit from '@/components/datasets/Edit.vue'

  export default defineComponent({
    components: {
      GlobalNav,
      DatasetEdit,
    },
    props: {
      id: {
        type: String,
        required: true,
      },
      targetDatasetGroupId: {
        type: String,
        required: false,
        default: null,
      },
      targetDatasetTemplateId: {
        type: String,
        required: false,
        default: null,
      },
    },
  })
</script>

<template>
  <div>
    <GlobalNav />
    <DatasetEdit
      :datasetGroupId="id"
      :targetDatasetGroupId="targetDatasetGroupId"
      :targetDatasetTemplateId="targetDatasetTemplateId"
    ></DatasetEdit>
  </div>
</template>
