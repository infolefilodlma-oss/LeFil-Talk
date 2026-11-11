# Le Fil Talk — Protocole d'autocontrôle obligatoire

## Principe
Aucune annonce d'amélioration sans une preuve correspondant exactement à la version considérée.
Les états du code, de la compilation, de l'APK et du fonctionnement Android sont DISTINCTS.
Une capture antérieure ne prouve JAMAIS une version nouvelle.

## Étapes de travail, dans l'ordre
1. **État initial** — relever commit SHA, workflow/run, APK et anomalie; identifier la dernière version réellement testée. Documenter les fonctions à préserver.
2. **Périmètre** — écrire UNE modification attendue et les fichiers touchés; vérifier la compatibilité avec les Espaces, menus, messages, chiffrement, notifications et appels natifs. Ne pas modifier les autres services.
3. **Prévention** — vérifier les ancrages dans FluffyChat 2.11.5, préparer le rollback vers le commit antérieur et les critères de test avant toute écriture.
4. **Modification** — effectuer le changement minimal; vérifier le diff, les textes intacts et les fonctions non concernées. Aucune conclusion visuelle à ce stade.
5. **Compilation** — identifier le run lié au NOUVEAU commit SHA; vérifier sa conclusion, les journaux, le nom Android, la signature et le SHA-256 de l'APK. Une compilation réussie ne signifie pas qu'une fonction marche.
6. **Essai réel** — tester l'APK correspondant au même SHA sur Android : accueil, lisibilité, accès au menu, Espaces, salons, messages, notifications appareil fermé, appels audio/vidéo avec un correspondant, déchiffrement et reconnexion. Distinguer « testé » et « non testé ».
7. **Décision** — n'écrire « corrigé et vérifié » que si le test de la fonction et la non-régression sont démontrés. Sinon : « code modifié », « compilé » ou « non validé », précisément.
8. **Anomalie** — arrêter les changements, restaurer l'état précédent du code, vérifier la restauration et ne pas prétendre restaurer les données de téléphone. Reprise uniquement après nouvelle décision motivée.

## Règles de preuve
- Toute comparaison visuelle : deux captures IDENTIFIÉES (ancienne version / nouvelle version), à écran et contexte comparables.
- Ne jamais décrire une ancienne capture comme une preuve de la nouvelle APK.
- Chaque livraison : lien exact, commit SHA, run ID, résultat des essais, défauts restants.
- Les notifications et appels sont OBLIGATOIRES; ne pas cacher un défaut pour faire croire au fonctionnement.
- Aucune publication comme version destinée aux adhérents si une obligation reste non validée.
- Si une preuve manque, le statut est **NON VÉRIFIÉ**, jamais « OK ».
- Aucun rapport long : synthèse opérationnelle de quelques lignes, avec preuve.

## Référence
Base FluffyChat 2.11.5, branche `fluffychat-reprise`; garder les fonctions natives Matrix (Espaces, salons, chiffrement, appels et menus) et l'identité Le Fil Talk. Ne pas toucher à Agora, Atrium web, VPS ou autres branches dans ce chantier.


## Références techniques obligatoires (lues le 11/11/2026)
- FluffyChat officiel : https://fluffy.chat/faq/ (UnifiedPush/ntfy) et https://fluffy.chat/ (notifications, Espaces, appels expérimentaux).
- Code source figé v2.11.5 : https://github.com/krille-chan/fluffychat/blob/v2.11.5/lib/utils/background_push.dart (le booléen `firebaseEnabled = false` déclenche l'alerte si aucun distributeur UnifiedPush n'est disponible).
- Architecture push publiée par FluffyChat : https://fluffychat.im/privacy/ (serveur Matrix -> passerelle push -> Firebase -> appareil). **FCM dans l'APK seul n'est pas une solution** : projet Firebase et passerelle compatibles nécessaires.
- Matrix, spécification de référence : https://spec.matrix.org/latest/client-server-api/ (E2EE optionnel selon les salons, protections des clés et recommandations de vérification).
- Capacités officielles : https://www.matrix.org/ecosystem/clients/fluffychat/ (appels 1:1, Espaces ; MatrixRTC expérimental).
- Toute décision importante doit citer une référence technique et, si nécessaire, être corroborée par un problème/REX reproductible upstream avant l'implémentation ; ne pas confondre témoignage et preuve.

## REX : défauts réellement observés le 11/11/2026
1. Versions 30/34 : de nombreux liens GitHub / ChatGPT ont bloqué sur Samsung ; version 34 finalement installée, preuve : capture 15:44 de l'application. **Ne pas rouvrir ce diagnostic à zéro ni prétendre que les liens sont fiabilisés.**
2. Accueil version 34 : logo rond visible, texte intégral et lisible. **Gel de l'accueil : aucune modification sans nouvelle régression constatée.**
3. Notifications version 34 : fenêtre « Notifications indisponibles » confirmée ; workflow sans intégration Firebase et code upstream non activé. **Aucune suppression cosmétique de l'alerte.**
4. Connexion version 34 : liste multiserveurs et descriptions anglaises, alors que matrix.org a été retenu.
5. Parcours crypto version 34 : écrans de restauration, réinitialisation et phrase de passe imposés. **Décision utilisateur : ne pas imposer le chiffrement/configuration crypto au premier accès.** Conserver E2EE disponible ultérieurement et les clés existantes ; ne jamais réinitialiser les comptes ou supprimer la sécurité.
6. Vidéo version 30 : écran caméra ouvert ; **cela ne prouve pas l'établissement d'un appel**, l'audio bidirectionnel, la réception en arrière-plan ni l'interopérabilité.

## Plan de tests opérationnel — ordre verrouillé
A. **Avant correction** : pour chacun des points, citer lignes de source v2.11.5, documentation officielle et REX ; formuler hypothèse falsifiable, correctif minimal, tests avant/après, rollback. L'absence d'une des trois preuves bloque l'écriture du correctif.
B. **Push** : obtenir une architecture entièrement fonctionnelle (FCM + passerelle autorisée et correctement configurée, OU UnifiedPush automatique sans installation manuelle pour l'adhérent). Vérifier tokens, enregistrement de pusher Matrix, réception de message appli fermée/écran verrouillé et après redémarrage. Aucune promesse avant ces tests. Ne pas réutiliser aveuglément la passerelle Firebase d'un autre projet.
C. **Connexion** : serveur matrix.org présélectionné mais bouton « Créer mon compte » toujours accessible. Tester nouvelle inscription, compte existant, réouverture de session. Ne pas détruire l'option serveur alternatif en interne.
D. **Chiffrement différé** : démarrer dans des salons non chiffrés lorsque c'est possible, laisser E2EE optionnel pour plus tard ; respecter les salons déjà chiffrés et ne jamais proposer de réinitialisation de clés sans diagnostic. Tester qu'aucun écran obligatoire de récupération n'empêche le premier accès **sans désactiver ni affaiblir en secret le chiffrement existant**.
E. **Audio/vidéo** : deux appareils/comptes réels ; appels entrant/sortant, son dans les deux sens, vidéo, caméra/micro, verrouillage écran, arrière-plan, et échec réseau ; consigner les résultats observés, ne pas déduire d'un écran caméra.
F. **Non-régression** : Espaces, salons, recherche, menu natif, messages, pièces jointes, reconnexion, données et identité graphique. Tests réels sur téléphone indispensables.
G. **Distribution** : conservation SHA de l'APK et de la signature ; installer et mettre à jour sur Samsung sans effacer la session, contrôler nom de package et compatibilité de signature. Ne jamais republier une version « validée » sans tests B à G.

## Tableau de livraison à tenir par le développeur (pas par l'utilisateur)
| Élément | État contrôlé 11/11/2026 |
|---|---|
| Révision | `a0bee9fbf12c898bc259abba1ac5674a2c1d356c` |
| Compilation | GitHub Actions #34, run 43026414703, réussite |
| APK | 105393776 octets, SHA256 `341de9c6555ae7d7a15b2ef35a3b7bed12be61d4afcffcdc48769e772d4bca77` |
| Installation | Captures Samsung 15:44, app ouverte (version exacte à confirmer dans Android) |
| Accueil | Affiché sur les captures, gelé |
| Push | Échec prouvé |
| Connexion préconfigurée | Échec prouvé |
| Crypto sans obstacle | Échec prouvé |
| Appel de bout en bout | Non testé |
| Livraison adhérents | REFUSÉE en l'état |

**Règle de passage** : toute correction attend ces preuves ; chaque contrôle sera exécuté par le développeur avec les outils disponibles, et l'utilisateur ne sera sollicité que pour l'essai physique irréductible.


## Recherches vérifiées — 11 novembre 2026 (documentation et tickets développeurs)
Sources consultées, précisément datées, pour ne plus improviser :
- Architecture des notifications (éditeur) : https://fluffychat.im/privacy/ — le serveur Matrix envoie à une passerelle push qui transmet à FCM ; activer l'API Firebase dans l'APK sans passerelle et autorisation correspondantes ne prouve rien.
- Spécification Matrix Push Gateway : https://spec.matrix.org/latest/push-gateway-api/ — route POST `/_matrix/push/v1/notify` et contrat homeserver/passerelle.
- Ticket FluffyChat #3385 (ouvert) : https://github.com/krille-chan/fluffychat/issues/3385 — sélection automatique FCM/UnifiedPush problématique quand plusieurs distributeurs sont présents ; bien tester les cas sans fournisseur.
- Plan de tests créé par les développeurs, ticket #3676 : https://github.com/krille-chan/fluffychat/issues/3676 — réception push en arrière-plan/terminé, messages, médias, connexion et autres parcours ; **adopter comme liste de contrôle de base**, la compléter avec nos objectifs.
- Ticket #3908 (ouvert) : https://github.com/krille-chan/fluffychat/issues/3908 — appel audio pouvant activer la caméra et dysfonctionnement du capteur de proximité ; tests obligatoires « appel audio sans activation caméra » et appareil contre l'oreille.
- Annonce de l'équipe FluffyChat 11 septembre : https://matrix.org/blog/2026/09/11/this-week-in-matrix-2026-09-11/ — MatrixRTC/LiveKit demande l'annonce du support RTC par le serveur, matrix.org était donné comme compatible ; vérifier à l'exécution.
- Changelog officiel : https://github.com/krille-chan/fluffychat/blob/main/CHANGELOG.md — v2.11 corrige notamment l'audio d'appel et le comportement des notifications ; **ne pas recréer un appel personnalisé**.
- Ticket #3047 (ouvert) : https://github.com/krille-chan/fluffychat/issues/3047 — récupération de clé et second compte problématiques ; aucune réinitialisation automatique autorisée.
- FAQ officielle : https://fluffy.chat/faq/ — sans clé de récupération, les anciens messages chiffrés peuvent devenir indéchiffrables. « Chiffrement plus tard » signifie **parcours initial simplifié**, jamais suppression des clés ou réinitialisation silencieuse.
- Référence fonctionnalités Matrix officielle : https://www.matrix.org/ecosystem/clients/fluffychat/ — appels 1:1 mentionnés comme stables ; MatrixRTC expérimental.

### Contrôles bloquants ajoutés aux résultats upstream
1. Réception d'une notification avec appli arrière-plan, terminée, écran verrouillé ; contrôle du pusher enregistré et du bon fournisseur (tickets #3385 et #3676). Aucun effacement cosmétique de l'alerte.
2. Audio : personne A appelle B et inversement ; aucune caméra ne s'allume spontanément, capteur de proximité vérifié (ticket #3908). Vidéo : réception, image et son bidirectionnels ; test de fin d'appel.
3. Vérification des clés : compte neuf versus compte existant, ne pas confondre ignorer une étape facultative avec perdre les clés ; consigner tout cas de message illisible (#3047).
4. Tester les parcours de la version originale (sans notre personnalisation) quand c'est nécessaire pour distinguer bug upstream et régression Le Fil.
5. Accepter un correctif uniquement avec une source, une preuve de la cause, une preuve de compilation et une preuve de comportement sur téléphone ; sinon **NON VALIDÉ**.
