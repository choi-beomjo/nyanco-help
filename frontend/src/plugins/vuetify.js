// src/plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

const vuetify = createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#1E88E5', // 블루
          secondary: '#FFC107', // 노랑
          accent: '#8E24AA', // 보라
        },
      },
    },
  },
})

export default vuetify
