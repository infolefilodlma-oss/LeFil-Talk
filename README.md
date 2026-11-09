# Le Fil Talk — Android (Matrix)

Projet distinct de l'application **Le Fil**. Objectif : produire un APK Android **Le Fil Talk** fondé sur [Element X Android](https://github.com/element-hq/element-x-android), puis vérifier sa signature et son installation avant diffusion depuis le-fil.net.

## État

- Dépôt initialisé ; **aucun APK Le Fil Talk publié**.
- Source amont de référence : `element-hq/element-x-android`, tag `v26.10.1`, sous licence AGPL-3.0 (voir les licences amont).
- La compilation exploratoire assemble **Element X F-Droid debug non personnalisé**, seulement pour diagnostiquer la faisabilité. **Ne pas distribuer cet artefact comme Le Fil Talk**.
- À faire : préserver les droits et notices, personnaliser nom/identité/package et serveur Matrix selon les paramètres effectivement validés, configurer une clé pérenne de signature et tester l'installation et les mises à jour.

## Isolation

Aucune modification du dépôt `LeFil-FDroid`, du VPS ni du site public. La personnalisation ne doit pas altérer les protocoles et la sécurité Matrix.
