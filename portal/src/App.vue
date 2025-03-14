<template>
  <div id="app">
    <header>
      <nav class="bg-white border-gray-200 px-4 lg:px-6 py-2.5 dark:bg-gray-800">
        <div class="flex items-center justify-between mx-auto max-w-screen-xl">
          <!-- Logo -->
          <a href="/portal/public" class="flex items-center">
            <img src="@/assets/banner.jpg" class="mr-3 h-6 sm:h-9" alt="Logo" />
          </a>

          <!-- Botón del menú hamburguesa para móviles -->
          <button
            @click="toggleMenu"
            type="button"
            class="inline-flex items-center p-2 ml-3 text-sm text-gray-500 rounded-lg lg:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
            aria-controls="navbar"
            aria-expanded="false"
          >
            <span class="sr-only">Abrir menú</span>
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16m-7 6h7"
              ></path>
            </svg>
          </button>

          <!-- Navbar Links -->
          <div
            :class="[
              'w-full lg:flex lg:justify-center lg:items-center',
              menuOpen ? 'block' : 'hidden',
            ]"
            id="navbar"
          >
            <ul class="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0">
              <li>
                <router-link
                  to="/"
                  class="block py-2 pr-4 pl-3 text-gray-700 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-primary-700 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent"
                >
                  Home
                </router-link>
              </li>
              <li>
                <router-link
                  to="/contacto"
                  class="block py-2 pr-4 pl-3 text-gray-700 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-primary-700 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent"
                >
                  Contacto
                </router-link>
              </li>
              <li>
                <router-link
                  to="/noticias"
                  class="block py-2 pr-4 pl-3 text-gray-700 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-primary-700 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent"
                >
                  Noticias
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      menuOpen: false, // Estado para controlar el menú hamburguesa
    }
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen
    },
  },
}
</script>

<style scoped>
/* Navbar general */
nav {
  background-color: #ffffff;
  color: #333333;
  padding: 10px 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Logo */
img {
  height: 40px;
}

/* Links del navbar */
nav ul {
  list-style-type: none;
  display: flex;
  flex-direction: column; /* Por defecto, columnas en móviles */
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
}

nav ul li {
  margin-bottom: 10px; /* Espaciado en móviles */
}

nav ul li a {
  text-decoration: none;
  color: #5bc0de;
  font-size: 18px;
  padding: 10px 15px;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

nav ul li a:hover,
nav ul li a.router-link-active {
  background-color: #5bc0de;
  color: white;
}

/* Layout en pantallas grandes */
@media (min-width: 1024px) {
  nav ul {
    flex-direction: row; /* Fila en pantallas grandes */
    gap: 30px;
  }

  nav ul li {
    margin-bottom: 0; /* Sin margen en pantallas grandes */
  }
}

/* Estilo del botón hamburguesa */
button {
  background: none;
  border: none;
  cursor: pointer;
}

/* Contenido principal */
main {
  padding: 20px;
}
</style>
