#!/usr/bin/env python3
"""Personnalisation minimale de FluffyChat v2.11.5 ; aucune création de salon ni désactivation du chiffrement."""
from pathlib import Path
from PIL import Image, ImageOps
from urllib.request import urlopen
import hashlib
import os
from urllib.parse import urlparse

root = Path("fluffychat")
# Le composant graphique est versionne separément; aucune dependance serveur.
from shutil import copyfile
copyfile(Path("tools/lefil_banner.dart"), root / "lib/widgets/lefil_banner.dart")
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
# Candidat de test en mode release AOT, signé avec la clé DEBUG Android :
# ne jamais présenter cette signature comme une signature de publication définitive.
change("android/app/build.gradle.kts", 'signingConfig = signingConfigs.getByName("release")', 'signingConfig = signingConfigs.getByName("debug")')
change("lib/config/app_config.dart", "static const Color primaryColor = Color(0xFF261386);", "static const Color primaryColor = Color(0xFF4A0050);")
# Identite et passerelle push specifiques a Le Fil Talk.
# Le jeton FCM de notre projet ne fonctionne pas avec la passerelle Firebase d'une autre application.
gateway = os.environ.get("LEFIL_PUSH_GATEWAY_URL", "").strip()
parsed = urlparse(gateway)
if (not gateway or parsed.scheme != "https" or not parsed.netloc
        or parsed.username or parsed.password or parsed.query or parsed.fragment
        or parsed.path != "/_matrix/push/v1/notify"
        or parsed.hostname == "push.fluffychat.im"):
    raise RuntimeError("Passerelle push Le Fil HTTPS dediee obligatoire : refuse de compiler sans configuration")
change("lib/config/app_config.dart",
       "static const String pushNotificationsAppId = 'chat.fluffy.fluffychat';",
       "static const String pushNotificationsAppId = 'net.lefil.talk';")
change("lib/config/setting_keys.dart",
       "'https://push.fluffychat.im/_matrix/push/v1/notify',",
       f"'{gateway}',")

# Nom visible dans l'interface (distinct du libellé Android dans le manifeste).
change("lib/config/setting_keys.dart",
       "applicationName<String>('chat.fluffy.application_name', 'FluffyChat'),",
       "applicationName<String>('chat.fluffy.application_name', 'Le Fil Talk'),")
# Menu de soutien : adapter uniquement le texte visible et la destination du lien.
# Le fonctionnement du menu et les autres liens FluffyChat restent inchangés.
change("lib/pages/chat_list/client_chooser_button.dart",
       "Text(L10n.of(context).supportFluffyChat),",
       "Text('Soutenir Le Fil'),")
change("lib/pages/chat_list/client_chooser_button.dart",
       "'https://ko-fi.com/post/How-can-I-support-FluffyChat-J2G325WE6I',",
       "'https://le-fil.net/soutenir.html',")
# Accueil: supprimer la publicité technique Matrix et l'anglais de l'écran initial.
# Conserver les boutons et les parcours natifs de connexion et inscription.
change("lib/pages/intro/intro_page.dart",
       "L10n.of(context).appSubtitle,",
       "'Se relier malgré la distance et la dispersion',")
change("lib/pages/intro/intro_page.dart",
       "welcomeText ?? L10n.of(context).appDescription,",
       "welcomeText ?? 'Bienvenue sur Le Fil Talk. Retrouvez vos discussions, vos groupes et vos amis.',")
change("lib/pages/intro/intro_page.dart",
       "L10n.of(context).loginWithMatrixId,",
       "'Autre méthode de connexion',")
# Premier écran destiné aux adhérents francophones : texte compact, lisible,
# sans libellés anglais ni formulaires techniques ajoutés.
change("lib/pages/intro/intro_page.dart",
       "style: TextStyle(fontSize: 20),",
       "style: TextStyle(fontSize: 16),")
change("lib/pages/intro/intro_page.dart",
       "L10n.of(context).createNewAccount,",
       "'Créer mon compte',")
change("lib/pages/intro/intro_page.dart",
       "child: Text(L10n.of(context).signIn),",
       "child: Text('Se connecter'),")

change("lib/config/themes.dart", "seedColor: seed ?? Color(AppSettings.colorSchemeSeedInt.value),", "seedColor: const Color(0xFF4A0050),")
# Bandeau identitaire uniquement sur l'accueil et la liste des discussions.
# Conserver les menus, fonctions natives, recherche et interactions existantes.
change("lib/pages/intro/intro_page.dart",
       "import 'package:fluffychat/widgets/matrix.dart';",
       "import 'package:fluffychat/widgets/matrix.dart';\nimport 'package:fluffychat/widgets/lefil_banner.dart';")
change("lib/pages/intro/intro_page.dart",
       "        title: addMultiAccount\n            ? Text(L10n.of(context).addAccount)\n            : Text(AppSettings.applicationName.value),",
       "        title: addMultiAccount\n            ? Text(L10n.of(context).addAccount)\n            : const LeFilBanner(compact: true),")
change("lib/pages/intro/intro_page.dart",
       "        centerTitle: true,",
       "        centerTitle: true,\n        titleSpacing: 0,\n        toolbarHeight: 72,")
change("lib/pages/chat_list/chat_list_view.dart",
       "import 'package:fluffychat/pages/chat_list/start_chat_fab.dart';",
       "import 'package:fluffychat/pages/chat_list/start_chat_fab.dart';\nimport 'package:fluffychat/widgets/lefil_banner.dart';")
change("lib/pages/chat_list/chat_list_view.dart",
       "                    child: ChatListViewBody(controller),",
       "                    child: Column(\n                      children: [\n                        const SafeArea(\n                          bottom: false,\n                          child: LeFilBanner(),\n                        ),\n                        Expanded(child: ChatListViewBody(controller)),\n                      ],\n                    ),")

change("lib/config/themes.dart", "      useMaterial3: true,", "      useMaterial3: true,\n      fontFamily: 'Poppins',")
# Après une connexion réussie, ouvrir directement les conversations.
# La sauvegarde / vérification cryptographique reste disponible dans Réglages > Sauvegarde.
# NE PAS supprimer le chiffrement, les clés, ni l'écran de sauvegarde ; il devient facultatif à l'arrivée.
for route in (
    "lib/pages/login/login.dart",
    "lib/pages/intro/intro_page_presenter.dart",
    "lib/utils/sign_in_flows/check_homeserver.dart",
):
    change(route, "context.go('/backup');", "context.go('/rooms');")

# En-tête bleu du Fil, tout en conservant l'ergonomie et les composants natifs FluffyChat.
change("lib/config/themes.dart",
       "backgroundColor: isColumnMode ? colorScheme.surface : null,",
       "backgroundColor: const Color(0xFF0C1853),\n        foregroundColor: Colors.white,")

# Ne pas interrompre l'ouverture des discussions par un avertissement cryptographique.
# Masquer uniquement le SnackBar de 15 secondes ; les etats, cles, controles,
# reglages et fonctions de verification des appareils restent natifs.
change("lib/pages/chat_list/chat_list.dart",
       """    if (client.userDeviceKeys[client.userID!]?.deviceKeys.values.any(
          (device) => !device.verified && !device.blocked,
        ) ??
        false) {
      late final ScaffoldFeatureController controller;
      final theme = Theme.of(context);
      controller = ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          duration: const Duration(seconds: 15),
          showCloseIcon: true,
          backgroundColor: theme.colorScheme.errorContainer,
          closeIconColor: theme.colorScheme.onErrorContainer,
          content: Text(
            L10n.of(context).oneOfYourDevicesIsNotVerified,
            style: TextStyle(color: theme.colorScheme.onErrorContainer),
          ),
          action: SnackBarAction(
            onPressed: () {
              controller.close();
              router.go('/rooms/settings/devices');
            },
            textColor: theme.colorScheme.onErrorContainer,
            label: L10n.of(context).settings,
          ),
        ),
      );
    }
""",
       "")
change("lib/pages/chat_list/chat_list.dart",
       "    final router = GoRouter.of(context);\n    final client = Matrix.of(context).client;\n    await client.roomsLoading;",
       "    final client = Matrix.of(context).client;\n    await client.roomsLoading;")

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
original_logo_path = Path("LogoLeFilTalk.png")
expected_sha256 = "f8cc9c0dbd585615aa3d7ffebff924415ef66761610a5aaeb1ece33b01995f5b"
actual_sha256 = hashlib.sha256(original_logo_path.read_bytes()).hexdigest()
if actual_sha256 != expected_sha256:
    raise RuntimeError(f"Logo non conforme à l'image fournie par l'utilisateur: {actual_sha256}")
logo = Image.open(original_logo_path).convert("RGBA")
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
# Remplacer les éléments visuels FluffyChat effectivement affichés, sans redessiner le logo.
# Adapter uniquement les dimensions du logo source, conserver sa forme et ses couleurs.
for directory in (root / "assets/logo/img", root / "assets/logo/mini"):
    for path in directory.glob("*.png"):
        if path.name in {"logo_background.png", "logo_foreground.png", "logo_mono.png", "logo.png", "logo_standalone.png"} and directory == assets:
            continue
        with Image.open(path) as template:
            canvas_size = template.size
        out = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        fit = ImageOps.contain(logo, (max(1, int(canvas_size[0] * .93)), max(1, int(canvas_size[1] * .93))), Image.Resampling.LANCZOS)
        out.alpha_composite(fit, ((canvas_size[0] - fit.width) // 2, (canvas_size[1] - fit.height) // 2))
        out.save(path)
# Image de démarrage Android : remplacer le chat FluffyChat dans TOUS les dossiers de densité.
for path in (root / "android/app/src/main/res").glob("drawable-*/splash.png"):
    with Image.open(path) as template:
        canvas_size = template.size
    out = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    fit = ImageOps.contain(logo, (max(1, int(canvas_size[0] * .88)), max(1, int(canvas_size[1] * .88))), Image.Resampling.LANCZOS)
    out.alpha_composite(fit, ((canvas_size[0] - fit.width) // 2, (canvas_size[1] - fit.height) // 2))
    out.save(path)
# Fournir un fond bleu profond au splash, dans la palette Le Fil.
for path in (root / "android/app/src/main/res").glob("drawable-*/background.png"):
    with Image.open(path) as template:
        size = template.size
    Image.new("RGB", size, "#0C1853").save(path)
print("Logo original SHA256 vérifié, identité des icônes et du splash remplacée, aucune préconfiguration des espaces.")
