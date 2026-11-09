#!/usr/bin/env python3
"""Palette Le Fil Talk dans les couleurs sémantiques Compose, sans modifier Matrix."""
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
    "SemanticColorsDark.kt": {
        "bgAccentRest": "0xFFF3B9FA",
        "bgAccentHovered": "0xFFFFCDFD",
        "bgAccentPressed": "0xFFE5A4F0",
        "bgAccentSubtle": "0xFF45234A",
    },
}
for filename, mappings in changes.items():
    path = root / filename
    original = path.read_text(encoding="utf-8")
    source = original
    import_anchor = "import io.element.android.compound.annotations.CoreColorToken"
    if source.count(import_anchor) != 1:
        raise SystemExit(f"Version Element X inattendue : {path}")
    source = source.replace(import_anchor, "import androidx.compose.ui.graphics.Color\\n" + import_anchor)
    for key, argb in mappings.items():
        import re
        pattern = rf"(?m)^(    {re.escape(key)} = )[^,\\n]+(,)$"
        replacement = rf"\\g<1>Color({argb})\\2"
        updated, count = re.subn(pattern, replacement, source)
        if count != 1:
            raise SystemExit(f"Jeton sémantique introuvable/ambigu : {filename} {key}")
        source = updated
    path.write_text(source, encoding="utf-8")
    print(f"{filename} : {len(mappings)} couleurs du Fil appliquées.")
