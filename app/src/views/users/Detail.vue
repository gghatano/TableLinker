<script lang="ts">
  import { defineComponent } from 'vue'
  import GlobalNav from '@/components/GlobalNav.vue'
  import UserDetail from '@/components/user/Detail.vue'
  export default defineComponent({
    components: {
      GlobalNav,
      UserDetail,
    },
  })
</script>

<template>
  <div>
    <GlobalNav />
    <div class="p-d-flex p-jc-center">
      <UserDetail style="width: 600px; margin: 40px" />
    </div>
  </div>
</template>
