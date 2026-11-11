# Le Fil Talk — Référence et plan de réception
Date de l'audit : 2026-11-11
Statut : DOCUMENT DE CADRAGE, PAS UNE CERTIFICATION DE L'APK
Périmètre : branche `fluffychat-reprise` uniquement. Aucun changement des autres projets ou du VPS.

## 1. Objectif immuable
Application Android **Le Fil Talk** utilisant **Matrix**, simple pour les adhérents : installation et connexion accessibles, discussions privées et en groupe, notifications push de messages et d'appels quand l'application n'est pas à l'écran, appels audio et vidéo réellement fonctionnels, sécurité conservée, logo rond et identité du Fil. Serveur d'essai : matrix.org. Aucun serveur supplémentaire ne doit être installé sans étude et décision explicite.

## 2. Deux références distinctes — ne pas les confondre

### R0 — Dernière APK de test dont la compilation a été rapportée réussie
- GitHub Actions : exécution numéro **17** du workflow FluffyChat, selon les informations de l'exécution précédemment communiquées.
- Commit source : `b94c821` (abrégé).
- APK annoncée : 48,9 Mo ; SHA-256 rapporté : `fbd98e382695c603e918d9c67e7b94b0776a052e729db70d0a68f6d040d70607`.
- Identifiant : `net.lefil.talk`.
- Signature : clé Android **debug**, donc pas une identité de distribution définitive.
- Essai Samsung rapporté : téléchargement, installation et lancement réussis ; logo et police présents ; problèmes d'avertissements de sécurité et de notifications constatés.
- **Limite de preuve** : cet audit n'a pas re-téléchargé l'APK ni recontrôlé le SHA-256 ; le numéro d'exécution GitHub ne constitue pas son `run_id` REST ; l'essai Samsung n'est pas un procès-verbal complet de messages/appels/notifications.
- Interdiction de qualifier R0 « APK prête pour les adhérents ».

### R1 — Code actuel (non validé fonctionnellement)
- Dépôt : `infolefilodlma-oss/LeFil-Talk`, branche `fluffychat-reprise`.
- Base téléchargée dans le workflow : tag officiel FluffyChat `v2.11.5`.
- Le script `tools/brand_fluffychat.py` personnalise l'identifiant, le logo, Poppins, les intitulés, une route après connexion, le bandeau et une notification de vérification d'appareil.
- Le composant `tools/lefil_banner.dart` ajoute le bandeau « Accueil du Fil ».
- **Non démontré** : compilation et lancement de ce code exact sur Samsung ; non-régression de sa modification des avertissements.
- Le workflow actuel ne comporte pas de commande explicite `flutter analyze` ni `flutter test`, utilise une clé debug, et publie l'APK sous un tag fixe avec `gh release upload --clobber`.
- Le `README.md` historique évoque encore Element X : documentation de la branche non cohérente.

## 3. Tableau de conformité actuel
| Exigence | État probant au 11/11/2026 | Preuve à obtenir |
| --- | --- | --- |
| Installer et démarrer l'APK | Vérifié sur un candidat antérieur, R0 rapporté | Refaire sur candidate finale |
| Logo Le Fil / Poppins | Observés sur R0 | Contrôle sur candidate finale |
| Bandeau violet/rose et lien Accueil | Code R1 seulement | Capture + ouverture du lien sur Samsung |
| Première connexion simple | Non conforme / partiel | Parcours neuf sans écran technique inattendu |
| Messages individuels | Non validé intégralement | Deux comptes, envoi/réception |
| Groupes | Non validé | Groupe à trois, notifications et médias |
| Notifications push | **Bloquant** : alerte constatée, pas de FCM activé dans le workflow | Push réel en arrière-plan, appareil verrouillé et app fermée normalement |
| Appel audio sortant/entrant | Non validé | Deux appareils, micro/sonnerie/raccrochage |
| Vidéo sortante/entrante | Non validé | Deux appareils, caméra et son, Wi-Fi et mobile |
| Sécurité | Non-régression non prouvée | Contrôle cryptographie, appareils, sauvegarde |
| Mise à jour sans perte de comptes | Non démontré ; signature debug | Signature pérenne et essai de mise à jour |
| Compilation automatique | R0 rapportée réussie | Réexécution R1 + vérification fichier exact |
| Livraison aux adhérents | **Interdite** | Réussite de tous les tests obligatoires |

## 4. Architecture : faits vérifiés, points à décider
**Notifications :**
- FluffyChat v2.11.5 possède dans `lib/utils/background_push.dart` une voie FCM conditionnée par la configuration Google et une voie UnifiedPush ; l'absence de FCM peut produire un avertissement.
- La spécification Matrix impose un `pusher` côté client, une passerelle HTTP Matrix push et un fournisseur de notifications : https://spec.matrix.org/latest/push-gateway-api/
- FluffyChat décrit son architecture opérationnelle avec une passerelle et Firebase : https://fluffychat.im/privacy/
- **Décision non prise** : service de distribution push et coûts/maintenance pour une application Android portant un autre package que FluffyChat. Ne pas supposer que le gateway public de FluffyChat accepte l'identité et les jetons de Le Fil Talk.
- Avant tout code FCM : vérifier configuration Android, passerelle compatible avec le même projet, conservation de l'ID pusher, permissions Android 13+, test réel de réception. Aucune désactivation d'alerte en remplacement.

**Appels :**
- Dans FluffyChat v2.11.5, `lib/pages/chat/chat.dart` teste `getLiveKitServiceUrls()` et comporte du code MatrixRTC/LiveKit.
- Matrix annonce les appels 1:1 stables et MatrixRTC expérimental pour FluffyChat : https://matrix.org/ecosystem/clients/fluffychat/
- Le projet FluffyChat annonce MatrixRTC/LiveKit et des appels Android entrants : https://matrix.org/blog/2026/09/11/this-week-in-matrix-2026-09-11/
- **À prouver** : disponibilité réelle des transports RTC sur matrix.org au moment des tests, compatibilité du client compilé, invitation, sonnerie, microphone, vidéo et arrière-plan. Aucune installation VPS implicite.

## 4 bis. Résultat de la première contre-vérification officielle (lecture seule)
- **Appels : piste native étayée.** Le projet FluffyChat annonçait en septembre 2026 l'intégration d'appels MatrixRTC 1:1 et de groupe via LiveKit, avec CallKit Android ; matrix.org était cité comme serveur annonçant MatrixRTC. Source : https://matrix.org/blog/2026/09/11/this-week-in-matrix-2026-09-11/
- **Limite importante :** le catalogue officiel Matrix continue de classer les appels 1:1 comme stables mais MatrixRTC comme **expérimental** pour FluffyChat. Source : https://matrix.org/ecosystem/clients/fluffychat/
- **Implémentation :** le code FluffyChat 2.11.5 inspecté appelle `getLiveKitServiceUrls()` et n'active les appels RTC que si un service est découvert. Aucun test fonctionnel de Le Fil Talk sur deux appareils n'a été réalisé par cet audit.
- **Notifications : architecture identifiée, pas encore déployée.** FluffyChat documente Matrix → passerelle push FluffyChat → FCM → téléphone : https://fluffychat.im/privacy/ ; voir aussi https://spec.matrix.org/latest/push-gateway-api/
- **Décision de méthode :** ne pas ajouter de configuration Firebase, changer de passerelle ni installer LiveKit tant que les paramètres opérationnels d'une chaîne push Le Fil et les essais MatrixRTC n'ont pas été établis. Aucun résultat n'autorise actuellement une diffusion aux adhérents.

## 5. Plan de travail senior à suivre, sans improvisation
**Phase 0 — Gel de référence :**
1. Conserver R0 comme témoin et conserver le SHA et la signature rapportés ; ne pas écraser l'ancien artefact de test sans l'avoir préservé.
2. Relever le commit exact et le run_id de la prochaine compilation qualifiée ; ne pas deviner les identifiants manquants.
3. Ne pas considérer une réussite GitHub Actions comme preuve fonctionnelle sur téléphone.

**Phase 1 — Décisions d'architecture avant modification :**
1. Prouver une solution notifications cohérente de bout en bout (Matrix → passerelle → FCM / autre → Android).
2. Prouver une solution audio/vidéo cohérente avec matrix.org et les dépendances MatrixRTC.
3. Chiffrer coûts, permissions, signatures, responsabilité de maintenance et risques. Aucun nouveau serveur installé sans accord.

**Phase 2 — Durcir la fabrication :**
1. Avant publication, ajouter contrôles statiques, tests automatisés, contrôle des dépendances, identité et signature.
2. Abandonner l'écrasement silencieux d'une APK déjà publiée ; conserver chaque candidate avec commit, version et checksum.
3. Préparer une signature de production pérenne sans exposer de secrets GitHub.
4. Revoir le README obsolète, sans changer les autres branches.

**Phase 3 — Réception réelle :**
1. Deux appareils et deux comptes ; essai complet des messages, groupes, appels et notifications.
2. Premier lancement par un non-technicien ; sécurité et accessibilité.
3. Installation neuve et mise à jour de la version précédente.
4. Livrer seulement si tous les critères obligatoires sont réussis ; sinon garder l'APK en test.

## 6. Règles permanentes
- Toute modification : hypothèse démontrée, fichiers visés, sauvegarde/retour arrière, tests ciblés **et** tests de non-régression, preuve effective.
- À la première anomalie introduite : arrêter, restaurer si sûr, vérifier, ne plus modifier avant nouvelle décision.
- Ni Agora, ni Atrium, ni VPS, ni autres branches.
- Pas de compilation supplémentaire sans changement utile et sans motif de contrôle.
- L'utilisateur ne réalise que les actions non automatisables : accès à comptes externes et essais de réception sur Samsung.
- **Interdiction de présenter comme « terminé » ce qui est seulement préparé ou compilé.**

## 7. Prochaine action autorisée
Effectuer une étude de faisabilité **en lecture seule** de l'architecture notifications et appels. Ne programmer aucune correction de ces fonctions tant que leurs dépendances ne sont pas validées. Ensuite seulement, préparer une unique intervention maîtrisée sur la chaîne CI, avec non-régression.
