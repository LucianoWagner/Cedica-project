<template>
  <div class="home-container">
    <!-- Introducción -->
    <section class="intro">
      <h1>Bienvenidos a CEDICA</h1>
      <p>
        El Centro de Equitación para Personas con Discapacidad y Carenciadas, CEDICA, es una
        Asociación Civil sin Fines de Lucro fundada en 1994 en la ciudad de La Plata, Provincia de
        Buenos Aires, Argentina.
      </p>
      <p>
        CEDICA trabaja con la finalidad de <strong>igualar oportunidades</strong>, promoviendo la
        reinserción familiar, el logro de la escolaridad, la integración laboral y la mejora
        integral de la calidad de vida de los Jinetes y Amazonas (“J&A”) que forman parte de la
        institución.
      </p>
      <img src="../assets/banner.jpg" alt="Banner" class="banner-img" />
    </section>

    <!-- Actividades -->
    <section class="activities">
      <h2>Nuestras Actividades</h2>
      <div class="activity-cards">
        <div class="activity-card">
          <h3>Terapias y Actividades Asistidas con Caballos (TACAs)</h3>
          <p>
            Terapia integral que apunta a la recuperación de la persona en sus dimensiones
            biológica, psíquica y social. El caballo es nuestro principal recurso de trabajo.
          </p>
        </div>
        <div class="activity-card">
          <h3>Voluntariado</h3>
          <p>
            Cada año, numerosos estudiantes universitarios se suman como voluntarios para apoyar las
            actividades de la institución, acompañando a nuestros Jinetes y Amazonas.
          </p>
        </div>
        <div class="activity-card">
          <h3>Capacitación</h3>
          <p>
            Organizamos programas de formación en Terapias Asistidas con Caballos para profesionales
            y voluntarios interesados en especializarse en este campo.
          </p>
        </div>
      </div>
    </section>

    <!-- Equipo de Trabajo -->
    <section class="team">
      <h2>Equipo de Trabajo</h2>
      <p>
        Nuestro equipo está integrado por profesionales capacitados en TACAs, incluyendo Terapistas
        Ocupacionales, Psicólogos, Psicopedagogos, Psicomotricistas, Profesores de Educación Física
        y Equitación, Instructores de Volteo y Médico Veterinario. También contamos con personal
        ecuestre y nuestros caballos entrenados.
      </p>
      <div class="team-img"></div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
}
</script>

<style scoped>
/* General Container */
.home-container {
  padding: 20px;
  background-color: #f8f9fa;
  font-family: Arial, sans-serif;
}

/* Introducción */
.intro {
  text-align: center;
  margin-bottom: 40px;
}

.intro h1 {
  font-size: 2.5rem;
  color: #5bc0de; /* Celeste */
}

.intro p {
  font-size: 1.2rem;
  margin: 10px 0;
  color: #333;
  line-height: 1.6;
}

.banner-img {
  width: 100%;
  max-width: 200px; /* Limitar el tamaño máximo de la imagen */
  margin: 20px auto; /* Centrar la imagen horizontalmente */
  display: block; /* Asegurar que la imagen sea un bloque para centrarse */
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Actividades */
.activities {
  text-align: center;
  margin: 40px 0;
}

.activities h2 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
}

.activity-cards {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.activity-card {
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  width: 300px;
  padding: 20px;
  text-align: center;
}

.activity-card h3 {
  margin-top: 15px;
  color: #5bc0de;
}

.activity-card p {
  font-size: 1rem;
  color: #555;
  line-height: 1.5;
}

/* Equipo de Trabajo */
.team {
  margin: 40px 0;
  text-align: center;
}

.team h2 {
  font-size: 2rem;
  color: #333;
}

.team p {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 20px;
}

.team-img img {
  width: 100%;
  max-width: 600px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
