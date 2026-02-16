import { ref } from 'vue'
import { api } from './api'
import { membres } from './membre'
import router from './router'


export const editMode = ref(false)
export const editId = ref<number | null>(null)
export const form = ref({
  nom: "",
  prenom: "",
  email: "",
  telephone: "",
  cotisation_payee: false,
})


export const resetForm = () => {
  form.value = {
    nom: "",
    prenom: "",
    email: "",
    telephone: "",
    cotisation_payee: false,
  }
  editMode.value = false
  editId.value = null
}


export const chargerMembres = async () => {
  try {
    const response = await api.get("/membres")
    membres.value = response.data
  } catch (error) {
    console.error("Erreur chargement membres:", error)
  }
}


export const editerMembre = (membre: any) => {

  editMode.value = true
  editId.value = membre.id
  form.value = {
    nom: membre.nom,
    prenom: membre.prenom,
    email: membre.email,
    telephone: membre.telephone || "",
    cotisation_payee: membre.cotisation_payee,
  }
  router.push('/')

  window.scrollTo({ top: 0, behavior: "smooth" })
}


export const supprimerMembre = async (id: number) => {
  if (confirm("Êtes-vous sûr de vouloir supprimer ce membre ?")) {
    try {

      await api.delete(`/membres/${id}`)
      alert("Membre supprimé avec succès")

      await chargerMembres()
    } catch (error) {
      console.error("Erreur suppression:", error)
      alert("Erreur lors de la suppression")
    }
  }
}


export const sauvegarderMembre = async () => {
  try {
    if (editMode.value) {

      await api.put(`/membres/${editId.value}`, form.value)
      alert("Membre modifié avec succès")
    } else {

      await api.post("/membres", form.value)
      alert("Membre ajouté avec succès")
    }
    resetForm()

    await chargerMembres()
    router.push('/membres')
  } catch (error) {
    console.error("Erreur sauvegarde:", error)

    alert("Erreur lors de la sauvegarde")
  }
}


export const annuler = () => {
  resetForm()
  router.push('/membres')
}
