import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'
import afficher_membres from '@/components/afficher_membres.vue'
import Formulaires from '@/components/Formulaires.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{path:'/',name:'Home',component:Formulaires},
  {path:'/membres',name:'Membres', component: afficher_membres}],
})

export default router
