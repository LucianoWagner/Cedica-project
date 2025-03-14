<template>
  <nav class="flex items-center justify-center mt-4">
    <ul class="inline-flex items-center space-x-2">
      <li>
        <button
          :disabled="pagination.page === 1"
          @click="changePage(pagination.page - 1)"
          class="px-3 py-1 border rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Anterior
        </button>
      </li>
      <li v-for="page in totalPages" :key="page">
        <button
          @click="changePage(page)"
          :class="{
            'bg-blue-500 text-white': page === pagination.page,
            'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700':
              page !== pagination.page,
          }"
          class="px-3 py-1 border rounded-md"
        >
          {{ page }}
        </button>
      </li>
      <li>
        <button
          :disabled="pagination.page === totalPages"
          @click="changePage(pagination.page + 1)"
          class="px-3 py-1 border rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Siguiente
        </button>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  props: {
    pagination: {
      type: Object,
      required: true,
    },
  },
  computed: {
    totalPages() {
      return Math.ceil(this.pagination.total / this.pagination.per_page)
    },
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.$emit('page-change', page)
      }
    },
  },
}
</script>
