// plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css' // Asegura la importación

const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi', // Usar Material Design Icons
  },
})

export default vuetify