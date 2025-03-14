<template>
  <div class="flex justify-center items-center min-h-screen bg-white-100">
    <div class="w-full max-w-lg bg-white rounded-lg shadow-lg">
      <div class="bg-blue-700 text-white text-center py-4 rounded-t-lg">
        <h2 class="text-lg font-bold">Formulario de Contacto</h2>
      </div>
      <div class="p-6">
        <form id="contact-form" @submit.prevent="submitForm">
          <!-- Nombre Completo -->
          <div class="mb-5">
            <label
              for="nombre"
              class="form-label block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >Nombre Completo</label
            >
            <input
              type="text"
              v-model="nombre"
              id="nombre"
              class="form-control shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"
              placeholder="Ingresa tu nombre"
              required
            />
          </div>

          <!-- Correo Electrónico -->
          <div class="mb-5">
            <label
              for="email"
              class="form-label block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >Correo Electrónico</label
            >
            <div class="relative">
              <div class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
                <svg
                  class="w-4 h-4 text-gray-500 dark:text-gray-400"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="currentColor"
                  viewBox="0 0 20 16"
                >
                  <path
                    d="m10.036 8.278 9.258-7.79A1.979 1.979 0 0 0 18 0H2A1.987 1.987 0 0 0 .641.541l9.395 7.737Z"
                  />
                  <path
                    d="M11.241 9.817c-.36.275-.801.425-1.255.427-.428 0-.845-.138-1.187-.395L0 2.6V14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2.5l-8.759 7.317Z"
                  />
                </svg>
              </div>
              <input
                type="email"
                v-model="email"
                id="email"
                class="form-control shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pl-10 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"
                placeholder="Ingresa tu correo"
                required
              />
            </div>
          </div>

          <!-- Mensaje -->
          <div class="mb-5">
            <label
              for="mensaje"
              class="form-label block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >Mensaje</label
            >
            <textarea
              v-model="mensaje"
              id="mensaje"
              class="form-control shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"
              placeholder="Escribe tu mensaje"
              rows="4"
              required
            ></textarea>
          </div>

          <!-- Botón Enviar -->
          <div class="flex justify-center">
            <button
              type="submit"
              class="btn btn-primary btn-lg g-recaptcha px-6 py-2 text-sm font-medium text-white bg-blue-700 rounded-lg shadow hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
              data-sitekey="6Le_JIIqAAAAAKOTL7kO2QPHixOO5QZnzWYCJU5U"
              data-callback="verifyCaptcha"
              data-action="submit"
            >
              Enviar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      nombre: '',
      email: '',
      mensaje: '',
      recaptchaSiteKey: '6Le_JIIqAAAAAKOTL7kO2QPHixOO5QZnzWYCJU5U', // Clave reCAPTCHA
    }
  },
  mounted() {
    // Verificar si reCAPTCHA se ha cargado
    const checkRecaptcha = setInterval(() => {
      if (window.grecaptcha) {
        console.log('entreeeeee')
        this.recaptchaLoaded = true
        clearInterval(checkRecaptcha)
      }
    }, 100)
  },
  methods: {
    submitForm() {
      if (!this.nombre.trim()) {
        alert('El nombre es obligatorio.')
        return
      }
      if (!this.email.trim()) {
        alert('El correo electrónico es obligatorio.')
        return
      }
      // Validación de formato de correo
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(this.email)) {
        alert('Por favor, ingresa un correo electrónico válido.')
        return
      }
      if (!this.mensaje.trim()) {
        alert('El mensaje es obligatorio.')
        return
      }

      // Si pasa todas las validaciones, ejecuta reCAPTCHA
      if (this.recaptchaLoaded) {
        console.log('Validaciones pasadas. Ejecutando reCAPTCHA...')
        try {
          grecaptcha
            .execute(this.recaptchaSiteKey, { action: 'submit' })
            .then((token) => {
              this.verifyCaptcha(token)
            })
            .catch((error) => {
              // Si grecaptcha arroja un error, manejarlo aquí
              console.error('Error al ejecutar reCAPTCHA:', error)
              alert(
                'Hubo un problema con la validación de reCAPTCHA. Por favor, inténtalo nuevamente.',
              )
            })
        } catch (error) {
          // Captura errores relacionados con un sitio clave inválido
          console.error('Error de configuración de reCAPTCHA:', error)
          alert(
            'Hubo un problema al configurar reCAPTCHA. Por favor, verifica la clave del sitio o inténtalo más tarde.',
          )
        }
      } else {
        alert('reCAPTCHA no se ha cargado correctamente. Inténtalo de nuevo.')
      }
    },

    verifyCaptcha(token) {
      this.handleSubmit(token)
    },

    async handleSubmit(token) {
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/messages/`,
          {
            full_name: this.nombre,
            email: this.email,
            description: this.mensaje,
            status: 'Pendiente',
            captcha: token,
          },
          {
            headers: { 'Content-Type': 'application/json' },
          },
        )
        alert(response.data.message) // Confirmación de éxito
        this.resetForm() // Resetea el formulario
      } catch (error) {
        if (error.response) {
          alert(error.response.data.error || 'Error al enviar el mensaje.')
        } else if (error.request) {
          alert('No se pudo contactar al servidor.')
        } else {
          alert('Error desconocido: ' + error.message)
        }
      }
    },

    resetForm() {
      this.nombre = ''
      this.email = ''
      this.mensaje = ''
    },
  },
}
</script>

<style scoped>
.shadow {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

input:focus,
textarea:focus {
  outline: none;
}
</style>
