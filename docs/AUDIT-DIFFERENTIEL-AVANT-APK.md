# Le Fil Talk — audit différentiel avant APK

Date : 2026-11-11

## Périmètre et références

- Dépôt : `infolefilodlma-oss/LeFil-Talk`
- Branche : `element-x-matrixorg-reprise`
- Base prévue : Element X Android `v26.10.1`
- Preuve de compilation principale : GitHub Actions `43063330080`
- Commit de référence du dépôt local : `690c346ccd34fff3efbe7be5344cc17add4c245c`
- État avant audit : modification locale existante de `tools/apply_lefil_welcome.py`, issue de la microétape 1.3

Cet audit ne compile pas, ne publie pas et ne modifie aucune source Android ni aucun workflow.

## Matrice différentielle

| Exigence | Attendu | Réellement intégré au build | Preuve | Écart | Gravité |
|---|---|---|---|---|---|
| Nom de l’application | `Le Fil Talk` sans suffixe visible | Oui dans le build FCM de référence | Run `43063330080`, contrôle `application-label:'Le Fil Talk'` | Aucun sur cette preuve | CONFORME |
| Identifiant Android | Identité Le Fil Talk cohérente | Oui pour le build FCM | Run `43063330080`, paquet `net.lefil.talk.debug` | Le paquet de production pérenne n’est pas défini | À CORRIGER |
| Logo rond officiel | `LogoLeFilTalk.png` dans le lanceur et l’onboarding | Logo et icônes traités par `apply_visual_brand.py` | Script exécuté dans `43063330080`; PNG local 1254×1254 | Capture réelle absente ; onboarding corrigé mais non exécuté dans ce run | BLOQUANT |
| Poppins | Police embarquée et visible dans les écrans concernés | Script exécuté | `apply_poppins.py` appelé dans `43063330080` | Aucun rendu, contraste ou licence vérifié visuellement | BLOQUANT |
| Bleu `#0C1853` | Couleur de marque appliquée | Script exécuté | `apply_theme_colors.py` appelé dans `43063330080` | Couverture et rendu clair/sombre non prouvés | À CORRIGER |
| Prune `#4A0050` | Couleur de marque appliquée | Script exécuté pour le thème/splash | `apply_theme_colors.py` et `apply_visual_brand.py` appelés | Capture et contraste non prouvés | À CORRIGER |
| Accueil « Bienvenue sur Le Fil » | Accueil personnalisé réellement compilé | Non dans `43063330080` | `apply_lefil_welcome.py` absent du workflow FCM | Le script modifié 1.3 n’a pas encore produit d’APK | BLOQUANT |
| Création de compte prioritaire | « Je crée mon compte gratuit » → `onCreateAccount()` | Non démontré dans un build | Appel présent seulement dans le script local 1.3 | Pas d’APK ni test UI correspondant | BLOQUANT |
| Connexion existante | « J’ai déjà un compte » avec flux natif | Non démontré dans un build | Script local 1.3 conserve `onSignIn`/`OnSignIn` | Test de compte existant absent | BLOQUANT |
| QR et connexion manuelle | Restent accessibles dans le parcours connexion | Non démontré dans un build | Présents dans le script 1.3, non exécuté par le workflow FCM | Tests UI absents | À CORRIGER |
| Deuxième compte matrix.org | `prompt=create`, sans effacer une session | Mécanisme Element X intact ; parcours UI non intégré au build de référence | `OAuthPrompt.Create` dans v26.10.1 et metadata matrix.org | Test réel avec session navigateur existante absent | BLOQUANT |
| Identité OAuth | Nom/logo/site/légal cohérents | Nom contrôlé ; logo/site/légal non configurés | `OAuthConfig.kt`, `BuildTimeConfig.kt`; site `le-fil.net` retournait 503 | URLs publiques indispensables non disponibles et non intégrées | BLOQUANT |
| Retour navigateur Android | Retour natif OAuth fonctionnel | Non testé | Code natif conservé ; aucun test appareil | Preuve de callback absente | BLOQUANT |
| Aide débutant | Explications non bloquantes, récupération et clé de récupération | `apply_signup_help.py` n’est pas appelé par `43063330080` | Workflow FCM : aucun appel | Aide non intégrée à l’APK de référence | BLOQUANT |
| Mot de passe oublié | Renvoi officiel, sans collecte locale | Non intégré/démontré | Spécification seulement dans `docs/PARCOURS-INSCRIPTION-MATRIX-ORG.md` | URL et écran réel non vérifiés | À CORRIGER |
| Chiffrement et clé de récupération | Mécanismes natifs conservés et compréhensibles | Mécanismes amont non modifiés | Workflow et scripts ne patchent pas le SDK Matrix | Tests de récupération et second appareil absents | NON VÉRIFIÉ |
| Accueil connecté | Accès Papote, Sentiers, Oasis | Non dans `43063330080` | `apply_lefil_navigation.py` absent du workflow | Script non intégré | BLOQUANT |
| Véritables espaces Matrix | Identifiants réels confirmés | Non | `docs/REPRISE-QUALITE-LEFIL-TALK.md` indique qu’ils ne sont pas fournis | Navigation ne peut pas être validée | BLOQUANT |
| Discussions / contacts / profil | Navigation native cohérente avec Atrium | Non démontré | Prototype `preview/TalkVisualPreview.kt` explicitement non probant | Pas de capture Element X réelle | À CORRIGER |
| Messages individuels et collectifs | Envoi/réception synchronisés | Non testé | Aucun test de deux comptes | Fonction native seulement présumée conservée | NON VÉRIFIÉ |
| Images et pièces jointes | Fonctions natives conservées | Non testé | Aucun test appareil | Absence de preuve fonctionnelle | NON VÉRIFIÉ |
| Synchronisation Atrium ↔ Android | Même compte et messages synchronisés | Non testé | Aucun essai croisé | Absence de preuve fonctionnelle | BLOQUANT |
| Appels audio/vidéo | Entrants/sortants et permissions | Non testé | `docs/REPRISE-QUALITE-LEFIL-TALK.md` le classe non vérifié | Aucun appareil ni second compte testé | NON VÉRIFIÉ |
| Notifications FCM | Configuration Le Fil et passerelle validées | Configuration patchée dans un build FCM | Run `43063330080`, Firebase et gateway contrôlés | Réception réelle et Sygnal non prouvées | BLOQUANT |
| Accessibilité | Contraste, tailles, petits écrans, mode sombre | Non démontré | Aucun screenshot ni test UI réel | Validation visuelle absente | BLOQUANT |
| Scripts de personnalisation | Tous les scripts utiles appliqués dans un ordre contrôlé | Partiel | `43063330080` appelle `brand_candidate`, `apply_visual_brand`, `apply_poppins`, `apply_theme_colors` | N’appelle pas welcome/navigation/signup | BLOQUANT |
| Compatibilité combinée | Transformations appliquées aux vrais fichiers v26.10.1 | Partielle | Test temporaire combiné welcome + signup réussi ; aucun build | `apply_visual_brand`/theme/Poppins non combinés dans ce contrôle | À CORRIGER |
| Ressources référencées | Logo et polices présentes aux chemins utilisés | Partiel | Script de marque crée `onboarding_logo`; preview séparée | Ressource finale dans APK non contrôlée | À CORRIGER |
| CI précompilation | Bloquer une source ou un script invalide | Oui pour les contrôles présents | `tools/preflight_lefil_talk.py` vérifie syntaxe, logo, workflow et chemins | Ne vérifie pas l’intégration effective de welcome/navigation/signup | À CORRIGER |
| Installation et démarrage | APK de la même exécution installée, PID et captures | Prévu, pas prouvé pour `43063330080` | `element-x-candidate.yml` et `android_smoke.sh` le prévoient | Le run de référence FCM n’est pas ce pipeline Android smoke | BLOQUANT |
| Signature | Signature contrôlée | Oui pour le build FCM debug | `apksigner verify` réussi dans `43063330080` | Pas de clé de distribution pérenne | BLOQUANT |
| Mise à jour | Installation par-dessus et conservation de session | Non testé | Aucun test d’upgrade | Absence de preuve | NON VÉRIFIÉ |
| Publication | Interdite avant validation humaine | Workflows de publication existants | `publish-*.yml` peuvent publier des préversions | Garde-fou documentaire, pas une autorisation de release | À CORRIGER |

## Scripts réellement appelés

Le workflow `element-x-gplay-fcm.yml` utilisé par `43063330080` appelait, dans cet ordre :

1. `brand_candidate.py`
2. `apply_visual_brand.py`
3. `apply_poppins.py`
4. `apply_theme_colors.py`
5. `ci/prepare_elementx_fcm.py`

À la suite de cette microétape, les workflows candidats appellent désormais, dans cet ordre :

1. `brand_candidate.py`
2. `apply_visual_brand.py`
3. `apply_poppins.py`
4. `apply_theme_colors.py`
5. `apply_lefil_welcome.py`
6. `apply_signup_help.py`
7. `apply_lefil_navigation.py`

Cette correction est présente dans `element-x-candidate.yml` et `element-x-gplay-fcm.yml`. Le déclenchement du workflow FCM inclut maintenant `tools/**` et `LogoLeFilTalk.png`.

Le workflow `talk-brand-apk.yml` reste une chaîne historique distincte : il appelle `brand_candidate.py`, `apply_visual_brand.py` et `apply_signup_help.py`, contient une publication de préversion et ne doit pas être utilisé comme preuve de l’APK candidate complète.

## Contradictions et documents à actualiser

- `docs/IDENTITE-VISUELLE-TALK-ANDROID.md` indique que le logo est intégré, mais précise que Poppins, thème complet, captures et mise en page ne sont pas validés.
- `docs/PARCOURS-INSCRIPTION-MATRIX-ORG.md` décrit une spécification validée sur le principe mais explicitement non implémentée.
- `docs/REPRISE-QUALITE-LEFIL-TALK.md` conserve des diagnostics historiques et confirme l’absence de tests réels.
- Le prototype `preview/TalkVisualPreview.kt` ne doit pas être utilisé comme preuve de l’APK.
- L’identité OAuth Le Fil Talk ne peut pas être finalisée tant que des URL HTTPS publiques du site, du logo et des documents légaux ne sont pas vérifiables.

## Corrections nécessaires, dans l’ordre

1. Stabiliser les URL publiques HTTPS : logo, présentation, confidentialité et conditions.
2. Ajouter une chaîne de patch candidate unique et ordonnée : identité, visuel, Poppins, thème, accueil, aide d’inscription, navigation.
3. Ajouter un contrôle de transformation sur les vrais fichiers Element X v26.10.1, avec liste exacte des fichiers modifiés et retour arrière automatique.
4. Ajouter des contrôles CI bloquants pour vérifier les textes, les boutons, les ressources et les appels OAuth attendus.
5. Vérifier les espaces Matrix réels avant de présenter Papote, Sentiers et Oasis comme fonctionnels.
6. Compiler une unique APK candidate après validation de ces contrôles.
7. Installer cette même APK sur un téléphone, puis tester inscription, deuxième compte, connexion existante, chiffrement, messages, espaces, appels, notifications et mise à jour.
8. Comparer les captures et journaux à cette matrice avant toute publication.

## Tests automatiques manquants

- Test de présence et d’ordre des scripts dans le workflow final.
- Test de transformation de `OnBoardingView.kt` sur la source réelle v26.10.1.
- Test de transformation de `HomeView.kt` et `HomeSpacesView.kt` sans conflit Kotlin.
- Test des textes et actions `Je crée mon compte gratuit` / `J’ai déjà un compte`.
- Test statique `onCreateAccount` → `isAccountCreation=true` → `OAuthPrompt.Create`.
- Test de présence du logo et de Poppins dans l’APK finale.
- Test de ressources clair/sombre et de contraste.
- Test d’installation, démarrage et capture sur Android de la même exécution.
- Test fonctionnel à deux comptes pour messages, chiffrement et synchronisation Atrium.
- Test appels audio/vidéo, notifications arrière-plan et écran verrouillé.
- Test d’installation par-dessus une version précédente.

## Critères d’autorisation d’une APK candidate

Une unique APK candidate pourra être autorisée seulement si :

- la chaîne complète de scripts est appliquée aux sources Element X v26.10.1 sans fichier inattendu ;
- le paquet, le nom, le logo, Poppins, les couleurs et les écrans d’accueil sont contrôlés ;
- les URL OAuth publiques et légales sont vérifiées ;
- `prompt=create`, la connexion existante et le retour Android sont testés ;
- l’aide débutant et la récupération des clés sont testées sans contournement de sécurité ;
- les vrais espaces Papote, Sentiers et Oasis sont confirmés ;
- l’APK est installée et démarrée sur téléphone réel, avec captures et journaux ;
- les messages, pièces jointes, chiffrement, appels, notifications et synchronisation Atrium sont testés ;
- signature, mise à jour et retour arrière sont vérifiés ;
- aucun écart BLOQUANT ou NON VÉRIFIÉ ne subsiste sans décision explicite du commanditaire.

## Résultats de correction de l’audit

Écarts automatiquement corrigeables traités :

- ajout de `apply_lefil_welcome.py` au workflow candidate ;
- ajout de `apply_signup_help.py` après l’accueil ;
- ajout de `apply_lefil_navigation.py` après l’aide ;
- ajout du contrôle préflight de présence et d’ordre des sept patches ;
- ajout des chemins `tools/**` et `LogoLeFilTalk.png` au déclenchement FCM ;
- vérification combinée des transformations sur les fichiers réels Element X v26.10.1 dans un répertoire temporaire.

Preuves exécutées :

- `python3 tools/preflight_lefil_talk.py` : réussi ;
- validation YAML des deux workflows : réussie ;
- application combinée welcome + signup_help + navigation sur les sources v26.10.1 : réussie ;
- contrôle statique `OAuthPrompt.Create` conservé : réussi ;
- `git diff --check` : réussi.

Ces preuves valident la chaîne de scripts et le workflow, pas une APK. Aucun build ni test appareil n’a été exécuté.

Écarts restant ouverts :

- URL OAuth publiques et légales non vérifiées ;
- rendu visuel et accessibilité non capturés ;
- inscription, deuxième compte, retour navigateur et clés non testés sur appareil ;
- vrais espaces Matrix non fournis ;
- messages, pièces jointes, synchronisation Atrium, appels et notifications non testés ;
- signature de distribution, mise à jour et retour arrière de l’APK non testés.

## Décision

**APK BLOQUÉE.**

Les scripts essentiels d’accueil, d’aide à l’inscription et de navigation ne sont pas intégrés dans la compilation de référence. Les parcours réels, la synchronisation, les appels, les notifications, l’accessibilité et l’installation sur téléphone ne sont pas démontrés. Aucune nouvelle compilation ni publication ne doit être lancée avant correction et validation des écarts bloquants.

## Vérification complémentaire des URL officielles — microétape 1.5

Vérification effectuée le 2026-11-11, sans modification du site :

| URL | Preuve | Résultat |
|---|---|---|
| `https://le-fil.net/` | `curl -L` et accès navigateur retournent HTTP `503 Service Unavailable`, réponse 416 octets | Accessibilité non démontrée ; impossible de distinguer une panne temporaire d’une page inexistante |
| `https://le-fil.net/mentions/` | `curl -L` et accès navigateur retournent HTTP `503 Service Unavailable`, réponse 416 octets | Contenu légal et politique de confidentialité non examinables |
| Logo public du dépôt | `https://raw.githubusercontent.com/infolefilodlma-oss/LeFil-Talk/element-x-matrixorg-reprise/LogoLeFilTalk.png`, HTTP 200, PNG 1254×1254, SHA-256 `813b78bb290474d416705ff2a1aa1ca930a7bff27581343f667d3b271ce89b7c` | Actif vérifié, mais hébergé sur `raw.githubusercontent.com`, pas sur `le-fil.net` |

Aucune constante OAuth n’a été modifiée. L’URL GitHub du logo n’est pas retenue comme valeur finale : l’implémentation Element X exige que l’hôte de `logoUri` corresponde à celui de `clientUri`, et le site `le-fil.net` reste indisponible. La présentation de l’application, la politique de confidentialité et les conditions d’utilisation ne sont donc pas vérifiées.

Le blocage OAuth de l’audit reste ouvert jusqu’au retour HTTP normal du site et à la vérification du contenu de `/mentions/`. Les modifications 1.3, les sessions, les clés et le SDK Matrix restent inchangés.

## Validation précompilation — résultat

Écarts corrigeables automatiquement traités :

- les workflows candidats appliquent maintenant les sept scripts dans l’ordre contrôlé ;
- `tools/verify_lefil_transformations.py` vérifie le contenu produit, les textes, le logo généré, Poppins, les couleurs, la navigation et l’absence de modification des modules Matrix/Rust, appels et notifications ;
- le préflight vérifie la présence du vérificateur et l’ordre complet avant toute compilation.

Preuves :

- `python3 tools/preflight_lefil_talk.py` : réussi ;
- copie temporaire complète d’Element X v26.10.1 : sept transformations appliquées, vérificateur réussi ;
- YAML de tous les workflows : valide ;
- syntaxe du vérificateur : valide ;
- `git diff --check` : réussi.

Cette validation démontre la transformation des sources, pas le fonctionnement de l’APK. Restent NON VÉRIFIÉS : rendu sur téléphone, inscription matrix.org avec session existante, retour navigateur, chiffrement et clé de récupération, messages, espaces réels, synchronisation Atrium, appels, notifications, accessibilité et mise à jour.

Décision de précompilation : **AUTORISATION TECHNIQUE D’UNE COMPILATION DE TEST UNIQUEMENT**, après validation humaine de cette microétape. Cette autorisation ne vaut ni validation fonctionnelle, ni autorisation de distribution.

## Inventaire des mauvaises surprises avant APK

### Différentiel local / distant

- Branche locale : `element-x-matrixorg-reprise`.
- HEAD local : `690c346ccd34fff3efbe7be5344cc17add4c245c`.
- HEAD distant vérifié par `git ls-remote` : `690c346ccd34fff3efbe7be5344cc17add4c245c`.
- Aucun commit local supplémentaire n’existe.
- Les corrections annoncées sont uniquement dans l’arbre de travail local : quatre fichiers suivis modifiés et deux fichiers non suivis.
- Les fichiers non transmis sont : `.github/workflows/element-x-candidate.yml`, `.github/workflows/element-x-gplay-fcm.yml`, `tools/apply_lefil_welcome.py`, `tools/preflight_lefil_talk.py`, `tools/verify_lefil_transformations.py` et ce document d’audit.
- La branche distante ne contient donc pas encore le workflow corrigé ni le vérificateur.

Une future compilation GitHub déclenchée sur la branche distante actuelle n’utiliserait pas ces corrections locales. Il faut d’abord enregistrer et transmettre les fichiers, puis vérifier le nouveau commit distant avant toute compilation.

### Inventaire des 17 risques

| Risque | Preuve disponible | Test manquant | Statut |
|---|---|---|---|
| Identité OAuth | Le code natif transmet nom, logo et URL au fournisseur ; les corrections OAuth ne sont pas transmises | Métadonnées et page OAuth réelles avec identité Le Fil Talk | BLOQUANT |
| Inscription matrix.org | `prompt=create` confirmé dans le code v26.10.1 et les métadonnées matrix.org | Création réelle d’un compte depuis l’APK | BLOQUANT |
| Deuxième compte | `OAuthPrompt.Create` existe ; aucune APK corrigée disponible à distance | Création avec une session navigateur d’un autre compte | BLOQUANT |
| Retour navigateur | Redirect URI natif conservé dans Element X | Retour Android après OAuth, application froide et reprise de session | BLOQUANT |
| Sécurité et clés | SDK Matrix et chiffrement non modifiés | Sauvegarde, récupération et vérification des appareils | BLOQUANT |
| Logo | PNG officiel vérifié localement, script de marque présent | Capture de l’APK corrigée sur téléphone | BLOQUANT |
| Poppins | Script local appliqué avec succès sur une copie v26.10.1 | Présence et lisibilité dans l’APK finale, clair/sombre | BLOQUANT |
| Couleurs | Scripts locaux produisent les tokens attendus | Contraste et rendu réel sur petits écrans | À CORRIGER |
| Espaces Papote/Sentiers/Oasis | Script local ajoute la navigation native et le filtrage | Vérification des espaces existants avec compte réel | BLOQUANT |
| Salons réels | Les identifiants réels ne sont pas fournis | Ouverture de chaque espace réel | BLOQUANT |
| Synchronisation Atrium | Architecture Matrix commune documentée | Message envoyé sur Atrium puis reçu sur Android, et inversement | BLOQUANT |
| Messages et pièces jointes | Fonctions Element X natives conservées en théorie | Messages individuels/collectifs, images et pièces jointes | NON VÉRIFIÉ |
| Appels audio/vidéo | Aucun code d’appel modifié | Appels entrants/sortants avec permissions | NON VÉRIFIÉ |
| Notifications | Configuration FCM et passerelle contrôlées statiquement dans le run 43063330080 | Réception ouverte, arrière-plan et écran verrouillé | BLOQUANT |
| Accessibilité | Aucun contrôle visuel final | Contraste, tailles, TalkBack, clavier et petits écrans | BLOQUANT |
| Mise à jour | Aucun test d’upgrade | Installation par-dessus une version précédente et conservation de session | BLOQUANT |
| Démarrage et installation | Smoke test prévu dans un workflow différent ; APK corrigée non compilée | Installation, lancement, PID, capture et logs de la même APK | BLOQUANT |

### Conditions avant demande d’installation

1. Enregistrer les six fichiers locaux modifiés ou ajoutés dans un commit traçable, sans écraser les travaux existants.
2. Transmettre ce commit sur `element-x-matrixorg-reprise` avec autorisation explicite.
3. Vérifier que `git ls-remote` pointe sur le commit contenant les workflows corrigés.
4. Vérifier dans GitHub Actions que le workflow distant contient les sept scripts et `verify_lefil_transformations.py`.
5. Exécuter le préflight distant et le vérificateur de contenu sur Element X v26.10.1.
6. Vérifier l’artefact, le paquet, le nom, la signature et le SHA-256.
7. Installer l’APK issue de cette même exécution sur un téléphone réel.
8. Capturer l’accueil, le logo, Poppins, les couleurs et les écrans OAuth.
9. Tester inscription, deuxième compte, compte existant et retour navigateur.
10. Tester chiffrement, clé de récupération et vérification d’un second appareil.
11. Tester espaces réels, messages, pièces jointes et synchronisation Atrium.
12. Tester appels, permissions et notifications hors application.
13. Tester accessibilité, petits écrans, mode sombre et erreurs compréhensibles.
14. Tester la mise à jour par-dessus une version précédente.
15. Comparer les preuves à cette matrice et obtenir une validation humaine explicite.

Décision mise à jour : **APK BLOQUÉE**. Les corrections locales passent les contrôles statiques, mais elles ne sont pas enregistrées dans un commit ni présentes sur la branche distante. Aucune compilation, publication ou demande d’installation n’est autorisée à ce stade.
