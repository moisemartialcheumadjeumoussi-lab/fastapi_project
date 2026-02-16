
<template>
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
</template>
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
