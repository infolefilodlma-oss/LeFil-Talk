#!/usr/bin/env python3
"""Couleurs de la capture Le Fil Talk, mode clair, sans modifier Matrix."""
from pathlib import Path

root = Path("upstream/libraries/compound/src/main/kotlin/io/element/android/compound/tokens/generated")
changes = {
    "SemanticColorsLight.kt": {
        "bgActionPrimaryRest": "0xFF4A0050",
        "bgActionPrimaryHovered": "0xFF62006B",
        "bgActionPrimaryPressed": "0xFF26002C",
        "bgAccentRest": "0xFF4A0050",
        "bgAccentHovered": "0xFF62006B",
        "bgAccentPressed": "0xFF26002C",
        "bgAccentSubtle": "0xFFF3EAF5",
        "bgCanvasDefault": "0xFFF8F6FB",
    },
}
for filename, mappings in changes.items():
    path = root / filename
    original = path.read_text(encoding="utf-8")
    source = original
    import_anchor = "import io.element.android.compound.annotations.CoreColorToken"
    if source.count(import_anchor) != 1:
        raise SystemExit(f"Version Element X inattendue : {path}")
    source = source.replace(import_anchor, "import androidx.compose.ui.graphics.Color" + chr(10) + import_anchor)
    lines = source.splitlines()
    for key, argb in mappings.items():
        matches = [i for i, line in enumerate(lines) if line.startswith(f"    {key} = ")]
        if len(matches) != 1:
            raise SystemExit(f"Jeton sémantique introuvable/ambigu : {filename} {key}")
        i = matches[0]
        if not lines[i].endswith(","):
            raise SystemExit(f"Syntaxe de jeton inattendue : {filename} {key}")
        lines[i] = f"    {key} = Color({argb}),"
    source = chr(10).join(lines) + chr(10)
    path.write_text(source, encoding="utf-8")
    print(f"{filename} : {len(mappings)} couleurs du Fil appliquées.")

# Le Fil Talk démarre en thème clair. Le choix explicite de l'adhérent
# (clair, sombre ou système) reste ensuite conservé.
preferences = Path("upstream/libraries/preferences/impl/src/main/kotlin/io/element/android/libraries/preferences/impl/store/DefaultAppPreferencesStore.kt")
source = preferences.read_text(encoding="utf-8")
old = """    override fun getThemeFlow(): Flow<String?> {
        return store.data.map { prefs ->
            prefs[themeKey]
        }
    }
"""
new = """    override fun getThemeFlow(): Flow<String?> {
        return store.data.map { prefs ->
            prefs[themeKey] ?: "Light"
        }
    }
"""
if source.count(old) != 1:
    raise SystemExit("Source amont inattendue pour le thème clair par défaut.")
preferences.write_text(source.replace(old, new, 1), encoding="utf-8")
print("Thème clair par défaut ; le choix clair/sombre/système reste modifiable.")
