<script setup lang="ts">
import { api } from '../api'
import { ref, onMounted } from 'vue'

const Stats = ref({
  total_membres: 0,
  cotisations_payees: 0,
  cotisations_impayees: 0,
});

onMounted(() => {
  chargerStats();
});

const chargerStats = async () => {
  try {
    const response = await api.get("/stats");
    Stats.value = response.data;
  } catch (error) {
    console.error("erreur stats", error);
  }
};
</script>

<template>
  <header>
    <!-- Bloc du haut : titre + stats (inchangé) -->
    <div class="header-top">
      <h1>Gestion des membres</h1>
      <div class="stats">
        <div class="stat">
          <span class="label">Total des membres</span>
          <span class="value">{{ Stats.total_membres }}</span>
        </div>
        <div class="stat">
          <span class="label">Cotisations payées</span>
          <span class="value">{{ Stats.cotisations_payees }}</span>
        </div>
      </div>
    </div>

    <nav class="navbar">
      <!-- Lien vers la page d'accueil -->
      <RouterLink to="/" class="nav-lien" active-class="actif" exact>
         Accueil
      </RouterLink>

      <!-- Lien vers le formulaire d'ajout -->
      <RouterLink to="/formulaire" class="nav-lien" active-class="actif">
         Ajouter Membre
      </RouterLink>

      <!-- Lien vers la liste des membres -->
      <RouterLink to="/membres" class="nav-lien" active-class="actif">
         Gestion des membres
      </RouterLink>
    </nav>

  </header>
</template>

<style scoped>
header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 2rem 0 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}


.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

h1 {
  font-size: 1.5rem;
  font-weight: 700;
}

.stats {
  display: flex;
  gap: 2rem;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat .label {
  font-size: 0.8rem;
  opacity: 0.85;
}

.stat .value {
  font-size: 1.8rem;
  font-weight: bold;
}


.navbar {
  display: flex;
  gap: 0.5rem;
  background: rgba(0, 0, 0, 0.15);
  padding: 0.5rem 1rem;
  border-radius: 10px 10px 0 0;
}


.nav-lien {
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  transition: background 0.25s, color 0.25s;
}


.nav-lien:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}


.nav-lien.actif {
  background: white;
  color: #667eea;
  font-weight: 700;
}
</style>
