#!/usr/bin/env python3
"""Non-network, non-secret preflight tests for Le Fil's FCM patcher."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("prepare_elementx_fcm.py").resolve()
MAIN = "libraries/pushproviders/firebase/src/main/res/values/firebase.xml"
DEBUG = "libraries/pushproviders/firebase/src/debug/res/values/firebase.xml"
SOURCE = "libraries/pushproviders/firebase/src/main/kotlin/io/element/android/libraries/pushproviders/firebase/FirebaseConfig.kt"
CONFIG = "plugins/src/main/kotlin/config/BuildTimeConfig.kt"
TEMPLATES = {
    MAIN: "<resources><string name='project_id'>vector-alpha</string></resources>\n",
    DEBUG: '<resources><string name="google_app_id">912726360885</string></resources>\n',
    SOURCE: 'object FirebaseConfig { const val PUSHER_HTTP_URL: String = "https://matrix.org/_matrix/push/v1/notify" }\n',
    CONFIG: 'val PUSHER_APP_ID_DEBUG: String? = null\n',
}
FAKE = {
    "project_info": {"project_id": "le-fil-talk", "project_number": "765432109876"},
    "client": [{
        "client_info": {
            "android_client_info": {"package_name": "net.lefil.talk.debug"},
            "mobilesdk_app_id": "1:765432109876:android:012345abcdef"
        },
        "api_key": [{"current_key": "AIzaTESTKEYEXAMPLE"}]
    }]
}

class Tests(unittest.TestCase):
    def run_case(self, cfg=FAKE, gateway="https://push.le-fil.net/_matrix/push/v1/notify"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "upstream"
            for relative, content in TEMPLATES.items():
                p = root / relative
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)
            env = os.environ.copy()
            env["LEFIL_FIREBASE_ANDROID_CONFIG"] = json.dumps(cfg)
            env["LEFIL_PUSH_GATEWAY_URL"] = gateway
            result = subprocess.run([sys.executable, str(SCRIPT)], cwd=directory, env=env,
                                    text=True, capture_output=True, check=False)
            content = {relative: (root / relative).read_text() for relative in TEMPLATES}
            return result, content

    def test_valid_config_updates_four_files(self):
        result, output = self.run_case()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("le-fil-talk", output[MAIN])
        self.assertNotIn("vector-alpha", output[MAIN])
        self.assertIn("765432109876", output[DEBUG])
        self.assertIn("push.le-fil.net", output[SOURCE])
        self.assertIn("net.lefil.talk.debug", output[CONFIG])

    def test_wrong_android_package_fails_without_writing(self):
        cfg = json.loads(json.dumps(FAKE))
        cfg["client"][0]["client_info"]["android_client_info"]["package_name"] = "net.bad.app"
        result, output = self.run_case(cfg)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output, TEMPLATES)

    def test_upstream_firebase_is_forbidden(self):
        cfg = json.loads(json.dumps(FAKE))
        cfg["project_info"]["project_number"] = "912726360885"
        result, output = self.run_case(cfg)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output, TEMPLATES)

    def test_upstream_gateway_is_forbidden(self):
        result, output = self.run_case(gateway="https://matrix.org/_matrix/push/v1/notify")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output, TEMPLATES)

    def test_http_gateway_is_forbidden(self):
        result, output = self.run_case(gateway="http://push.le-fil.net/_matrix/push/v1/notify")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output, TEMPLATES)

if __name__ == "__main__":
    unittest.main(verbosity=2)
