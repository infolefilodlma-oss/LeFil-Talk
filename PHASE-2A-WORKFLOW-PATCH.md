# Phase 2A — Workflow Patch Required

Phase 2A Svelte modifications are committed on branch `phase-2a-ui-simplification`.
Workflow modification blocked by GitHub OAuth `workflow` scope.

## Modification Required

File: `.github/workflows/zam-web-d3d4.yml`  
Step: "Apply isolated Web Push files only" (line 28–34)

**Replace:**
```yaml
      - name: Apply isolated Web Push files only
        run: |
          set -euo pipefail
          cp ci/zam-web/src/lib/webPush.ts zam/src/lib/webPush.ts
          cp ci/zam-web/src/lib/webPush.test.ts zam/src/lib/webPush.test.ts
          git -C zam diff --check
          git -C zam diff -- src/lib/webPush.ts src/lib/webPush.test.ts
```

**With:**
```yaml
      - name: Apply isolated patches (Phase 1 + Phase 2A)
        run: |
          set -euo pipefail
          # Phase 1: Web Push
          cp ci/zam-web/src/lib/webPush.ts zam/src/lib/webPush.ts
          cp ci/zam-web/src/lib/webPush.test.ts zam/src/lib/webPush.test.ts
          # Phase 2A: UI simplification (settings navigation + app settings)
          mkdir -p zam/src/lib/utils zam/src/lib/components/layout
          cp ci/zam-web/src/lib/utils/settingsNav.ts zam/src/lib/utils/settingsNav.ts
          cp ci/zam-web/src/lib/components/layout/AppSettings.svelte zam/src/lib/components/layout/AppSettings.svelte
          git -C zam diff --check
          git -C zam diff -- src/lib/webPush.ts src/lib/webPush.test.ts src/lib/utils/settingsNav.ts src/lib/components/layout/AppSettings.svelte | head -100
```

## Options to Authorize

1. **gh auth refresh** (requests interactive flow):
   ```bash
   gh auth refresh -h github.com -s workflow
   # Follow GitHub's web browser prompt
   ```

2. **Manual GitHub Web UI**:
   - Navigate to `.github/workflows/zam-web-d3d4.yml`
   - Edit file directly via GitHub Web UI
   - Apply changes above
   - Commit

3. **Repository Settings** (for future push):
   - Settings → Actions → General
   - Authorize workflow modifications for bot/app

## After Authorization

Once workflow scope is granted:

```bash
git checkout phase-2a-ui-simplification
git push  # Will succeed with workflow changes
```

## What Changes Do

1. Copy Phase 1 files (webPush.ts) — existing, no changes
2. Copy Phase 2A files:
   - `ci/zam-web/src/lib/utils/settingsNav.ts` → `zam/src/lib/utils/settingsNav.ts`
   - `ci/zam-web/src/lib/components/layout/AppSettings.svelte` → `zam/src/lib/components/layout/AppSettings.svelte`

## Phase 2A What's Inside

### settingsNav.ts

Restructures settings groups for Le Fil Talk (simplified interface):

- **Account**: account, security, privacy
- **App**: appearance, messages-media, notifications, voice
- **Plus d'options**: general, keybinds, emotes, rich-presence, plugins, server, about, debug

### AppSettings.svelte

Adds expandable "Plus d'options" section:
- `moreOptionsExpanded` state tracks expansion
- Mobile: "▶ Plus d'options" / "▼ Plus d'options" button
- Desktop: same toggle in sidebar
- Second and third groups hidden until "Plus d'options" is expanded
- All settings remain fully accessible

## Testing After Workflow Runs

GitHub Actions will execute:
1. npm run check — TypeScript/Svelte validation
2. npm run test — Unit tests
3. npm run lint — Code style
4. npm run build — Production build

Artifact: `zam-web-v1.60.3-*.tar.gz`

Verify in browser (Phase 2A specific):
- ✓ Settings panel opens correctly
- ✓ Main tabs visible: Account, App
- ✓ "Plus d'options" button visible
- ✓ Click "Plus d'options" expands to show advanced settings
- ✓ All advanced settings accessible
- ✓ No regressions in messages, calls, notifications

## Notes

- Phase 1 (webPush) corrections preserved — no changes
- No runtime modifications needed
- No VPS changes required
- No production deployment (until approved)
