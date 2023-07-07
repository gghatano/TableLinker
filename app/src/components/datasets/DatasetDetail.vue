<script lang="ts">
  import { defineComponent, unref, computed, reactive, toRefs } from 'vue'
  import { useGetDatasetQuery } from '@/modules/graphql'
  import { useResult } from '@vue/apollo-composable'

  type Props = {
    datasetId: string
  }

  export default defineComponent({
    props: {
      datasetId: {
        type: String,
        required: true,
      },
    },
    setup(props: Props) {
      const state = reactive({
        visibleSearch: false,
      })

      const { result, loading } = useGetDatasetQuery({
        id: props.datasetId,
      })

      const dataset = useResult(result)
      const attrs = computed(() => unref(dataset)?.attrs)

      const isOwner = computed(() => true) // TODO

      return {
        ...toRefs(state),
        dataset,
        attrs,
        loading,
        isOwner,
      }
    },
  })
</script>

<template>
  <div v-if="dataset != null">
    <div>
      <h3>基本情報</h3>
      <div class="desrcriptions">
        <div class="desrcription-item">
          <div class="desrcription-item--label">データ件数</div>
          <div
            class="desrcription-item--value desrcription-item--value__number"
          >
            {{ dataset.numRecords }} 件
          </div>
        </div>
        <div class="desrcription-item">
          <div class="desrcription-item--label">データサイズ</div>
          <div
            class="desrcription-item--value desrcription-item--value__number"
          >
            <span>{{ dataset.fileSize }} byte</span>
          </div>
        </div>
      </div>
    </div>
    <div>
      <h3>カラム情報</h3>
      <DataTable
        :value="attrs"
        dataKey="id"
        :rowHover="true"
        :loading="loading"
        :resizableColumns="true"
        columnResizeMode="expand"
        responsiveLayout="scroll"
      >
        <Column field="index" header="#">
          <template #body="{ data }">
            {{ data.index + 1 }}
          </template>
        </Column>
        <Column field="name" header="名前">
          <template #body="{ data }">
            {{ data.name }}
          </template>
        </Column>
        <Column field="name" header="意味型">
          <template #body="{ data }">
            {{ data.attrTypeName }}
          </template>
        </Column>
        <Column field="name" header="データ型">
          <template #body="{ data }">
            {{ data.dataTypeName }}
          </template>
        </Column>
        <Column field="name" header="サンプル値">
          <template #body="{ data }">
            <template v-for="sampleValue in data.sampleValues">
              {{ sampleValue }},
            </template>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .content {
    padding: 30px;
  }

  .edit-button {
    position: absolute;
    right: 40px;
    z-index: 1000;
    top: 222px;
  }

  .desrcriptions {
    display: flex;
    flex-direction: row;
    margin-bottom: 30px;

    .desrcription-item {
      display: flex;
      flex-direction: row;
      margin-bottom: 30px;
      border: #dbdbdb 1px solid;

      &--label {
        background-color: #dbdbdb;
        padding: 8px;
        width: 180px;
      }

      &--value {
        min-width: 180px;
        padding: 5px;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        &__number {
          justify-content: flex-end;
        }
        //text-align: right;
      }
    }
  }
</style>
