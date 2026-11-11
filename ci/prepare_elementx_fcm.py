#!/usr/bin/env python3
"""Configure Element X v26.10.1 gplay debug with Le Fil Firebase credentials only.
Fail closed; no modification to Matrix, crypto, calls or upstream production build.
"""
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

root = Path("upstream")
package = "net.lefil.talk.debug"

def stop(message):
    raise SystemExit("FCM PREFLIGHT FAILED: " + message)

raw = os.environ.get("LEFIL_FIREBASE_ANDROID_CONFIG", "").strip()
gateway = os.environ.get("LEFIL_PUSH_GATEWAY_URL", "").strip()
if not raw or not gateway:
    stop("Firebase Android config and Le Fil gateway URL are both required")
try:
    cfg = json.loads(raw)
except (TypeError, ValueError):
    stop("Invalid Firebase JSON")
project = cfg.get("project_info", {})
project_id = str(project.get("project_id", ""))
project_number = str(project.get("project_number", ""))
if not re.fullmatch(r"[a-z][a-z0-9-]{4,40}", project_id) or not re.fullmatch(r"\d{5,20}", project_number):
    stop("Invalid Firebase project_info")
if project_id == "vector-alpha" or project_number == "912726360885":
    stop("The upstream Element Firebase project cannot be reused")
clients = [c for c in cfg.get("client", [])
           if c.get("client_info", {}).get("android_client_info", {}).get("package_name") == package]
if len(clients) != 1:
    stop("Firebase must contain exactly one Android application " + package)
client = clients[0]
app_id = client["client_info"]["mobilesdk_app_id"]
if not re.fullmatch(r"1:" + re.escape(project_number) + r":android:[a-fA-F0-9]+", app_id):
    stop("Firebase Android app ID does not match its project")
keys = [str(x.get("current_key", "")) for x in client.get("api_key", [])]
if len(keys) != 1 or not keys[0].startswith("AIza"):
    stop("Firebase Android API key missing")
url = urlsplit(gateway)
if (url.scheme != "https" or not url.hostname or url.username or url.password or
        url.query or url.fragment or url.path != "/_matrix/push/v1/notify"):
    stop("Gateway must be HTTPS ending exactly in /_matrix/push/v1/notify")
if url.hostname in ("matrix.org", "push.fluffychat.im", "push.element.io") or url.hostname.endswith(".element.io"):
    stop("Upstream push gateway cannot be reused without authorization")
main = root / "libraries/pushproviders/firebase/src/main/res/values/firebase.xml"
debug = root / "libraries/pushproviders/firebase/src/debug/res/values/firebase.xml"
source = root / "libraries/pushproviders/firebase/src/main/kotlin/io/element/android/libraries/pushproviders/firebase/FirebaseConfig.kt"
config = root / "plugins/src/main/kotlin/config/BuildTimeConfig.kt"
original = {p: p.read_text(encoding="utf-8") for p in (main, debug, source, config)}
required = {
    main: "vector-alpha",
    debug: "912726360885",
    source: 'const val PUSHER_HTTP_URL: String = "https://matrix.org/_matrix/push/v1/notify"',
    config: 'val PUSHER_APP_ID_DEBUG: String? = null',
}
for p, anchor in required.items():
    if original[p].count(anchor) != 1:
        stop("Unexpected pinned upstream source: " + str(p))
values = {
    "default_web_client_id": "",
    "firebase_database_url": str(project.get("firebase_url", "")),
    "gcm_defaultSenderId": project_number,
    "google_api_key": keys[0],
    "google_crash_reporting_api_key": keys[0],
    "google_storage_bucket": str(project.get("storage_bucket", "")),
    "project_id": project_id,
}
xml_main = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n' + "".join(
    f'  <string name="{key}" translatable="false">{escape(value)}</string>\n'
    for key, value in values.items()
) + "</resources>\n"
xml_debug = ('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
             f'  <string name="google_app_id" translatable="false">{escape(app_id)}</string>\n'
             "</resources>\n")
ET.fromstring(xml_main)
ET.fromstring(xml_debug)
new_source = original[source].replace(
    required[source], 'const val PUSHER_HTTP_URL: String = "' + gateway + '"')
new_config = original[config].replace(
    required[config], 'val PUSHER_APP_ID_DEBUG: String? = "net.lefil.talk.debug"')
for path, content in ((main, xml_main), (debug, xml_debug), (source, new_source), (config, new_config)):
    path.write_text(content, encoding="utf-8")
print("Le Fil Talk FCM configured for debug, project:", project_id)
print("Gateway host:", url.hostname)
print("No upstream Element Firebase configuration retained in debug resources.")
