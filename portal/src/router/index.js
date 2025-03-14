import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ContactoView from '../views/ContactoView.vue'
import NoticiasView from '../views/ArticlesView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/contacto', name: 'contacto', component: ContactoView },
  { path: '/noticias', name: 'noticias', component: NoticiasView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
