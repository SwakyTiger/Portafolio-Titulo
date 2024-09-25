<template>
    <v-container class="centered-container">
        <v-card class="custom-card">
            <v-card-title class="custom-title">

            </v-card-title>
            <v-list-item lines="two" :prepend-avatar="require('@/assets/icon-account.png')" :title="userName"
                class="avatar-item"></v-list-item>

            <v-card class="contenedor">
                <v-layout permanent density="compact">
                    <v-navigation-drawer permanent>
                        <v-list density="compact" nav>
                            <v-list-item prepend-icon="mdi-view-dashboard" title="Mi Cuenta" value="home"></v-list-item>
                            <v-list-item prepend-icon="mdi-forum" title="Historial" value="about"></v-list-item>
                        </v-list>
                    </v-navigation-drawer>
                    <v-main style="height: 250px"></v-main>
                </v-layout>
                <v-card class="info">
                    <v-form disabled style="color: black; ">
                        <v-text-field v-model="fullName" label="Nombre" ></v-text-field>
                        <v-text-field v-model="userName" label="Nombre de Usuario"></v-text-field>
                        <v-text-field v-model="email" label="Correo"></v-text-field>
                        <v-text-field v-model="phoneNumber" label="Last name"></v-text-field>
                    </v-form>
                </v-card>
            </v-card>
        </v-card>
    </v-container>
</template>

<script>
import keycloak from '@/keycloak'; // Importa tu instancia de Keycloak

export default {
    name: 'miCuenta',
    data() {
        return {
            fullName: '',
            userName: '',
            email: '',
            phoneNumber: ''
        };
    },
    methods: {
        get_user_data() {
            if (keycloak.authenticated) {
                const token = keycloak.tokenParsed;

                // Asumiendo que las propiedades están en el token
                const firstName = token.given_name || ''; // Nombre
                const lastName = token.family_name || ''; // Apellido
                this.fullName = `${firstName} ${lastName}`; // Nombre completo

                this.userName = token.preferred_username || ''; // Nombre de usuario
                this.email = token.email || ''; // Email
            }
        }
    },
    mounted() {
        this.get_user_data();
    }
};
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
    width: 50%;
}

.custom-card {
    width: 100%;
}

.custom-title {
    background-color: #4a9573;
    width: 100%;
    height: 200px;
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
}

.info {
    width: 100%;
    margin: 10px;
    background-color: rgba(255, 255, 255, 0.226);
}

/* Aquí puedes agregar estilos específicos para este componente */
h1 {
    color: #42b983;
    /* Ejemplo de estilo */
}
</style>