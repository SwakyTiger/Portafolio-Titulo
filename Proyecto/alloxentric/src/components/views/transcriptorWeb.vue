<template>
  <v-app>
    <h1 class="titulo">Transcriptor Web</h1>
    <v-alert v-if="showAlert" type="error" dismissible @click="showAlert = false">
      El usuario no está autenticado. Por favor, inicia sesión para continuar.
    </v-alert>
    <v-container fluid>
        <v-row justify="center">
          <v-col cols="12" sm="10" md="8" lg="6">
            <v-card class="mt-4 pa-4">
              <v-card-title class="text-h4 justify-center">
                Transcriptor de Audio
              </v-card-title>

              <v-alert
                v-model="showAlert"
                dismissible
                color="error"
                icon="mdi-alert-circle"
                border="left"
                prominent
                class="mt-4"
              >
                El usuario no está autenticado. Por favor, inicia sesión para continuar.
              </v-alert>

              <v-card-text>
                <v-file-input
                  v-model="archivo"
                  label="Seleccionar archivo de audio"
                  accept="audio/*"
                  prepend-icon="mdi-file-music"
                  :rules="[v => !!v || 'Se requiere un archivo de audio']"
                  @change="handleFileUpload"
                ></v-file-input>

                <v-btn
                  color="primary"
                  @click="iniciarTranscripcion"
                  :loading="isTranscribing"
                  :disabled="!archivo || isTranscribing"
                  block
                  class="mt-4"
                >
                  <v-icon left>mdi-transcribe</v-icon>
                  Transcribir Audio
                </v-btn>

                <v-divider class="my-4"></v-divider>

                <v-row align="center" class="mt-2">
                  <v-col cols="auto">
                    <v-chip color="secondary" label>
                      <v-icon left>mdi-account</v-icon>
                      Usuario: {{ username }}
                    </v-chip>
                  </v-col>
                  <v-col cols="auto">
                    <v-chip color="info" label>
                      <v-icon left>mdi-credit-card</v-icon>
                      Créditos: {{ creditos }}
                    </v-chip>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <v-card v-if="transcripcion" class="mt-4">
              <v-card-title class="text-h5">
                <v-icon left color="success">mdi-text-to-speech</v-icon>
                Transcripción
              </v-card-title>
              <v-card-text>
                <v-textarea
                  v-model="transcripcion"
                  readonly
                  outlined
                  rows="10"
                  hide-details
                ></v-textarea>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="copiarTranscripcion">
                  <v-icon left>mdi-content-copy</v-icon>
                  Copiar
                </v-btn>
                <v-btn color="secondary" text @click="descargarTranscripcion">
                  <v-icon left>mdi-download</v-icon>
                  Descargar
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
    {{ snackbarMessage }}
  </v-snackbar>
  </v-app>
</template>
<script>
import keycloak from '@/keycloak';
import axios from 'axios';

export default {
  data() {
    return {
      archivo: null,
      transcripcion: '',
      numeroTelefono: '', // Número de teléfono del usuario, se obtendrá en get_user_data
      usuarioId: null, // ID del usuario en el sistema, se obtendrá de find_usuario
      usuario: null,
      transcrito: null,
      creditos: 0, // Créditos disponibles, se obtendrá de find_usuario
      showAlert: false,
      isTranscribing: false,
      isAuthenticated: false,
      snackbar: false,
      snackbarMessage: '',
      snackbarColor: ''
    };      
  },
  methods: {
    handleFileUpload(event) {
      this.archivo = event.target.files[0];
    },
    async get_user_data() {
      if (keycloak.authenticated) {
        const token = keycloak.tokenParsed;
        //const phonePrefix = token.prefijo || '';
        this.username = token.preferred_username
        this.email = token.email
        await this.obtenerInformacionUsuario();
      }
    },
    async obtenerInformacionUsuario() {
      try {
        const response = await axios.get(`http://localhost:8000/bot/${this.email}/${this.username}`);
        const usuario = response.data.usuario;
        const suscripciones = response.data.suscripciones;
        
        this.usuarioId = usuario.id_usuario;
        this.creditos = suscripciones.creditos || 0; // Guardar los créditos disponibles
      } catch (error) {
        console.error("Error al obtener información del usuario:", error);
        alert("No se pudo obtener la información del usuario.");
      }
    },
    async restarCredito() {
      try {
        await axios.put(`http://localhost:8000/restar-creditos/${this.username}`);
        this.creditos -= 1; // Actualizar los créditos en el frontend
        console.log("Crédito restado exitosamente.");
      } catch (error) {
        console.error("Error al restar crédito:", error);
        alert("No se pudo restar el crédito.");
      }
    },
    async iniciarTranscripcion() {
      // Asegurarse de que se hayan obtenido los créditos del usuario
      if (this.creditos <= 0) {
        alert("No tienes suficientes créditos para realizar la transcripción.");
        return;
      }

      if (!this.archivo) {
        alert("Por favor, selecciona un archivo de audio.");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.archivo);

      this.isTranscribing = true;
    try {
      const response = await axios.post("http://localhost:8000/transcribir-audio/", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      this.transcripcion = response.data.transcripcion;
      await this.restarCredito();
      this.mostrarNotificacion('success', 'Transcripción completada con éxito.');
      // Guardar la transcripción en la base de datos
      await this.guardarTranscripcion();
    } catch (error) {
      console.error("Error al transcribir el audio:", error);
      this.mostrarNotificacion('error', 'Ocurrió un error al transcribir el audio.');
    } finally {
      this.isTranscribing = false;
    }
  },
  async guardarTranscripcion() {
      try {
        await axios.post("http://localhost:8000/guardar-transcrito", null, {
          params: {
            id_usuario: this.usuarioId,
            username: this.username,
            transcrito: this.transcripcion
          }
        });
      } catch (error) {
        console.error("Error al guardar la transcripción:", error);
        this.mostrarNotificacion('error', 'No se pudo guardar la transcripción.');
      }
    },
  copiarTranscripcion() {
    navigator.clipboard.writeText(this.transcripcion).then(() => {
      this.mostrarNotificacion('success', 'Transcripción copiada al portapapeles.');
    }).catch((err) => {
      console.error('Error al copiar: ', err);
      this.mostrarNotificacion('error', 'No se pudo copiar la transcripción.');
    });
  },
  descargarTranscripcion() {
    const blob = new Blob([this.transcripcion], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'transcripcion.txt';
    link.click();
    URL.revokeObjectURL(link.href);
  },
  mostrarNotificacion(tipo, mensaje) {
    this.snackbarMessage = mensaje;
    this.snackbarColor = tipo === 'success' ? 'green' : 'red';
    this.snackbar = true;
   },
  },
  async created() {
    await this.get_user_data(); // Llama a get_user_data cuando el componente se monta para obtener los datos del usuario
  }
};
</script>




<style scoped>
.titulo {
  padding: 50px;
  width: 100%;
  background-color: #1ebea4;
  color: white;
  text-align: center;
  font-size: 3rem;
}
.transcriptor {
  font-size: 2.5rem;
  padding: 30px;
  text-align: center;
  color: #42b983;
}
.transcription-box {
  margin-top: 2rem;
  border: 2px solid #1ebea4;
}
</style>