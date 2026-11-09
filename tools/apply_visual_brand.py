#!/usr/bin/env python3
"""Branding Le Fil Talk : ressources Android uniquement, sans changer Matrix."""
from pathlib import Path
from PIL import Image
import hashlib

root=Path("upstream")
logo_path=Path("LogoLeFilTalk.png")
if not logo_path.is_file():
    raise SystemExit(f"Logo officiel absent : {logo_path}. Aucun autre logo ne sera utilisé.")
raw=logo_path.read_bytes()
if len(raw)>5_000_000 or not raw.startswith(bytes.fromhex("89504e470d0a1a0a")):
    raise SystemExit("Logo officiel invalide ou trop volumineux.")
img=Image.open(logo_path)
img.verify()
img=Image.open(logo_path).convert("RGBA")
if img.size != (1254,1254):
    raise SystemExit(f"Dimensions du logo officiel inattendues : {img.size}")
print("Logo officiel vérifié",logo_path,hashlib.sha256(raw).hexdigest())

# Icones du lanceur : remplacer uniquement les images raster de l'icone Element.
# Conserver les XML adaptatifs, la structure de l'application et ses mecanismes de login.
densities={"mdpi":48,"hdpi":72,"xhdpi":96,"xxhdpi":144,"xxxhdpi":192}
base=root/"appicon/element/src/main/res"
for density,size in densities.items():
    folder=base/f"mipmap-{density}"
    for name in ("ic_launcher.webp","ic_launcher_round.webp"):
        dest=folder/name
        if not dest.exists():
            raise SystemExit(f"Ressource amont inattendue : {dest}")
        canvas=Image.new("RGBA",(size,size),(0,0,0,0))
        fitted=img.copy()
        fitted.thumbnail((round(size*.98),round(size*.98)),Image.Resampling.LANCZOS)
        canvas.alpha_composite(fitted,((size-fitted.width)//2,(size-fitted.height)//2))
        canvas.save(dest,"WEBP",lossless=True,method=6)
    # L'icone adaptative foreground est une ressource distincte.
    fg=folder/"ic_launcher_foreground.webp"
    if not fg.exists():
        raise SystemExit(f"Ressource amont inattendue : {fg}")
    size_fg=Image.open(fg).size
    foreground=Image.new("RGBA",size_fg,(0,0,0,0))
    fitted=img.copy()
    fitted.thumbnail((round(size_fg[0]*.48),round(size_fg[1]*.48)),Image.Resampling.LANCZOS)
    foreground.alpha_composite(fitted,((size_fg[0]-fitted.width)//2,(size_fg[1]-fitted.height)//2))
    foreground.save(fg,"WEBP",lossless=True,method=6)

# Onboarding : point d'extension amont, utilise si la ressource existe.
onboard=root/"features/login/impl/src/main/res/drawable-nodpi/onboarding_logo.png"
onboard.parent.mkdir(parents=True,exist_ok=True)
logo=img.copy()
logo.thumbnail((420,420),Image.Resampling.LANCZOS)
logo.save(onboard)

# Violet du Fil : uniquement les fonds de lancement, sans modifier les tokens
# generes du systeme de design Element X.
colors=root/"app/src/main/res/values/colors.xml"
s=colors.read_text()
needle='<color name="splashscreen_bg_light">#FFFFFFFF</color>'
if s.count(needle)!=1:
    raise SystemExit("Source amont inattendue pour couleur de lancement")
colors.write_text(s.replace(needle,'<color name="splashscreen_bg_light">#FF4A0050</color>'))
print("Identite Le Fil Talk : logo officiel, icones, onboarding et violet #4A0050.")
