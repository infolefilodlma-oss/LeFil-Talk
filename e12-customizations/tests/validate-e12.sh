#!/bin/bash
set -euo pipefail

# Validation E12 : vérifier que les personnalisations sont présentes dans le build Web

echo "=== VALIDATION E12 BUILD WEB ==="

BUILD_WEB="${1:-.}"

# Vérifier fichiers clés
test -f "$BUILD_WEB/index.html" || (echo "❌ index.html manquant" && exit 1)
test -f "$BUILD_WEB/config.json" || (echo "❌ config.json manquant" && exit 1)
test -f "$BUILD_WEB/main.dart.js" || (echo "❌ main.dart.js manquant" && exit 1)
test -f "$BUILD_WEB/assets/assets/logo/mini/le_fil_echo_logo.jpg" || (echo "❌ Logo E12 manquant" && exit 1)

echo "✅ Fichiers présents"

# Vérifier config.json
grep -q '"applicationName": "Le Fil Echo"' "$BUILD_WEB/config.json" || (echo "❌ applicationName manquant" && exit 1)
grep -q '"defaultHomeserver": "matrix.org"' "$BUILD_WEB/config.json" || (echo "❌ defaultHomeserver manquant" && exit 1)

echo "✅ Configuration E12 valide"

# Vérifier branding dans JS compilé
grep -q "Le Fil" "$BUILD_WEB/main.dart.js" || (echo "❌ Branding 'Le Fil' manquant" && exit 1)
grep -q "le_fil_echo_logo" "$BUILD_WEB/main.dart.js" || (echo "❌ Référence logo E12 manquante" && exit 1)

echo "✅ Branding E12 compilé"

echo ""
echo "🎯 Validation E12 réussie"
exit 0
