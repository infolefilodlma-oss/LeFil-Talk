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

# L'etiquette visible doit rester strictement « Le Fil Talk »,
# y compris pour l'APK de test. Le suffixe technique .debug reste interne.
gradle = Path("upstream/app/build.gradle.kts")
source = gradle.read_text(encoding="utf-8")
for old, new in (
    ('resValue("string", "app_name", "$baseAppName dbg")', 'resValue("string", "app_name", baseAppName)'),
    ('resValue("string", "app_name", "$baseAppName nightly")', 'resValue("string", "app_name", baseAppName)'),
):
    if source.count(old) != 1:
        raise SystemExit(f"Etiquette Android inattendue : {old}")
    source = source.replace(old, new)
gradle.write_text(source, encoding="utf-8")
assert source.count('resValue("string", "app_name", baseAppName)') == 3
print("Nom visible Android strictement Le Fil Talk : debug, release, nightly.")
