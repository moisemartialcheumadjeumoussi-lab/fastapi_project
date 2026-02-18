<script setup lang="ts">
// On importe useRouter pour pouvoir naviguer vers d'autres pages au clic d'un bouton
import { useRouter } from 'vue-router'

const router = useRouter()

// Fonction appelée quand l'utilisateur clique sur "Ajouter un membre"
const allerAjouter = () => {
  router.push('/formulaire') // redirige vers la route /ajouter
}


const allerGestion = () => {
  router.push('/membres') // redirige vers la route /membres
}
</script>

<template>
  <div class="accueil">


    <div class="hero-icon">Viens on fom😴😋</div>

    <h1 class="titre">Bienvenue dans votre espace de gestion</h1>

    <p class="sous-titre">
      Gérez facilement vos membres, suivez les cotisations et gardez votre association organisée.
    </p>


    <div class="separateur"></div>

    <div class="cartes">

      <div class="carte" @click="allerAjouter">

        <div class="carte-icon"></div>
        <h2>Ajouter un membre</h2>
        <p>Enregistrez un nouveau membre avec ses informations et son statut de cotisation.</p>
        <button class="btn-carte btn-violet">Accéder au formulaire →</button>
      </div>


      <div class="carte" @click="allerGestion">
        <div class="carte-icon"></div>
        <h2>Gestion des membres</h2>
        <p>Consultez, modifiez ou supprimez les membres existants de votre association.</p>
        <button class="btn-carte btn-bleu">Voir tous les membres →</button>
      </div>

    </div>
  </div>
</template>

<style scoped>
/*
  "scoped" signifie que ces styles s'appliquent UNIQUEMENT à ce composant,
  sans affecter le reste de l'application.
*/

.accueil {
  /* Centre tout le contenu horizontalement et verticalement */
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 3rem 2rem;
  max-width: 900px;
  margin: 0 auto; /* Centre le bloc dans la page */
}

.hero-icon {
  font-size: 5rem; /* Grande icône décorative */
  margin-bottom: 1rem;
  /* Animation douce au chargement */
  animation: apparaitre 0.6s ease-out;
}

.titre {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2d2d2d;
  margin-bottom: 1rem;
  animation: apparaitre 0.7s ease-out;
}

.sous-titre {
  font-size: 1.1rem;
  color: #666;
  max-width: 600px; /* Empêche le texte d'être trop large */
  line-height: 1.6; /* Meilleure lisibilité */
  animation: apparaitre 0.8s ease-out;
}

.separateur {
  /* Ligne décorative horizontale avec un dégradé */
  width: 80px;
  height: 4px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 2px;
  margin: 2rem 0;
}

.cartes {
  /* Affiche les deux cartes côte à côte avec CSS Grid */
  display: grid;
  grid-template-columns: 1fr 1fr; /* Deux colonnes égales */
  gap: 2rem; /* Espace entre les cartes */
  width: 100%;
  animation: apparaitre 0.9s ease-out;
}

/* Sur mobile, passer les cartes en colonne */
@media (max-width: 600px) {
  .cartes {
    grid-template-columns: 1fr;
  }
  .titre {
    font-size: 1.6rem;
  }
}

.carte {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); /* Ombre légère */
  cursor: pointer; /* Le curseur devient une main au survol */
  transition: transform 0.3s, box-shadow 0.3s; /* Animation douce */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

/* Au survol : la carte se lève légèrement */
.carte:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
}

.carte-icon {
  font-size: 2.5rem;
}

.carte h2 {
  font-size: 1.2rem;
  color: #333;
}

.carte p {
  color: #777;
  font-size: 0.95rem;
  line-height: 1.5;
}

.btn-carte {
  margin-top: 0.5rem;
  padding: 0.65rem 1.4rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-carte:hover {
  opacity: 0.85;
}

/* Couleur violette pour le bouton Ajouter */
.btn-violet {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

/* Couleur bleue pour le bouton Gestion */
.btn-bleu {
  background: linear-gradient(135deg, #2196f3, #0d47a1);
  color: white;
}

/* Animation d'apparition au chargement de la page */
@keyframes apparaitre {
  from {
    opacity: 0;
    transform: translateY(15px); /* Part légèrement du bas */
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
