#!/usr/bin/env python3
"""Accueil Le Fil Talk sur l'ecran natif de connexion Element X v26.10.1.

Aucune modification de Matrix, des appels, des notifications ou des salons.
Les espaces sont presentes, sans inventer des salons sur matrix.org.
"""
from pathlib import Path

path = Path("upstream/features/login/impl/src/main/kotlin/io/element/android/features/login/impl/screens/onboarding/OnBoardingView.kt")
src = path.read_text(encoding="utf-8")
old_logo = """            ElementLogoAtom(
                size = ElementLogoAtomSize.Large,
                modifier = Modifier.padding(top = ElementLogoAtomSize.Large.shadowRadius / 2)
            )"""
new_logo = """            Image(
                painter = painterResource(id = R.drawable.onboarding_logo),
                contentDescription = "Logo officiel Le Fil Talk",
                modifier = Modifier
                    .padding(24.dp)
                    .height(160.dp)
            )"""
assert src.count(old_logo) == 1, "Ancrage logo Element X inattendu"
src = src.replace(old_logo, new_logo)
old_text = """                Text(
                    text = stringResource(id = R.string.screen_onboarding_welcome_title),
                    color = ElementTheme.colors.textPrimary,
                    style = ElementTheme.typography.fontHeadingLgBold,
                    textAlign = TextAlign.Center,
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = stringResource(id = R.string.screen_onboarding_welcome_message, state.productionApplicationName),
                    color = ElementTheme.colors.textPrimary,
                    style = ElementTheme.typography.fontBodyLgRegular,
                    textAlign = TextAlign.Center,
                )"""
new_text = """                Text(
                    text = "Bienvenue sur Le Fil",
                    color = ElementTheme.colors.textPrimary,
                    style = ElementTheme.typography.fontHeadingLgBold,
                    textAlign = TextAlign.Center,
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Se relier malgré la distance et la dispersion",
                    color = ElementTheme.colors.textSecondary,
                    style = ElementTheme.typography.fontBodyMdRegular,
                    textAlign = TextAlign.Center,
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Papote · Échanger librement",
                    color = ElementTheme.colors.textPrimary,
                    style = ElementTheme.typography.fontBodyMdRegular,
                    textAlign = TextAlign.Center,
                )
                Text(
                    text = "Sentiers · Cheminer par thèmes",
                    color = ElementTheme.colors.textPrimary,
                    style = ElementTheme.typography.fontBodyMdRegular,
                    textAlign = TextAlign.Center,
                )
                Text(
                    text = "Oasis · Se retrouver localement",
                    color = ElementTheme.colors.textPrimary,
                    style = ElementTheme.typography.fontBodyMdRegular,
                    textAlign = TextAlign.Center,
                )
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = "Connexion gratuite avec matrix.org",
                    color = ElementTheme.colors.textSecondary,
                    style = ElementTheme.typography.fontBodySmRegular,
                    textAlign = TextAlign.Center,
                )"""
assert src.count(old_text) == 1, "Ancrage accueil Element X inattendu"
src = src.replace(old_text, new_text)

old_buttons = """    ButtonColumnMolecule {
        val signInButtonStringRes = if (state.canLoginWithQrCode || state.canCreateAccount) {
            R.string.screen_onboarding_sign_in_manually
        } else {
            CommonStrings.action_continue
        }
        if (state.canLoginWithQrCode) {
            Button(
                text = stringResource(id = R.string.screen_onboarding_sign_in_with_qr_code),
                leadingIcon = IconSource.Vector(CompoundIcons.QrCode()),
                onClick = onSignInWithQrCode,
                modifier = Modifier.fillMaxWidth()
            )
        }
        val defaultAccountProvider = state.defaultAccountProvider
        if (defaultAccountProvider == null) {
            Button(
                text = stringResource(id = signInButtonStringRes),
                onClick = {
                    onSignIn(state.mustChooseAccountProvider)
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag(TestTags.onBoardingSignIn)
            )
        } else {
            Button(
                text = stringResource(id = R.string.screen_onboarding_sign_in_to, defaultAccountProvider.friendlyServerName()),
                showProgress = isLoading,
                onClick = {
                    state.eventSink(OnBoardingEvent.OnSignIn(defaultAccountProvider))
                },
                enabled = state.submitEnabled || isLoading,
                modifier = Modifier
                    .fillMaxWidth()
            )
        }
        if (state.canCreateAccount) {
            TextButton(
                text = stringResource(id = R.string.screen_onboarding_sign_up),
                onClick = onCreateAccount,
                modifier = Modifier
                    .fillMaxWidth()
            )
        }
"""
new_buttons = """    ButtonColumnMolecule {
        val defaultAccountProvider = state.defaultAccountProvider
        if (state.canCreateAccount) {
            Button(
                text = "Je crée mon compte gratuit",
                onClick = onCreateAccount,
                modifier = Modifier.fillMaxWidth()
            )
        }
        if (defaultAccountProvider == null) {
            TextButton(
                text = "J'ai déjà un compte",
                onClick = { onSignIn(state.mustChooseAccountProvider) },
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag(TestTags.onBoardingSignIn)
            )
        } else {
            TextButton(
                text = "J'ai déjà un compte",
                onClick = { state.eventSink(OnBoardingEvent.OnSignIn(defaultAccountProvider)) },
                enabled = state.submitEnabled || isLoading,
                modifier = Modifier.fillMaxWidth()
            )
        }
        if (state.canLoginWithQrCode) {
            Button(
                text = stringResource(id = R.string.screen_onboarding_sign_in_with_qr_code),
                leadingIcon = IconSource.Vector(CompoundIcons.QrCode()),
                onClick = onSignInWithQrCode,
                modifier = Modifier.fillMaxWidth()
            )
        }
"""
assert src.count(old_buttons) == 1, "Ancrage des boutons d'accueil Element X inattendu"
src = src.replace(old_buttons, new_buttons)
path.write_text(src, encoding="utf-8")
print("Accueil Le Fil Talk applique : logo officiel, création de compte prioritaire, connexion native secondaire, QR conservé.")
