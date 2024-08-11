import { createRouter, createWebHistory } from 'vue-router'
import planDetails from '@/components/views/planDetails.vue'
import RegistroUsuario from '@/components/views/RegistroUsuario.vue'
import crudPlanes from '@/components/views/crudPlanes.vue'

const routes = [
  {
    path: '/planDetails',
    name: 'planDetails',
    component: planDetails
  },
  {
    path: '/RegistroUsuario',
    name: 'RegistroUsuario',
    component: RegistroUsuario
  },
  {
    path: '/crudPlanes',
    name: 'crudPlanes',
    component: crudPlanes
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router