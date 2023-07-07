<script lang="ts">
  import { computed, defineComponent, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useGetSession } from '@/modules/session'

  import Logo from './shared/Logo.vue'
  export default defineComponent({
    components: {
      Logo,
    },
    setup() {
      const router = useRouter()
      const menu = ref()

      const { currentUser } = useGetSession()
      const userName = computed(() => currentUser.value?.name)

      const toggleMenu = (event: Event) => {
        menu.value.toggle(event)
      }

      const globalMenuItems = [
        {
          label: '検索',
          icon: 'pi pi-fw pi-search',
          to: '/datasets',
        },
      ]

      const userMenuItems = [
        {
          label: 'ユーザ情報',
          icon: 'pi pi-fw pi-user',
          to: '/user',
        },
        {
          label: 'アップロード一覧',
          icon: 'pi pi-fw pi-upload',
          to: '/user/datasets',
        },
        {
          separator: true,
        },
        {
          label: 'ログアウト',
          icon: 'pi pi-fw pi-power-off',
          to: '/logout',
        },
      ]

      const onUpload = () => {
        router.push({ name: 'DatasetNew' })
      }

      return {
        globalMenuItems,
        userMenuItems,
        onUpload,
        toggleMenu,
        userName,
        menu,
      }
    },
  })
</script>

<template>
  <Menubar :model="globalMenuItems">
    <template #start>
      <router-link :to="{ name: 'Home' }">
        <Logo width="160px" style="margin: 0 10px" />
      </router-link>
    </template>
    <template #end>
      <div class="p-d-inline-flex p-flex-column p-flex-md-row">
        <Button
          type="button"
          class="p-button-link p-mr-2"
          icon="pi pi-angle-down"
          iconPos="right"
          :label="userName"
          @click="toggleMenu"
        />
        <Button
          label="アップロード"
          icon="pi pi-upload"
          iconPos="left"
          class="p-button-rounded p-button-sm"
          @click="onUpload"
        />
      </div>
      <Menu ref="menu" :model="userMenuItems" :popup="true" />
    </template>
  </Menubar>
</template>

<style lang="scss" scoped></style>
