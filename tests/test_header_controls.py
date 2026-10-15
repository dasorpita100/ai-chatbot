"""
Automated Integration and Component Tests for PerplexAI Header Controls.
Tests Theme Switching, Multi-Language i18n, and Authentication workflows using Streamlit AppTest.
"""

import os
import unittest
from streamlit.testing.v1 import AppTest
import auth
import i18n

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))

class TestHeaderControls(unittest.TestCase):

    def test_theme_toggle_flow(self):
        """Verify theme button cycles between System (Auto), Light, and Dark mode."""
        at = AppTest.from_file(APP_PATH, default_timeout=15)
        at.run()
        self.assertEqual(len(at.exception), 0, f"App crashed on startup: {at.exception}")

        # Initial default must be System (Auto)
        self.assertEqual(at.session_state.theme_mode, "💻 System (Auto)")
        theme_btn = at.button(key="hdr_theme_btn")
        self.assertIsNotNone(theme_btn)
        self.assertEqual(theme_btn.label, "💻 System")

        # Click theme toggle -> Switch to Light mode
        theme_btn.click().run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state.theme_mode, "☀️ Light")
        theme_btn_light = at.button(key="hdr_theme_btn")
        self.assertEqual(theme_btn_light.label, "☀️ Light")

        # Click theme toggle again -> Switch to Dark mode
        theme_btn_light.click().run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state.theme_mode, "🌙 Dark")
        theme_btn_dark = at.button(key="hdr_theme_btn")
        self.assertEqual(theme_btn_dark.label, "🌙 Dark")

        # Click theme toggle again -> Return to System (Auto)
        theme_btn_dark.click().run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state.theme_mode, "💻 System (Auto)")
        self.assertEqual(at.button(key="hdr_theme_btn").label, "💻 System")

    def test_language_selector_flow(self):
        """Verify language dropdown updates all interface text dynamically."""
        at = AppTest.from_file(APP_PATH, default_timeout=15)
        at.run()
        self.assertEqual(len(at.exception), 0)

        # Default language is English
        self.assertEqual(at.session_state.language, "en")

        # Select Spanish
        es_btn = at.button(key="hdr_lang_pick_es")
        self.assertIsNotNone(es_btn)
        es_btn.click().run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state.language, "es")

        # Verify translated UI strings appear
        hero_texts = [m.value for m in at.markdown if "¿En qué puedo ayudarte" in m.value]
        self.assertTrue(len(hero_texts) > 0, "Spanish hero heading not found after language switch")

        # Select French
        fr_btn = at.button(key="hdr_lang_pick_fr")
        fr_btn.click().run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state.language, "fr")
        hero_fr = [m.value for m in at.markdown if "Que puis-je faire pour vous" in m.value]
        self.assertTrue(len(hero_fr) > 0, "French hero heading not found after language switch")

        # Select German
        de_btn = at.button(key="hdr_lang_pick_de")
        de_btn.click().run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state.language, "de")
        hero_de = [m.value for m in at.markdown if "Wie kann ich Ihnen helfen" in m.value]
        self.assertTrue(len(hero_de) > 0, "German hero heading not found after language switch")

        # Return to English
        en_btn = at.button(key="hdr_lang_pick_en")
        en_btn.click().run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state.language, "en")
        hero_en = [m.value for m in at.markdown if "What can I help you with" in m.value]
        self.assertTrue(len(hero_en) > 0, "English hero heading not found after restoring language")

    def test_authentication_backend(self):
        """Verify real SQLite PBKDF2 authentication, sessions, and input validation."""
        # Test 1: Demo user authentication
        success, msg, user = auth.authenticate_user("demo@perplexai.com", "Demo1234!")
        self.assertTrue(success)
        self.assertEqual(user["email"], "demo@perplexai.com")

        # Test 2: Invalid password rejection
        fail_pwd, msg_pwd, _ = auth.authenticate_user("demo@perplexai.com", "WrongPassword123")
        self.assertFalse(fail_pwd)
        self.assertIn("Invalid", msg_pwd)

        # Test 3: Non-existent user rejection
        fail_user, _, _ = auth.authenticate_user("ghost@example.com", "AnyPassword123")
        self.assertFalse(fail_user)

        # Test 4: New user registration with validation
        test_email = "test.tester@domain.com"
        # Invalid email format
        bad_email, msg_bad_email, _ = auth.register_user("not-an-email", "Tester", "Secret123")
        self.assertFalse(bad_email)

        # Short password
        short_pwd, msg_short, _ = auth.register_user("valid@domain.com", "Tester", "123")
        self.assertFalse(short_pwd)

        # Successful registration
        reg_ok, reg_msg, new_user = auth.register_user(test_email, "Test User", "SecurePass123")
        if reg_ok:
            self.assertEqual(new_user["email"], test_email)
            # Authenticate newly created user
            auth_ok, _, authed_user = auth.authenticate_user(test_email, "SecurePass123")
            self.assertTrue(auth_ok)
            self.assertEqual(authed_user["email"], test_email)

        # Duplicate email prevention
        dup_ok, dup_msg, _ = auth.register_user(test_email, "Duplicate", "SecurePass123")
        self.assertFalse(dup_ok)
        self.assertIn("already exists", dup_msg)

        # Test 5: Session lifecycle
        session_token = auth.create_session(user["id"])
        self.assertTrue(len(session_token) > 20)
        session_user = auth.get_user_by_session(session_token)
        self.assertIsNotNone(session_user)
        self.assertEqual(session_user["id"], user["id"])
        auth.delete_session(session_token)
        self.assertIsNone(auth.get_user_by_session(session_token))

    def test_authenticated_state_ui(self):
        """Verify that when authenticated, header displays user profile menu instead of Sign in."""
        at = AppTest.from_file(APP_PATH, default_timeout=15)
        at.run()

        # Unauthenticated: Sign in button is visible
        auth_btn = at.button(key="hdr_auth_btn")
        self.assertIsNotNone(auth_btn)
        self.assertEqual(auth_btn.label, "Sign in")

        # Simulate authenticated session
        at.session_state.authenticated = True
        at.session_state.user = {"id": 1, "name": "Alex Morgan", "email": "demo@perplexai.com", "created_at": "2026-10-15"}
        at.run()
        self.assertEqual(len(at.exception), 0)

        # Sign in button should no longer exist; user menu button should exist
        sign_in_buttons = [b for b in at.button if b.key == "hdr_auth_btn"]
        self.assertEqual(len(sign_in_buttons), 0)

        # Sign out button inside user popover is available
        signout_btn = at.button(key="hdr_signout_action")
        self.assertIsNotNone(signout_btn)

        # Clicking sign out clears session and restores Sign In button
        signout_btn.click().run()
        self.assertEqual(len(at.exception), 0)
        self.assertFalse(at.session_state.authenticated)
        self.assertIsNotNone(at.button(key="hdr_auth_btn"))

if __name__ == "__main__":
    unittest.main()
