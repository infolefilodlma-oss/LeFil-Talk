# Le Fil Talk Android — référence graphique et garde-fous

Date : 2026-11-09. Statut : cahier des charges visuel, non implémenté.

## Référence utilisateur
Capture d'écran fournie le 09/11/2026 de l'interface Talk intégrée à l'Atrium (interface web de messagerie). La capture constitue la **référence d'identité visuelle**, et non un plan d'architecture ou une demande de recopier le DOM web dans Element X.

Éléments visibles : bandeau supérieur violet sombre avec nuances rose/violet, logo Le Fil Talk ; fond extérieur gris-lavande très clair ; panneaux clairs arrondis ; bouton « Nouveau message » violet foncé ; bulles de messages bleu pâle ; fond de conversation pastel bleuté/lavande ; barre de saisie arrondie ; navigation discussions/contacts/profil ; disposition à deux colonnes en grand écran.

## Identité à préserver
- Couleurs : violet profond pour actions et éléments actifs ; lavande très claire pour fonds ; bleu pâle pour bulles ; accents rose-violet discrets. Les couleurs exactes restent à relever de la capture et à valider pour contraste WCAG, sans inventer une palette officielle.
- Police : **Poppins** souhaitée par l'utilisateur, pour titres, libellés, boutons et messages lorsque compatible avec le système Android et les composants natifs.
- Logo Le Fil Talk : utiliser un actif du projet existant, pas une reproduction approximative.
- Coins arrondis et espacements confortables, priorité à la lisibilité et aux petites tailles d'écran.
- Smartphone : conserver navigation et gestes **natifs Element X**. Ne pas imposer le layout deux colonnes du site web à un écran mobile.

## Contraintes de maintenance
1. Inspecter d'abord le système de thèmes, typographie et ressources de la version Element X Android épinglée. Favoriser tokens, ressources et points d'extension prévus par l'amont.
2. Éviter le fork profond des écrans de conversation, de connexion, du SDK Matrix et des composants de navigation.
3. Limiter les adaptations à la marque, aux couleurs, à la police et à une aide d'inscription légère et indépendante, dans cet ordre, sans changements fonctionnels hors périmètre.
4. Vérifier les licences et l'intégration de la police Poppins et des actifs graphiques.
5. Prévoir contraste clair/sombre, accessibilité, grands caractères, affichage petit écran et claviers ouverts.
6. Avant/après : captures et tests ciblés de connexion, conversations, envoi/réception, liste des contacts, notifications et retour navigateur ; rollback du patch si régression.
7. Ne pas annoncer que l'APK actuel reflète cette identité : **aucune adaptation graphique démontrée à ce stade**.

## Prochaine action
Examiner les ressources de thème et de typographie de Element X v26.10.1 et produire une modification minimale, vérifiée par compilation et capture d'écran Android.
