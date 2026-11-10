#!/usr/bin/env python3
"""Personnalisation minimale de FluffyChat v2.11.5 ; aucune création de salon ni désactivation du chiffrement."""
from pathlib import Path
from PIL import Image
from urllib.request import urlopen

root = Path("fluffychat")
def change(path, old, new):
    p = root / path
    source = p.read_text(encoding="utf-8")
    if source.count(old) != 1:
        raise RuntimeError(f"Ancrage inattendu dans {path}: {old!r} ({source.count(old)})")
    p.write_text(source.replace(old, new), encoding="utf-8")

change("android/app/src/main/AndroidManifest.xml", 'android:label="FluffyChat"', 'android:label="Le Fil Talk"')
# Conserver la résolution correcte des classes natives malgré le nouvel applicationId.
for activity in ("MainActivity", "FcmPushService", "UnifiedPushService"):
    change("android/app/src/main/AndroidManifest.xml",
           f'android:name=".{activity}"', f'android:name="chat.fluffy.fluffychat.{activity}"')
change("android/app/build.gradle.kts", 'applicationId = "chat.fluffy.fluffychat"', 'applicationId = "net.lefil.talk"')
change("lib/config/app_config.dart", "static const Color primaryColor = Color(0xFF261386);", "static const Color primaryColor = Color(0xFF4A0050);")
change("lib/config/themes.dart", "seedColor: seed ?? Color(AppSettings.colorSchemeSeedInt.value),", "seedColor: const Color(0xFF4A0050),")
change("lib/config/themes.dart", "      useMaterial3: true,", "      useMaterial3: true,\n      fontFamily: 'Poppins',")
# Poppins 400/500/700 : pour une identité cohérente tout en gardant les composants natifs.
fonts = root / "assets/fonts"
fonts.mkdir(parents=True, exist_ok=True)
for weight in ("Regular", "Medium", "Bold"):
    url = f"https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-{weight}.ttf"
    data = urlopen(url, timeout=35).read()
    if len(data) < 10000 or data[:4] not in (bytes.fromhex("00010000"), b"OTTO"):
        raise RuntimeError(f"Police invalide: {weight}")
    (fonts / f"Poppins-{weight}.ttf").write_bytes(data)
pub = root / "pubspec.yaml"
source = pub.read_text(encoding="utf-8")
anchor = "  uses-material-design: true\n"
if source.count(anchor) != 1:
    raise RuntimeError("Ancrage pubspec fonts absent")
font_yaml = """  fonts:
    - family: Poppins
      fonts:
        - asset: assets/fonts/Poppins-Regular.ttf
          weight: 400
        - asset: assets/fonts/Poppins-Medium.ttf
          weight: 500
        - asset: assets/fonts/Poppins-Bold.ttf
          weight: 700
"""
pub.write_text(source.replace(anchor, anchor + font_yaml), encoding="utf-8")
# L'icône vient uniquement du logo officiel Le Fil Talk.
logo = Image.open("LogoLeFilTalk.png").convert("RGBA")
if logo.size != (1254, 1254):
    raise RuntimeError("Logo officiel inattendu")
assets = root / "assets/logo/img"
# Icônes legacy: conserver le logo rond entier sur fond transparent.
for name in ("logo.png", "logo_standalone.png"):
    logo.resize((1024, 1024), Image.Resampling.LANCZOS).save(assets / name)
# Icône adaptative Android: zone de sûreté centrale pour les masques circulaires.
# Ne pas remplir toute la surface: le système recadre sur certains téléphones.
safe = 672
foreground = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
small_logo = logo.resize((safe, safe), Image.Resampling.LANCZOS)
foreground.alpha_composite(small_logo, ((1024 - safe) // 2, (1024 - safe) // 2))
foreground.save(assets / "logo_foreground.png")
bg = Image.new("RGBA", (1024, 1024), "#0C1853")
bg.save(assets / "logo_background.png")
# Icône monochrome cohérente (silhouette alpha du logo).
mono = Image.new("RGBA", (1024, 1024), "white")
mono.putalpha(logo.resize((1024, 1024), Image.Resampling.LANCZOS).getchannel("A"))
mono.save(assets / "logo_mono.png")
print("Identité Le Fil Talk appliquée: logo, nom, couleurs et Poppins. Aucune préconfiguration des espaces.")
