<script lang="ts">
  import { parse } from 'papaparse'
  //  import Cookies from 'js-cookie'
  import { FilterMatchMode, FilterOperator } from 'primevue/api'
  import {
    defineComponent,
    reactive,
    computed,
    watch,
    toRefs,
    ref,
    unref,
  } from 'vue'

  export default defineComponent({
    props: {
      csv: {
        type: String,
        default: null,
      },
      url: {
        type: String,
        default: null,
      },
      array: {
        type: Array,
        default: null,
      },
      arrayHeaders: {
        type: Array,
        required: false,
        default: null,
      },
      file: {
        type: File,
        default: null,
      },
      encoding: {
        type: String,
        default: null,
      },
      attrs: {
        type: Array,
        required: false,
        default: null,
      },
      rows: {
        type: Number,
        required: false,
        default: 10,
      },
    },
    setup(props) {
      const state = reactive({
        loading: false,
        csvtext: null,
        csvheaders: null,
        csvdata: null,
        isEmpty: computed(() => state.csvdata === null),
        csvViewHeaders: [] as string[],
        filters: null,
      })

      async function loadCsv() {
        state.loading = true
        const csv = props.csv

        parse(csv, {
          header: true,
          complete: function (results) {
            analyzeCSV(results.data, results.meta.fields)
            state.loading = false
          },
        })
      }

      async function loadUrl() {
        state.loading = true
        const url = props.url

        parse(url, {
          header: true,
          download: true,
          complete: function (results) {
            analyzeCSV(results.data, results.meta.fields)
            state.loading = false
          },
        })
      }

      function loadFile() {
        if (props.file != null) return
        const file = props.file
        parse(file, {
          header: true,
          error: function () {
            state.loading = false
          },
          complete: function (results) {
            analyzeCSV(results.data, results.meta.fields)
          },
        })
      }

      function loadArray() {
        const array = props.array
        const arrayHeaders =
          props.arrayHeaders == null ? array.shift() : props.arrayHeaders
        const data = array.map((row) => {
          const obj = {}
          for (let i = 0; i < arrayHeaders.length; i++) {
            const header = arrayHeaders[i]
            const value = row[i]
            obj[header] = value
          }
          return obj
        })
        analyzeCSV(data, arrayHeaders)
      }

      const clearFilter = () => {
        state.filters = {
          global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        }
        state.csvViewHeaders.forEach((header) => {
          state.filters[header] = {
            operator: FilterOperator.AND,
            value: null,
            constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }],
          }
        })
      }

      const analyzeCSV = function (csvArray, csvHeaders) {
        if (csvArray != null) {
          state.csvheaders = csvHeaders
          state.csvdata = csvArray
          state.csvViewHeaders = state.csvheaders
          clearFilter()
        }
      }

      watch(() => props.file, loadFile)
      watch(() => props.url, loadUrl)
      watch(() => props.csv, loadCsv)
      watch(() => props.encoding, loadFile)

      if (props.csv != null) {
        loadCsv()
      } else if (props.file != null) {
        loadFile()
      } else if (props.url != null) {
        loadUrl()
      } else if (props.array != null) {
        loadArray()
      }

      const matchModeOptions = ref([
        { label: '部分一致', value: FilterMatchMode.CONTAINS },
        { label: '完全一致', value: FilterMatchMode.EQUALS },
        { label: '前方一致', value: FilterMatchMode.STARTS_WITH },
        { label: '後方一致', value: FilterMatchMode.ENDS_WITH },
        //{ label: '以下', value: FilterMatchMode.LT },
        //{ label: '以上', value: FilterMatchMode.GT },
      ])

      const op = ref()
      function onToggleField(event) {
        unref(op).toggle(event)
      }

      return {
        ...toRefs(state),
        onToggleField,
        op,
        matchModeOptions,
        clearFilter,
      }
    },
  })
</script>

<template>
  <div class="data-preview">
    <div :class="{ 'p-sr-only': !loading }">
      <ProgressBar mode="indeterminate" style="height: 0.5em" />
    </div>
    <DataTable
      v-model:filters="filters"
      class="data-preview__table"
      :value="csvdata"
      dataKey="index"
      :rowHover="true"
      filterDisplay="menu"
      :paginator="true"
      :globalFilterFields="csvheaders"
      :rows="rows"
      paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
      :rowsPerPageOptions="[5, 10, 25, 50, 100]"
      currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
      responsiveLayout="scroll"
      :resizableColumns="true"
      columnResizeMode="expand"
      :scrollable="true"
      scrollHeight="flex"
      :removableSort="true"
    >
      <template #header>
        <div class="p-d-flex p-jc-between p-ai-center">
          <div class="p-d-flex p-jc-start p-ai-center">
            <template v-if="filters != null">
              <div class="p-input-icon-right">
                <InputText
                  v-model="filters['global'].value"
                  type="text"
                  placeholder="キーワード"
                  class="p-inputtext-sm"
                />
                <i class="pi pi-search" />
              </div>
              <Button
                label="クリア"
                icon="pi pi-times"
                class="p-button-success p-button-text p-button-sm"
                @click="clearFilter"
              ></Button>
            </template>
          </div>
          <div>
            <Button
              type="button"
              icon="pi pi-search"
              label="表示項目"
              class="p-button-secondary p-button-text p-button-sm"
              @click="onToggleField"
            />
            <!-- <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText placeholder="Keyword Search" />
            </span> -->
          </div>
        </div>
      </template>
      <template #empty> No Data </template>
      <template v-for="(header, index) in csvViewHeaders" :key="index">
        <Column
          :field="header"
          :header="header"
          sortable
          style="min-width: 8rem"
          :filterMatchModeOptions="matchModeOptions"
        >
          <template #body="{ data }">
            {{ data[header] }}
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <InputText
              v-model="filterModel.value"
              type="text"
              class="p-column-filter"
              :placeholder="`Search by ${header}`"
              @input="filterCallback()"
            />
          </template>
        </Column>
      </template>
    </DataTable>

    <OverlayPanel
      id="overlay_panel"
      ref="op"
      appendTo="body"
      style="width: 450px"
      :breakpoints="{ '960px': '75vw' }"
    >
      <DataTable
        v-model:selection="csvViewHeaders"
        :value="csvheaders"
        selectionMode="multiple"
        responsiveLayout="scroll"
        :metaKeySelection="false"
        scrollable
        scrollHeight="300px"
        :virtualScrollerOptions="{ itemSize: 10 }"
      >
        <Column field="name" header="名前" style="width: 100%">
          <template #body="{ data }">
            {{ data }}
          </template>
        </Column>
      </DataTable>
    </OverlayPanel>
  </div>
</template>

<style lang="scss" scoped>
  .data-preview {
    height: calc(100vh - 340px);
  }
</style>
