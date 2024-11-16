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
                prepend-icon="mdi mdi-credit-card" 
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
              <template v-slot:[`item.fecha_transcrito`]="{ item }">
                <span>{{ formatDate(item.fecha_transcrito) }}</span>
              </template>
              <template v-slot:[`item.data_transcrito`]="{ item }">
                <div class="mensaje">
                  <span v-if="!item.isExpanded && item.data_transcrito.length > 100">
                    {{ truncateMessage(item.data_transcrito) }}
                  </span>
                  <span v-else>{{ item.data_transcrito }}</span>
                  <v-btn
                    v-if="item.data_transcrito.length > 100" 
                    text 
                    @click="toggleExpand(item)"
                    color="grey-lighten-2"
                    variant="flat"
                    size="x-small"
                    class="leer_mas"
                  >
                    {{ item.isExpanded ? 'Leer menos ⇧' : 'Leer más ⇩' }}
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import keycloak from "@/keycloak";
import axios from "axios"; // Asegúrate de tener axios instalado

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
      userName: '',
      email: '',
      search: '',
      selectedYear : null,
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
          key: 'fecha_transcrito',
          sortable: true,
          title: 'Fecha/Hora',
        },
      ],
      desserts: [],
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
        this.userName = token.preferred_username || '';
        this.email = token.email || "";
      }
    },
    async fetchHistoriales() {
      try {
        const username = this.userName;
        const response = await axios.get(`http://localhost:8000/historial-transcrito?username=${username}`);
        this.desserts = response.data.historiales.map(historial => ({
          data_transcrito: historial.data_transcrito,
          fecha_transcrito: historial.fecha_transcrito,
          isExpanded: false, // Nuevo campo para controlar la expansión
        }));
      } catch (error) {
        console.error("Error al obtener historiales:", error);
      }
    },
    toggleExpand(item) {
      item.isExpanded = !item.isExpanded; // Cambia el estado de expansión
    },
    truncateMessage(message, length = 100) {
      return message.length > length ? message.substring(0, length) + '...' : message;
    },
    formatDate(date) {
      if (!date) return '';
      const formattedDate = new Date(date);
      if (isNaN(formattedDate)) return '';
      
      return formattedDate.toLocaleString("es-ES", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
    },
  },
  computed: {
    filteredDesserts() {
      return this.desserts.filter(item => {
        const matchesSearch = item.data_transcrito.toLowerCase().includes(this.search.toLowerCase());
        const itemDate = new Date(item.fecha_transcrito);
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
    this.fetchHistoriales();
  },
}
</script>

<style scoped>
.mensaje{
  padding: 10px 0px 10px 0px;
}
.leer_mas{
  margin-left: 5px !important;
}
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