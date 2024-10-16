<template>
  <v-container fluid class="pa-0">
    <v-card flat>
      <v-card-title class="custom-title text-h4 font-weight-bold white--text pb-4">
                <h1>Historial</h1>
            </v-card-title>

      <v-row no-gutters>
        <v-col cols="12" md="3">
          <v-card flat class="h-100">
            <v-list>
              <v-list-item
                :prepend-avatar="require('@/assets/icon-account.png')"
                :title="fullName"
                :subtitle="email"
              ></v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-list nav density="compact">
              <v-list-item
                prepend-icon="mdi-view-dashboard"
                title="Mi Cuenta"
                value="home"
                to="/miCuenta"
              ></v-list-item>
              <v-list-item
                prepend-icon="mdi-forum"
                title="Historial"
                value="about"
                to="/historyTranscriptor"
              ></v-list-item>
              <v-list-item 
              prepend-icon="mdi-forum" 
              title="Mis Suscripciones" 
              value="about"
              to="/miSuscripcion"
              ></v-list-item>
              <v-list-item
                prepend-icon="mdi-logout"
                :title="isAuthenticated ? 'Cerrar Sesión' : ''"
                @click="handleAuthAction"
                id="authButton"
                class="error--text"
              ></v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <v-col cols="12" md="9">
          <v-card flat class="pa-6">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="search"
                  label="Buscar"
                  prepend-inner-icon="mdi-magnify"
                  outlined
                  dense
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="selectedYear"
                  :items="years"
                  label="Año"
                  outlined
                  dense
                  hide-details
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="selectedMonth"
                  :items="months"
                  label="Mes"
                  outlined
                  dense
                  hide-details
                ></v-select>
              </v-col>
            </v-row>

            <v-data-table
              :headers="headers"
              :items="filteredDesserts"
              :search="search"
              :items-per-page="10"
              class="mt-4"
            >
            </v-data-table>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import keycloak from "@/keycloak";

export default {
  name: 'HistorialTranscriptor',
  data() {
    const currentYear = new Date().getFullYear();
    const startYear = 2023;

    const years = [{ title: 'Todos los años', value: null }];
    for (let year = startYear; year <= currentYear; year++) {
      years.push({ title: year.toString(), value: year });
    }

    return {
      fullName: '',
      email: '',
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
          sortable: true,
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
      years: years,
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
      isAuthenticated: false,
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
        this.fullName = token.name || "";
        this.email = token.email || "";
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    },
  },
  computed: {
    filteredDesserts() {
      return this.desserts.filter(item => {
        const matchesSearch = item.data_transcrito.toLowerCase().includes(this.search.toLowerCase());
        const itemDate = new Date(item.fecha);
        const matchesYear = this.selectedYear ? itemDate.getFullYear() === this.selectedYear : true;
        const matchesMonth = this.selectedMonth ? itemDate.getMonth() + 1 === this.selectedMonth : true;
        return matchesSearch && matchesYear && matchesMonth;
      });
    }
  },
  mounted() {
    this.isAuthenticated = keycloak.authenticated;
    keycloak.onAuthLogout = () => {
      this.isAuthenticated = false;
    };
    this.get_user_data();
  },
}
</script>

<style scoped>
.v-card {
  border-radius: 8px;
}
.v-list-item--active {
  background-color: #e6f7f0;
}
#authButton {
  font-size: 14px;
  color: #ff5252;
}
.v-data-table {
  background-color: white;
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
}
</style>