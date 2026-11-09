# Le Fil Talk Android — référence graphique et garde-fous

Date : 2026-11-09. Statut : logo intégré au build de diagnostic ; personnalisation native étendue demandée le 09/11/2026, à implémenter et tester.

## Référence utilisateur
Capture d'écran fournie le 09/11/2026 de l'interface Talk intégrée à l'Atrium (interface web de messagerie). La capture constitue la **référence d'identité visuelle**, et non un plan d'architecture ou une demande de recopier le DOM web dans Element X.

Éléments visibles : bandeau supérieur violet sombre avec nuances rose/violet, logo Le Fil Talk ; fond extérieur gris-lavande très clair ; panneaux clairs arrondis ; bouton « Nouveau message » violet foncé ; bulles de messages bleu pâle ; fond de conversation pastel bleuté/lavande ; barre de saisie arrondie ; navigation discussions/contacts/profil ; disposition à deux colonnes en grand écran.

## Décision utilisateur du 09/11/2026 — périmètre strict
**Priorité 1 : logo Le Fil Talk existant et couleur de marque.**
**Priorité 2 : intégrer Poppins si compatible avec les ressources de police Android natives ; en cas d'incompatibilité, documenter la preuve technique et conserver une police lisible.**
**Adapter également, lorsque l'architecture Element X le permet sans régression, les couleurs, fonds, bulles, arrondis, espacements et écrans d'accueil. Ne pas recopier littéralement le DOM web Atrium ni remplacer les mécanismes natifs Matrix.**
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
3. Personnaliser progressivement le thème natif (logo, couleurs, typographie Poppins, fonds, bulles et espacements) via les points d'extension réels d'Element X, sans fork profond ni régression. L'aide d'inscription reste un chantier fonctionnel distinct.
4. Vérifier les licences et l'intégration de la police Poppins et des actifs graphiques.
5. Prévoir contraste clair/sombre, accessibilité, grands caractères, affichage petit écran et claviers ouverts.
6. Avant/après : captures et tests ciblés de connexion, conversations, envoi/réception, liste des contacts, notifications et retour navigateur ; rollback du patch si régression.
7. Le logo a été intégré dans la compilation de diagnostic réussie ; **la police Poppins, le thème complet, la mise en page et les captures avant/après ne sont pas encore validés**.

## Prochaine action
Examiner les ressources de logo et de couleur de Element X v26.10.1 ; adapter uniquement ces deux éléments, puis envisager Poppins si triviale. Vérifier par compilation et capture d'écran Android.
