#!/usr/bin/env python3
"""Aide d'inscription Le Fil Talk sur le flux Matrix natif (Element X v26.10.1)."""
from pathlib import Path
root=Path("upstream/features/login/impl/src/main/kotlin/io/element/android/features/login/impl")
def replace(path,old,new):
    p=root/path
    s=p.read_text(encoding="utf-8")
    if s.count(old)!=1:
        raise SystemExit(f"Source amont inattendue : {p} ({s.count(old)} correspondances)")
    p.write_text(s.replace(old,new),encoding="utf-8")

p=Path("screens/onboarding/OnBoardingView.kt")
replace(p,"import androidx.compose.foundation.Image\n","import androidx.compose.foundation.Image\nimport androidx.compose.material3.AlertDialog\nimport androidx.compose.material3.Text as MaterialText\nimport androidx.compose.material3.TextButton as MaterialTextButton\nimport androidx.compose.runtime.mutableStateOf\nimport androidx.compose.runtime.setValue\n")
replace(p,"    val buttons = @Composable {\n","    var showSignUpHelp by remember { mutableStateOf(false) }\n    if (showSignUpHelp) {\n        AlertDialog(\n            onDismissRequest = { showSignUpHelp = false },\n            title = { MaterialText(\"Bienvenue sur Le Fil Talk\") },\n            text = { MaterialText(\"Pour discuter avec les membres du Fil, créez gratuitement un compte sur matrix.org.\\n\\n1. Choisissez un nom d'utilisateur (pas votre adresse e-mail).\\n2. Créez un mot de passe et conservez-le.\\n3. Confirmez votre adresse e-mail si matrix.org le demande.\\n4. Conservez votre clé de récupération des messages chiffrés si elle est proposée.\\n\\nVotre identifiant ressemblera à @prenom:matrix.org.\") },\n            confirmButton = {\n                MaterialTextButton(onClick = { showSignUpHelp = false; onCreateAccount() }) {\n                    MaterialText(\"Créer mon compte\")\n                }\n            },\n            dismissButton = {\n                MaterialTextButton(onClick = { showSignUpHelp = false }) { MaterialText(\"Plus tard\") }\n            },\n        )\n    }\n    val buttons = @Composable {\n")
replace(p,"            onCreateAccount = onCreateAccount,\n            onReportProblem = onReportProblem,\n","            onCreateAccount = { showSignUpHelp = true },\n            onReportProblem = onReportProblem,\n")

p=Path("screens/confirmaccountprovider/ConfirmAccountProviderPresenter.kt")
replace(p,"        var userInput by rememberSaveable { mutableStateOf<String?>(null) }\n","        // Creation de compte Le Fil Talk : matrix.org propose sans bloquer les comptes existants.\n        var userInput by rememberSaveable { mutableStateOf<String?>(if (params.isAccountCreation) \"matrix.org\" else null) }\n")
print("Aide d'inscription, bouton natif et matrix.org preselectionne : patch applique.")
