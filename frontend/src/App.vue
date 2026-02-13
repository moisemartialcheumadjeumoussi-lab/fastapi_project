<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

const loading = ref(false);
const editMode = ref(false);
const editId = ref(null);

//membres et propriété
const membres = ref("[]");
const Stats = ref({
  total_membres: 0,
  cotisations_payees: 0,
  cotisations_impayees: 0,
});
const form = ref({
  nom: "",
  prenom: "",
  email: "",
  telephone: "",
  cotisation_payee: false,
});

//fonctions api
const chargerMembres = async () => {
  loading.value = true;
  try {
    const response = await api.get("/membres");
    membres.value = response.data;
  } catch (error) {
    console.error("erreur de chargement", error);
    alert("Erreur lors du chargement des membres");
  } finally {
    loading.value = false;
  }
};

const chargerStats = async () => {
  try {
    const response = await api.get("/stats");
    membres.value = response.data;
  } catch (error) {
    console.error("erreur stats", error);
  }
};
const sauvegarderMembre = async () => {
  try {
    if (editMode.value) {
      await api.put("/membres/${editId.value}", form.value);
      alert("membre modifié avec succès");
    } else {
      await api.post("/membres", form.value);
      alert("membre ajouté avec succès");
    }
    resetForm();
    await chargerMembres();
    await chargerStats();
  } catch (error) {
    console.error("erreur sauvegarde", error);
    alert("erreur lors de la sauvegarde");
  }
};
const editerMembre = (membre) => {
  editMode.value = true;
  editId.value = membre.id;
  form.value = {
    nom: membre.nom,
    prenom: membre.prenom,
    email: membre.email,
    telephone: membre.telephone || "",
    cotisation_payee: membre.cotisation_payee,
  };
  window.scrollTo({ top: 0, behavior: "smooth" });
};
const supprimerMembreConfirm = async (id) => {
  if (confirm("êtes vous sûr de vouloir supprimer ce membre??")) {
    try {
      await api.delete("/membres/${id}");
      alert("membre supprimé");
      await chargerMembres();
      await chargerStats();
    } catch (error) {
      console.error("erreur suppression", error);
      alert("erreur lors de la suppression");
    }
  }
};
const annuler = async () => {
  resetForm();
};
const resetForm = () => {
  form.value = {
    nom: "",
    prenom: "",
    email: "",
    telephone: "",
    cotisation_payee: false,
  };
  editMode.value = false;
  editId.value = null;
};
const formatDate = (date) => {
  return new Date(date).toLocaleDateString("fr-Fr");
};

onMounted(() => {
  chargerMembres();
  chargerStats();
});
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  min-height: 100vh;
  background: #f5f5f5;
}

header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 1rem;
}

.stats {
  display: flex;
  gap: 2rem;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat .label {
  font-size: 0.9rem;
  opacity: 0.9;
}

.stat .value {
  font-size: 2rem;
  font-weight: bold;
}

main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.form-section,
.list-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="tel"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.form-group.checkbox {
  display: flex;
  align-items: center;
}

.form-group.checkbox label {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
}

.btn-secondary {
  background: #ddd;
  color: #333;
}

.btn-secondary:hover {
  background: #ccc;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.membres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.membre-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  transition: transform 0.3s;
}

.membre-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.membre-card.impaye {
  border-left: 4px solid #f44336;
}

.membre-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.membre-header h3 {
  color: #333;
  font-size: 1.2rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge.payee {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.impayee {
  background: #ffebee;
  color: #c62828;
}

.membre-info p {
  margin: 0.5rem 0;
  color: #666;
}

.membre-info .date {
  font-size: 0.85rem;
  color: #999;
  margin-top: 1rem;
}

.membre-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn-edit {
  background: #2196f3;
  color: white;
  flex: 1;
}

.btn-edit:hover {
  background: #1976d2;
}

.btn-delete {
  background: #f44336;
  color: white;
  flex: 1;
}

.btn-delete:hover {
  background: #d32f2f;
}
</style>

<template>
  <div class="app">
    <header>
      <h1>Gestion des membres au node</h1>
      <div class="stats">
        <div class="stat">
          <span class="label">Total des membres</span>
          <span class="value">{{ Stats.total_membres }}</span>
        </div>
        <div class="'stat'">
          <span class="label">cotisation_payee</span>
          <span class="value">{{ Stats.cotisations_payees }}</span>
        </div>
      </div>
    </header>
    <main>
      <section class="form-section">
        <h2>{{ editMode ? "modifier" : "Ajouter" }} un membre</h2>
        <form @submit.prevent="sauvegarderMembre">
          <div class="form-group">
            <label>Nom</label>
            <input v-model="form.nom" required type="text" />
          </div>
          <div class="form-group">
            <label>Prenom</label>
            <input v-model="form.prenom" required type="text" />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="form.email" required type="email" />
          </div>
          <div class="form-group">
            <label>Telephone</label>
            <input v-model="form.telephone" type="tel" />
          </div>
          <div class="form-group checkbox">
            <label>
              <input v-model="form.cotisation_payee" type="checkbox" />
              cotisation payée
            </label>
          </div>
          <div class="buttons">
            <button type="submit" class="btn-primary">
              {{ editMode ? "Modifier" : "Ajouter" }}
            </button>
            <button v-if="editMode" @click="annuler" type="button" class="btn-secondary">
              Annuler
            </button>
          </div>
        </form>
      </section>
      <section class="list-section">
        <h2>Liste des membres ({{ membres.length }})</h2>
        <div v-if="loading" class="loading">En cours de téléchargement</div>
        <div v-else-if="membres.length === 0" class="empty">Aucun membre enregistré</div>
        <div v-else class="membres-grid">
          <div
            v-for="membre in membres"
            :key="membre.id"
            class="membre-card"
            :class="{ impaye: !membre.cotisation_payee }"
          >
            <div class="membre-header">
              <h3>{{ membre.prenom }} {{ membre.nom }}</h3>
              <span class="badge" :class="membre.cotisation_payee ? 'payee' : 'impayee'">
                {{ membre.cotisation_payee ? "Payée" : " Impayée" }}
              </span>
            </div>
            <div class="membre-info">
              <p>{{ membre.email }}</p>
              <p v-if="membre.telephone">{{ membre.telephone }}</p>
              <p class="date">Inscrit le {{ formatDate(membre.date_inscription) }}</p>
            </div>
            <div class="membre-actions">
              <button @click="editerMembre(membre)" class="btn-edit">Modifier</button>
              <button @click="supprimerMembreConfirm(membre.id)" class="btn-delete">
                Supprimer
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>
