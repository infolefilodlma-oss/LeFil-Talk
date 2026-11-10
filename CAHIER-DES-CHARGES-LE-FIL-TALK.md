# Le Fil Talk — Cahier des charges de référence
Version 1.0 — 10 novembre 2026
Statut : décisions utilisateur consolidées ; les fonctions non testées restent NON VALIDÉES.

## 1. Objectif et public
Application Android de messagerie conviviale pour les adhérents du Fil : aussi simple et plaisante à utiliser qu'un groupe WhatsApp ou Telegram. Favoriser les échanges spontanés et l'engagement, pas reproduire un forum sur téléphone. Interface accessible, claire, agréable, sans surcharge.

## 2. Architecture décidée
- Client Android Le Fil Talk : personnalisation minimale et vérifiée de **FluffyChat** (Flutter), candidat prioritaire. Code amont de référence version verrouillée **v2.11.5**.
- **Element Web ou Cinny** : choix ultérieur pour le pilotage web des salons, espaces, membres et droits ; PAS de développement d'une interface web parallèle dans l'APK.
- **atrium.le-fil.net** : adresse souhaitée pour la solution web Matrix (déploiement effectif non vérifié).
- **talk.le-fil.net** : adresse souhaitée pour la présentation/l'accès à Le Fil Talk, ne constitue pas en soi l'hébergement de l'APK.
- Matrice de salons, permissions et adhésions maintenue côté serveur Matrix, disponible dans les différents clients.
- Hébergement Matrix public utilisé lors des essais : matrix.org, mais ne pas afficher inutilement « matrix.org » dans les écrans d'accueil et d'aide ; le domaine peut rester visible quand le protocole ou le navigateur de connexion l'exige.
- Aucune création ou préconfiguration des salons et espaces dans l'APK. L'administration sera faite depuis le web.
- **Papote** = salon commun ; **Sentiers** = espaces thématiques ; **Oasis** = espaces locaux. Ne pas ajouter de boutons artificiels permanents ou de filtrages des espaces codés en dur.

## 3. Identité
- Nom visible et marque : **Le Fil Talk** (sans suffixe technique dbg, nightly, F-Droid, etc.).
- Logo officiel rond du Fil Talk issu de **LogoLeFilTalk.png** ; ne jamais le remplacer par un logo approximatif, ni mettre un logo généré à sa place.
- Couleurs : bleu profond **#0C1853** et prune **#4A0050** ; application harmonisée en modes clair/sombre si pris en charge, contraste et lisibilité vérifiés.
- Police **Poppins**, légèrement plus petite que dans la précédente APK Element X, sans dégrader l'accessibilité. Vérifier les débordements sur écrans Android réels.
- S'inspirer autant que possible de l'esthétique de **FluffyChat** observée sur les captures transmises par l'utilisateur : liste de conversations simple, nouveau message évident, peu de menus, disposition élégante.
- Ne pas surcharger l'interface avec une landing page intégrée. Éventuel accueil « welcome » web à étudier plus tard dans Element Web ou Cinny.

## 4. Fonctions indispensables
- Connexion/inscription simples, immédiatement compréhensibles.
- Discussions privées, discussions de groupe, salons et espaces natifs Matrix.
- Messages texte, images, fichiers et messages vocaux selon capacités du client natif.
- Appels **audio ET vidéo**, à tester réellement entre appareils.
- Notifications de nouveaux messages avec application en arrière-plan ou fermée, à tester sur téléphone.
- Navigation native de FluffyChat préservée ; ne pas reconstruire la messagerie ni remplacer les composants existants sans nécessité.

## 5. Chiffrement et sécurité — règle prioritaire
- L'utilisateur ne souhaite **aucun parcours de récupération cryptographique imposé au démarrage** qui retarde l'accès aux échanges ordinaires.
- Salons ordinaires configurés **non chiffrés depuis le web** quand cela est pertinent ; ne jamais activer le chiffrement implicitement dans l'APK.
- Ne pas supprimer le chiffrement ou la sécurité d'une conversation privée et ne pas prétendre que les demandes de vérification peuvent être supprimées sans conséquence ; examiner précisément le comportement natif de la version choisie et réaliser un essai.
- Si la vérification/récupération est facultative, elle doit pouvoir être reportée ; si indispensable à certains usages chiffrés, le signaler honnêtement.
- Pas d'exposition superflue de détails Matrix dans les écrans grand public.

## 6. Contraintes de réalisation
- Développer sur la branche distincte **fluffychat-reprise** dans **infolefilodlma-oss/LeFil-Talk**.
- Préserver intégralement la branche et les travaux **Element X** pour retour arrière.
- Travailler avec l'amont FluffyChat versionné ; changements ciblés (identité, thème, police, accueil minimal uniquement si justifié).
- Sauvegarde/rollback Git par commits ; aucune suppression d'un autre projet, aucune publication en production sans validation.
- Exécuter les précontrôles rapides avant compilation ; arrêter immédiatement sur ancrage manquant ou erreur de dépendance. Ne pas lancer de cycles longs redondants.
- Garder intactes les fonctionnalités natives : messagerie, groupes/espaces, notifications, appels, connexion.
- Respecter les licences des composants amont et les obligations de redistribution.

## 7. Recette bloquante de l'APK
1. Compilation Android ARM64 terminée avec succès ; APK réelle produite.
2. Contrôle package, **nom visible exact**, icône officielle, version/signature et SHA-256.
3. Installation et démarrage sur émulateur fiable ; captures et logs conservés.
4. Inspection visuelle : couleurs exactes, rond du logo, Poppins, tailles, ergonomie et absence de boutons Papote/Sentiers/Oasis ajoutés artificiellement.
5. Connexion d'un compte Matrix existant et inscription de test ; absence de blocage cryptographique pour salons non chiffrés et vérification des limites.
6. Vérifier l'affichage des salons/espaces créés sur le web et leur synchronisation sur smartphone.
7. Envoyer/recevoir texte, photo, pièce jointe, message vocal.
8. **Tester** appels audio et vidéo entre deux appareils, avec sonnerie et permissions.
9. **Tester** notifications téléphone écran éteint/application fermée.
10. Vérifier les erreurs et régressions ; pas de déclaration « validé » avant preuves.

## 8. Livrable
- **Un fichier .apk ARM64 téléchargeable directement dans la conversation** et installable sur téléphone ; pas un lien GitHub Actions 404 ni une archive ZIP présentée comme APK.
- Bien distinguer APK de test, APK installée et version validée ; jamais inventer un téléchargement, une réussite ou un test.
- À terme, distribution durable de l'APK signée et correctement versionnée ; conserver l'identité de signature pour les mises à jour.

## 9. Ce qui n'est PAS demandé
- Aucune création de serveur Matrix, salon ou espace depuis l'APK.
- Aucun menu artificiel séparant Sentiers et Oasis, ni copie de la page Atrium dans le téléphone.
- Aucune programmation automatique de rappels ou veilles.
- Ne pas confondre Element Web avec Elementor WordPress.
- Pas de changement de technologie supplémentaire sans preuve et décision explicite.

## 10. État du chantier à la rédaction
- Branche FluffyChat créée, script de personnalisation et CI GitHub ajoutés.
- Compilation et tests finaux de la **nouvelle APK FluffyChat** non encore validés.
- Ancienne branche Element X fonctionnelle au démarrage préservée, mais non retenue comme base principale.
- Le présent cahier des charges sert de source de vérité pour chaque modification et pour le différentiel final.
