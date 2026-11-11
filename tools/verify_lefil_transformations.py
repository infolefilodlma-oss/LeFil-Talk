#!/usr/bin/env python3
"""Vérifie le résultat des patches Le Fil Talk sur Element X v26.10.1."""
from pathlib import Path
import hashlib
import struct
import subprocess

root = Path("upstream")

def read(relative):
    path = root / relative
    if not path.is_file():
        raise SystemExit(f"TRANSFORMATIONS BLOQUÉES : fichier absent : {path}")
    return path.read_text(encoding="utf-8")

def require(condition, message):
    if not condition:
        raise SystemExit("TRANSFORMATIONS BLOQUÉES : " + message)
    print("OK :", message)

onboarding = read("features/login/impl/src/main/kotlin/io/element/android/features/login/impl/screens/onboarding/OnBoardingView.kt")
confirm = read("features/login/impl/src/main/kotlin/io/element/android/features/login/impl/screens/confirmaccountprovider/ConfirmAccountProviderPresenter.kt")
home = read("features/home/impl/src/main/kotlin/io/element/android/features/home/impl/HomeView.kt")
spaces = read("features/home/impl/src/main/kotlin/io/element/android/features/home/impl/spaces/HomeSpacesView.kt")
typography = read("libraries/compound/src/main/kotlin/io/element/android/compound/tokens/generated/TypographyTokens.kt")
compound_typography = read("libraries/compound/src/main/kotlin/io/element/android/compound/tokens/CompoundTypography.kt")
colors = read("libraries/compound/src/main/kotlin/io/element/android/compound/tokens/generated/SemanticColorsLight.kt")

logo = Path("LogoLeFilTalk.png")
require(logo.is_file(), "logo officiel présent")
raw = logo.read_bytes()
require(raw[:8] == bytes.fromhex("89504e470d0a1a0a"), "logo officiel PNG valide")
require(struct.unpack(">II", raw[16:24]) == (1254, 1254), "logo officiel 1254 x 1254")
onboarding_logo = root / "features/login/impl/src/main/res/drawable-nodpi/onboarding_logo.png"
require(onboarding_logo.is_file(), "logo onboarding généré")
require(hashlib.sha256(onboarding_logo.read_bytes()).hexdigest() != hashlib.sha256(raw).hexdigest(),
        "logo onboarding redimensionné par le patch")

require('text = "Bienvenue sur Le Fil"' in onboarding, "titre d'accueil Le Fil présent")
require('text = "Je crée mon compte gratuit"' in onboarding, "bouton création principal présent")
require('onClick = onCreateAccount' in onboarding, "création reliée à onCreateAccount")
require('text = "J\'ai déjà un compte"' in onboarding, "bouton connexion secondaire présent")
require('onSignIn(state.mustChooseAccountProvider)' in onboarding or 'OnBoardingEvent.OnSignIn' in onboarding,
        "connexion native conservée")
require('onSignInWithQrCode' in onboarding, "connexion QR conservée")
require('showSignUpHelp' in onboarding and 'onCreateAccount = { showSignUpHelp = true }' in onboarding,
        "aide inscription présente sans remplacer le flux natif")
require('matrix.org' in confirm or 'matrix.org' in onboarding, "matrix.org référencé pour l'inscription")
require('LeFilNavigation' in home and 'Papote' in home and 'Sentiers' in home and 'Oasis' in home,
        "navigation Papote/Sentiers/Oasis présente")
require('leFilSection' in home and 'visibleSpaces' in spaces, "filtrage des espaces branché sur l'écran natif")
require('fontFamily = leFilPoppins' in typography and 'fontFamily = leFilPoppins' in compound_typography,
        "Poppins appliquée aux deux ensembles typographiques")
for token in ('0xFF4A0050', '0xFF26002C', '0xFFF8F6FB'):
    require(token in colors, f"couleur {token} présente")

modified = subprocess.run(
    ["git", "-C", str(root), "diff", "--name-only"],
    text=True, capture_output=True, check=True,
).stdout.splitlines()
for path in modified:
    require(not path.startswith(("libraries/matrix/", "libraries/rustsdk/", "features/call/", "features/notifications/")),
            f"fonction native préservée : {path}")

print("Transformations Le Fil Talk vérifiées ; aucune compilation exécutée.")
