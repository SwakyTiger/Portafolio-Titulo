<template>
  <div class="registrarse">
    <h2>Registro</h2>
    <img src="https://alloxentric.com/wp-content/uploads/2020/11/alloxentric_logo-3x.png" alt="" class="logo">
  </div>
  <br>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="10">
        <v-card class="elevation-12 custom-border" border>
          <v-card-text>
            <v-form @submit.prevent="registerUser">
              <v-text-field
                v-model="user.nombre"
                label="Nombre"
                required
              ></v-text-field>
              <v-text-field
                v-model="user.apellido"
                label="Apellido"
                required
              ></v-text-field>
              <v-text-field
                v-model="user.prefijo"
                label="Prefijo (Ejemplo: +56)"
                required
              ></v-text-field>
              <v-text-field
                v-model="user.numero_telefono"
                label="Número de Teléfono"
                required
              ></v-text-field>
              <v-text-field
                v-model="user.email"
                label="Correo electrónico"
                type="email"
                required
              ></v-text-field>
              <v-text-field
                v-model="user.pwd"
                label="Contraseña"
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                required
              ></v-text-field>
              <v-text-field
                v-model="user.confirmPassword"
                label="Confirmar contraseña"
                :type="showPassword ? 'text' : 'password'"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions class="justify-center pb-4">
            <v-btn variant="elevated" color="black" @click="registerUser" min-width="164">
              Registrarse
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: {
        nombre: '',
        apellido: '',
        prefijo: '',
        numero_telefono: '',
        email: '',
        pwd: '',
        confirmPassword: ''
      },
      showPassword: false,
    };
  },
  methods: {
    async registerUser() {
      try {
        if (this.user.pwd !== this.user.confirmPassword) {
          alert("Las contraseñas no coinciden");
          return;
        }

        const payload = {
          id_usuario: null,
          nombre: this.user.nombre,
          apellido: this.user.apellido,
          prefijo: this.user.prefijo,
          numero_telefono: parseInt(this.user.numero_telefono),
          email: this.user.email,
          pwd: this.user.pwd
        };

        const response = await axios.post('http://localhost:8000/usuarios', payload);

        if (response.status === 201) {
          alert("Usuario registrado exitosamente");
          // Redireccionar o limpiar el formulario si es necesario
        }
      } catch (error) {
        console.error(error);
        alert("Error al registrar el usuario");
      }
    }
  }
};
</script>


<style scoped>
.registrarse {
  padding: 100px;
  width: 100%;
  background-color: #f5f5f5;
  text-align: center;
  font-size: 5rem
}
.custom-border {
  border-color: #00FFF0 !important;
}
.logo{
  width: 20%;
}
.v-card{
  background-image: linear-gradient(#ffffff, #1DBEA8);
}
.v-text-field{
  width: 70%;
  padding-left: 300px;
  
}
</style>
