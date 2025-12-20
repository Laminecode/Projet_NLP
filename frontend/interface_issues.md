Problèmes identifiés dans `frontend/interface.tsx`

Résumé
------
Ce document liste les problèmes détectés dans `frontend/interface.tsx`, leur gravité, exemples de reproduction 

Problèmes identifiés dans `frontend/interface.tsx`

Résumé
------
Ce document liste les problèmes détectés dans `frontend/interface.tsx`, leur gravité, exemples de reproduction et lignes concernées.

Problèmes actuels identifiés dans `frontend/interface.tsx` (liste sans solutions)

1) Base API codée en dur
- Ligne : 5

2) `fetchData` — validation / gestion des erreurs (points de contrôle)
- Début de la fonction `fetchData`: ligne 127
- Vérification `response.ok` et validation `data === null/undefined`: lignes 132–139
- Construction du message d'erreur et `setError`: ligne 148

3) Points d'appel pour chargement des données
- Déclaration de `loadAllData`: ligne 157
- Appels `fetchData<...>` (liste de endpoints dans `Promise.all`): lignes 161–179

4) Réinitialisation / affichage de l'erreur
- `setError(null)` après début du chargement: ligne 159
- Bouton de fermeture de l'alerte d'erreur (reset): ligne 295

5) Conversions et formatage numérique
- Déclaration de `safeToFixed`: lignes 236–240
- Principales utilisations de `safeToFixed` dans le rendu (labels, TF-IDF, z-scores, pourcentages, scores): lignes 364, 463, 479, 498, 510, 615, 629, 649, 663

6) Rendus conditionnels (présence des guards pour les données)
- Vue d'ensemble conditionnelle (`overview`): ligne 320
- Onglet `lexical`: ligne 399
- Onglet `sentiment`: ligne 584
- Guard `sentimentScores && (...)`: ligne 606
- Onglet `bias`: ligne 681

7) Emplacement des types / interfaces
- Déclarations d'interfaces TypeScript (en-tête du fichier): lignes 7–86

Note: Ce document liste uniquement les points observables et leurs emplacements dans le fichier `frontend/interface.tsx`. Aucune solution ou correction n'est fournie ici.














