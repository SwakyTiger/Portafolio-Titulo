<template>
    <v-container class="centered-container">
        <v-card class="custom-card">
            <v-card-title class="custom-title">
                <h1>Mi Cuenta</h1>
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
                            <v-list-item prepend-icon="mdi mdi-logout" id="authButton" @click="handleAuthAction"
                                to="/">{{
                                    isAuthenticated ? 'Cerrar Sesion' : '' }}</v-list-item>
                        </v-list>

                    </v-navigation-drawer>
                    <v-main style="height: 250px"></v-main>
                </v-layout>
                <v-card class="info">
                    <v-list>
                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>Nombre</v-list-item-title>
                                <v-list-item-subtitle>{{ fullName }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>Nombre de Usuario</v-list-item-title>
                                <v-list-item-subtitle>{{ userName }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>Correo</v-list-item-title>
                                <v-list-item-subtitle>{{ email }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>

                        <v-list-item>
                            <v-list-item-content>
                                <v-list-item-title>Número</v-list-item-title>
                                <v-list-item-subtitle>{{ phoneNumber }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>
                        <v-list-item>
                            <v-btn x-large color="#42b983" dark class="mt-8" to="/editarInfoUser">Editar</v-btn>
                        </v-list-item>
                    </v-list>
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

                this.fullName = token.name;
                this.userName = token.preferred_username || '';
                this.email = token.email || '';

                // Propiedades personalizadas
                const phonePrefix = token.prefijo || '';
                const phoneNumber = token.telefono || '';
                this.phoneNumber = `${phonePrefix} ${phoneNumber}`.trim();

                // Mostrar en la consola para depurar
                console.log('Full Name:', this.fullName);
                console.log('Username:', this.userName);
                console.log('Email:', this.email);
                console.log('Phone Number:', this.phoneNumber);
            }
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
}

.info {
    width: 100%;
    margin: 10px;
    background-color: rgba(255, 255, 255, 0.226);
}

#authButton {
    font-size: 14px;
    color: red;
}
</style>