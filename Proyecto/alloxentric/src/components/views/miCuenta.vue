<template>
    <v-container fluid class="pa-0">
        <v-card flat>
            <v-card-title class="custom-title text-h4 font-weight-bold white--text pb-4">
                <h1>Mi Cuenta</h1>
            </v-card-title>

            <v-row no-gutters>
                <v-col cols="12" md="3">
                    <v-card flat class="h-100">
                        <v-list>
                            <v-list-item lines="two" :prepend-avatar="require('@/assets/icon-account.png')"
                                :title="fullName" :subtitle="email" class="avatar-item">
                            </v-list-item>
                        </v-list>
                        <v-divider></v-divider>
                        <v-list nav density="compact">
                            <v-list-item prepend-icon="mdi-view-dashboard" title="Mi Cuenta" value="home"
                                to="/miCuenta"></v-list-item>
                            <v-list-item prepend-icon="mdi-forum" title="Historial" value="about"
                                to="/historyTranscriptor"></v-list-item>
                            <v-list-item prepend-icon="mdi-logout" :title="isAuthenticated ? 'Cerrar Sesión' : ''"
                                @click="handleAuthAction" to="/" id="authButton" class="error--text"></v-list-item>
                        </v-list>
                    </v-card>
                </v-col>

                <v-col cols="12" md="9">
                    <v-card flat class="pa-6">
                        <v-list>
                            <v-list-item>
                                <v-list-item-title class="text-h6">Nombre</v-list-item-title>
                                <v-list-item-subtitle>{{ fullName }}</v-list-item-subtitle>
                            </v-list-item>

                            <v-list-item>
                                <v-list-item-title class="text-h6">Nombre de Usuario</v-list-item-title>
                                <v-list-item-subtitle>{{ userName }}</v-list-item-subtitle>
                            </v-list-item>

                            <v-list-item>
                                <v-list-item-title class="text-h6">Correo</v-list-item-title>
                                <v-list-item-subtitle>{{ email }}</v-list-item-subtitle>
                            </v-list-item>

                            <v-list-item>
                                <v-list-item-title class="text-h6">Número</v-list-item-title>
                                <v-list-item-subtitle>{{ phoneNumber }}</v-list-item-subtitle>
                            </v-list-item>
                        </v-list>

                        <v-btn x-large color="#42b983" dark class="mt-8"
                            :href="`http://localhost:8081/realms/Transcriptor/account/`" target="_blank">
                            Editar
                        </v-btn>

                    </v-card>
                </v-col>
            </v-row>
        </v-card>
    </v-container>
</template>

<script>
import keycloak from '@/keycloak';

export default {
    name: 'MiCuenta',
    data() {
        return {
            fullName: '',
            userName: '',
            email: '',
            phoneNumber: '',
            isAuthenticated: false,
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

.v-img {
    background-color: #1ebea4;
}

.v-list-item-title {
    font-weight: bold;
    color: #42b983;
}

.v-list-item-subtitle {
    color: rgba(0, 0, 0, 0.6);
    font-weight: bold;
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