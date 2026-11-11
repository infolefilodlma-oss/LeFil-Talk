# PLAN DE CHARGE ET CONTRÔLE QUALITÉ — LE FIL TALK
Date : 10 novembre 2026 — référence : CAHIER-DES-CHARGES-LE-FIL-TALK.md
Statut : plan de pilotage, non preuve de livraison.

## Méthode impérative
- **Une source de vérité :** cahier des charges, identité officielle fournie par l'utilisateur et preuves issues du build.
- **Ne pas corriger à l'aveugle.** Reconstituer le résultat attendu, écart constaté, causes possibles et test court qui discrimine les causes ; vérifier les API/versions amont.
- **Ne pas multiplier les compilations.** Précontrôles statiques puis tests unitaires/ressources, ensuite une compilation, enfin tests sur le fichier exact. Réutiliser les APK signées identiques pour la recette.
- **Zéro régression :** branche Element X intacte ; FluffyChat version v2.11.5 figée ; modifications ciblées ; sauvegarde Git et retour arrière par revert ; pas de modifications hors périmètre.
- **Point d'arrêt :** à la première anomalie, suspendre les changements, revenir à l'état stable ciblé si nécessaire, corriger la cause démontrée et vérifier. Ne jamais lancer une nouvelle modification avant d'avoir diagnostiqué la précédente.
- **Travail vérifié plutôt que temps passé :** chaque étape se termine avec une preuve et un critère GO/NO-GO. Aucun succès de compilation ne vaut validation du produit.

## PRIORITÉ ABSOLUE — supprimer le frein à l'inscription (décision utilisateur)
**Aucune nouvelle livraison aux adhérents avant validation de l'inscription et de la première connexion.** La réussite de la compilation, des icônes ou de l'émulateur ne compense pas un parcours d'accès bloquant.

Critères d'acceptation sur téléphone :
1. Depuis la première ouverture, proposer clairement « Créer mon compte » et « J'ai déjà un compte », sans choix de fournisseur Matrix ni jargon technique préalable.
2. Utiliser matrix.org en arrière-plan sans le présenter comme une étape de choix ; ne pas promettre de masquer le domaine lorsqu'une authentification extérieure doit légalement/techniquement l'afficher.
3. Inscription possible de bout en bout, puis arrivée dans l'application, sans création de salons artificiels.
4. Accès aux salons non chiffrés **sans vérification d'identité ni récupération de clé cryptographique imposées** ; si le fournisseur exige une authentification ou des contrôles de sécurité, ne jamais prétendre pouvoir les contourner.
5. Vérifier aussi le retour d'un adhérent déjà inscrit et le comportement après fermeture/réouverture.
6. Tester en conditions réelles (Android, compte neuf et existant) ; documenter les étapes et le résultat avec captures. **NO-GO si l'une échoue.**

**Risque de configuration confirmé dans le code amont v2.11.5** : définir simplement `AppSettings.presetHomeserver` masque le bouton natif « Créer un compte » dans `intro_page.dart` lorsque `hasPresetHomeserver` est vrai. Il ne faut donc PAS appliquer ce paramètre seul. Une personnalisation du routage de création et connexion, respectant le fournisseur et ses contraintes, doit être testée avant d'être retenue.

## Dépendances et plan de charge (ordre strict)
| Lot | Intervention | Contrôles avant travail | Preuve / condition de sortie | État |
|---|---|---|---|---|
| 0. Périmètre | Relire le cahier des charges ; confirmer web pilote, Android contenant | Vérifier branches, version et logo SHA256 | Aucun salon ni espace créés/codés dans l'APK ; Element X préservé | Établi |
| 1. Identité | Logo utilisateur *strictement inchangé*, icônes adaptatives Android et splash ; fond bleu/prune | Comparaison SHA256 du PNG source ; inventaire des ressources FluffyChat | Contrôler les images générées ET celles extraites de l'APK ; absence de mascotte/titre FluffyChat visible | Ressources inspectées, parcours complet non validé |
| 2. Ergonomie | Interface native FluffyChat, couleurs #0C1853 et #4A0050, Poppins légèrement réduite | Vérifier thèmes clair/sombre, réglages dynamiques et échelles Android | Captures réelles sur plusieurs écrans, non-troncature, contraste, taille lisible | Partiellement réalisé, non validé |
| 3. Accès | Inscription/connexion sans écran technique superflu | Déterminer le comportement réel de FluffyChat v2.11.5 sur matrix.org | Essai avec compte existant et création de compte, sans récupération cryptographique bloquante pour salon non chiffré ; limites documentées | Non testé |
| 4. Messagerie | Discussions privées, groupe, espaces natifs, messages et fichiers | Ne pas préconfigurer Papote/Sentiers/Oasis ; configuration côté web | Envoyer/recevoir texte, image, pièce jointe, vocal ; espaces synchronisés depuis web | Non testé |
| 5. Communication | Audio, vidéo, notifications | Vérifier gestion Android de permissions, UnifiedPush/FCM, identité de paquet et services ; compatibilité appels | Essai **entre deux appareils** ; appel entrant/sortant, notification application fermée et écran éteint | Non testé |
| 6. Fabrication | APK ARM64 optimisée, nom Le Fil Talk, signature/version | Vérifier Kotlin/Flutter/Rust/SDK versions, noms des activités, ABI et espace disque | AAPT/apksigner, SHA256, manifeste, taille et ressources; pas de distribution de debug 206 Mo | APK de test 105,5 Mo compilée et inspectée |
| 7. Installation | Test du **même fichier** sur Android ; distribution smartphone | Utiliser la bonne ABI pour chaque cible ; ne pas confondre réussite d'émulateur et usage réel | Installation, lancement, captures et logs sur Android + téléchargement finalisé sur smartphone | Émulateur x86-64 réussi ; Samsung et téléchargement non validés |
| 8. Livraison | Une APK test puis une version finale signée et durable | Toutes preuves 1–7, traçabilité des risques, obligations AGPL | Fichier direct téléchargeable, testé, version et clé de signature maîtrisées ; aucun « terminé » prématuré | Non validé |

## Risques et mesures préventives
- **Ressources de marque** : comparer l'empreinte du PNG fourni, les images Android générées, les assets réellement empaquetés et les captures runtime ; une réussite de compilation n'est pas un contrôle d'identité.
- **ABI différente** : Android ARM64 pour Samsung ; x86-64 pour émulateur ; choisir au démarrage du test, ne jamais utiliser la même APK sur des architectures incompatibles.
- **Distribution GitHub >100 Mo** : la présence en Release ne prouve pas la réception du fichier par Chrome ; tester la finalisation ; si échec, réduire/adapter la méthode de distribution avant nouvel essai.
- **Signature provisoire** : une release AOT signée debug n'est pas une distribution finale. Préparer une identité de signature durable pour les mises à jour, sans publier de clé privée.
- **Déclenchements GitHub** : chemins des workflows et scripts définis précisément ; ne pas déclencher des builds par une documentation modifiée.
- **Chiffrement et notifications** : ne pas « désactiver » des protections ou supposer un push fonctionnel à partir du manifeste ; valider sur compte et téléphone.
- **Modifications d'Element Web** : hors du périmètre Android ; aucune action sur le serveur ou les domaines sans décision et vérification.
- **Obligations AGPL** : conserver attribution/licence, publier le code source correspondant selon obligations applicables.

## Preuves d'exécution disponibles au 10 novembre 2026
- Compilations FluffyChat ARM64 réussies dans GitHub Actions, APK optimisée test publiée : https://github.com/infolefilodlma-oss/LeFil-Talk/actions/runs/42880008871
- Test Android avec build x86-64 terminé avec succès : https://github.com/infolefilodlma-oss/LeFil-Talk/actions/runs/42884274907
- **Ne pas déclarer** validés : installation sur Samsung, téléchargement smartphone, appels audio/vidéo, notifications, navigation complète, comportement du chiffrement, accessibilité.
- Les échecs précédents ont été liés notamment aux ressources et aux scripts de livraison ainsi qu'à une erreur d'architecture cible : ce sont des défauts de méthode à empêcher par les précontrôles.

## Discipline de livraison
1. Préparer la matrice de conformité *avant* chaque modification (attendu / actuel / test / résultat).
2. Pour chaque action Git : modification ciblée, revue du diff, contrôles statiques, rollback documenté.
3. S'arrêter au premier test rouge et analyser les artefacts ; aucun correctif spéculatif en chaîne.
4. Ne lancer la compilation complète qu'après validation des préconditions.
5. Faire vérifier automatiquement les préconditions de paquet, icône, ABI, signature, ressources ; vérifier réellement les écrans et fonctions sur appareils.
6. Ne communiquer comme « terminé » que ce qui est accompagné d'une preuve.
