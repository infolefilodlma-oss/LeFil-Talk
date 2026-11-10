# Le Fil Talk — garde-fous de développement (branche element-x-matrixorg-reprise)

Ce fichier s'adresse aux agents et aux développeurs. **Les mots ici ne sont pas une preuve de validation** : `.github/workflows/element-x-candidate.yml` exécute des contrôles bloquants.

## Périmètre
- Dépôt unique : `infolefilodlma-oss/LeFil-Talk`. Ne pas modifier LeFil-FDroid, le VPS, les sites ni les autres dépôts.
- Source amont : Element X Android `v26.10.1`; garder les fonctions natives Matrix, notifications, appels et inscription `matrix.org`.
- Interface prévue : nom visible exact **Le Fil Talk**, logo officiel rond `LogoLeFilTalk.png`, Poppins, couleurs #0C1853 et #4A0050, accueil Le Fil, Papote / Sentiers / Oasis.
- Ne jamais inventer de salons, d'alias Matrix ou de preuves de fonctionnement. Les vrais salons restent à confirmer.

## Obligations avant toute modification
1. Lire ce fichier, `docs/REPRISE-QUALITE-LEFIL-TALK.md`, puis le workflow et les derniers logs pertinents. Ne pas rediagnostiquer un fait déjà confirmé.
2. Identifier un défaut démontré et son **test de reproduction**, le changement minimal et la marche arrière.
3. Avant tout build Android : `python3 tools/preflight_lefil_talk.py`. Toute erreur bloque la compilation. Tester la syntaxe et les chemins avant un émulateur.
4. Une correction = une cause. Ne pas reconstruire l'APK lorsqu'un correctif ne concerne que le test ou la livraison ; réutiliser l'artefact déjà validé.
5. Après deux échecs comparables, **arrêter les nouvelles tentatives répétitives** et changer de diagnostic. Ni boucles de compilations ni changements aveugles de version Android.

## Réception / interdictions
- Aucun succès déclaré sur une compilation seule. Exiger l'identité et la signature de l'APK, l'installation, le lancement, une capture, les logs et les essais des fonctions exigées.
- Aucun `gh release` automatique à partir du workflow de diagnostic : APK de test **non publiable** tant que les tests réels, la signature de distribution et le lien direct ne sont pas validés.
- Vérifier les fonctions natives et les interfaces déjà acquises à chaque modification. Une absence de test est une limite, pas une réussite.
- Ne pas pousser de modifications hors périmètre, ne pas écraser d'autres branches. Garder une reprise possible par retour au commit précédent.

## Suivi de vérité
Documenter dans `docs/REPRISE-QUALITE-LEFIL-TALK.md` les faits observés, les limites et les échecs encore ouverts. Une preuve est un identifiant GitHub Actions / log / artefact, pas une affirmation.
