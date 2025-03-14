import axios from 'axios'

const articlesStore = {
  state: {
    articles: [],
    pagination: {
      page: 1,
      per_page: 10,
      total: 0,
    },
    isLoading: false,
    error: null,
  },
  mutations: {
    SET_ARTICLES(state, articles) {
      state.articles = articles
    },
    SET_PAGINATION(state, pagination) {
      state.pagination = pagination
    },
    SET_LOADING(state, isLoading) {
      state.isLoading = isLoading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
  },
  actions: {
    async fetchArticles({ commit }, page = 1) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)

      try {
        console.log(import.meta.env.VITE_API_BASE_URL)
        console.log('holaaaaaa')
        const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/articles/`, {
          params: { page },
        })
        commit('SET_ARTICLES', response.data.data)
        commit('SET_PAGINATION', {
          page: response.data.page,
          per_page: response.data.per_page,
          total: response.data.total,
        })
      } catch (error) {
        commit('SET_ERROR', 'No se pudieron cargar los artículos.')
      } finally {
        commit('SET_LOADING', false)
      }
    },
  },
  getters: {
    articles: (state) => state.articles,
    pagination: (state) => state.pagination,
    isLoading: (state) => state.isLoading,
    error: (state) => state.error,
  },
}

export default articlesStore
