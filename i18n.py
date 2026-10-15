"""
Internationalization (i18n) Module for PerplexAI Chatbot.
Provides centralized multi-language dictionaries and localization helper functions.
Supports English (Default), Spanish, French, German, and Japanese.
"""

from typing import Any, Dict
import streamlit as st

SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {"name": "English", "native_name": "English", "flag": "🇺🇸", "label": "English"},
    "es": {"name": "Spanish", "native_name": "Español", "flag": "🇪🇸", "label": "Español"},
    "fr": {"name": "French", "native_name": "Français", "flag": "🇫🇷", "label": "Français"},
    "de": {"name": "German", "native_name": "Deutsch", "flag": "🇩🇪", "label": "Deutsch"},
    "ja": {"name": "Japanese", "native_name": "日本語", "flag": "🇯🇵", "label": "日本語"},
}

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "ai_chat": {
        "en": "AI Chat",
        "es": "Chat IA",
        "fr": "Chat IA",
        "de": "KI-Chat",
        "ja": "AIチャット"
    },
    "gemini_online": {
        "en": "Gemini Online",
        "es": "Gemini En línea",
        "fr": "Gemini En ligne",
        "de": "Gemini Online",
        "ja": "Gemini オンライン"
    },
    "theme_light": {
        "en": "☀️ Light",
        "es": "☀️ Claro",
        "fr": "☀️ Clair",
        "de": "☀️ Hell",
        "ja": "☀️ ライト"
    },
    "theme_dark": {
        "en": "🌙 Dark",
        "es": "🌙 Oscuro",
        "fr": "🌙 Sombre",
        "de": "🌙 Dunkel",
        "ja": "🌙 ダーク"
    },
    "sign_in": {
        "en": "Sign in",
        "es": "Iniciar sesión",
        "fr": "Se connecter",
        "de": "Anmelden",
        "ja": "ログイン"
    },
    "sign_out": {
        "en": "Sign out",
        "es": "Cerrar sesión",
        "fr": "Déconnexion",
        "de": "Abmelden",
        "ja": "ログアウト"
    },
    "my_account": {
        "en": "My Account",
        "es": "Mi Cuenta",
        "fr": "Mon Compte",
        "de": "Mein Konto",
        "ja": "マイアカウント"
    },
    "signed_in_as": {
        "en": "Signed in as",
        "es": "Conectado como",
        "fr": "Connecté en tant que",
        "de": "Angemeldet als",
        "ja": "ログイン中:"
    },
    "new_chat": {
        "en": "+ New Thread",
        "es": "+ Nuevo Hilo",
        "fr": "+ Nouveau Fil",
        "de": "+ Neuer Thread",
        "ja": "+ 新規スレッド"
    },
    "nav_home": {
        "en": "💬 Home",
        "es": "💬 Inicio",
        "fr": "💬 Accueil",
        "de": "💬 Startseite",
        "ja": "💬 ホーム"
    },
    "nav_discover": {
        "en": "🧭 Discover",
        "es": "🧭 Descubrir",
        "fr": "🧭 Découvrir",
        "de": "🧭 Entdecken",
        "ja": "🧭 発見"
    },
    "nav_library": {
        "en": "📚 Library",
        "es": "📚 Biblioteca",
        "fr": "📚 Bibliothèque",
        "de": "📚 Bibliothek",
        "ja": "📚 ライブラリ"
    },
    "nav_settings": {
        "en": "⚙️ Settings",
        "es": "⚙️ Ajustes",
        "fr": "⚙️ Paramètres",
        "de": "⚙️ Einstellungen",
        "ja": "⚙️ 設定"
    },
    "preferences_title": {
        "en": "⚙️ Preferences & AI Controls",
        "es": "⚙️ Preferencias y Controles IA",
        "fr": "⚙️ Préférences & Contrôles IA",
        "de": "⚙️ Einstellungen & KI-Steuerung",
        "ja": "⚙️ 設定とAIコントロール"
    },
    "appearance_theme": {
        "en": "🌓 Appearance / Theme",
        "es": "🌓 Apariencia / Tema",
        "fr": "🌓 Apparence / Thème",
        "de": "🌓 Erscheinungsbild / Design",
        "ja": "🌓 外観 / テーマ"
    },
    "ai_model": {
        "en": "🤖 AI Model",
        "es": "🤖 Modelo de IA",
        "fr": "🤖 Modèle d'IA",
        "de": "🤖 KI-Modell",
        "ja": "🤖 AIモデル"
    },
    "assistant_persona": {
        "en": "🎭 Assistant Persona",
        "es": "🎭 Personalidad del Asistente",
        "fr": "🎭 Persona de l'Assistant",
        "de": "🎭 Assistenten-Persona",
        "ja": "🎭 アシスタントペルソナ"
    },
    "api_status_connected": {
        "en": "API Status: Connected",
        "es": "Estado de API: Conectado",
        "fr": "Statut API : Connecté",
        "de": "API-Status: Verbunden",
        "ja": "APIステータス: 接続完了"
    },
    "api_status_missing": {
        "en": "API Key Missing",
        "es": "Falta clave de API",
        "fr": "Clé API manquante",
        "de": "API-Schlüssel fehlt",
        "ja": "APIキーがありません"
    },
    "hero_title": {
        "en": "What can I help you with?",
        "es": "¿En qué puedo ayudarte hoy?",
        "fr": "Que puis-je faire pour vous ?",
        "de": "Wie kann ich Ihnen helfen?",
        "ja": "何をお手伝いしましょうか？"
    },
    "hero_subtitle": {
        "en": "Ask questions, analyze concepts, write code, or explore curated prompts below.",
        "es": "Haz preguntas, analiza conceptos, escribe código o explora las sugerencias a continuación.",
        "fr": "Posez des questions, analysez des concepts, écrivez du code ou explorez les suggestions ci-dessous.",
        "de": "Stellen Sie Fragen, analysieren Sie Konzepte, programmieren Sie oder entdecken Sie Vorschläge.",
        "ja": "質問したり、概念を分析したり、コードを書いたり、おすすめのプロンプトを探索できます。"
    },
    "sug_festivals": {
        "en": "🎵  Upcoming music festivals\n\nExplore 2026 global dates, venues & lineups ↗",
        "es": "🎵  Próximos festivales de música\n\nExplora fechas globales de 2026, sedes y artistas ↗",
        "fr": "🎵  Festivals de musique à venir\n\nDécouvrez les dates, lieux et artistes 2026 ↗",
        "de": "🎵  Kommende Musikfestivals\n\nTermine, Orte und Line-ups für 2026 ↗",
        "ja": "🎵  注目の音楽フェスティバル\n\n2026年の世界各国の開催日程と会場 ↗"
    },
    "sug_maxwell": {
        "en": "⚡  Research on Maxwell's Equations\n\nClassical electromagnetism, optics & wave theory ↗",
        "es": "⚡  Ecuaciones de Maxwell\n\nElectromagnetismo clásico, óptica y teoría de ondas ↗",
        "fr": "⚡  Équations de Maxwell\n\nÉlectromagnétisme classique, optique et ondes ↗",
        "de": "⚡  Forschung zu Maxwell-Gleichungen\n\nElektromagnetismus, Optik & Wellentheorie ↗",
        "ja": "⚡  マクスウェル方程式の研究\n\n古典電磁気学、光学および波動論 ↗"
    },
    "sug_gemini": {
        "en": "🔍  What is Google Gemini AI?\n\nMultimodal architecture, models & key capabilities ↗",
        "es": "🔍  ¿Qué es Google Gemini AI?\n\nArquitectura multimodal, modelos y capacidades clave ↗",
        "fr": "🔍  Qu'est-ce que Google Gemini AI ?\n\nArchitecture multimodale, modèles et fonctionnalités ↗",
        "de": "🔍  Was ist Google Gemini AI?\n\nMultimodale Architektur, Modelle & Schlüsselfunktionen ↗",
        "ja": "🔍  Google Gemini AIとは？\n\nマルチモーダル設計と主要機能 ↗"
    },
    "sug_crypto": {
        "en": "💰  Know more about crypto\n\nBlockchain fundamentals, Bitcoin & DeFi ecosystem ↗",
        "es": "💰  Aprende más sobre cripto\n\nFundamentos de blockchain, Bitcoin y ecosistema DeFi ↗",
        "fr": "💰  En savoir plus sur la crypto\n\nPrincipes blockchain, Bitcoin et écosystème DeFi ↗",
        "de": "💰  Mehr über Krypto erfahren\n\nBlockchain-Grundlagen, Bitcoin & DeFi-Ökosystem ↗",
        "ja": "💰  仮想通貨について学ぶ\n\nブロックチェーンの基礎、ビットコインとDeFi ↗"
    },
    "projects_header": {
        "en": "Projects & Threads",
        "es": "Proyectos e Hilos",
        "fr": "Projets et Fils",
        "de": "Projekte & Threads",
        "ja": "プロジェクトとスレッド"
    },
    "active_conversations": {
        "en": "Active Conversations",
        "es": "Conversaciones Activas",
        "fr": "Conversations Actives",
        "de": "Aktive Unterhaltungen",
        "ja": "アクティブな会話"
    },
    "chat_placeholder": {
        "en": "Ask anything or search web...",
        "es": "Pregunta lo que sea o busca en la web...",
        "fr": "Demandez n'importe quoi ou cherchez sur le web...",
        "de": "Fragen Sie beliebiges oder durchsuchen Sie das Web...",
        "ja": "何でも質問するかウェブを検索..."
    },
    "select_language": {
        "en": "Select Language",
        "es": "Seleccionar Idioma",
        "fr": "Choisir la Langue",
        "de": "Sprache Auswählen",
        "ja": "言語を選択"
    },
    "auth_modal_title": {
        "en": "Sign in to PerplexAI",
        "es": "Iniciar sesión en PerplexAI",
        "fr": "Connexion à PerplexAI",
        "de": "Bei PerplexAI anmelden",
        "ja": "PerplexAIにログイン"
    },
    "auth_tab_login": {
        "en": "Sign In",
        "es": "Iniciar Sesión",
        "fr": "Se Connecter",
        "de": "Anmelden",
        "ja": "ログイン"
    },
    "auth_tab_signup": {
        "en": "Create Account",
        "es": "Crear Cuenta",
        "fr": "Créer un Compte",
        "de": "Konto Erstellen",
        "ja": "アカウント作成"
    },
    "auth_email": {
        "en": "Email address",
        "es": "Correo electrónico",
        "fr": "Adresse e-mail",
        "de": "E-Mail-Adresse",
        "ja": "メールアドレス"
    },
    "auth_password": {
        "en": "Password",
        "es": "Contraseña",
        "fr": "Mot de passe",
        "de": "Passwort",
        "ja": "パスワード"
    },
    "auth_confirm_password": {
        "en": "Confirm password",
        "es": "Confirmar contraseña",
        "fr": "Confirmer le mot de passe",
        "de": "Passwort bestätigen",
        "ja": "パスワードの確認"
    },
    "auth_fullname": {
        "en": "Full name",
        "es": "Nombre completo",
        "fr": "Nom complet",
        "de": "Vollständiger Name",
        "ja": "氏名"
    },
    "auth_login_btn": {
        "en": "Sign In",
        "es": "Iniciar Sesión",
        "fr": "Se Connecter",
        "de": "Anmelden",
        "ja": "ログイン"
    },
    "auth_signup_btn": {
        "en": "Create Account",
        "es": "Crear Cuenta",
        "fr": "Créer un Compte",
        "de": "Konto Erstellen",
        "ja": "アカウント作成"
    },
    "auth_success_login": {
        "en": "Successfully signed in!",
        "es": "¡Sesión iniciada correctamente!",
        "fr": "Connexion réussie !",
        "de": "Erfolgreich angemeldet!",
        "ja": "ログインしました！"
    },
    "auth_success_signup": {
        "en": "Account created successfully! You are now logged in.",
        "es": "¡Cuenta creada exitosamente! Has iniciado sesión.",
        "fr": "Compte créé avec succès ! Vous êtes connecté.",
        "de": "Konto erfolgreich erstellt! Sie sind jetzt angemeldet.",
        "ja": "アカウントが正常に作成され、ログインしました。"
    },
    "auth_demo_hint": {
        "en": "💡 Quick Demo Login: demo@perplexai.com / Demo1234!",
        "es": "💡 Acceso Demo Rápido: demo@perplexai.com / Demo1234!",
        "fr": "💡 Compte Démo : demo@perplexai.com / Demo1234!",
        "de": "💡 Schnelle Demo-Anmeldung: demo@perplexai.com / Demo1234!",
        "ja": "💡 デモ用ログイン: demo@perplexai.com / Demo1234!"
    },
    "auth_member_since": {
        "en": "Member since",
        "es": "Miembro desde",
        "fr": "Membre depuis",
        "de": "Mitglied seit",
        "ja": "登録日:"
    },
    "auth_role": {
        "en": "Plan: Pro Member ❋",
        "es": "Plan: Miembro Pro ❋",
        "fr": "Forfait : Membre Pro ❋",
        "de": "Tarif: Pro-Mitglied ❋",
        "ja": "プラン: Proメンバー ❋"
    }
}

def get_text(key: str, lang: str = "en", **kwargs: Any) -> str:
    """Retrieves localized text for a key, falling back to English if missing."""
    lang_dict = TRANSLATIONS.get(key, {})
    text = lang_dict.get(lang) or lang_dict.get("en", key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

def t(key: str, **kwargs: Any) -> str:
    """Convenience shortcut for localized text using current session state language."""
    current_lang = "en"
    if hasattr(st, "session_state") and "language" in st.session_state:
        current_lang = st.session_state.language
    return get_text(key, lang=current_lang, **kwargs)
