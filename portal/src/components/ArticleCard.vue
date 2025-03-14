<template>
  <div
    class="block max-w-sm p-6 bg-white border border-gray-200 rounded-2xl shadow-lg transition-transform transform hover:scale-105 hover:shadow-xl dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
  >
    <!-- Título del artículo -->
    <h5 class="mb-2 text-3xl font-semibold text-gray-900 dark:text-white">
      {{ article.title }}
    </h5>
    <!-- Fecha de publicación -->
    <h6 class="mb-3 text-sm text-gray-500 dark:text-gray-400">
      {{ formatDate(article.published_at) }}
    </h6>
    <!-- Resumen del artículo -->
    <p class="font-normal text-lg text-gray-700 dark:text-gray-400">
      {{ article.summary }}
    </p>
    <!-- Botón "Read more" -->
    <button
      class="inline-flex items-center mt-4 px-5 py-3 text-base font-medium text-center text-white bg-gradient-to-r from-blue-500 to-blue-700 rounded-full hover:bg-gradient-to-r hover:from-blue-600 hover:to-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-gradient-to-r dark:from-blue-600 dark:to-blue-700 dark:hover:from-blue-700 dark:hover:to-blue-800 dark:focus:ring-blue-800"
      @click="showDetails"
    >
      Ver más
    </button>
  </div>
</template>

<script>
import { formatDate } from '@/filters/index.js'

export default {
  props: {
    article: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatDate,
    showDetails() {
      console.log('Emitido evento con artículo:', this.article)
      // Emitimos el artículo para abrir el modal en el componente padre
      this.$emit('open-modal', this.article)
    },
  },
}
</script>
