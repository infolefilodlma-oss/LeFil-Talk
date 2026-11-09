#!/usr/bin/env python3
"""Applique Poppins aux tokens Compose d'Element X v26.10.1, sans toucher à Matrix."""
from pathlib import Path
from urllib.request import Request, urlopen

root = Path("upstream/libraries/compound")
tokens = root / "src/main/kotlin/io/element/android/compound/tokens/generated/TypographyTokens.kt"
compound = root / "src/main/kotlin/io/element/android/compound/tokens/CompoundTypography.kt"
for path in (tokens, compound):
    if not path.is_file():
        raise SystemExit(f"Source Element X absente : {path}")
    source = path.read_text()
    if "fontFamily = FontFamily.Default" not in source:
        raise SystemExit(f"Tokens typographiques inattendus : {path}")

fonts = root / "src/main/res/font"
fonts.mkdir(parents=True, exist_ok=True)
for weight, name in [(400, "Regular"), (500, "Medium"), (700, "Bold")]:
    url = f"https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-{name}.ttf"
    with urlopen(Request(url, headers={"User-Agent": "LeFil-Talk-CI"}), timeout=30) as response:
        data = response.read(1_000_001)
    if not 10_000 < len(data) < 1_000_000 or data[:4] not in (b"\\x00\\x01\\x00\\x00", b"OTTO"):
        raise SystemExit(f"Fichier de police non valide : {name}")
    (fonts / f"poppins_{name.lower()}.ttf").write_bytes(data)

for path in (tokens, compound):
    source = path.read_text()
    source = source.replace("import androidx.compose.ui.text.font.FontFamily", "import androidx.compose.ui.text.font.Font\nimport androidx.compose.ui.text.font.FontFamily")
    source = source.replace("import androidx.compose.ui.text.font.FontWeight", "import androidx.compose.ui.text.font.FontWeight\nimport io.element.android.compound.R")
    family = """private val leFilPoppins = FontFamily(
    Font(R.font.poppins_regular, FontWeight.Normal),
    Font(R.font.poppins_medium, FontWeight.Medium),
    Font(R.font.poppins_bold, FontWeight.Bold),
)

"""
    anchor = "object TypographyTokens {" if path == tokens else "// 32px (Material) vs 34px"
    if source.count(anchor) != 1:
        raise SystemExit(f"Ancrage de typographie inattendu : {path}")
    source = source.replace(anchor, family + anchor)
    source = source.replace("fontFamily = FontFamily.Default", "fontFamily = leFilPoppins")
    path.write_text(source)
print("Poppins appliquée aux tokens typographiques Compose et Material3, poids 400/500/700.")
