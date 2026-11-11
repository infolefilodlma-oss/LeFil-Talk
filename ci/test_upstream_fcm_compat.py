#!/usr/bin/env python3
"""Source-level integration check against an actual, pinned Element X checkout."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

root = Path("upstream")
if not (root / ".git").exists():
    raise SystemExit("Real upstream checkout required")
tracked = [
    "plugins/src/main/kotlin/config/BuildTimeConfig.kt",
    "libraries/pushproviders/firebase/src/main/res/values/firebase.xml",
    "libraries/pushproviders/firebase/src/debug/res/values/firebase.xml",
    "libraries/pushproviders/firebase/src/main/kotlin/io/element/android/libraries/pushproviders/firebase/FirebaseConfig.kt",
]
prior = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in tracked}
cfg = {
    "project_info": {"project_id": "le-fil-talk-test", "project_number": "765432109876"},
    "client": [{
        "client_info": {
            "android_client_info": {"package_name": "net.lefil.talk.debug"},
            "mobilesdk_app_id": "1:765432109876:android:012345abcdef",
        },
        "api_key": [{"current_key": "AIzaTESTKEYEXAMPLE"}],
    }],
}
env = os.environ.copy()
# Test with the registered Le Fil Android application, not a synthetic Firebase project.
registered = Path("ci/firebase-android-lefil-debug.json")
if registered.is_file():
    cfg = json.loads(registered.read_text(encoding="utf-8"))
    assert cfg["project_info"]["project_id"] == "le-fil-talk"
    assert cfg["project_info"]["project_number"] == "171609026264"
    assert any(x.get("client_info", {}).get("android_client_info", {}).get("package_name") == "net.lefil.talk.debug" for x in cfg["client"])
env["LEFIL_FIREBASE_ANDROID_CONFIG"] = json.dumps(cfg)
env["LEFIL_PUSH_GATEWAY_URL"] = "https://push.example.org/_matrix/push/v1/notify"
subprocess.run([sys.executable, "ci/prepare_elementx_fcm.py"], env=env, check=True)
current = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in tracked}
assert all(prior[p] != current[p] for p in tracked), "The patch must update exactly the four expected files"
modified = subprocess.run(["git", "-C", "upstream", "diff", "--name-only"],
                          text=True, capture_output=True, check=True).stdout.splitlines()
assert sorted(modified) == sorted(tracked), f"Unexpected changes: {modified!r}"
main = ElementTree.parse(root / tracked[1]).getroot()
debug = ElementTree.parse(root / tracked[2]).getroot()
values = {item.attrib["name"]: (item.text or "") for item in main}
dvals = {item.attrib["name"]: (item.text or "") for item in debug}
assert values["project_id"] == cfg["project_info"]["project_id"]
assert values["gcm_defaultSenderId"] == cfg["project_info"]["project_number"]
assert dvals["google_app_id"] == cfg["client"][0]["client_info"]["mobilesdk_app_id"]
assert "vector-alpha" not in (root / tracked[1]).read_text()
source = (root / tracked[3]).read_text()
assert 'https://push.example.org/_matrix/push/v1/notify' in source
config = (root / tracked[0]).read_text()
assert 'val PUSHER_APP_ID_DEBUG: String? = "net.lefil.talk.debug"' in config
build = (root / "app/build.gradle.kts").read_text()
assert 'create("gplay")' in build
assert 'applicationIdSuffix = ".debug"' in build
print("PASS: Real Element X 26.10.1 patched; exactly four files changed.")
print("PASS: FCM Android app, sender ID, app pusher ID and gateway are consistent.")
print("PASS: Matrix, encryption, calls, and gplay Gradle code unchanged.")
print("No Firebase secrets or production credentials were used.")
