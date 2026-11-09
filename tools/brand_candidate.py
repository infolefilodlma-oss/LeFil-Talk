#!/usr/bin/env python3
"""Personnalisation minimale et contrôlée des constantes de l'application Element X."""
from pathlib import Path

p = Path("upstream/plugins/src/main/kotlin/config/BuildTimeConfig.kt")
original = p.read_text(encoding="utf-8")
replacements = {
    'const val APPLICATION_ID = "io.element.android.x"': 'const val APPLICATION_ID = "net.lefil.talk"',
    'const val APPLICATION_NAME = "Element X"': 'const val APPLICATION_NAME = "Le Fil Talk"',
}
for old, new in replacements.items():
    if original.count(old) != 1:
        raise SystemExit(f"Source amont inattendue, arrêt sans modification : {old}")
updated = original
for old, new in replacements.items():
    updated = updated.replace(old, new)
p.write_text(updated, encoding="utf-8")
print("Identifiant Android : net.lefil.talk ; nom : Le Fil Talk")
print("Code Matrix, configuration du serveur et notifications inchangés.")
