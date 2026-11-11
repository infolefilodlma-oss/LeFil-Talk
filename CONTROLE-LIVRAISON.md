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
