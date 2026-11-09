#!/usr/bin/env python3
"""Installer l'atelier visuel dans un module Android Compose existant, sans toucher aux sources de production."""
from pathlib import Path
from urllib.request import urlopen, Request
import argparse, shutil, re
p=argparse.ArgumentParser()
p.add_argument("--module",required=True,help="Chemin du module Android Compose")
p.add_argument("--namespace",required=True,help="Namespace Android du module, par exemple com.example.preview")
a=p.parse_args()
if not re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+",a.namespace):
    raise SystemExit("Namespace invalide")
module=Path(a.module)
if not (module/"build.gradle.kts").exists() and not (module/"build.gradle").exists():
    raise SystemExit("Module Android Gradle absent")
dest=module/"src/debug"
src=dest/"java"/Path(*a.namespace.split("."))
res=dest/"res"
src.mkdir(parents=True,exist_ok=True)
(res/"drawable-nodpi").mkdir(parents=True,exist_ok=True)
(res/"font").mkdir(parents=True,exist_ok=True)
code=Path(__file__).with_name("TalkVisualPreview.kt").read_text(encoding="utf-8")
code=code.replace("package net.lefil.talk.preview",f"package {a.namespace}")
code=code.replace("import net.lefil.talk.preview.R",f"import {a.namespace}.R")
(src/"TalkVisualPreview.kt").write_text(code,encoding="utf-8")
logo=Path("LogoLeFilTalk.png")
if not logo.is_file():
    raise SystemExit("LogoLeFilTalk.png absent : lancer depuis la racine du dépôt")
shutil.copyfile(logo,res/"drawable-nodpi/lefil_talk_logo.png")
for weight in ("Regular","Medium","Bold"):
    url=f"https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-{weight}.ttf"
    data=urlopen(Request(url,headers={"User-Agent":"LeFilTalkPreview"}),timeout=30).read()
    if len(data)<10000 or data[:4] not in (bytes.fromhex("00010000"),b"OTTO"):
        raise SystemExit(f"Police invalide: {weight}")
    (res/"font"/f"poppins_{weight.lower()}.ttf").write_bytes(data)
print("Atelier installé dans src/debug uniquement ; logo et Poppins locaux. Ouvrir TalkVisualPreview.kt dans Android Studio.")
