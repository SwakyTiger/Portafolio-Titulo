import { createRouter, createWebHistory } from 'vue-router'
import planDetails from '@/components/views/planDetails.vue'
import RegistroUsuario from '@/components/views/RegistroUsuario.vue'
import crudPlanes from '@/components/views/crudPlanes.vue'
import cuadraturaMensual from '@/components/views/cuadraturaMensual.vue'
import login from '@/components/views/login.vue'
import ventasReport from '@/components/views/ventasReport.vue'
import resumenPago from '@/components/views/resumenPago.vue'

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
  },
  {
    path: '/CuadraturaMensual',
    name: 'cuadraturaMensual',
    component: cuadraturaMensual
  },
  {
    path: '/login',
    name: 'login',
    component: login
  },
  {
    path: '/ventasReport',
    name: 'ventasReport',
    component: ventasReport
  },
  {
    path: '/resumenPago',
    name: 'resumenPago',
    component: resumenPago
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
