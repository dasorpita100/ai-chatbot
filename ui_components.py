"""
UI Components and Templates Module for PerplexAI Chatbot.
Houses all HTML structures, layout templates, styling loaders, and interactive header controls.
Supports Dynamic Theme Switching (Light/Dark), Multi-Language (i18n), and SQLite Authentication.
"""

import os
import streamlit as st
import streamlit.components.v1 as components
import i18n
from i18n import t, SUPPORTED_LANGUAGES
import auth

DARK_THEME_CSS = """
:root, html, body, .stApp {
    --app-bg: #111315 !important;
    --sidebar-bg: #181A1D !important;
    --card-bg: #1E2125 !important;
    --card-bg-hover: #192A25 !important;
    --card-border: #2E343C !important;
    --border-subtle: #24292F !important;
    --text-primary: #FFFFFF !important;
    --text-secondary: #E2E8F0 !important;
    --text-muted: #94A3B8 !important;
    --brand-green: #10B981 !important;
    --brand-green-dark: #34D399 !important;
    --brand-green-bg: rgba(16, 185, 129, 0.16) !important;
    --brand-green-border: rgba(16, 185, 129, 0.38) !important;
    --brand-badge-bg: #272C33 !important;
    --user-bubble-bg: #22262B !important;
    --user-bubble-border: #333942 !important;
    --assistant-bubble-bg: #1A1D21 !important;
    --assistant-bubble-border: #292E36 !important;
    --code-bg: #14171A !important;
    --chat-input-bg: #1A1D21 !important;
    --chat-input-border: #353B44 !important;
    --chat-input-text: #FFFFFF !important;
    --chat-input-placeholder: #94A3B8 !important;
    --chat-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    --pro-btn-bg: #F3F4F6 !important;
    --pro-btn-text: #111827 !important;
    --expander-bg: #1A1D21 !important;
    --card-shadow: 0 2px 6px rgba(0, 0, 0, 0.25) !important;
}
"""

LIGHT_THEME_CSS = """
:root, html, body, .stApp {
    --app-bg: #FAFAFB !important;
    --sidebar-bg: #FFFFFF !important;
    --card-bg: #FFFFFF !important;
    --card-bg-hover: #F0FDF4 !important;
    --card-border: #E5E7EB !important;
    --border-subtle: #ECEEF1 !important;
    --text-primary: #0F172A !important;
    --text-secondary: #334155 !important;
    --text-muted: #64748B !important;
    --brand-green: #10B981 !important;
    --brand-green-dark: #059669 !important;
    --brand-green-bg: #ECFDF5 !important;
    --brand-green-border: #A7F3D0 !important;
    --brand-badge-bg: #EEF2F6 !important;
    --user-bubble-bg: #F3F4F6 !important;
    --user-bubble-border: #E5E7EB !important;
    --assistant-bubble-bg: #FFFFFF !important;
    --assistant-bubble-border: #ECEEF1 !important;
    --code-bg: #F8FAFC !important;
    --chat-input-bg: #FFFFFF !important;
    --chat-input-border: #CBD5E1 !important;
    --chat-input-text: #0F172A !important;
    --chat-input-placeholder: #64748B !important;
    --chat-shadow: 0 10px 30px rgba(0, 0, 0, 0.08) !important;
    --pro-btn-bg: #111827 !important;
    --pro-btn-text: #FFFFFF !important;
    --expander-bg: #F9FAFB !important;
    --card-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
}
"""

SYSTEM_THEME_CSS = f"""
@media (prefers-color-scheme: dark) {{
    {DARK_THEME_CSS}
}}
@media (prefers-color-scheme: light) {{
    {LIGHT_THEME_CSS}
}}
"""

def load_custom_css(file_path: str = "style.css", theme_mode: str = "💻 System (Auto)", *args, **kwargs):
    """Reads external CSS and dynamically applies the chosen theme variables with client persistence."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            base_css = f.read()

        if "Dark" in theme_mode:
            theme_override = DARK_THEME_CSS
        elif "Light" in theme_mode:
            theme_override = LIGHT_THEME_CSS
        else:
            theme_override = SYSTEM_THEME_CSS

        st.markdown(f"<style>\n{base_css}\n{theme_override}\n</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Styling file '{file_path}' not found.")

def render_brand():
    """Renders the sidebar brand header with logo, title, and PRO badge."""
    st.markdown("""
    <div class="brand-container">
        <div class="brand-logo-group">
            <div class="brand-icon">❋</div>
            <span class="brand-title">PerplexAI</span>
        </div>
        <span class="brand-badge">PRO</span>
    </div>
    """, unsafe_allow_html=True)

@st.dialog("Sign in to PerplexAI", width="small")
def show_auth_dialog():
    """Renders the authentication modal dialog supporting Sign In and Account Registration."""
    tab_login, tab_signup = st.tabs([t("auth_tab_login"), t("auth_tab_signup")])

    with tab_login:
        st.markdown(f"<div style='margin-bottom: 0.75rem;'><span class='auth-demo-badge'>{t('auth_demo_hint')}</span></div>", unsafe_allow_html=True)
        with st.form("auth_login_form", clear_on_submit=False):
            email = st.text_input(t("auth_email"), placeholder="demo@perplexai.com", key="auth_login_email").strip()
            password = st.text_input(t("auth_password"), placeholder="••••••••", type="password", key="auth_login_password")
            submit = st.form_submit_button(t("auth_login_btn"), use_container_width=True, type="primary")

            if submit:
                success, msg, user = auth.authenticate_user(email, password)
                if success and user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    token = auth.create_session(user["id"])
                    st.session_state.session_token = token
                    st.query_params["session"] = token
                    st.success(t("auth_success_login"))
                    st.rerun()
                else:
                    st.error(msg or t("auth_error_credentials"))

    with tab_signup:
        with st.form("auth_signup_form", clear_on_submit=False):
            name = st.text_input(t("auth_fullname"), placeholder="Alex Morgan", key="auth_reg_name").strip()
            email = st.text_input(t("auth_email"), placeholder="alex@example.com", key="auth_reg_email").strip()
            password = st.text_input(t("auth_password"), placeholder="Minimum 6 characters", type="password", key="auth_reg_password")
            confirm_pwd = st.text_input(t("auth_confirm_password"), placeholder="Confirm your password", type="password", key="auth_reg_confirm")
            submit = st.form_submit_button(t("auth_signup_btn"), use_container_width=True, type="primary")

            if submit:
                if password != confirm_pwd:
                    st.error(t("auth_error_mismatch"))
                else:
                    success, msg, user = auth.register_user(email, name, password)
                    if success and user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        token = auth.create_session(user["id"])
                        st.session_state.session_token = token
                        st.query_params["session"] = token
                        st.success(t("auth_success_signup"))
                        st.rerun()
                    else:
                        st.error(msg)

def render_top_bar(status_text: str = None, current_theme: str = "☀️ Light"):
    """Renders the top interactive application bar in the center canvas with functional controls."""
    if not status_text:
        status_text = t("gemini_online")

    # Interactive top navigation container
    with st.container(key="top_nav_container"):
        components.html("""
        <script>
        (function() {
            function tagHeaderControls() {
                try {
                    var doc = window.parent.document;
                    var sel = '.st-key-top_nav_container .st-key-hdr_theme_btn button, ' +
                              '.st-key-top_nav_container .st-key-hdr_lang_popover div[data-testid="stPopover"] > button, ' +
                              '.st-key-top_nav_container .st-key-hdr_lang_popover button, ' +
                              '.st-key-top_nav_container .st-key-hdr_auth_btn button, ' +
                              '.st-key-top_nav_container .st-key-hdr_user_menu div[data-testid="stPopover"] > button, ' +
                              '.st-key-top_nav_container .st-key-hdr_user_menu button';
                    var btns = doc.querySelectorAll(sel);
                    btns.forEach(function(b) {
                        if (!b.classList.contains('header-control')) {
                            b.classList.add('header-control');
                        }
                    });
                } catch(e) {}
            }
            tagHeaderControls();
            setInterval(tagHeaderControls, 300);
        })();
        </script>
        """, height=0, width=0)
        col_title, col_theme, col_lang, col_auth = st.columns(
            [2.8, 1.0, 1.0, 1.0],
            vertical_alignment="center",
            gap="small"
        )

        with col_title:
            st.markdown(f"""
            <div class="top-title-group">
                <span class="top-chat-title">{t("ai_chat")}</span>
                <div class="top-status-pill">
                    <span class="pulse-dot"></span>
                    <span>{status_text}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_theme:
            # Active theme toggle button supporting System (Auto) -> Light -> Dark
            curr_mode = st.session_state.get("theme_mode", "💻 System (Auto)")
            if "Dark" in curr_mode:
                theme_btn_label = "🌙 Dark"
            elif "Light" in curr_mode:
                theme_btn_label = "☀️ Light"
            else:
                theme_btn_label = "💻 System"

            def _toggle_theme_action():
                curr = st.session_state.get("theme_mode", "💻 System (Auto)")
                if "System" in curr:
                    next_mode = "☀️ Light"
                    param = "light"
                elif "Light" in curr:
                    next_mode = "🌙 Dark"
                    param = "dark"
                else:
                    next_mode = "💻 System (Auto)"
                    param = "system"

                st.session_state.theme_mode = next_mode
                st.session_state.theme_mode_selector = next_mode
                st.query_params["theme"] = param

            st.button(
                theme_btn_label,
                key="hdr_theme_btn",
                help="Toggle theme: System (Auto) → Light → Dark",
                use_container_width=True,
                on_click=_toggle_theme_action
            )

        with col_lang:
            # Language dropdown popover with on_click callback
            active_lang = st.session_state.get("language", "en")
            active_info = SUPPORTED_LANGUAGES.get(active_lang, SUPPORTED_LANGUAGES["en"])

            def _pick_language_action(chosen_code: str):
                st.session_state.language = chosen_code
                st.query_params["lang"] = chosen_code

            with st.popover(active_info["label"], key="hdr_lang_popover", help="Select Language", use_container_width=True):
                st.markdown(f"<p class='popover-header'>{t('select_language')}</p>", unsafe_allow_html=True)
                for code, info in SUPPORTED_LANGUAGES.items():
                    is_active = (code == active_lang)
                    tick = "✓ " if is_active else "  "
                    btn_label = f"{tick}{info['flag']} {info['native_name']}"
                    st.button(
                        btn_label,
                        key=f"hdr_lang_pick_{code}",
                        use_container_width=True,
                        on_click=_pick_language_action,
                        args=(code,)
                    )

        with col_auth:
            # Authentication button / account menu
            if not st.session_state.get("authenticated", False):
                if st.button(t("sign_in"), key="hdr_auth_btn", help="Sign in to your account", use_container_width=True):
                    show_auth_dialog()
            else:
                user = st.session_state.get("user", {})
                raw_name = user.get("name") or user.get("email", "User")
                display_name = raw_name.split()[0] if " " in raw_name else raw_name
                if len(display_name) > 9:
                    display_name = display_name[:8] + "…"
                with st.popover(f"👤 {display_name}", key="hdr_user_menu", help="Account Profile", use_container_width=True):
                    st.markdown(f"**{user.get('name', 'User')}**")
                    st.caption(user.get("email", ""))
                    st.markdown(f"<div class='account-role-pill'>{t('auth_role')}</div>", unsafe_allow_html=True)
                    st.caption(f"{t('auth_member_since')}: {user.get('created_at', '2026')}")
                    st.divider()
                    if st.button(f"🚪 {t('sign_out')}", key="hdr_signout_action", use_container_width=True):
                        token = st.session_state.get("session_token")
                        if token:
                            auth.delete_session(token)
                        st.session_state.authenticated = False
                        st.session_state.user = None
                        st.session_state.session_token = None
                        if "session" in st.query_params:
                            del st.query_params["session"]
                        st.rerun()

def render_hero(heading: str = None, subtitle: str = None):
    """Renders the centered hero greeting section with dynamic localization."""
    if not heading:
        heading = t("hero_title")
    if not subtitle:
        subtitle = t("hero_subtitle")

    st.markdown(f"""
    <div class="hero-wrapper">
        <h1 class="hero-heading">{heading}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_user_message(content: str):
    """Renders a user message bubble with user avatar header."""
    st.markdown(f"""
    <div class="user-bubble">
        <div class="user-bubble-header">
            <span>👤</span> You
        </div>
        {content}
    </div>
    """, unsafe_allow_html=True)

def render_assistant_message(content: str, model_name: str, persona_name: str):
    """Renders an assistant response card with Gemini branding and model tag."""
    st.markdown("""
    <div class="assistant-bubble">
        <div class="assistant-header">
            <span>✨</span> Gemini Assistant
        </div>
    """, unsafe_allow_html=True)
    st.markdown(content)
    st.markdown(f"""
        <div class="message-actions">
            <span>Model: {model_name}</span>
            <span>•</span>
            <span>Persona: {persona_name.split()[0]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_right_header(count: int):
    """Renders the header for the right Projects/Threads panel with dynamic localization."""
    title_text = t("projects_header")
    st.markdown(f"""
    <div class="right-panel-header">
        <span class="right-panel-title">{title_text} ({count})</span>
        <span style="color: var(--text-muted); cursor: pointer; font-size: 1.1rem; font-weight: 700;">···</span>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_status():
    """Renders the green API connected indicator in the sidebar with dynamic localization."""
    status_label = t("api_status_connected")
    st.markdown(f"""
    <div class="status-badge-sidebar">
        <span>●</span> {status_label}
    </div>
    """, unsafe_allow_html=True)
