#!/usr/bin/env bash
set -Eeuo pipefail
mkdir -p lefil-fluffychat-smoke
proof=lefil-fluffychat-smoke
on_exit() {
  code=$?
  if (( code != 0 )); then
    timeout 20s adb logcat -d -t 1200 > "$proof/logcat-erreur.txt" 2>&1 || true
    echo "::error::Le Fil Talk: test de démarrage échoué (code $code)"
  fi
}
trap on_exit EXIT
test -s release-apk/Le-Fil-Talk-FluffyChat-test.apk
timeout 70s adb wait-for-device
timeout 120s adb install -r release-apk/Le-Fil-Talk-FluffyChat-test.apk | tee "$proof/installation.txt"
timeout 25s adb shell pm path net.lefil.talk | tee "$proof/package.txt" | grep -q package:
timeout 15s adb logcat -c || true
timeout 45s adb shell am start -W -n net.lefil.talk/chat.fluffy.fluffychat.MainActivity > "$proof/lancement.txt" 2>&1
cat "$proof/lancement.txt"
sleep 8
timeout 25s adb shell pidof net.lefil.talk > "$proof/pid.txt" || true
timeout 25s adb shell screencap -p /sdcard/lefil-talk-demarrage.png
timeout 25s adb pull /sdcard/lefil-talk-demarrage.png "$proof/ecran.png"
timeout 55s adb shell uiautomator dump /sdcard/lefil-talk.xml > "$proof/hierarchie-log.txt" 2>&1 || true
timeout 25s adb pull /sdcard/lefil-talk.xml "$proof/hierarchie.xml" || true
timeout 25s adb logcat -d -t 1200 > "$proof/logcat.txt" || true
test -s "$proof/pid.txt" || { echo "::error::Processus non détecté"; exit 1; }
test -s "$proof/ecran.png"
echo "TEST OK: installée, lancée, toujours active après 8 secondes ; image sauvegardée."
echo "Les appels, inscriptions et notifications ne sont PAS encore testés."
