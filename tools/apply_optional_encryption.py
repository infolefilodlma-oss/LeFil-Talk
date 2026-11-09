#!/usr/bin/env python3
"""Le Fil Talk: nouvelles conversations non chiffrées par défaut, chiffrement activable ensuite."""
from pathlib import Path

ROOT = Path("upstream")

def replace_once(relative, old, new):
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"Fichier Element X absent : {path}")
    source = path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"Ancrage inattendu dans {path}: attendu 1, trouvé {count}. Arrêt sans patch partiel.")
    path.write_text(source.replace(old, new, 1), encoding="utf-8")
    print(f"Modifié : {path}")

# Les nouvelles conversations directes, privées de groupe et les conversions de DM
# en conversation de groupe commencent sans E2EE. Les salons déjà chiffrés ne changent pas.
replace_once(
    "features/startchat/impl/src/main/kotlin/io/element/android/features/startchat/impl/DefaultStartDMAction.kt",
    "isEncryped = !sessionEnterpriseService.isEncryptionDisabledByHomeserver(),",
    "isEncryped = false, // Le Fil Talk : chiffrement activable ensuite dans la conversation.",
)
replace_once(
    "features/createroom/impl/src/main/kotlin/io/element/android/features/createroom/impl/configureroom/ConfigureRoomPresenter.kt",
    "isEncrypted = !sessionEnterpriseService.isEncryptionDisabledByHomeserver(),",
    "isEncrypted = false, // Le Fil Talk : chiffrement activable ensuite dans les paramètres de la conversation.",
)
replace_once(
    "features/invitepeople/impl/src/main/kotlin/io/element/android/features/invitepeople/impl/DefaultInvitePeoplePresenter.kt",
    "isEncrypted = true,",
    "isEncrypted = false, // Le Fil Talk : chiffrement activable ensuite dans les paramètres de la conversation.",
)

# Ne pas supprimer la capacité native d'activer E2EE ultérieurement.
security = ROOT / "features/securityandprivacy/impl/src/main/kotlin/io/element/android/features/securityandprivacy/impl/root/SecurityAndPrivacyPresenter.kt"
security_source = security.read_text(encoding="utf-8")
if "room.enableEncryption()" not in security_source or "SecurityAndPrivacyEvent.ConfirmEnableEncryption" not in security_source:
    raise SystemExit("Le point d'activation native du chiffrement n'est plus présent : arrêt.")

# Ne pas demander de clé de récupération tant qu'aucune conversation chiffrée n'existe.
room_list = "features/home/impl/src/main/kotlin/io/element/android/features/home/impl/roomlist/RoomListPresenter.kt"
replace_once(
    room_list,
    "        val securityBannerState by rememberSecurityBannerState(securityBannerDismissed)\n",
    "            val hasEncryptedRooms = roomSummaries.dataOrNull().orEmpty().any { it.info.isEncrypted == true }\n"
    "            val securityBannerState by rememberSecurityBannerState(securityBannerDismissed, hasEncryptedRooms)\n",
)
replace_once(
    room_list,
    "    private fun rememberSecurityBannerState(\n        securityBannerDismissed: Boolean,\n    ): State<SecurityBannerState> {",
    "    private fun rememberSecurityBannerState(\n        securityBannerDismissed: Boolean,\n        hasEncryptedRooms: Boolean,\n    ): State<SecurityBannerState> {",
)
replace_once(
    room_list,
    "                    recoveryState = recoveryState,\n",
    "                    recoveryState = recoveryState,\n                    hasEncryptedRooms = hasEncryptedRooms,\n",
)
replace_once(
    room_list,
    "        val currentSecurityBannerDismissed by rememberUpdatedState(securityBannerDismissed)\n",
    "        val currentSecurityBannerDismissed by rememberUpdatedState(securityBannerDismissed)\n"
    "        val currentHasEncryptedRooms by rememberUpdatedState(hasEncryptedRooms)\n",
)
replace_once(
    room_list,
    "                    hasEncryptedRooms = hasEncryptedRooms,\n",
    "                    hasEncryptedRooms = currentHasEncryptedRooms,\n",
)
replace_once(
    room_list,
    "    private fun calculateBannerState(\n        securityBannerDismissed: Boolean,\n        recoveryState: RecoveryState,\n    ): SecurityBannerState {\n        if (securityBannerDismissed) {",
    "    private fun calculateBannerState(\n        securityBannerDismissed: Boolean,\n        recoveryState: RecoveryState,\n        hasEncryptedRooms: Boolean,\n    ): SecurityBannerState {\n        if (securityBannerDismissed || !hasEncryptedRooms) {",
)

# Adapter les tests natifs : pas de bannière avant le premier salon chiffré,
# puis bannière de sauvegarde proposée dès qu'un salon chiffré existe.
test_path = "features/home/impl/src/test/kotlin/io/element/android/features/home/impl/roomlist/RoomListPresenterTest.kt"
test_file = ROOT / test_path
test_source = test_file.read_text(encoding="utf-8")
old = """            val initialState = consumeItemsUntilPredicate {
                it.contentState is RoomListContentState.Rooms
            }.last()
            assertThat(initialState.contentAsRooms().securityBannerState).isEqualTo(SecurityBannerState.SetUpRecovery)
            encryptionService.emitRecoveryState(RecoveryState.INCOMPLETE)
"""
new = """            val initialState = consumeItemsUntilPredicate {
                it.contentState is RoomListContentState.Rooms
            }.last()
            assertThat(initialState.contentAsRooms().securityBannerState).isEqualTo(SecurityBannerState.None)
            roomList.summaries.emit(listOf(aRoomSummary(isEncrypted = true)))
            assertThat(awaitItem().contentAsRooms().securityBannerState).isEqualTo(SecurityBannerState.SetUpRecovery)
            encryptionService.emitRecoveryState(RecoveryState.INCOMPLETE)
"""
if test_source.count(old) != 1:
    raise SystemExit(f"Test RoomListPresenter inattendu: premier scénario ({test_source.count(old)} occurrences).")
test_source = test_source.replace(old, new, 1)
# The incomplete-backup banner test also needs an encrypted room to justify the prompt.
anchor = """        val syncService = FakeSyncService(initialSyncState = SyncState.Running)
        val presenter = createRoomListPresenter(
"""
replacement = """        val syncService = FakeSyncService(initialSyncState = SyncState.Running)
        roomList.summaries.emit(listOf(aRoomSummary(isEncrypted = true)))
        val presenter = createRoomListPresenter(
"""
if test_source.count(anchor) != 1:
    raise SystemExit("Test de confirmation de clé introuvable ou ambigu.")
test_source = test_source.replace(anchor, replacement, 1)
test_file.write_text(test_source, encoding="utf-8")

# Vérifications statiques strictes des trois chemins de création.
checks = [
    ("features/startchat/impl/src/main/kotlin/io/element/android/features/startchat/impl/DefaultStartDMAction.kt", "isEncryped = false"),
    ("features/createroom/impl/src/main/kotlin/io/element/android/features/createroom/impl/configureroom/ConfigureRoomPresenter.kt", "isEncrypted = false"),
    ("features/invitepeople/impl/src/main/kotlin/io/element/android/features/invitepeople/impl/DefaultInvitePeoplePresenter.kt", "isEncrypted = false"),
]
for relative, expected in checks:
    source = (ROOT / relative).read_text(encoding="utf-8")
    if expected not in source:
        raise SystemExit(f"Vérification échouée : {relative}")
print("OK : les trois créations démarrent sans chiffrement.")
print("OK : le chiffrement natif reste activable dans les paramètres de conversation.")
print("OK : aucune demande de récupération n'apparaît avant la première conversation chiffrée.")
