# Le Fil Talk Android — référence graphique et garde-fous

Date : 2026-11-09. Statut : périmètre graphique minimal décidé par l'utilisateur, non implémenté.

## Référence utilisateur
Capture d'écran fournie le 09/11/2026 de l'interface Talk intégrée à l'Atrium (interface web de messagerie). La capture constitue la **référence d'identité visuelle**, et non un plan d'architecture ou une demande de recopier le DOM web dans Element X.

Éléments visibles : bandeau supérieur violet sombre avec nuances rose/violet, logo Le Fil Talk ; fond extérieur gris-lavande très clair ; panneaux clairs arrondis ; bouton « Nouveau message » violet foncé ; bulles de messages bleu pâle ; fond de conversation pastel bleuté/lavande ; barre de saisie arrondie ; navigation discussions/contacts/profil ; disposition à deux colonnes en grand écran.

## Décision utilisateur du 09/11/2026 — périmètre strict
**Priorité 1 : logo Le Fil Talk existant et couleur de marque.**
**Priorité 2, facultative : police Poppins uniquement si son intégration native est simple et maintenable.**
**Ne pas reproduire les bulles, fonds, navigation, arrondis, bandeau ou mise en page de l'interface web Atrium.**
La capture et le HTML de l'Atrium sont une référence pour identifier les couleurs, pas un cahier des charges de refonte Android.

## Couleurs relevées dans le HTML fourni
- Violet principal : `#4A0050`
- Violet sombre : `#26002C`
- Orange accent : `#F17E18`
Ces valeurs proviennent des variables CSS de l'interface Talk fournie, et ne sont pas des couleurs inventées.

## Identité à préserver
- Couleurs : violet profond pour actions et éléments actifs ; lavande très claire pour fonds ; bleu pâle pour bulles ; accents rose-violet discrets. Les couleurs exactes restent à relever de la capture et à valider pour contraste WCAG, sans inventer une palette officielle.
- Police : **Poppins** souhaitée par l'utilisateur, pour titres, libellés, boutons et messages lorsque compatible avec le système Android et les composants natifs.
- Logo Le Fil Talk : utiliser un actif du projet existant, pas une reproduction approximative.
- Coins arrondis et espacements confortables, priorité à la lisibilité et aux petites tailles d'écran.
- Smartphone : conserver navigation et gestes **natifs Element X**. Ne pas imposer le layout deux colonnes du site web à un écran mobile.

## Contraintes de maintenance
1. Inspecter d'abord les ressources de logo, couleur de marque et éventuellement typographie de la version Element X Android épinglée. Favoriser les ressources prévues par l'amont.
2. Éviter le fork profond des écrans de conversation, de connexion, du SDK Matrix et des composants de navigation.
3. Limiter les adaptations au logo et à la couleur de marque. Poppins seulement si son intégration ne crée pas de maintenance disproportionnée. L'aide d'inscription est un chantier fonctionnel distinct.
4. Vérifier les licences et l'intégration de la police Poppins et des actifs graphiques.
5. Prévoir contraste clair/sombre, accessibilité, grands caractères, affichage petit écran et claviers ouverts.
6. Avant/après : captures et tests ciblés de connexion, conversations, envoi/réception, liste des contacts, notifications et retour navigateur ; rollback du patch si régression.
7. Ne pas annoncer que l'APK actuel reflète cette identité : **aucune adaptation graphique démontrée à ce stade**.

## Prochaine action
Examiner les ressources de logo et de couleur de Element X v26.10.1 ; adapter uniquement ces deux éléments, puis envisager Poppins si triviale. Vérifier par compilation et capture d'écran Android.
