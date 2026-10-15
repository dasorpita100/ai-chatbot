# 🤖 AI Chatbot

An interactive conversational AI web application built with [Streamlit](https://streamlit.io/) and powered by Google's [Gemini API](https://ai.google.dev/) using the official `google-genai` SDK.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
  - [Running the Test Script](#running-the-test-script)
  - [Launching the Web Application](#launching-the-web-application)
- [Configuration](#configuration)
- [Project Change Log](#project-change-log)
  - [How to Log Changes](#how-to-log-changes)
  - [Changelog Entries](#changelog-entries)

---

## 📖 Overview

This project provides an AI chatbot interface with a dedicated teacher/assistant persona. It retains conversational context across turns, handles API errors cleanly, and allows users to restart chat sessions at any time.

---

## ✨ Key Features

- **Multi-Turn Chat Context**: Preserves conversation history using Streamlit's `st.session_state` and Gemini's stateful chat session.
- **Custom System Persona**: Preconfigured system instructions defining the chatbot as a patient, encouraging teacher and assistant.
- **Session Management**: Dedicated **"New conversation"** button to instantly reset chat history and start fresh.
- **Error Handling**: Graceful exception reporting for network issues, invalid keys, or model unavailability.
- **Standalone Test Script**: Separate lightweight verification script (`testGemini.py`) to test API credentials and connectivity independently of the UI.

---

## 🛠 Tech Stack

- **Language**: Python 3.10+
- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **LLM SDK**: [`google-genai`](https://pypi.org/project/google-genai/) (Google GenAI Python SDK)
- **Environment Management**: [`python-dotenv`](https://pypi.org/project/python-dotenv/)
- **Models**:
  - `gemini-flash-latest` (Streamlit chatbot interface)
  - `gemini-3.8-flash` (Test script)

---

## 📁 Project Structure

```text
ai-chatbot/
├── .env                # Local environment variables (GEMINI_API_KEY, GOOGLE_CLIENT_ID) - do not commit
├── .venv/              # Python virtual environment
├── app.py              # Main Streamlit application and conversation flow
├── auth.py             # SQLite authentication engine (PBKDF2-HMAC-SHA256, sessions, validation)
├── i18n.py             # Internationalization dictionary & localization helper functions
├── ui_components.py    # UI template rendering functions & interactive header components
├── style.css           # Complete CSS styling, theme definitions, & responsive layout
├── tests/              # Automated unit and integration test suite
│   └── test_header_controls.py # Header controls, theme toggle, i18n & auth test suite
├── testGemini.py       # Quick API connectivity and response validation script
└── README.md           # Project documentation and change tracking log
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher installed.
- A valid Google Gemini API key (from [Google AI Studio](https://aistudio.google.com/)).

### Environment Setup

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Configure your API Key**:
   Ensure you have a `.env` file in the project root with the following line:
   ```env
   GEMINI_API_KEY="your_gemini_api_key_here"
   ```

3. **Install Dependencies** (if reinstalling or on a new machine):
   ```bash
   pip install streamlit google-genai python-dotenv
   ```

### Running the Test Script

Before running the web app, you can verify your Gemini API connection:

```bash
python testGemini.py
```

### Launching the Web Application

Run the Streamlit development server:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## ⚙️ Configuration

System prompt and persona settings are located in [app.py](file:///Users/orpitadas/ai-chatbot/app.py) under `SYSTEM_INSTRUCTIONS`. You can tweak the assistant's behavior, tone, or restrictions directly in that variable.

---

## 📝 Project Change Log

Use this section to record all modifications, enhancements, bug fixes, and refactoring across the codebase.

### How to Log Changes

Whenever you modify any file or add a feature, append an entry to the table below or create a dated release section following this structure:

- **Date**: YYYY-MM-DD
- **Type**: `Added` | `Changed` | `Fixed` | `Removed` | `Security`
- **File / Component**: File path or module affected
- **Description**: What was done and why

---

### Changelog Entries

| Date | Type | Component / File | Description | Author |
| :--- | :--- | :--- | :--- | :--- |
| **2026-10-15** | `Fixed` | [style.css](file:///Users/orpitadas/ai-chatbot/style.css), [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py), [tests/verify_sizes.py](file:///Users/orpitadas/ai-chatbot/tests/verify_sizes.py) | **Pixel-Perfect 120×56px Header Control Standardization**: Implemented unified `.header-control` rule fixing Light, English, and Sign in buttons to exact identical dimensions (`width: 120px`, `height: 56px`, `border-radius: 14px`, `box-sizing: border-box`, `border-width: 1px`). Re-engineered parent column flex layout with `flex: 0 0 120px` and `gap: 12px` without shrinking or stretching. Attached `.header-control` class to the button elements in the live DOM. Verified in headless Chrome via Chrome DevTools Protocol (CDP) that all 3 controls have exact identical computed dimensions (`120px` × `56px`), identical bounding rects (`120.00` × `56.00`), identical vertical baseline alignment (`top: 57.125px`), and equal `12.00px` spacing across both Dark and Light themes. | Assistant |
| **2026-10-15** | `Fixed` | [style.css](file:///Users/orpitadas/ai-chatbot/style.css), [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py), [i18n.py](file:///Users/orpitadas/ai-chatbot/i18n.py) | **Header Button Proportions & Dimensions Standardization**: Excluded header action buttons from the 72px suggestion card button rule in `style.css`. Unified `.st-key-hdr_theme_btn`, `.st-key-hdr_lang_popover`, and `.st-key-hdr_auth_btn` to identical `38px` height, `8px` border radius, and balanced `[2.8, 1.0, 1.0, 1.0]` column proportions. Removed redundant arrow character from language labels in `i18n.py` to prevent duplicate chevron artifacts in `st.popover`. | Assistant |
| **2026-10-15** | `Fixed` | [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py), [style.css](file:///Users/orpitadas/ai-chatbot/style.css) | **Equalized Dimensions for Header Buttons**: Normalized the 3 header action control column ratios to `[2.2, 1.0, 1.0, 1.0]`. Set `width: 100%` and uniform `height: 42px` across the theme toggle, language popover, and authentication button wrappers for geometric consistency. | Assistant |
| **2026-10-15** | `Fixed` | [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py), [style.css](file:///Users/orpitadas/ai-chatbot/style.css) | **Removed White Box Artifact at Top Canvas**: Removed indented `<script>` block in `load_custom_css` that was mistakenly parsed by Markdown as a codeblock (`<pre><code>`), eliminating the white rectangle at the top of the screen. Added theme-adaptive `--code-bg` styling for `pre` and `code` elements. | Assistant |
| **2026-10-15** | `Fixed` | [app.py](file:///Users/orpitadas/ai-chatbot/app.py), [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py), [.streamlit/config.toml](file:///Users/orpitadas/ai-chatbot/.streamlit/config.toml), [tests/test_header_controls.py](file:///Users/orpitadas/ai-chatbot/tests/test_header_controls.py) | **Restored & Fixed System (Auto) Theme Engine**: Reinstated `SYSTEM_THEME_CSS` using `@media (prefers-color-scheme: dark)` and `@media (prefers-color-scheme: light)` media query tokens. Configured `💻 System (Auto)` as default in `app.py`. Enabled 3-state cycling for header button (`💻 System` ➔ `☀️ Light` ➔ `🌙 Dark`), restored selector in sidebar Preferences, and removed hardcoded `base="light"` from `config.toml` so Streamlit adapts seamlessly. | Assistant |
| **2026-10-15** | `Fixed` | [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py), [app.py](file:///Users/orpitadas/ai-chatbot/app.py), [style.css](file:///Users/orpitadas/ai-chatbot/style.css), [i18n.py](file:///Users/orpitadas/ai-chatbot/i18n.py), [auth.py](file:///Users/orpitadas/ai-chatbot/auth.py), [tests/test_header_controls.py](file:///Users/orpitadas/ai-chatbot/tests/test_header_controls.py) | **Header Controls Full Functional Overhaul**: Replaced static mockup header elements with functional controls. **Theme Toggle**: Real-time Light/Dark toggle with label update (`☀️ Light`/`🌙 Dark`), URL query sync (`?theme=`), and client storage persistence. **Language Dropdown**: Implemented `i18n.py` supporting English (default), Spanish, French, German, and Japanese, updating the entire UI dynamically with URL persistence. **Authentication**: Built real SQLite backend in `auth.py` with PBKDF2-HMAC-SHA256 password hashing, validation, session tokens, `@st.dialog` modal for login/signup, demo account (`demo@perplexai.com`), user profile menu, and sign out flow. Added full integration test suite. | Assistant |
| **2026-10-15** | `Changed` | [app.py](file:///Users/orpitadas/ai-chatbot/app.py), [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py), [style.css](file:///Users/orpitadas/ai-chatbot/style.css) | Removed System (Auto) theme option completely. Configured pristine Light Mode (`☀️ Light`) as the default active state across session initialization and config, with clean toggle options strictly between `☀️ Light` and `🌙 Dark`. | Assistant |
| **2026-10-15** | `Fixed` | [style.css](file:///Users/orpitadas/ai-chatbot/style.css), [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py) | Comprehensive Dark Mode Contrast Overhaul: boosted typography variables (`--text-primary: #FFFFFF`, `--text-secondary: #E2E8F0`, `--text-muted: #94A3B8`), forced full dark background on all nested BaseWeb modal and dialog containers, and fixed sidebar button text visibility. | Assistant |
| **2026-10-15** | `Fixed` | [style.css](file:///Users/orpitadas/ai-chatbot/style.css) | Fixed unreadable/washed-out typography in Streamlit modals, dialogs, and the Deploy window: applied theme-adaptive background (`var(--card-bg)`), high-contrast headings, legible secondary captions (`var(--text-secondary)`), and styled action links/buttons. | Assistant |
| **2026-10-15** | `Changed` | [app.py](file:///Users/orpitadas/ai-chatbot/app.py), [style.css](file:///Users/orpitadas/ai-chatbot/style.css) | Cleaned up sidebar UI: tucked the Appearance/Theme dropdown into the collapsible `⚙️ Preferences & AI Controls` expander (linked to `⚙️ Settings` navigation), eliminating standalone dropdown clutter, and themed BaseWeb dropdowns. | Assistant |
| **2026-10-15** | `Fixed` | [app.py](file:///Users/orpitadas/ai-chatbot/app.py), [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py) | Fixed `TypeError: unexpected keyword argument 'theme_mode'` by adding automatic module reloading via `importlib.reload(ui_components)` in `app.py` and making `load_custom_css` signature accept flexible positional and keyword arguments (`*args, **kwargs`). | Assistant |
| **2026-10-15** | `Added` | [style.css](file:///Users/orpitadas/ai-chatbot/style.css), [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py), [app.py](file:///Users/orpitadas/ai-chatbot/app.py) | Added dynamic Theme Engine supporting **Light Mode**, **Dark Mode**, and **System Mode (Auto)**: created CSS variables design token system with Perplexity-style dark theme, sidebar theme switcher, and top bar mode badge. | Assistant |
| **2026-10-15** | `Fixed` | [style.css](file:///Users/orpitadas/ai-chatbot/style.css), [.streamlit/config.toml](file:///Users/orpitadas/ai-chatbot/.streamlit/config.toml), [app.py](file:///Users/orpitadas/ai-chatbot/app.py) | Fixed low-contrast / invisible text issues across entire app: enforced light theme config, added explicit high-contrast typography rules for buttons, cards, captions, and input placeholders, and unified suggestion/thread cards into single clickable components. | Assistant |
| **2026-10-15** | `Changed` | [style.css](file:///Users/orpitadas/ai-chatbot/style.css), [ui_components.py](file:///Users/orpitadas/ai-chatbot/ui_components.py), [app.py](file:///Users/orpitadas/ai-chatbot/app.py) | Modularized UI architecture: extracted all CSS rules into dedicated `style.css` and encapsulated HTML layout templates in `ui_components.py`, decoupling UI presentation from `app.py`. | Assistant |
| **2026-10-15** | `Changed` | [app.py](file:///Users/orpitadas/ai-chatbot/app.py) | Redesigned UI to match and elevate the Perplexity reference: 3-panel architecture (Navigation Sidebar, Center Chat Canvas, Right Projects & Threads panel), 2x2 interactive suggestion cards with pastel icon badges, multi-thread project management, system personas, and sleek typography. | Assistant |
| **2026-10-15** | `Added` | [README.md](file:///Users/orpitadas/ai-chatbot/README.md) | Created project documentation and change tracking log system. | Assistant / User |
| **2026-10-15** | `Fixed` | [app.py](file:///Users/orpitadas/ai-chatbot/app.py) | Added granular exception reporting (`{type(e).__name__}: {e}`) to display actionable Gemini API error messages. | Developer |
| **2026-10-15** | `Added` | [app.py](file:///Users/orpitadas/ai-chatbot/app.py) | Implemented "New conversation" reset button to clear session messages and re-initialize chat state. | Developer |
| **2026-10-15** | `Added` | [app.py](file:///Users/orpitadas/ai-chatbot/app.py) | Configured custom `SYSTEM_INSTRUCTIONS` persona (friendly AI assistant & patient teacher). | Developer |
| **2026-10-15** | `Added` | [app.py](file:///Users/orpitadas/ai-chatbot/app.py) | Integrated Streamlit chat UI (`st.chat_input`, `st.chat_message`, `st.session_state`) with Google GenAI chat client. | Developer |
| **2026-10-15** | `Added` | [testGemini.py](file:///Users/orpitadas/ai-chatbot/testGemini.py) | Created standalone test script to test Gemini API connectivity with `gemini-3.8-flash`. | Developer |
| **2026-10-15** | `Added` | [.env](file:///Users/orpitadas/ai-chatbot/.env) | Created environment variable configuration file for storing `GEMINI_API_KEY`. | Developer |
| **2026-10-15** | `Added` | Project Setup | Initialized project repository with Python virtual environment (`.venv`) and installed dependencies (`streamlit`, `google-genai`, `python-dotenv`). | Developer |

---

### Change Log Template (For New Entries)

Copy and paste this snippet at the top of the changelog entries table for each new change:

```markdown
| YYYY-MM-DD | Added / Changed / Fixed | [filename.ext](file:///Users/orpitadas/ai-chatbot/filename.ext) | Detailed description of the change | Your Name |
```
