// src/stores/index.js
import { createStore } from 'vuex'
import articlesStore from './Articles.js'

export default createStore({
  modules: {
    articlesStore,
  },
})
