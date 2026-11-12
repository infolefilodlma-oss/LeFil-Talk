# Phase 2A - Interface Simplification (Le Fil Talk)

## État

Phase 2A simplify interface for Zam v1.60.3. Modifications prêtes, application workflow limitée par permissions GitHub OAuth.

## Modifications Préparées

### 1. CSS Simplification (`ci/zam-web/le-fil-simplification.css`)

Masque les fonctions secondaires :
- Debug settings tab
- Plugins settings tab
- Rich Presence settings tab

Preserve sécurité alerts et fonctions principales :
- Messages
- Spaces/Rooms
- Calls, Search, Notifications

### 2. Composant Svelte Runtime (`ci/zam-web/src/lib/LeFilSimplification.svelte`)

Applique les règles de simplification à l'app au runtime via MutationObserver.

## Application Manuelle

### Option 1 : Modification Workflow (Recommandée)

Le workflow `.github/workflows/zam-web-d3d4.yml` doit être modifié pour :

```yaml
- name: Apply Le Fil simplification patches
  run: |
    set -euo pipefail
    # Copy webPush (existing)
    cp ci/zam-web/src/lib/webPush.ts zam/src/lib/webPush.ts
    cp ci/zam-web/src/lib/webPush.test.ts zam/src/lib/webPush.test.ts
    # NEW: Apply simplification CSS
    cat ci/zam-web/le-fil-simplification.css >> zam/src/app.css
    # NEW: Copy simplification component (optional - for future)
    # cp ci/zam-web/src/lib/LeFilSimplification.svelte zam/src/lib/LeFilSimplification.svelte
```

### Option 2 : Application Locale (Développeur)

```bash
cd zam
cat ../ci/zam-web/le-fil-simplification.css >> src/app.css
npm ci
npm run build
```

### Option 3 : Merge dans Zam source

Les modifications peuvent être préparées comme patch à appliquer directement à Zam v1.60.3.

## Fichiers Concernés

- `ci/zam-web/le-fil-simplification.css` — CSS rules pour masquer options secondaires
- `ci/zam-web/src/lib/LeFilSimplification.svelte` — Composant runtime (optionnel)
- `.github/workflows/zam-web-d3d4.yml` — Workflow CI (nécessite modification)

## Tests

Après application des modifications :

```bash
npm run check    # TypeScript/Svelte check
npm run test     # Run tests
npm run lint     # Lint check
npm run build    # Build web client
```

La compilation devrait générer :
- `zam/build/index.html`
- `zam/build/_app/immutable/` (JS/CSS bundles)
- `zam-web-v1.60.3-*.tar.gz`

## Prochaines Étapes

1. ✅ Fichiers de patch créés et prêts
2. ❌ Workflow modifié (bloqué par permissions OAuth)
3. ⏳ Compilation GitHub Actions (en attente de modification workflow)
4. ⏳ Vérification non-régression
5. ⏳ Approbation Philippe

## Blocage Technique

Le workflow `.github/workflows/zam-web-d3d4.yml` requiert `workflow` scope OAuth pour modification.
Approches alternatives :
- Utiliser un PAT (Personal Access Token) avec permissions `workflow`
- Modifier le repo settings pour autoriser certains utilisateurs à modifier workflows
- Exécuter manuellement les étapes de build localement

## Validation Fonctionnelle

À faire en navigateur après build :
- Accès aux messages privés ✓
- Accès aux salons ✓
- Appels audio/vidéo ✓
- Recherche ✓
- Notifications ✓
- Debug tab masqué ✓
- Plugins tab masqué ✓
- Alerts sécurité toujours visibles ✓
