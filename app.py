import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

import importlib
import i18n
from i18n import t, SUPPORTED_LANGUAGES
importlib.reload(i18n)

import auth
importlib.reload(auth)

import ui_components
importlib.reload(ui_components)

# Import UI components and styling loader from dedicated UI modules
from ui_components import (
    load_custom_css,
    render_brand,
    render_top_bar,
    render_hero,
    render_user_message,
    render_assistant_message,
    render_right_header,
    render_sidebar_status
)

# ---------------------------------------------------------
# Page Configuration & CSS Injection
# ---------------------------------------------------------
load_dotenv()

st.set_page_config(
    page_title="PerplexAI | Gemini Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Session State & Query Param Synchronization
# ---------------------------------------------------------
# 1. Synchronize Language
query_lang = st.query_params.get("lang")
if "language" not in st.session_state:
    st.session_state.language = query_lang if query_lang in SUPPORTED_LANGUAGES else "en"

# 2. Synchronize Theme (Default: System Auto Mode)
query_theme = st.query_params.get("theme")
if "theme_mode" not in st.session_state:
    if query_theme == "dark":
        st.session_state.theme_mode = "🌙 Dark"
    elif query_theme == "light":
        st.session_state.theme_mode = "☀️ Light"
    else:
        st.session_state.theme_mode = "💻 System (Auto)"

# 3. Synchronize Authentication & Restore Session Token
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.session_token = None

query_session = st.query_params.get("session")
if query_session and not st.session_state.authenticated:
    user_info = auth.get_user_by_session(query_session)
    if user_info:
        st.session_state.authenticated = True
        st.session_state.user = user_info
        st.session_state.session_token = query_session

# Load external CSS styling and inject chosen theme palette
load_custom_css("style.css", theme_mode=st.session_state.theme_mode)

# ---------------------------------------------------------
# Default Threads & State Initialization
# ---------------------------------------------------------
DEFAULT_THREADS = [
    {
        "id": "th-1",
        "title": "Learning from 100 Athletes",
        "snippet": "From athletes, high performance rituals...",
        "messages": [
            {"role": "user", "content": "How do elite athletes structure their morning routines?"},
            {"role": "assistant", "content": "Top athletes focus on 3 pillars: progressive hydration, deliberate mobility priming, and mental visualization before checking any digital devices."}
        ],
        "created_at": "Today"
    },
    {
        "id": "th-2",
        "title": "Research on Maxwell's Equations",
        "snippet": "Maxwell's equation-theoretical derivation...",
        "messages": [
            {"role": "user", "content": "Explain Maxwell's equations in simple terms."},
            {"role": "assistant", "content": "Maxwell's four equations describe how electric charges produce electric fields, how magnetic poles never exist in isolation, and how changing magnetic fields induce electricity and vice-versa."}
        ],
        "created_at": "Yesterday"
    },
    {
        "id": "th-3",
        "title": "What does a Senior Architect do?",
        "snippet": "Physiological respiration vs mental load...",
        "messages": [
            {"role": "user", "content": "What is the core difference between a Senior Software Engineer and a Software Architect?"},
            {"role": "assistant", "content": "A Senior Engineer focuses on building high-quality, testable, and maintainable systems for specific features, whereas a Software Architect balances cross-cutting trade-offs, system evolvability, resilience, and business alignment."}
        ],
        "created_at": "3 days ago"
    },
    {
        "id": "th-4",
        "title": "Write a sweet note",
        "snippet": "In the eighteenth century epistolary style...",
        "messages": [
            {"role": "user", "content": "Write a warm thank-you note to a mentor."},
            {"role": "assistant", "content": "Dear Mentor, Your patient guidance and thoughtful questions have shaped how I approach every complex challenge. Thank you for believing in my potential."}
        ],
        "created_at": "Oct 12"
    },
    {
        "id": "th-5",
        "title": "Meet Artisan Cake Bakers",
        "snippet": "Physical space and culinary chemistry...",
        "messages": [
            {"role": "user", "content": "What makes sourdough pastries so distinct?"},
            {"role": "assistant", "content": "Slow fermentation allows wild yeasts and lactobacilli to break down phytates and develop rich organic acids, yielding an airy crumb and deep aromatic crust."}
        ],
        "created_at": "Oct 10"
    }
]

if "threads" not in st.session_state:
    st.session_state.threads = DEFAULT_THREADS

if "current_thread_id" not in st.session_state:
    st.session_state.current_thread_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Home"

# ---------------------------------------------------------
# Persona & System Instructions
# ---------------------------------------------------------
PERSONA_PROMPTS = {
    "Patient Teacher & Mentor": (
        "You are an inspiring, friendly AI assistant and patient teacher. "
        "Answer clearly and accurately. Break complicated tasks into smaller steps. "
        "Use real-world examples and analogies. Admit when unsure. Be polite and encouraging."
    ),
    "Senior Software Architect": (
        "You are a Principal Software Architect. Provide robust, production-grade solutions. "
        "Write clean, idiomatic code with type annotations and best practices. "
        "Explain architectural trade-offs, scalability, and security considerations."
    ),
    "Executive Analyst (Concise)": (
        "You are a sharp executive analyst. Deliver structured, high-signal insights. "
        "Use bullet points, bold key takeaways, and eliminate fluff. Focus on direct answers and actionable steps."
    ),
    "Creative Brainstormer": (
        "You are an imaginative creative collaborator. Think outside the box, propose innovative angles, "
        "and generate vivid analogies, concepts, and ideas with enthusiasm."
    )
}

# ---------------------------------------------------------
# Sidebar Component (Matches left panel in reference)
# ---------------------------------------------------------
with st.sidebar:
    render_brand()

    # "New thread" action button
    st.markdown('<div class="new-thread-btn">', unsafe_allow_html=True)
    if st.button(t("new_chat"), key="new_thread_top", use_container_width=True):
        st.session_state.current_thread_id = None
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    # Navigation menu items with dynamic localization
    nav_items = [
        ("", t("nav_home"), "Home"),
        ("", t("nav_discover"), "Discover"),
        ("", t("nav_library"), "Library"),
        ("", t("nav_settings"), "Settings")
    ]

    for icon, label, nav_key in nav_items:
        is_active = (st.session_state.active_nav == nav_key)
        btn_type = "primary" if is_active else "secondary"
        if st.button(
            f"{icon}  {label}",
            key=f"nav_btn_{nav_key}",
            use_container_width=True,
            type=btn_type
        ):
            st.session_state.active_nav = nav_key
            st.rerun()

    # Collapsible Preferences & AI Controls
    is_settings_active = (st.session_state.active_nav == "Settings")
    with st.expander(t("preferences_title"), expanded=is_settings_active):
        theme_options = ["💻 System (Auto)", "☀️ Light", "🌙 Dark"]

        # Ensure theme_mode_selector widget state is in sync with session_state.theme_mode
        if "theme_mode_selector" in st.session_state and st.session_state.theme_mode_selector != st.session_state.theme_mode:
            st.session_state.theme_mode_selector = st.session_state.theme_mode

        def _on_sidebar_theme_change():
            sel = st.session_state.theme_mode_selector
            st.session_state.theme_mode = sel
            if "Dark" in sel:
                st.query_params["theme"] = "dark"
            elif "Light" in sel:
                st.query_params["theme"] = "light"
            else:
                st.query_params["theme"] = "system"

        idx = None if "theme_mode_selector" in st.session_state else (theme_options.index(st.session_state.theme_mode) if st.session_state.theme_mode in theme_options else 0)
        chosen_theme = st.selectbox(
            t("appearance_theme"),
            theme_options,
            index=idx,
            key="theme_mode_selector",
            on_change=_on_sidebar_theme_change
        )

        selected_model = st.selectbox(
            t("ai_model"),
            ["gemini-flash-latest", "gemini-3.8-flash"],
            index=0,
            help="gemini-flash-latest provides low-latency responses; gemini-3.8-flash handles complex reasoning."
        )

        selected_persona = st.selectbox(
            t("assistant_persona"),
            list(PERSONA_PROMPTS.keys()),
            index=0
        )

        temperature = st.slider(
            "🌡️ Creativity (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1
        )

    # API Status check
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error(f"⚠️ {t('api_status_missing')} in `.env`")
    else:
        render_sidebar_status()

# ---------------------------------------------------------
# Main Layout: Center (Chat & Suggestions) + Right (Projects & Threads)
# ---------------------------------------------------------
col_main, col_right = st.columns([3.4, 1.2], gap="large")

with col_main:
    # Render interactive top navigation bar
    render_top_bar(status_text=t("gemini_online"), current_theme=st.session_state.theme_mode)

    if not api_key:
        st.error(t("api_status_missing"))
        st.stop()

    client = genai.Client(api_key=api_key)

    # ---------------------------------------------------------
    # Render Hero State (When no messages yet in active conversation)
    # ---------------------------------------------------------
    if not st.session_state.messages:
        render_hero(
            heading=t("hero_title"),
            subtitle=t("hero_subtitle")
        )

        # 2x2 Suggestion Cards Grid (Single unified cards matching reference)
        c1, c2 = st.columns(2, gap="medium")

        with c1:
            # Card 1: Music festivals
            if st.button(
                t("sug_festivals"),
                key="sug_festivals",
                use_container_width=True
            ):
                st.session_state.pending_prompt = "What are the most exciting upcoming music festivals in 2026? Give dates, locations, genres, and tips."
                st.rerun()

            st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

            # Card 2: Maxwell's equations
            if st.button(
                t("sug_maxwell"),
                key="sug_maxwell",
                use_container_width=True
            ):
                st.session_state.pending_prompt = "Explain Maxwell's equations and their significance in physics, electromagnetic waves, and modern communication."
                st.rerun()

        with c2:
            # Card 3: What is Gemini AI
            if st.button(
                t("sug_gemini"),
                key="sug_gemini",
                use_container_width=True
            ):
                st.session_state.pending_prompt = "What is Google Gemini AI? Explain its multimodal architecture, models, and key capabilities."
                st.rerun()

            st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

            # Card 4: Crypto
            if st.button(
                t("sug_crypto"),
                key="sug_crypto",
                use_container_width=True
            ):
                st.session_state.pending_prompt = "Give me a structured overview of cryptocurrency, blockchain architecture, Bitcoin, and the DeFi ecosystem."
                st.rerun()

    # ---------------------------------------------------------
    # Render Active Conversation Messages
    # ---------------------------------------------------------
    else:
        col_chat_hdr1, col_chat_hdr2 = st.columns([3, 1])
        with col_chat_hdr1:
            st.caption(f"Conversation • {len(st.session_state.messages)} messages • Persona: {selected_persona}")
        with col_chat_hdr2:
            if st.button("🗑️ Clear chat", key="clear_chat_inline", use_container_width=True):
                st.session_state.messages = []
                st.session_state.current_thread_id = None
                st.rerun()

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                render_user_message(msg["content"])
            else:
                render_assistant_message(msg["content"], selected_model, selected_persona)

    # ---------------------------------------------------------
    # Process Prompts (from Chat Input OR Clicked Suggestion Cards)
    # ---------------------------------------------------------
    prompt_to_send = None

    if st.session_state.pending_prompt:
        prompt_to_send = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    user_input = st.chat_input(t("chat_placeholder"))
    if user_input:
        prompt_to_send = user_input

    if prompt_to_send:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt_to_send})
        render_user_message(prompt_to_send)

        # Send request to Gemini API
        system_instruction = PERSONA_PROMPTS.get(selected_persona, PERSONA_PROMPTS["Patient Teacher & Mentor"])

        with st.spinner("Synthesizing answer with Gemini..."):
            try:
                history_contents = []
                for m in st.session_state.messages:
                    role_type = "user" if m["role"] == "user" else "model"
                    history_contents.append(
                        types.Content(
                            role=role_type,
                            parts=[types.Part.from_text(text=m["content"])]
                        )
                    )

                response = client.models.generate_content(
                    model=selected_model,
                    contents=history_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=temperature
                    )
                )

                answer_text = response.text or "I was unable to generate a response. Please try rephrasing."

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer_text
                })

                # Register or update conversation thread
                if not st.session_state.current_thread_id:
                    new_id = f"th-{uuid.uuid4().hex[:6]}"
                    st.session_state.current_thread_id = new_id
                    title = prompt_to_send[:32] + "..." if len(prompt_to_send) > 32 else prompt_to_send
                    snippet = answer_text[:40].replace("\n", " ") + "..."
                    st.session_state.threads.insert(0, {
                        "id": new_id,
                        "title": title,
                        "snippet": snippet,
                        "messages": list(st.session_state.messages),
                        "created_at": "Just now"
                    })
                else:
                    for t_item in st.session_state.threads:
                        if t_item["id"] == st.session_state.current_thread_id:
                            t_item["messages"] = list(st.session_state.messages)
                            t_item["snippet"] = answer_text[:40].replace("\n", " ") + "..."
                            break

                st.rerun()

            except Exception as e:
                st.error(f"Gemini API Error: {type(e).__name__}: {e}")

# ---------------------------------------------------------
# Right Sidebar Panel: Projects & Recent Threads (Matches reference)
# ---------------------------------------------------------
with col_right:
    render_right_header(count=len(st.session_state.threads))

    if st.button("➕  New Project", key="new_project_btn", use_container_width=True):
        st.session_state.current_thread_id = None
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    for t_item in st.session_state.threads:
        is_active = (st.session_state.current_thread_id == t_item["id"])
        prefix = "🟢 " if is_active else "📁 "
        btn_label = f"{prefix} {t_item['title']}\n\n{t_item['snippet']}"
        if st.button(btn_label, key=f"open_thread_{t_item['id']}", use_container_width=True):
            st.session_state.current_thread_id = t_item["id"]
            st.session_state.messages = list(t_item["messages"])
            st.rerun()