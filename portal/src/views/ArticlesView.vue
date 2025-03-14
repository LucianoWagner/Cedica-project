<template>
  <div class="container mt-5">
    <h1 class="text-2xl font-bold">Actividades y Noticias</h1>

    <div v-if="isLoading" class="text-center">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="!isLoading && !error" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <ArticleCard
        v-for="article in articles"
        :key="article.title"
        :article="article"
        @open-modal="openModal"
      />
    </div>

    <Pagination :pagination="pagination" @page-change="fetchArticles" />

    <!-- Modal -->
    <div
      id="default-modal"
      v-if="selectedArticle"
      :class="selectedArticle ? 'flex' : 'hidden'"
      tabindex="-1"
      aria-hidden="true"
      class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full bg-opacity-60 bg-gray-900 backdrop-blur-lg"
    >
      <div class="relative p-6 w-full max-w-4xl max-h-full">
        <!-- Modal content -->
        <div
          class="relative bg-white rounded-xl shadow-xl dark:bg-gray-800 transition-all duration-300 ease-in-out"
        >
          <!-- Modal header -->
          <div
            class="flex items-center justify-between p-6 border-b rounded-t dark:border-gray-600"
          >
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ selectedArticle.title }}
            </h3>
          </div>

          <!-- Modal body with scrollable content -->
          <div class="modal-body-scroll p-6 space-y-6">
            <div class="space-y-6">
              <!-- Título del contenido -->
              <h4 class="text-lg font-semibold text-gray-900 border-b-2 pb-3">
                Contenido del artículo
              </h4>

              <!-- Contenido del artículo -->
              <p class="text-base leading-relaxed text-gray-700 dark:text-gray-300">
                {{ selectedArticle.content }}
              </p>
            </div>
          </div>

          <!-- Modal footer con botón de cerrar en la esquina -->
          <div class="flex justify-between items-center p-6 border-t border-gray-600 rounded-b">
            <!-- Publicado por en la izquierda -->
            <div class="text-sm text-gray-500">
              <strong>Publicado por:</strong> {{ selectedArticle.author }} el
              <strong>{{ formatDate(selectedArticle.published_at) }}</strong>
            </div>

            <!-- Botón de cerrar a la derecha -->
            <button
              data-modal-hide="default-modal"
              type="button"
              class="py-2.5 px-5 text-sm font-medium text-white focus:outline-none bg-blue-600 rounded-lg border border-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-700 dark:bg-blue-800 dark:text-gray-400 dark:border-blue-600 dark:hover:bg-blue-700 dark:hover:text-white"
              @click="closeModal"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import ArticleCard from '@/components/ArticleCard.vue'
import Pagination from '@/components/Pagination.vue'
import { formatDate } from '@/filters/index.js'

export default {
  components: { ArticleCard, Pagination },
  data() {
    return {
      selectedArticle: null,
    }
  },
  computed: {
    ...mapGetters(['articles', 'pagination', 'isLoading', 'error']),
  },
  methods: {
    formatDate,
    ...mapActions(['fetchArticles']),
    openModal(article) {
      console.log('Modal abierto con artículo:', article)
      this.selectedArticle = article
    },
    closeModal() {
      this.selectedArticle = null
    },
  },
  created() {
    this.fetchArticles()
  },
}
</script>

<style scoped>
/* Estilo para permitir el scroll horizontal en el cuerpo del modal */
.modal-body-scroll {
  max-height: 70vh; /* Limita la altura a un 70% de la ventana */
  overflow-y: auto; /* Agrega el scroll vertical cuando sea necesario */
  scroll-behavior: smooth; /* Desplazamiento suave */
  padding-right: 10px; /* Evitar que el contenido se mueva fuera de la vista */
}

/* Fondo del modal más oscuro con desenfoque */
#default-modal {
  background-color: rgba(0, 0, 0, 0.6); /* Fondo con transparencia para el modal */
  backdrop-filter: blur(10px); /* Desenfoque de fondo */
}

/* Bordes redondeados y sombra más moderna */
.relative {
  border-radius: 16px; /* Bordes más suaves */
  overflow: hidden; /* Asegura que el contenido no sobresalga */
}

/* Estilo para separar el título y el contenido */
.space-y-6 {
  margin-bottom: 24px;
}

/* Mejorar la apariencia del título en el modal */
h4 {
  font-size: 1.125rem; /* Aumentar tamaño de fuente */
  font-weight: 600; /* Poner en negrita */
  color: #333;
  margin-bottom: 12px; /* Separación entre título y contenido */
  border-bottom: 2px solid #ddd; /* Línea debajo del título */
  padding-bottom: 10px; /* Separar un poco más del contenido */
}

/* Mejorar la apariencia del contenido */
p {
  font-size: 1rem;
  line-height: 1.75rem;
  color: #444;
}

/* El botón de cerrar está alineado a la derecha en el pie del modal */
button {
  position: relative;
  bottom: 0;
}

/* Para las pequeñas pantallas */
@media (max-width: 768px) {
  .modal-body-scroll {
    max-height: 80vh; /* En pantallas pequeñas, el modal se hace un poco más alto */
  }
}
</style>
