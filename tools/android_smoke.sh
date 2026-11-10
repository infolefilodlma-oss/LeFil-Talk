#!/usr/bin/env bash
# Exécuté en un seul shell par android-emulator-runner ; les variables survivent.
set -Eeuo pipefail
mkdir -p lefil-talk-ui-proof
on_exit() {
  result=$?
  if [ "$result" -ne 0 ]; then
    echo "::error::Échec du contrôle Android (code $result). APK non validée."
    timeout 25s adb logcat -d -t 1500 > lefil-talk-ui-proof/logcat-echec.txt 2>&1 || true
    timeout 20s adb shell getprop sys.boot_completed > lefil-talk-ui-proof/boot-echec.txt 2>&1 || true
  fi
}
trap on_exit EXIT
APK="artefact/upstream/app/build/outputs/apk/fdroid/debug/app-fdroid-x86_64-debug.apk"
test -s "$APK" || { echo "::error::APK manquante dans l'artefact"; exit 1; }
timeout 120s adb wait-for-device
timeout 120s adb install -r "$APK"
timeout 25s adb shell pm path net.lefil.talk.debug | grep -q 'package:'
adb logcat -c || true
timeout 45s adb shell monkey -p net.lefil.talk.debug 1 > lefil-talk-ui-proof/launch.txt 2>&1
sleep 10
timeout 20s adb shell pidof net.lefil.talk.debug > lefil-talk-ui-proof/pid.txt || true
timeout 25s adb logcat -d -t 1500 > lefil-talk-ui-proof/logcat.txt || true
timeout 30s adb shell screencap -p /sdcard/lefil-talk-start.png
timeout 30s adb pull /sdcard/lefil-talk-start.png lefil-talk-ui-proof/startup-android14.png
timeout 90s adb shell uiautomator dump /sdcard/lefil-talk-ui.xml
timeout 30s adb pull /sdcard/lefil-talk-ui.xml lefil-talk-ui-proof/startup-hierarchy.xml
test -s lefil-talk-ui-proof/pid.txt || { echo "::error::Le Fil Talk ne reste pas lancé"; exit 1; }
test -s lefil-talk-ui-proof/startup-android14.png
test -s lefil-talk-ui-proof/startup-hierarchy.xml
if grep -Eqi "System UI isn't responding|isn't responding|Close app|ne répond pas" lefil-talk-ui-proof/startup-hierarchy.xml; then
  echo "::error::Blocage Android détecté"
  exit 1
fi
echo "TEST ANDROID : APK installée et lancée ; PID, captures et journaux archivés. Fonctions Matrix non encore validées."
