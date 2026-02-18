import { api } from './api'
import { membres } from './membre'






export const chargerMembres = async () => {
  try {
    const response = await api.get("/membres")
    membres.value = response.data
  } catch (error) {
    console.error("Erreur chargement membres:", error)
  }
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

