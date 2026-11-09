# Atelier visuel rapide — Le Fil Talk

Le fichier `preview/TalkVisualPreview.kt` contient un composant Jetpack Compose avec `@Preview`, indépendant des services Matrix. Il permet d'essayer rapidement la disposition et les couleurs dans Android Studio, sans attendre GitHub Actions ni fabriquer un APK.

## Utilisation
Dans Android Studio, ouvrir un projet Android **déjà configuré pour Compose Material 3**, ajouter temporairement le fichier dans les sources du module, puis ouvrir **Split** ou **Design**. Les modifications de dimensions et couleurs sont visibles via le rafraîchissement Preview. Ne pas ajouter ce fichier aux sources de production.

## Limites explicites
Ce prototype Compose n'est **pas encore une preuve de conformité Element X** : il ne réutilise pas les écrans ni les composants exacts d'Element X. Le texte du logo est un substitut ; la police Poppins n'est pas embarquée dans ce fichier. Il ne faut pas le présenter comme une capture de l'APK. La preuve finale devra être une capture d'Element X réellement compilé avec logo et police embarqués, puis un test des fonctions de messagerie.

## Référence validée
Capture utilisateur : bandeau rose/prune/bleu nuit, véritable logo transparent Le Fil Talk, police Poppins, bouton « Le Fil » vers https://le-fil.net, liste des discussions, fonds clairs et bulles bleu pâle. Pas de refonte du moteur Matrix. Les couleurs et espacements sont à ajuster sur le prototype **avant** les longues compilations.

## Sécurité
Aucun changement au SDK Matrix, aux écrans de production, au chiffrement, à la connexion ou aux notifications. Pour annuler cet atelier, supprimer seulement les fichiers du dossier `preview/`.
