<template>
    <v-app>

        <v-main class="bg-white">
            <v-carousel cycle height="400" hide-delimiter-background show-arrows-on-hover>
                <v-carousel-item v-for="(slide, i) in carouselSlides" :key="i">
                    <v-sheet :color="slide.color" height="100%">
                        <v-row class="fill-height" align="center" justify="center">
                            <div class="text-center">
                                <h3 class="text-h3 font-weight-bold white--text mb-4">{{ slide.title }}</h3>
                                <p class="text-h5 white--text">{{ slide.text }}</p>
                            </div>
                        </v-row>
                    </v-sheet>
                </v-carousel-item>
            </v-carousel>

            <v-container>
                <v-row class="text-center my-12">
                    <v-col cols="12">
                        <h1 class="text-h3 font-weight-bold" style="color: #42b983;">Transcribe tus audios de WhatsApp a
                            texto</h1>
                        <p class="text-h5 grey--text text--darken-1 my-4">Nunca más te pierdas un mensaje importante por
                            no poder escucharlo</p>

                        <v-row justify="center" class="mt-8">
                            <v-col cols="12" md="4" v-for="(feature, index) in features" :key="index">
                                <v-card outlined class="pa-4 h-100 d-flex flex-column" color="lighten-4">
                                    <v-icon size="48" color="#42b983" class="mb-4">{{ feature.icon }}</v-icon>
                                    <h3 class="text-h5 mb-2">{{ feature.title }}</h3>
                                    <p class="grey--text text--darken-1 flex-grow-1">{{ feature.description }}</p>
                                </v-card>
                            </v-col>
                        </v-row>

                        <v-btn x-large color="#42b983" dark class="mt-8" to="/planDetails">Comienza Ahora</v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import keycloak from '@/keycloak';
import config from "@/config";

export default {
    name: 'HomePage',
    data() {
        return {
            email: '',
            password: '',
            carouselSlides: [
                {
                    color: '#1ebea5',
                    title: 'Transcribe tus audios de WhatsApp',
                    text: 'Convierte fácilmente tus mensajes de voz en texto'
                },
                {
                    color: '#128c7e',
                    title: 'Ahorra tiempo',
                    text: 'Lee tus mensajes cuando no puedas escucharlos'
                },
                {
                    color: '#075e54',
                    title: 'Mejora tu productividad',
                    text: 'Organiza y busca en tus conversaciones transcritas'
                }
            ],
            features: [
                {
                    icon: 'mdi-text-to-speech',
                    title: 'Transcripción Precisa',
                    description: 'Nuestro avanzado algoritmo de IA garantiza transcripciones precisas de tus mensajes de voz.'
                },
                {
                    icon: 'mdi-clock-fast',
                    title: 'Rápido y Eficiente',
                    description: 'Obtén tus transcripciones en segundos, ahorrando tiempo valioso en tu día a día.'
                },
                {
                    icon: 'mdi-shield-check',
                    title: 'Privacidad Garantizada',
                    description: 'Tu seguridad es nuestra prioridad. Todos los datos se procesan con encriptación de extremo a extremo.'
                }
            ]
        }
    },
    methods: {
        async get_user_data() {
            if (keycloak.authenticated) {
                const token = keycloak.token; // Obtén el token JWT
                // Almacena el token en una cookie
                document.cookie = `token=${token}; path=/; secure; SameSite=Strict`;

                // Realiza la llamada a tu API
                const userData = {
                    id_usuario: token.sub,
                    nombre: token.given_name || '',
                    apellido: token.family_name || '',
                    prefijo: token.prefijo || '',
                    numero_telefono: token.telefono ? parseInt(token.telefono) : null,
                    email: token.email || '',
                    username: token.preferred_username || '',
                };

                // Llama a tu API para guardar o actualizar el usuario
                await this.get_user_data(userData);

                try {
                    const response = await fetch(`${config.BASE_URL}:8000/usuarios/${userData.id_usuario}`, {
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json',
                        },
                    });
                    if (response.status === 404) {
                        // Usuario no existe, lo guardamos
                        await fetch(`${config.BASE_URL}:8000/usuarios`, {
                            method: 'POST',
                            headers: {
                                'Authorization': `Bearer ${token}`,
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(userData),
                        });
                    } else if (response.ok) {
                        // Usuario existe, verificamos cambios
                        const userInDb = await response.json();
                        const hasChanges = this.checkForChanges(userInDb, userData);

                        if (hasChanges) {
                            await fetch(`${config.BASE_URL}:8000/usuarios/${userData.id_usuario}`, {
                                method: 'PUT',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'Authorization': `Bearer ${token}`,
                                },
                                body: JSON.stringify(userData),
                            });
                        }
                    } else {
                        throw new Error('Error al verificar el usuario en la base de datos');
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        },
        checkForChanges(userInDb, userData) {
            // Compara cada campo relevante
            return (
                userInDb.nombre !== userData.nombre ||
                userInDb.apellido !== userData.apellido ||
                userInDb.prefijo !== userData.prefijo ||
                userInDb.numero_telefono !== userData.numero_telefono ||
                userInDb.email !== userData.email ||
                userInDb.username !== userData.username
            );
        },
    },
    mounted() {
        this.get_user_data();
    }
}
</script>

<style scoped>
.v-application {
    background-color: white !important;
}
</style>