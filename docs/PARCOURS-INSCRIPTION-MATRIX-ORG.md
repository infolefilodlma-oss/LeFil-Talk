# Le Fil Talk — inscription simple, sans dette technique
Date : 2026-11-09. Statut : spécification validée sur le principe, **non implémentée**.

## Distinction fondamentale
- **Nom d'utilisateur Matrix** : choisi à l'inscription, par exemple `marie.dupont`. Sur matrix.org, l'identifiant Matrix complet est `@marie.dupont:matrix.org`. Ce n'est **pas** une adresse e-mail.
- **Adresse e-mail** : donnée distincte, pouvant servir à la vérification et à la récupération de compte selon le parcours proposé par matrix.org. Ne pas promettre qu'elle est toujours obligatoire ni qu'elle remplace l'identifiant Matrix.
- **Mot de passe** : secret du compte Matrix. Le Fil Talk ne doit ni le collecter dans un formulaire personnalisé, ni le stocker dans un serveur du Fil.
- **Serveur** : `matrix.org` sélectionné par défaut pour les nouveaux utilisateurs. Ne pas empêcher un utilisateur existant de choisir un autre serveur si Element X le permet.

## Message d'accueil proposé
**Bienvenue sur Le Fil Talk**

Pour discuter avec les membres du Fil, vous avez besoin d'un compte de messagerie gratuit sur matrix.org.

1. Appuyez sur **Créer mon compte**.
2. Choisissez un **nom d'utilisateur** (par exemple `marie.dupont`). **Ce n'est pas votre adresse e-mail.**
3. Choisissez un **mot de passe** et conservez-le.
4. Si matrix.org le demande, indiquez et confirmez votre **adresse e-mail**.
5. Revenez dans Le Fil Talk et connectez-vous avec votre nouveau compte.\n6. Dans les réglages de sécurité du compte, activez la **sauvegarde sécurisée des messages chiffrés** si elle est proposée, et conservez la **clé de récupération** dans un endroit sûr.

Votre adresse Matrix sera de la forme `@marie.dupont:matrix.org`. Vous pourrez la partager avec les autres adhérents pour qu'ils vous trouvent.

**J'ai déjà un compte** : connexion au lieu de création.

## En cas d'oubli du mot de passe
- Proposer une aide « Mot de passe oublié ? » qui renvoie **vers la récupération officielle du serveur matrix.org**, sans recueillir de mot de passe ni d'adresse e-mail dans un écran développé par Le Fil.
- La récupération par e-mail suppose une adresse e-mail **associée et vérifiée** sur le compte, ainsi que la disponibilité du mécanisme de récupération du serveur. **Ne pas promettre une récupération automatique ou garantie.**
- **Retrouver l'accès au compte n'est pas la même chose que retrouver les anciens messages chiffrés** : la sauvegarde sécurisée et la clé de récupération peuvent être nécessaires. Le popup doit avertir clairement, sans présenter cette sauvegarde comme activée d'office.
- Prévoir deux entrées distinctes : « Je n'ai pas encore de compte » et « J'ai déjà un compte / Mot de passe oublié ».
- Vérifier les URLs et écrans réels du fournisseur d'identité de matrix.org avant d'ajouter un lien ou un bouton dans l'application.

## Contraintes d'architecture anti-dette
1. S'appuyer sur le parcours d'inscription/connexion **natif d'Element X** et sur l'authentification officielle matrix.org. Ne pas créer de second compte Le Fil, de formulaire de mot de passe maison ou de passerelle d'identités improvisée.
2. L'aide doit être légère et **non bloquante** ; affichée au premier lancement, avec « J'ai déjà un compte » et « Plus tard », et accessible ensuite depuis l'aide. Ne pas empêcher le retour à l'application.
3. Pour le serveur par défaut, utiliser les **points de configuration publics et maintenus** d'Element X, après vérification dans la version amont épinglée. Ne pas modifier les bibliothèques Matrix ni coder en dur des URLs d'authentification susceptibles de changer.
4. La redirection vers le navigateur doit utiliser le mécanisme d'authentification supporté par Element X, y compris le retour à l'application. Ne pas utiliser un simple lien externe en le présentant comme une inscription intégrée si la reprise de session n'est pas prouvée.
5. Conserver la possibilité de mises à jour amont Element X sans conflit sur les écrans d'authentification ; modifications isolées, patch minimal, rollback.
6. **Avant publication** : tester de bout en bout sur téléphone réel : premier lancement, inscription, confirmation e-mail si demandée, retour, connexion, déconnexion, reconnexion, ajout d'un contact, message envoyé/reçu, fermeture/réouverture. Tester aussi « déjà un compte », « mot de passe oublié », récupération par e-mail vérifié, sauvegarde des messages chiffrés, erreur réseau et nom déjà pris.
7. Ne pas présenter l'inscription comme réalisée tant qu'un test réel ne l'a pas démontrée.

## Point technique à résoudre avant modification
Inspecter la version source exacte `element-x-android v26.10.1` et le flux d'authentification matrix.org pour identifier le point d'extension officiellement supporté. **Ne pas coder le popup à l'aveugle.**
