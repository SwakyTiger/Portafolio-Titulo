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
                  v-model="user.name"
                  label="Nombre"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="user.lastName"
                  label="Apellido"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="user.NroTelefono"
                  label="Ejemplo: +56 9 XXXX XXXX"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="user.email"
                  label="Correo electrónico"
                  type="email"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="user.password"
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
  
  <script setup>
  import { ref } from 'vue';
  
  const user = ref({
    name: '',
    lastName: '',
    email: '',
    NroTelefono: '',
    password: '',
    confirmPassword: ''
  });
  
  const showPassword = ref(false);
  
  const registerUser = () => {
    // Aquí iría la lógica para registrar al usuario
    console.log('Usuario a registrar:', user.value);
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
