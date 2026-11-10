#!/usr/bin/env python3
"""Contrôles rapides et bloquants AVANT toute compilation / émulateur."""
from pathlib import Path
import re
import struct
import subprocess

root = Path(__file__).resolve().parents[1]
def require(test, explanation):
    if not test:
        raise SystemExit("PREFLIGHT BLOQUÉ : " + explanation)
    print("OK :", explanation)

workflow = (root / ".github/workflows/element-x-candidate.yml").read_text(encoding="utf-8")
smoke = (root / "tools/android_smoke.sh").read_text(encoding="utf-8")
scripts = sorted((root / "tools").glob("*.py"))
require(len(scripts) >= 7, "scripts de personnalisation présents")
for script in scripts:
    compile(script.read_text(encoding="utf-8"), str(script), "exec")
require(True, "syntaxe Python de tous les scripts")
subprocess.run(["bash", "-n", str(root / "tools/android_smoke.sh")], check=True)
require(True, "syntaxe du test Android")
require("needs: preflight" in workflow and "needs: compile" in workflow,
        "jobs ordonnés : précontrôle puis compilation puis Android")
require("run: python3 tools/preflight_lefil_talk.py" in workflow,
        "précontrôle exécuté avant compilation")
require('script: bash "$GITHUB_WORKSPACE/tools/android_smoke.sh"' in workflow,
        "test Android en un seul processus shell, sans perte de variables")
require(workflow.count("name: lefil-talk-arm64-test-non-publiable") == 2,
        "nom d'artefact identique entre compilation et téléchargement")
relative = "upstream/app/build/outputs/apk/fdroid/debug/app-fdroid-x86_64-debug.apk"
require(f"artefact/{relative}" in smoke, "APK x86_64 testée au chemin téléchargé")
require("path: artefact" in workflow, "racine de téléchargement conforme au script")
require("adb install -r" in smoke and "adb shell pidof" in smoke and
        "screencap" in smoke and "uiautomator dump" in smoke,
        "test installation, processus et preuves visuelles présents")
require("grep -Fx \"application-label:'Le Fil Talk'\"" in workflow,
        "identité visible exacte bloquante")
require("git clone --depth 1 --branch v26.10.1" in workflow,
        "version amont verrouillée")
require("gh release" not in workflow, "pas de publication depuis la compilation diagnostique")
logo = (root / "LogoLeFilTalk.png").read_bytes()
require(logo[:8] == b"\\x89PNG\\r\\n\\x1a\\n" and
        len(logo) >= 24 and
        struct.unpack(">II", logo[16:24]) == (1254, 1254),
        "logo officiel PNG 1254 x 1254")
print("Précontrôle réussi : Android peut être compilé.")
