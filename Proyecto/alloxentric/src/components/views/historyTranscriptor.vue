<template>
  <v-container class="centered-container">
    <v-card class="custom-card">
      <v-card-title class="custom-title">
        <h1>Historial</h1>
      </v-card-title>

      <v-list-item lines="two" :prepend-avatar="require('@/assets/icon-account.png')" :title="fullName"
        class="avatar-item"></v-list-item>

      <v-card class="contenedor">
        <v-layout permanent density="compact">
          <v-navigation-drawer permanent>
            <v-list density="compact" nav>
              <v-list-item prepend-icon="mdi-view-dashboard" title="Mi Cuenta" value="home"
                to="/miCuenta"></v-list-item>
              <v-list-item prepend-icon="mdi-forum" title="Historial" value="about"
                to="/historyTranscriptor"></v-list-item>
              <v-list-item prepend-icon="mdi mdi-logout" id="authButton" @click="handleAuthAction">{{
                isAuthenticated ? 'Cerrar Sesion' : '' }}</v-list-item>
            </v-list>
          </v-navigation-drawer>

          <v-main>
            <v-card flat>
              <v-container class="filtros">
                <v-container class="search">
                  <v-text-field id="search" v-model="search" label="Search" prepend-inner-icon="mdi-magnify"
                    variant="outlined" hide-details single-line></v-text-field>
                </v-container>
                <v-container class="filtroFecha">
                  <v-select v-model="selectedYear" :items="years" label="Año" outlined></v-select>
                  <v-select v-model="selectedMonth" :items="months" label="Mes" outlined></v-select>
                </v-container>
              </v-container>
              <v-data-table :headers="headers" :items="filteredDesserts" :search="search"></v-data-table>
            </v-card>
          </v-main>
        </v-layout>
      </v-card>
    </v-card>
  </v-container>
</template>


<script>
import keycloak from "@/keycloak"; // Importa tu instancia de Keycloak

export default {
  data() {
    const currentYear = new Date().getFullYear();
    const startYear = 2023;  // Puedes cambiarlo al año en el que comienzas a almacenar datos

    const years = [{ title: 'Todos los años', value: null }];
    for (let year = startYear; year <= currentYear; year++) {
      years.push({ title: year.toString(), value: year });
    }

    return {
      fullName: '',
      search: '',
      selectedYear: null,
      selectedMonth: null,
      headers: [
        {
          align: 'start',
          key: 'data_transcrito',
          sortable: false,
          title: 'Mensaje Transcrito',
        },
        {
          align: 'start',
          key: 'fecha',
          sortable: false,
          title: 'Fecha/Hora',
        },
      ],

      desserts: [
        {
          data_transcrito: 'Hola, oye, no voy a poder llegar a la reunión a las 10. ¿Podemos moverla para las 11? Avísame si te sirve, porfa.',
          fecha: '2024-09-02',
        },
        {
          data_transcrito: 'Ah, me olvidé de decirte que la cena es mañana a las 8 en casa de Juan. No te preocupes por llevar nada, ya está todo listo.',
          fecha: '2024-09-03',
        },
        {
          data_transcrito: 'Hey, ¿puedes comprar leche cuando vengas? Se me olvidó cuando fui al súper. Gracias, nos vemos en un rato.',
          fecha: '2024-09-05',
        },
        {
          data_transcrito: 'Hola, Juan, acabo de ver el correo. Estoy revisando el documento que me mandaste, te envío los comentarios en una hora.',
          fecha: '2024-09-08',
        },
        {
          data_transcrito: 'Ah, me olvidé de decirte que el pato arrugó de nuevo y no va a entrar a jugar Cs, calladito champiñon.',
          fecha: '2024-09-09',
        },
        {
          data_transcrito: 'Necesito que me envíes el reporte antes de las 5 pm. Es urgente.',
          fecha: '2023-08-15',
        },
        {
          data_transcrito: 'Recuerda que la reunión de equipo es el viernes a las 10 am.',
          fecha: '2023-07-12',
        },
        {
          data_transcrito: 'El proyecto ha sido aprobado por el cliente. ¡Buen trabajo!',
          fecha: '2023-06-22',
        },
        {
          data_transcrito: '¿Podrías revisar el documento adjunto y darme tu feedback?',
          fecha: '2023-05-30',
        },
        {
          data_transcrito: 'El servidor estará en mantenimiento el próximo lunes de 2 am a 4 am.',
          fecha: '2023-04-17',
        },
        {
          data_transcrito: 'Hola, el paquete ha sido enviado y debería llegar el jueves.',
          fecha: '2022-11-03',
        },
        {
          data_transcrito: 'Recuerda que tienes una cita con el dentista el próximo miércoles.',
          fecha: '2022-10-20',
        },
        {
          data_transcrito: 'El evento se ha reprogramado para el próximo mes debido a la situación actual.',
          fecha: '2022-09-15',
        },
        {
          data_transcrito: 'Te envié la factura por correo. Por favor, confírmame si la recibiste.',
          fecha: '2022-08-09',
        },
        {
          data_transcrito: 'La presentación del proyecto es mañana a las 9 am. ¡No faltes!',
          fecha: '2022-07-05',
        },
        {
          data_transcrito: 'El cliente ha solicitado cambios en el diseño. Te paso los detalles en un rato.',
          fecha: '2022-06-18',
        },
        {
          data_transcrito: '¡Feliz cumpleaños! Espero que tengas un día increíble.',
          fecha: '2022-05-12',
        },
        {
          data_transcrito: 'El equipo ha completado la primera fase del proyecto. Ahora pasaremos a la siguiente.',
          fecha: '2022-04-30',
        },
        {
          data_transcrito: 'La reunión de seguimiento será el próximo lunes a las 2 pm.',
          fecha: '2022-03-21',
        },
        {
          data_transcrito: 'El curso de capacitación comienza el 1 de febrero. Por favor, regístrate a tiempo.',
          fecha: '2022-02-01',
        },
        {
          data_transcrito: 'El informe trimestral está listo y ha sido enviado a la dirección.',
          fecha: '2022-01-15',
        },
      ],
      years: years,  // Lista de años con opción de "sin filtro"
      months: [
        { title: 'Todos los meses', value: null },
        { title: 'Enero', value: 1 },
        { title: 'Febrero', value: 2 },
        { title: 'Marzo', value: 3 },
        { title: 'Abril', value: 4 },
        { title: 'Mayo', value: 5 },
        { title: 'Junio', value: 6 },
        { title: 'Julio', value: 7 },
        { title: 'Agosto', value: 8 },
        { title: 'Septiembre', value: 9 },
        { title: 'Octubre', value: 10 },
        { title: 'Noviembre', value: 11 },
        { title: 'Diciembre', value: 12 }
      ],
    }
  },
  methods: {
    handleAuthAction() {
            if (this.isAuthenticated) {
              keycloak.logout({
                    redirectUri: window.location.origin 
                });
            } else {
                keycloak.login();
            }
        },
    get_user_data() {
      if (keycloak.authenticated) {
        const token = keycloak.tokenParsed;

        console.log(token);
        for (const [key, value] of Object.entries(token)) {
          console.log(`${key}: ${value}`);
        }

        this.fullName = token.name || ""; // Guardar el nombre de usuario
      }
    },
  },
  computed: {
    filteredDesserts() {
      return this.desserts.filter(item => {
        // Filtrar por palabra clave
        const matchesSearch = item.data_transcrito.toLowerCase().includes(this.search.toLowerCase());

        // Filtrar por año y mes
        const itemDate = new Date(item.fecha);
        const matchesYear = this.selectedYear ? itemDate.getFullYear() === this.selectedYear : true;
        const matchesMonth = this.selectedMonth ? itemDate.getMonth() + 1 === this.selectedMonth : true;

        return matchesSearch && matchesYear && matchesMonth;
      });
    }
  },
  mounted() {
    // Verificar el estado de autenticación al montar el componente
    this.isAuthenticated = keycloak.authenticated;
        keycloak.onAuthLogout = () => {
            this.isAuthenticated = false;
            this.isAdmin = false; // Restablece el rol de admin cuando se cierre sesión
        };
    this.get_user_data();
  },
}
</script>



<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  /* Oculta el desbordamiento horizontal en toda la página */
}

.centered-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 70%;
}

.custom-card {
  width: 100%;
}

.custom-title {
  background-color: #1ebea4;
  width: 100%;
  height: 200px;
  display: flex;
  /* Asegura que el título esté centrado */
  align-items: center;
  justify-content: center;
  color: white;
  /* Cambiar el color del texto a blanco */
}

.avatar-item {
  background-color: #ffffff;
  width: 20%;
  padding: 2px;
}

.contenedor {
  width: 100%;
  display: flex;
  flex-direction: row;
  height: auto;
}

.info {
  width: 100%;
  margin: 10px;
  background-color: rgba(255, 255, 255, 0.226);
  height: auto;
}

.filtros {
  display: flex;
  flex-direction: row;
}

.search {
  width: 100%;
}

.filtroFecha {
  display: flex;
  width: 50%;
}

#authButton {
    font-size: 14px;
    color: red;
}
</style>