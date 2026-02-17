import {ref} from 'vue'


interface Membre {
  id: number
  nom: string
  prenom: string
  email: string
  telephone: string
  cotisation_payee: boolean
  date_inscription: string
}
export const membres = ref<Membre[]>([]);
export type {Membre};


