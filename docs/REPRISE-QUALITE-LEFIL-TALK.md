# Reprise qualité — Le Fil Talk

## Références et décisions acquises
- Dépôt : `infolefilodlma-oss/LeFil-Talk`, branche `element-x-matrixorg-reprise`.
- Base Android : `element-hq/element-x-android` tag `v26.10.1`; serveur public `matrix.org`.
- Interface demandée : nom **Le Fil Talk** sans suffixe visible, logo rond officiel, Poppins, bleu #0C1853, prune #4A0050, accueil et accès Papote / Sentiers / Oasis.
- Préserver les fonctions natives Element X (messages, notifications, appels, inscriptions). Les identifiants réels de salons ne sont pas fournis ; aucune preuve d'accès aux salons réels.
- `tools/brand_candidate.py` et les autres scripts sont des patches de l'amont cloné pendant le workflow. Ne pas remplacer l'amont ni reconstruire une messagerie.

## Diagnostics déjà vérifiés
- Exécution `42822433303` : compilation et vérifications APK réussies, **pas** un test de démarrage.
- Exécution `42822472133` : échec du job Android 14 lors du `test -s "$APK"` **avant installation**. La runner exécutait des lignes de `script:` dans des shells séparés : la variable shell n'était pas conservée. Ce résultat n'est **pas** une preuve de crash Android.
- Commit `6a4f01e2` : chemin de l'APK rendu explicite. Contrôle d'efficacité en attente au moment de cette rédaction (exécution `42826659679` en cours).
- Prévention ajoutée : désormais le script Android est **un fichier shell unique**, exécuté par une seule commande, syntaxiquement contrôlé avant compilation ; les chemins de l'APK sont testés dans la prévalidation.

## Pipeline attendu
1. `preflight` rapide : contrôles des sources, des scripts et des chemins de l'APK ; blocage si erreur.
2. `compile` conditionné au succès du précontrôle : APK, signature, identité et étiquette **Le Fil Talk**.
3. `android-test` conditionné à la compilation : installation et démarrage de l'APK de la **même** exécution, PID, capture et journaux.
4. Publication **distincte et interdite** par ce workflow. Une APK de test n'est pas une release approuvée.

## Ce qui n'est pas vérifié
- Tests sur un téléphone réel ; parcours complet d'inscription/connexion `matrix.org`.
- Qualité des écrans, navigation Papote / Sentiers / Oasis vers les vrais salons.
- Réception et émission de messages, notifications hors application, appels.
- Clé pérenne de signature, mise à jour d'une APK installée, distribution finale.

**Ne pas remplir ces cases sans des preuves réelles.** En cas d'échec, conserver les logs, identifier la cause, restaurer si nécessaire. Aucun compte rendu ne vaut un test.
