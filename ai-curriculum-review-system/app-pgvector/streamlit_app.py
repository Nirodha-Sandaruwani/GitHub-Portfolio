import os
import re
import textwrap
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Optional charts
PLOTLY_IMPORT_ERROR = None

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception as e:
    PLOTLY_AVAILABLE = False
    PLOTLY_IMPORT_ERROR = str(e)

# Optional pgvector / Postgres support
try:
    import psycopg
    PGVECTOR_AVAILABLE = True
except Exception:
    PGVECTOR_AVAILABLE = False

# Optional PDF report support
try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    PDF_AVAILABLE = True
except Exception:
    PDF_AVAILABLE = False


# ============================================================
# Page setup
# ============================================================

st.set_page_config(
    page_title="JAMK Course Similarity Review",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Paths and environment
# ============================================================

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
ENV_PATH = PROJECT_ROOT / ".env"

FINAL_EMBEDDINGS_PATH = DATA_DIR / "final_embeddings.parquet"
COURSES_CLEAN_PATH = DATA_DIR / "courses_clean.csv"

load_dotenv(ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL_NAME = "text-embedding-3-large"

FINAL_RECOMMENDATION_PATH = PROJECT_ROOT / "reports" / "tables" / "thresholds" / "final_threshold_recommendation.csv"

USE_PGVECTOR = os.getenv("USE_PGVECTOR", "false").strip().lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
PGVECTOR_TABLE = os.getenv("PGVECTOR_TABLE", "course_embeddings_app").strip()

FINAL_MODEL_NAME = ""
FINAL_TEXT_VARIANT = ""
FINAL_SIMILARITY_METRIC = ""
FINAL_SELECTION_RULE = ""
FINAL_LOCKED_THRESHOLD = 0.0


# ============================================================
# Brand and UI colors
# ============================================================

JAMK_SPINDLE = "#AEC9E7"
JAMK_MAGENTA = "#E5007D"
JAMK_PLUM = "#500257"

DEEP_NAVY = "#221B45"
TEXT_DARK = "#1B2235"
TEXT_MUTED = "#6B7287"
TEXT_SOFT = "#8790A3"

BG_WARM = "#F7F3EF"
BG_SOFT = "#FCFAF8"
CARD_WHITE = "#FFFFFF"
BORDER_SOFT = "#DDD7E5"
BORDER_LIGHT = "#ECE7F0"

SUCCESS = "#138A63"
WARNING = "#D97706"
DANGER = "#C43B3B"

SOFT_SUCCESS = "#ECF8F2"
SOFT_WARNING = "#FFF4E8"
SOFT_DANGER = "#FDEEEE"

HIGHLIGHT_ORANGE = "#FFE2BF"
HIGHLIGHT_BLUE = "#DDEDFB"


# ============================================================
# Styling
# ============================================================

st.markdown(
    f"""
    <style>
        :root {{
            --jamk-light: {JAMK_SPINDLE};
            --jamk-magenta: {JAMK_MAGENTA};
            --jamk-plum: {JAMK_PLUM};
            --deep-navy: {DEEP_NAVY};
            --text-dark: {TEXT_DARK};
            --text-muted: {TEXT_MUTED};
            --text-soft: {TEXT_SOFT};
            --bg-warm: {BG_WARM};
            --bg-soft: {BG_SOFT};
            --card-white: {CARD_WHITE};
            --border-soft: {BORDER_SOFT};
            --border-light: {BORDER_LIGHT};
            --success: {SUCCESS};
            --warning: {WARNING};
            --danger: {DANGER};
            --soft-success: {SOFT_SUCCESS};
            --soft-warning: {SOFT_WARNING};
            --soft-danger: {SOFT_DANGER};
        }}

        html, body, [class*="css"] {{
            font-family: "Inter", "Segoe UI", sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 12% 10%, rgba(174,201,231,0.20) 0%, rgba(174,201,231,0.00) 28%),
                radial-gradient(circle at 88% 8%, rgba(229,0,125,0.07) 0%, rgba(229,0,125,0.00) 18%),
                linear-gradient(135deg, var(--bg-warm) 0%, var(--bg-soft) 55%, #ffffff 100%);
            color: var(--text-dark);
        }}

        .block-container {{
            max-width: 1480px;
            padding-top: 2.0rem;
            padding-bottom: 2.2rem;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #fbf8fc 0%, #ffffff 100%);
            border-left: 1px solid var(--border-light);
        }}

        section[data-testid="stSidebar"] .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 1.2rem;
        }}

        .topbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.8rem;
            margin-top: 1.2rem;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }}

        .brand-mark {{
            width: 42px;
            height: 42px;
            border-radius: 14px;
            background: linear-gradient(135deg, {JAMK_PLUM} 0%, {JAMK_MAGENTA} 100%);
            box-shadow: 0 12px 26px rgba(80,2,87,0.22);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.05rem;
            font-weight: 800;
        }}

        .brand-title {{
            color: var(--deep-navy);
            font-size: 1.05rem;
            font-weight: 850;
            letter-spacing: -0.01em;
            line-height: 1.15;
        }}

        .brand-sub {{
            color: var(--text-muted);
            font-size: 0.86rem;
            margin-top: 0.1rem;
        }}

        .status-chip {{
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.5rem 0.75rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.82);
            border: 1px solid var(--border-light);
            color: var(--deep-navy);
            font-size: 0.84rem;
            font-weight: 760;
            box-shadow: 0 8px 20px rgba(34,27,69,0.04);
        }}

        .hero {{
            position: relative;
            overflow: hidden;
            border-radius: 32px;
            padding: 1.35rem 1.5rem 1.35rem 1.5rem;
            background:
                radial-gradient(circle at 88% 18%, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.00) 26%),
                linear-gradient(135deg, #1B1537 0%, #371246 48%, #640057 76%, #8F005F 100%);
            border: 1px solid rgba(255,255,255,0.10);
            box-shadow: 0 20px 48px rgba(32,19,61,0.18);
            margin-bottom: 1rem;
        }}

        .hero::before {{
            content: "";
            position: absolute;
            right: -90px;
            top: -70px;
            width: 220px;
            height: 220px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
        }}

        .hero-grid {{
            position: relative;
            z-index: 2;
            display: grid;
            grid-template-columns: 1.45fr 0.75fr;
            gap: 1rem;
            align-items: stretch;
        }}

        .hero-title {{
            color: white;
        }}

        .hero-label {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.34rem 0.68rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.11);
            border: 1px solid rgba(255,255,255,0.14);
            color: rgba(255,255,255,0.90);
            font-size: 0.76rem;
            font-weight: 760;
            margin-bottom: 0.65rem;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }}

        .hero-title h1 {{
            margin: 0;
            color: white;
            font-size: 2.1rem;
            line-height: 1.06;
            font-weight: 850;
            letter-spacing: -0.035em;
            max-width: 760px;
        }}

        .hero-title p {{
            margin: 0.65rem 0 0 0;
            color: rgba(255,255,255,0.92);
            line-height: 1.58;
            font-size: 0.97rem;
            max-width: 760px;
        }}

        .hero-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 0.9rem;
        }}

        .hero-tag {{
            display: inline-flex;
            align-items: center;
            padding: 0.42rem 0.8rem;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(229,0,125,0.23) 0%, rgba(255,255,255,0.08) 100%);
            border: 1px solid rgba(255,255,255,0.15);
            color: white;
            font-size: 0.82rem;
            font-weight: 760;
        }}

        .hero-side {{
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 24px;
            padding: 1rem;
            min-height: 100%;
            color: white;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        }}

        .hero-side-title {{
            color: rgba(255,255,255,0.76);
            font-size: 0.78rem;
            font-weight: 760;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.45rem;
        }}

        .hero-side-value {{
            color: white;
            font-size: 1.28rem;
            font-weight: 850;
            line-height: 1.15;
            margin-bottom: 0.3rem;
        }}

        .hero-side-text {{
            color: rgba(255,255,255,0.88);
            font-size: 0.9rem;
            line-height: 1.55;
        }}

        .mini-stat {{
            background: linear-gradient(180deg, #ffffff 0%, #fcfbfd 100%);
            border: 1px solid var(--border-light);
            border-radius: 22px;
            padding: 0.9rem 0.98rem;
            min-height: 104px;
            box-shadow: 0 8px 20px rgba(35,27,70,0.05);
        }}

        .mini-stat-label {{
            color: var(--text-muted);
            font-size: 0.81rem;
            margin-bottom: 0.18rem;
        }}

        .mini-stat-value {{
            color: var(--deep-navy);
            font-size: 1.18rem;
            line-height: 1.2;
            font-weight: 850;
        }}

        .mini-stat-sub {{
            color: var(--text-muted);
            font-size: 0.86rem;
            margin-top: 0.24rem;
            line-height: 1.42;
        }}

        .shell-card {{
            background: rgba(248, 214, 232, 0.96);
            border: 1px solid rgba(229, 0, 125, 0.14);
            border-radius: 12px;
            padding: 0.8rem;
            box-shadow: 0 14px 30px rgba(35,27,70,0.06);
            backdrop-filter: blur(4px);
            margin-bottom: 1rem;
        }}

        .surface-card {{
            background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(251,248,252,1) 100%);
            border: 1px solid var(--border-light);
            border-radius: 24px;
            padding: 1rem;
            box-shadow: 0 10px 22px rgba(35,27,70,0.05);
            min-height: 100%;
        }}

        .section-kicker {{
            color: #7A7093;
            font-size: 0.76rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.3rem;
        }}

        .section-title {{
            color: var(--deep-navy);
            font-size: 1.15rem;
            font-weight: 850;
            letter-spacing: -0.01em;
            margin-bottom: 0.35rem;
        }}

        .section-sub {{
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.55;
            margin-bottom: 0.8rem;
        }}

        .helper-box {{
            background: linear-gradient(135deg, rgba(174,201,231,0.13) 0%, rgba(255,255,255,0.96) 100%);
            border: 1px solid rgba(34,27,69,0.08);
            border-radius: 22px;
            padding: 1rem;
            margin-bottom: 0.85rem;
        }}

        .helper-box h4 {{
            margin: 0 0 0.45rem 0;
            color: var(--deep-navy);
            font-size: 0.98rem;
            font-weight: 850;
        }}

        .helper-box p {{
            margin: 0;
            color: var(--text-muted);
            font-size: 0.93rem;
            line-height: 1.62;
        }}

        .workspace-card {{
            background:
            linear-gradient(135deg, rgba(255,255,255,0.96) 0%, rgba(248,244,250,0.98) 100%);
            border: 1px solid rgba(34,27,69,0.08);
            border-radius: 24px;
            padding: 1rem;
            box-shadow: 0 10px 24px rgba(35,27,70,0.06);
            margin-bottom: 0.95rem;
        }}

        .glass-panel {{
            backdrop-filter: blur(8px);
        }}

        .panel-label {{
            color: #7A7093;
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
        }}

        .workbench-title {{
            color: var(--deep-navy);
            font-size: 1.08rem;
            font-weight: 850;
            letter-spacing: -0.01em;
            margin-bottom: 0.8rem;
        }}

        .explain-box {{
            background: rgba(174,201,231,0.10);
            border: 1px solid rgba(34,27,69,0.06);
            border-radius: 18px;
            padding: 0.78rem 0.85rem;
            margin-bottom: 0.65rem;
        }}

        .explain-title {{
            color: var(--deep-navy);
            font-size: 0.92rem;
            font-weight: 800;
            margin-bottom: 0.18rem;
        }}

        .explain-text {{
            color: var(--text-muted);
            font-size: 0.88rem;
            line-height: 1.5;
        }}

        .settings-list {{
            margin: 0;
            padding: 0;
        }}

        .settings-row {{
            padding: 0.45rem 0;
            border-bottom: 1px solid rgba(34,27,69,0.06);
            color: var(--text-muted);
            font-size: 0.92rem;
            line-height: 1.5;
        }}

        .settings-row:last-child {{
            border-bottom: 0;
            padding-bottom: 0;
        }}

        .settings-row b {{
            color: var(--deep-navy);
        }}

        .sidebar-title {{
            color: var(--deep-navy);
            font-size: 1.05rem;
            font-weight: 850;
            margin-bottom: 0.8rem;
            letter-spacing: -0.01em;
        }}

        .section-heading {{
            color: var(--deep-navy);
            font-size: 1.26rem;
            font-weight: 850;
            margin: 0.45rem 0 0.9rem 0;
            letter-spacing: -0.02em;
        }}

        .result-stat {{
            color: var(--deep-navy);
            font-size: 2.05rem;
            font-weight: 850;
            line-height: 1.05;
        }}

        .decision-banner {{
            padding: 0.8rem 0.8rem;
            border-radius: 18px;
            line-height: 1.55;
            font-size: 0.96rem;
            margin-top: 0.5rem;
        }}

        .decision-banner.good {{
            background: var(--soft-success);
            border: 1px solid rgba(19,138,99,0.20);
            color: #146b4d;
        }}

        .decision-banner.mid {{
            background: var(--soft-warning);
            border: 1px solid rgba(217,119,6,0.20);
            color: #8b4c0c;
        }}

        .decision-banner.bad {{
            background: var(--soft-danger);
            border: 1px solid rgba(196,59,59,0.20);
            color: #8d2424;
        }}

        .course-card {{
            background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(251,248,252,1) 100%);
            border: 1px solid var(--border-light);
            border-radius: 22px;
            padding: 1rem;
            box-shadow: 0 10px 20px rgba(35,27,70,0.04);
            margin-bottom: 0.3rem;
        }}

        .course-name {{
            color: var(--deep-navy);
            font-size: 1.06rem;
            font-weight: 850;
            margin-bottom: 0.1rem;
        }}

        .course-code {{
            color: {JAMK_PLUM};
            font-size: 0.92rem;
            font-weight: 800;
            margin-bottom: 0.62rem;
        }}

        .pill-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-bottom: 0.15rem;
        }}

        .pill {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            padding: 0.28rem 0.72rem;
            font-size: 0.85rem;
            font-weight: 800;
            border: 1px solid transparent;
        }}

        .pill.score {{
            background: rgba(174,201,231,0.26);
            color: var(--deep-navy);
            border-color: rgba(174,201,231,0.55);
        }}

        .pill.good {{
            background: rgba(19,138,99,0.10);
            color: #146b4d;
            border-color: rgba(19,138,99,0.22);
        }}

        .pill.mid {{
            background: rgba(217,119,6,0.10);
            color: #8b4c0c;
            border-color: rgba(217,119,6,0.22);
        }}

        .pill.bad {{
            background: rgba(196,59,59,0.10);
            color: #8d2424;
            border-color: rgba(196,59,59,0.22);
        }}

        .progress-track {{
            width: 100%;
            height: 10px;
            border-radius: 999px;
            background: #EEEAF2;
            overflow: hidden;
            margin: 0.7rem 0 0.2rem 0;
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, {JAMK_SPINDLE} 0%, {JAMK_MAGENTA} 60%, {JAMK_PLUM} 100%);
        }}

        .compare-note {{
            background: linear-gradient(135deg, rgba(174,201,231,0.12) 0%, rgba(255,255,255,0.98) 100%);
            border: 1px solid rgba(34,27,69,0.08);
            border-radius: 22px;
            padding: 1rem;
            line-height: 1.62;
            color: var(--text-dark);
        }}

        .compare-note strong {{
            color: var(--deep-navy);
        }}

        .streamlit-expanderHeader {{
            font-weight: 800 !important;
            color: {DEEP_NAVY} !important;
        }}

        div[data-testid="stDataFrame"] {{
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--border-light);
        }}

        div[data-testid="stForm"] {{
            border: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }}

        div[data-testid="stForm"] > div {{
            border: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }}

        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stFormSubmitButton"] > button {{
            border-radius: 14px !important;
            border: 1px solid rgba(80,2,87,0.15) !important;
            background: linear-gradient(135deg, #500257 0%, #E5007D 100%) !important;
            color: white !important;
            font-weight: 800 !important;
            min-height: 48px !important;
            box-shadow: 0 10px 22px rgba(80,2,87,0.18) !important;
            width: 100% !important;
        }}
        
        div[data-testid="stFormSubmitButton"] {{
            display: block;
            width: 100% !important;
        }}

        .stTextInput input,
        .stTextArea textarea {{
            border-radius: 16px !important;
        }}

        .review-note {{
            color: var(--text-muted);
            font-size: 0.9rem;
            line-height: 1.58;
            margin-top: 0.25rem;
        }}

        @media (max-width: 1100px) {{
            .hero-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .summary-card-report-actions {{
            margin-top: 0.8rem;
        }}
        
        .tight-metric-text {{
            margin-top: 0.55rem;
        }}

    /* Fix slider TRACK - this is the correct selector for 1.56 */
        section[data-testid="stSidebar"] .stSlider > div > div > div > div {{
            background: linear-gradient(90deg, #AEC9E7 0%, #E5007D 60%, #500257 100%) !important;
            }}

            /* Thumb dot */
            section[data-testid="stSidebar"] .stSlider > div > div > div > div > div {{
                background: #500257 !important;
                border-color: #500257 !important;
            }}

            /* Slider label text color */
            section[data-testid="stSidebar"] .stSlider label p {{
                color: #7A7093 !important;
                font-size: 0.88rem !important;
            }}

            /* Checkbox label text color */
            section[data-testid="stSidebar"] .stCheckbox label p {{
                color: #7A7093 !important;
                font-size: 0.88rem !important;
                line-height: 1.5 !important;
            }}

            /* Inner explain-box — compact like process preview */
            section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"] {{
                background: rgba(174,201,231,0.10) !important;
                border: 1px solid rgba(34,27,69,0.06) !important;
                border-radius: 14px !important;
                padding: 0.45rem 1.2rem !important;
                margin: 0 !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"] > div {{
                margin: 0 !important;
                padding: 0 !important;
            }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Helpers
# ============================================================

def clean_text_value(value) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)
    text = value.replace("\xa0", " ").replace("\r\n", "\n").replace("\r", "\n").replace("\t", " ")
    text = " ".join(text.split())
    return text.strip()


def safe_html_text(text) -> str:
    text = clean_text_value(text)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def split_multiline_to_list(text: str) -> List[str]:
    if not text:
        return []
    items = [clean_text_value(line) for line in text.split("\n")]
    return [item for item in items if item]


def ensure_sentence_like_boundary(text: str) -> str:
    if not text:
        return ""
    if text.endswith((".", "!", "?", ":", ";")):
        return text
    return text + "."


def join_list_field(value: List[str], separator: str = " ") -> str:
    cleaned = [clean_text_value(v) for v in value]
    cleaned = [v for v in cleaned if v]
    if separator == " ":
        cleaned = [ensure_sentence_like_boundary(v) for v in cleaned]
    return separator.join(cleaned).strip()


def prefix_if_text_exists(prefix: str, text: str) -> str:
    text = clean_text_value(text)
    if not text:
        return ""
    return f"{prefix}{text}"


def build_embedding_text_enriched_from_form(
    course_name: str,
    objective_items: List[str],
    knowledge_items: List[str],
    practice_items: List[str],
    applying_items: List[str],
    multidisciplinary_items: List[str],
    communication_items: List[str],
    investigations_items: List[str],
    learning_outcomes_items: List[str],
    content_items: List[str],
    prerequisites_items: List[str],
) -> str:
    course_name_text = clean_text_value(course_name)
    objective_text = join_list_field(objective_items, separator=" ")
    competences_knowledge_text = join_list_field(knowledge_items, separator=" ")
    competences_practice_text = join_list_field(practice_items, separator=" ")
    competences_applying_text = join_list_field(applying_items, separator=" ")
    competences_multidisciplinary_text = join_list_field(multidisciplinary_items, separator=" ")
    competences_communication_text = join_list_field(communication_items, separator=" ")
    competences_investigations_text = join_list_field(investigations_items, separator=" ")
    learning_outcomes_text = join_list_field(learning_outcomes_items, separator=" ")
    content_text = join_list_field(content_items, separator=" ")
    prerequisites_text = join_list_field(prerequisites_items, separator=", ")

    parts = [
        course_name_text,
        objective_text,
        competences_knowledge_text,
        competences_practice_text,
        content_text,
        prefix_if_text_exists("Applying technology to practice includes: ", competences_applying_text),
        prefix_if_text_exists("Multidisciplinary competence includes: ", competences_multidisciplinary_text),
        prefix_if_text_exists("Communication and teamwork includes: ", competences_communication_text),
        prefix_if_text_exists("Investigations and information retrieval includes: ", competences_investigations_text),
        prefix_if_text_exists("Learning outcomes include: ", learning_outcomes_text),
        prefix_if_text_exists("Prerequisites include: ", prerequisites_text),
    ]

    parts = [clean_text_value(p) for p in parts]
    parts = [p for p in parts if p]
    return "\n".join(parts)


def score_to_percent(score: float) -> float:
    return round(float(score) * 100, 2)


def overlap_band(score: float, threshold: float) -> str:
    if score >= threshold + 0.08:
        return "Strong overlap indication"
    if score >= threshold:
        return "Potential overlap"
    if score >= threshold - 0.05:
        return "Related but below alert level"
    return "Low similarity"


def interpret_decision(top_score: float, threshold: float) -> Tuple[str, str]:
    if top_score >= threshold:
        return (
            "Potential overlap found",
            "The submitted course has at least one existing course above the alert level."
        )
    if top_score >= threshold - 0.05:
        return (
            "No overlap alert, but related content found",
            "The strongest match is below the alert level, but still close enough to justify human review."
        )
    return (
        "No meaningful overlap detected",
        "The submitted course did not reach the current alert level against the stored course set."
    )


def get_interpretation_pill_class(interpretation: str) -> str:
    if interpretation in {"Strong overlap indication", "Potential overlap"}:
        return "bad"
    if interpretation == "Related but below alert level":
        return "mid"
    return "good"


def make_safe_filename(text: str) -> str:
    cleaned = clean_text_value(text or "similarity_report")
    cleaned = re.sub(r"[^A-Za-z0-9_\- ]+", "", cleaned)
    cleaned = cleaned.replace(" ", "_")
    return cleaned or "similarity_report"


def generate_report_dataframe(
    input_course_name: str,
    input_course_code: str,
    threshold: float,
    text_variant: str,
    model_name: str,
    matches_df: pd.DataFrame,
) -> pd.DataFrame:
    report_df = matches_df.copy()
    report_df = report_df.rename(columns={
        "course_unit_code": "matched_course_unit_code",
        "course_name": "matched_course_name",
        "final_embedding_text": "matched_course_text",
    })
    report_df.insert(0, "input_course_name", input_course_name)
    report_df.insert(1, "input_course_code", input_course_code)
    report_df["locked_threshold"] = threshold
    report_df["model_name"] = model_name
    report_df["text_variant"] = text_variant
    report_df["similarity_percent"] = report_df["similarity_score"].apply(score_to_percent)
    return report_df


def split_sentences_for_highlighting(text: str) -> List[str]:
    text = clean_text_value(text)
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+", text)
    parts = [clean_text_value(p) for p in parts if clean_text_value(p)]
    return parts


def get_query_keywords(query_text: str) -> set:
    tokens = re.findall(r"\b[^\W\d_][^\W_\-]{2,}(?:-[^\W_]+)*\b", query_text.lower(), flags=re.UNICODE)
    stopwords = {
        "the", "and", "for", "with", "that", "this", "from", "into", "you", "your",
        "are", "can", "how", "use", "using", "used", "able", "understand", "understanding",
        "course", "learn", "learning", "includes", "include", "their", "them", "within",
        "have", "has", "will", "one", "two", "three", "about", "know"
    }
    return {t for t in tokens if t not in stopwords}


def sentence_overlap_score(sentence: str, query_keywords: set) -> int:
    sentence_tokens = set(
    re.findall(r"\b[^\W\d_][^\W_\-]{2,}(?:-[^\W_]+)*\b", sentence.lower(), flags=re.UNICODE)
)
    return len(sentence_tokens.intersection(query_keywords))


def highlight_overlap_sentences(
    text: str,
    query_text: str,
    highlight_color: str,
    min_overlap: int = 2,
) -> str:
    sentences = split_sentences_for_highlighting(text)
    if not sentences:
        return f"<span style='color:{TEXT_DARK};'>—</span>"

    query_keywords = get_query_keywords(query_text)
    rendered = []

    for sentence in sentences:
        overlap_count = sentence_overlap_score(sentence, query_keywords)
        safe_sentence = safe_html_text(sentence)
        if overlap_count >= min_overlap:
            rendered.append(
                f"<span style='color:{TEXT_DARK}; background:{highlight_color}; padding:0 0.14rem; border-radius:0.18rem;'>{safe_sentence}</span>"
            )
        else:
            rendered.append(
                f"<span style='color:{TEXT_DARK};'>{safe_sentence}</span>"
            )

    return " ".join(rendered)


def build_structured_match_view(row: pd.Series, query_text: str) -> str:
    overlap_flag = int(row.get("overlap_flag", 0))
    highlight_color = HIGHLIGHT_ORANGE if overlap_flag == 1 else HIGHLIGHT_BLUE

    sections = [
        ("Objective", row.get("objective_text", "")),
        ("EUR-ACE Knowledge and Understanding", row.get("competences_knowledge_text", "")),
        ("EUR-ACE Engineering Practice", row.get("competences_practice_text", "")),
        ("Content", row.get("content_text", "")),
        ("Prerequisites", row.get("prerequisites_text", "")),
    ]

    html_parts = []
    for label, value in sections:
        cleaned_value = clean_text_value(value)
        if cleaned_value:
            highlighted = highlight_overlap_sentences(
                cleaned_value,
                query_text=query_text,
                highlight_color=highlight_color,
                min_overlap=2,
            )
            html_parts.append(
                f"""
                <div style="margin-bottom:0.95rem;">
                    <div style="font-weight:800; color:{DEEP_NAVY}; margin-bottom:0.18rem; font-size:0.95rem;">{safe_html_text(label)}</div>
                    <div style="line-height:1.72; color:{TEXT_DARK}; font-size:0.96rem;">{highlighted}</div>
                </div>
                """
            )

    if not html_parts:
        return f"<div style='color:{TEXT_DARK};'>No structured course fields available.</div>"

    return "".join(html_parts)


def highlight_overlap_sentences_pdf(
    text: str,
    query_text: str,
    highlight_color_hex: str,
    min_overlap: int = 2,
) -> str:
    sentences = split_sentences_for_highlighting(text)
    if not sentences:
        return "—"

    query_keywords = get_query_keywords(query_text)
    rendered = []

    for sentence in sentences:
        overlap_count = sentence_overlap_score(sentence, query_keywords)
        safe_sentence = (
            sentence.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        if overlap_count >= min_overlap:
            rendered.append(f'<font backcolor="{highlight_color_hex}">{safe_sentence}</font>')
        else:
            rendered.append(safe_sentence)

    return " ".join(rendered)


# ============================================================
# Charts
# ============================================================

def make_ring_figure(score_percent: float, threshold_percent: float):
    if not PLOTLY_AVAILABLE:
        return None

    if score_percent >= threshold_percent:
        bar_color = DANGER
        steps = [
        {"range": [0, threshold_percent], "color": "#F3EDF6"},
        {"range": [threshold_percent, 100], "color": "#FDEEEE"},
    ]
    elif score_percent >= threshold_percent - 5:
        bar_color = WARNING
        steps = [
        {"range": [0, threshold_percent - 5], "color": "#E8F2FB"},
        {"range": [threshold_percent - 5, threshold_percent], "color": "#FFF4E8"},
        {"range": [threshold_percent, 100], "color": "#FDEEEE"},
    ]
    else:
        bar_color = SUCCESS
        steps = [
        {"range": [0, threshold_percent - 5], "color": "#ECF8F2"},
        {"range": [threshold_percent - 5, threshold_percent], "color": "#FFF4E8"},
        {"range": [threshold_percent, 100], "color": "#F6F7FA"},
    ]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score_percent,
            number={"suffix": "%", "font": {"size": 36, "color": DEEP_NAVY}},
            gauge={
                "axis": {"range": [0, 100], "visible": False},
                "bar": {"color": bar_color, "thickness": 0.28},
                "bgcolor": "white",
                "borderwidth": 0,
                "steps": steps,
                "threshold": {
                    "line": {"color": JAMK_PLUM, "width": 4},
                    "thickness": 0.8,
                    "value": threshold_percent,
                },
            },
            title={"text": "Top match", "font": {"size": 14, "color": TEXT_MUTED}},
        )
    )
    fig.update_layout(
        height=250,
        margin=dict(l=15, r=15, t=10, b=10),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
    )
    return fig


def make_distribution_chart(matches_df: pd.DataFrame, threshold_percent: float):
    if not PLOTLY_AVAILABLE:
        return None

    chart_df = matches_df.copy()
    chart_df["similarity_percent"] = chart_df["similarity_score"].apply(score_to_percent)
    colors = [DANGER if int(v) == 1 else JAMK_SPINDLE for v in chart_df["overlap_flag"]]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=chart_df["course_unit_code"],
            y=chart_df["similarity_percent"],
            marker_color=colors,
            text=[f"{v:.1f}%" for v in chart_df["similarity_percent"]],
            textposition="outside",
            hovertemplate="<b>%{{x}}</b><br>Similarity: %{{y:.2f}}%<extra></extra>",
        )
    )
    fig.add_hline(
        y=threshold_percent,
        line_dash="dash",
        line_color=JAMK_PLUM,
        annotation_text=f"Threshold {threshold_percent:.0f}%",
        annotation_position="top right",
    )
    fig.update_layout(
        height=340,
        margin=dict(l=15, r=15, t=20, b=15),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        xaxis_title="Course code",
        yaxis_title="Similarity %",
        yaxis_range=[0, max(100, chart_df["similarity_percent"].max() + 10)],
    )
    return fig


# ============================================================
# PDF report
# ============================================================

def create_similarity_pdf_bytes(
    input_course_code: str,
    input_course_name: str,
    input_sections: dict,
    top_score: float,
    above_threshold_count: int,
    threshold: float,
    matches_df: pd.DataFrame,
    query_text: str,
) -> bytes:
    if not PDF_AVAILABLE:
        raise RuntimeError("reportlab is not installed, so PDF export is not available.")

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "JAMKTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor(DEEP_NAVY),
        spaceAfter=8,
        alignment=TA_LEFT,
    )
    subtitle_style = ParagraphStyle(
        "JAMKSubtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor(TEXT_MUTED),
        spaceAfter=8,
    )
    section_style = ParagraphStyle(
        "JAMKSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor(JAMK_PLUM),
        spaceAfter=6,
        spaceBefore=8,
    )
    label_style = ParagraphStyle(
        "JAMKLabel",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor(DEEP_NAVY),
        spaceAfter=2,
    )
    body_style = ParagraphStyle(
        "JAMKBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor(TEXT_DARK),
        spaceAfter=5,
    )
    note_style = ParagraphStyle(
        "JAMKNote",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor(TEXT_MUTED),
        spaceAfter=6,
    )

    story = []

    story.append(Paragraph("JAMK Course Similarity Review Report", title_style))
    story.append(Paragraph(
        "This report supports curriculum review by highlighting existing courses that are most similar to the submitted course description.",
        subtitle_style
    ))

    header_table = Table(
        [
            ["Submitted course code", clean_text_value(input_course_code) or "—"],
            ["Submitted course name", clean_text_value(input_course_name) or "—"],
            ["Highest similarity", f"{score_to_percent(top_score):.2f}%"],
            ["Matches above alert level", str(int(above_threshold_count))],
            ["Alert level used in the system", f"{score_to_percent(threshold):.2f}%"],
        ],
        colWidths=[55 * mm, 115 * mm],
    )
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor(JAMK_SPINDLE)),
        ("BACKGROUND", (1, 0), (1, -1), colors.white),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor(TEXT_DARK)),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("LEADING", (0, 0), (-1, -1), 12),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(BORDER_SOFT)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))

    decision_title, decision_text = interpret_decision(top_score, threshold)
    story.append(Paragraph("Submitted course summary", section_style))

    for label, value in input_sections.items():
        cleaned = clean_text_value(value)
        if cleaned:
            story.append(Paragraph(label, label_style))
            story.append(Paragraph(
                cleaned.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
                body_style,
            ))

    story.append(Paragraph("Decision summary", section_style))
    story.append(Paragraph(f"<b>{decision_title}</b>", body_style))
    story.append(Paragraph(decision_text, body_style))

    story.append(Paragraph("Top matching existing courses", section_style))

    for idx, row in matches_df.iterrows():
        story.append(Paragraph(
            f"{idx + 1}. {clean_text_value(row['course_name'])} ({clean_text_value(row['course_unit_code'])})",
            label_style
        ))

        match_meta = Table(
            [[
                f"Similarity: {score_to_percent(float(row['similarity_score'])):.2f}%",
                "Above alert level" if int(row["overlap_flag"]) == 1 else "Below alert level",
                clean_text_value(row["interpretation"]),
            ]],
            colWidths=[42 * mm, 40 * mm, 83 * mm],
        )
        match_meta.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor(JAMK_SPINDLE)),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FDEEEE" if int(row["overlap_flag"]) == 1 else "#E8F2FB")),
            ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#F7E6F1")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor(TEXT_DARK)),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.8),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor(BORDER_SOFT)),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(match_meta)
        story.append(Spacer(1, 4))

        highlight_hex = HIGHLIGHT_ORANGE if int(row["overlap_flag"]) == 1 else HIGHLIGHT_BLUE

        detail_sections = [
            ("Objective", row.get("objective_text", "")),
            ("EUR-ACE Knowledge and Understanding", row.get("competences_knowledge_text", "")),
            ("EUR-ACE Engineering Practice", row.get("competences_practice_text", "")),
            ("Content", row.get("content_text", "")),
            ("Prerequisites", row.get("prerequisites_text", "")),
        ]

        for label, value in detail_sections:
            cleaned = clean_text_value(value)
            if cleaned:
                story.append(Paragraph(label, label_style))
                story.append(
                    Paragraph(
                        highlight_overlap_sentences_pdf(
                            cleaned,
                            query_text=query_text,
                            highlight_color_hex=highlight_hex,
                            min_overlap=2,
                        ),
                        body_style,
                    )
                )

        story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Orange highlight indicates overlap candidates above the threshold. Light blue highlight indicates lower-threshold related content. This report supports expert review and does not replace academic judgement.",
        note_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()


# ============================================================
# Data loading
# ============================================================

@st.cache_resource
def get_openai_client() -> Optional[OpenAI]:
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)


@st.cache_data
def load_courses_clean() -> pd.DataFrame:
    if not COURSES_CLEAN_PATH.exists():
        raise FileNotFoundError(
            f"Missing file: {COURSES_CLEAN_PATH}. Notebook 01 output is required."
        )

    df = pd.read_csv(COURSES_CLEAN_PATH, encoding="utf-8", keep_default_na=False).copy()

    required_columns = [
        "course_unit_code",
        "course_name",
        "objective_text",
        "competences_knowledge_text",
        "competences_practice_text",
        "content_text",
        "prerequisites_text",
    ]
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"courses_clean.csv is missing required columns: {missing}")

    return df

@st.cache_data
def load_final_recommendation() -> pd.DataFrame:
    if not FINAL_RECOMMENDATION_PATH.exists():
        raise FileNotFoundError(
            f"Missing file: {FINAL_RECOMMENDATION_PATH}. Run Notebook 04 first."
        )

    df = pd.read_csv(FINAL_RECOMMENDATION_PATH, encoding="utf-8", keep_default_na=False).copy()

    required_columns = [
        "recommendation_type",
        "model_name",
        "text_variant",
        "similarity_metric",
        "selection_rule",
        "locked_threshold",
    ]
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"final_threshold_recommendation.csv is missing required columns: {missing}")

    return df

@st.cache_data
def load_final_embeddings() -> pd.DataFrame:
    if not FINAL_EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(
            f"Missing file: {FINAL_EMBEDDINGS_PATH}. Run Notebook 05 first."
        )

    df = pd.read_parquet(FINAL_EMBEDDINGS_PATH).copy()

    required_columns = [
        "course_unit_code",
        "course_name",
        "final_embedding_text",
        "embedding_vector",
        "final_model_name",
        "final_text_variant",
        "final_similarity_metric",
        "final_selection_rule",
        "final_locked_threshold",
    ]
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"final_embeddings.parquet is missing required columns: {missing}")

    return df

def embedding_series_to_matrix(df: pd.DataFrame) -> np.ndarray:
    return np.array(df["embedding_vector"].tolist(), dtype=np.float32)

def quote_identifier(identifier: str) -> str:
    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError("SQL identifier must be a non-empty string.")
    return '"' + identifier.replace('"', '""') + '"'


def embedding_to_pgvector_text(vector) -> str:
    if isinstance(vector, np.ndarray):
        vector = vector.tolist()
    elif not isinstance(vector, list):
        vector = list(vector)

    return "[" + ",".join(str(float(x)) for x in vector) + "]"

def pgvector_search(
    query_embedding: np.ndarray,
    courses_clean_df: pd.DataFrame,
    threshold: float,
    limit: int = 10,
) -> pd.DataFrame:
    if not PGVECTOR_AVAILABLE:
        raise RuntimeError("psycopg is not installed, so pgvector mode cannot be used.")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured.")
    if not PGVECTOR_TABLE:
        raise RuntimeError("PGVECTOR_TABLE is not configured.")

    table_name_sql = quote_identifier(PGVECTOR_TABLE)
    query_vector_text = embedding_to_pgvector_text(query_embedding)

    sql = f"""
    SELECT
        course_unit_code,
        course_name,
        final_embedding_text,
        1 - (embedding_vector <=> %s::vector) AS similarity_score
    FROM {table_name_sql}
    ORDER BY embedding_vector <=> %s::vector
    LIMIT %s;
    """

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (query_vector_text, query_vector_text, limit))
            rows = cur.fetchall()

    result_df = pd.DataFrame(
        rows,
        columns=[
            "course_unit_code",
            "course_name",
            "final_embedding_text",
            "similarity_score",
        ],
    )

    structured_cols = [
        "course_unit_code",
        "objective_text",
        "competences_knowledge_text",
        "competences_practice_text",
        "content_text",
        "prerequisites_text",
    ]

    result_df = result_df.merge(
        courses_clean_df[structured_cols],
        on="course_unit_code",
        how="left",
    )

    result_df = result_df.sort_values("similarity_score", ascending=False).reset_index(drop=True)
    result_df["overlap_flag"] = (result_df["similarity_score"] >= threshold).astype(int)
    result_df["similarity_percent"] = result_df["similarity_score"].apply(score_to_percent)
    result_df["interpretation"] = result_df["similarity_score"].apply(lambda x: overlap_band(x, threshold))

    return result_df


def local_search(
    query_embedding: np.ndarray,
    embeddings_df: pd.DataFrame,
    courses_clean_df: pd.DataFrame,
    threshold: float,
    limit: int = 10,
) -> pd.DataFrame:
    matrix = embedding_series_to_matrix(embeddings_df)
    scores = matrix @ query_embedding

    result_df = embeddings_df[[
    "course_unit_code",
    "course_name",
    "final_embedding_text",
    ]].copy()
    result_df["similarity_score"] = scores

    structured_cols = [
        "course_unit_code",
        "objective_text",
        "competences_knowledge_text",
        "competences_practice_text",
        "content_text",
        "prerequisites_text",
    ]
    result_df = result_df.merge(
        courses_clean_df[structured_cols],
        on="course_unit_code",
        how="left",
    )

    result_df = result_df.sort_values("similarity_score", ascending=False).reset_index(drop=True)
    result_df["overlap_flag"] = (result_df["similarity_score"] >= threshold).astype(int)
    result_df["similarity_percent"] = result_df["similarity_score"].apply(score_to_percent)
    result_df["interpretation"] = result_df["similarity_score"].apply(lambda x: overlap_band(x, threshold))
    return result_df.head(limit).copy()


def embed_query_text(client: OpenAI, text: str) -> np.ndarray:
    response = client.embeddings.create(
        model=OPENAI_MODEL_NAME,
        input=[text],
    )
    vec = np.array(response.data[0].embedding, dtype=np.float32)
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("Received a zero-length embedding vector.")
    return vec / norm


# ============================================================
# Load system artifacts
# ============================================================

try:
    embeddings_df = load_final_embeddings()
    courses_clean_df = load_courses_clean()
    final_recommendation_df = load_final_recommendation()
    openai_client = get_openai_client()
except Exception as e:
    st.error(str(e))
    st.stop()

primary_recommendation_df = final_recommendation_df[
    final_recommendation_df["recommendation_type"] == "primary_recommendation"
].copy()

if primary_recommendation_df.empty:
    st.error("Could not find primary_recommendation in final_threshold_recommendation.csv.")
    st.stop()

primary_row = primary_recommendation_df.iloc[0]

FINAL_MODEL_NAME = str(primary_row["model_name"])
FINAL_TEXT_VARIANT = str(primary_row["text_variant"])
FINAL_SIMILARITY_METRIC = str(primary_row["similarity_metric"])
FINAL_SELECTION_RULE = str(primary_row["selection_rule"])
FINAL_LOCKED_THRESHOLD = float(primary_row["locked_threshold"])

if FINAL_MODEL_NAME != "openai_text-embedding-3-large":
    st.error(
        f"The primary recommendation uses {FINAL_MODEL_NAME}, "
        "but this app currently supports only OpenAI text-embedding-3-large."
    )
    st.stop()

artifact_model_names = set(embeddings_df["final_model_name"].astype(str).unique())
artifact_text_variants = set(embeddings_df["final_text_variant"].astype(str).unique())
artifact_similarity_metrics = set(embeddings_df["final_similarity_metric"].astype(str).unique())
artifact_selection_rules = set(embeddings_df["final_selection_rule"].astype(str).unique())

if artifact_model_names != {FINAL_MODEL_NAME}:
    st.error(
        f"Mismatch between final_embeddings.parquet and final_threshold_recommendation.csv. "
        f"Artifact model(s): {sorted(artifact_model_names)} | Recommendation: {FINAL_MODEL_NAME}"
    )
    st.stop()

if artifact_text_variants != {FINAL_TEXT_VARIANT}:
    st.error(
        f"Mismatch between final_embeddings.parquet and final_threshold_recommendation.csv. "
        f"Artifact text variant(s): {sorted(artifact_text_variants)} | Recommendation: {FINAL_TEXT_VARIANT}"
    )
    st.stop()

if artifact_similarity_metrics != {FINAL_SIMILARITY_METRIC}:
    st.error(
        f"Mismatch between final_embeddings.parquet and final_threshold_recommendation.csv. "
        f"Artifact similarity metric(s): {sorted(artifact_similarity_metrics)} | Recommendation: {FINAL_SIMILARITY_METRIC}"
    )
    st.stop()

if artifact_selection_rules != {FINAL_SELECTION_RULE}:
    st.error(
        f"Mismatch between final_embeddings.parquet and final_threshold_recommendation.csv. "
        f"Artifact selection rule(s): {sorted(artifact_selection_rules)} | Recommendation: {FINAL_SELECTION_RULE}"
    )
    st.stop()

if USE_PGVECTOR:
    if not PGVECTOR_AVAILABLE:
        st.error("USE_PGVECTOR=true, but psycopg is not installed.")
        st.stop()

    if not DATABASE_URL:
        st.error("USE_PGVECTOR=true, but DATABASE_URL is missing from the .env file.")
        st.stop()

    if not PGVECTOR_TABLE:
        st.error("USE_PGVECTOR=true, but PGVECTOR_TABLE is missing from the .env file.")
        st.stop()

    try:
        table_name_sql = quote_identifier(PGVECTOR_TABLE)

        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                    """,
                    (PGVECTOR_TABLE,),
                )
                existing_columns = {row[0] for row in cur.fetchall()}

        required_pgvector_columns = {
            "course_unit_code",
            "course_name",
            "final_embedding_text",
            "embedding_vector",
        }

        missing_pgvector_columns = required_pgvector_columns - existing_columns
        if missing_pgvector_columns:
            st.error(
                f"PGVECTOR_TABLE '{PGVECTOR_TABLE}' is missing required columns: "
                f"{sorted(missing_pgvector_columns)}"
            )
            st.stop()

    except Exception as e:
        st.error(f"Could not validate pgvector table '{PGVECTOR_TABLE}'. Details: {e}")
        st.stop()

if openai_client is None:
    st.error("OPENAI_API_KEY is missing. Add it to your `.env` file before running the app.")
    st.stop()

SYSTEM_BACKEND_LABEL = "pgvector live mode" if USE_PGVECTOR else "local parquet mode"
SYSTEM_ENGINE_LABEL = "OpenAI embeddings + pgvector" if USE_PGVECTOR else "OpenAI embeddings + local parquet"

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0 0.8rem; margin-bottom: 0.6rem;">
            <div class="panel-label">View options</div>
            <div class="workbench-title">Adjust the review display</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        top_k = st.slider("Number of matches to show", min_value=5, max_value=15, value=10, step=1)
        show_input_text = st.checkbox("Show submitted text used for comparison", value=False)


# ============================================================
# Sidebar helper panel
# ============================================================

with st.sidebar:
    process_preview_html = textwrap.dedent("""
<div class="glass-panel workspace-card">
<div class="panel-label">Process preview</div>
<div class="workbench-title">What happens next?</div>

<div class="explain-box">
<div class="explain-text">1. Understand your course</div>
<div class="explain-text">2. Check similarities</div>
<div class="explain-text">3. Highlight key points</div>
<div class="explain-text">4. Expert review</div>
</div>
</div>
    """)

    settings_html = textwrap.dedent(f"""
<div class="glass-panel workspace-card" style="margin-bottom:0;">
            <div class="panel-label">System settings</div>
            <div class="workbench-title">Current review settings</div>

<div class="settings-list">
                <div class="settings-row"><b>Alert level:</b> {score_to_percent(FINAL_LOCKED_THRESHOLD):.0f}%</div>
                <div class="settings-row"><b>Text representation:</b> {safe_html_text(FINAL_TEXT_VARIANT)}</div>
                <div class="settings-row"><b>Similarity metric:</b> {safe_html_text(FINAL_SIMILARITY_METRIC)}</div>
                <div class="settings-row"><b>Retrieval backend:</b> {safe_html_text(SYSTEM_BACKEND_LABEL)}</div>
                <div class="settings-row"><b>PDF report export:</b> {"Enabled" if PDF_AVAILABLE else "Not enabled"}</div>
            </div>
        </div>
    """)

    st.markdown(process_preview_html, unsafe_allow_html=True)
    st.markdown(settings_html, unsafe_allow_html=True)

# ============================================================
# Topbar and hero
# ============================================================

st.markdown(
    f"""
    <div class="topbar">
        <div class="brand">
            <div class="brand-mark">J</div>
            <div>
                <div class="brand-title">JAMK Course Similarity Review</div>
                <div class="brand-sub">Proof-of-concept for curriculum overlap detection</div>
            </div>
        </div>
        <div class="status-chip">Backend: {safe_html_text(SYSTEM_BACKEND_LABEL)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-grid">
            <div class="hero-title">
                <div class="hero-label">AI-assisted curriculum review workspace</div>
                <h1>Detect potential course overlap before it becomes a curriculum problem.</h1>
                <p>
                    Submit a proposed or revised course, compare it against the existing JAMK course set,
                    and review evidence-backed similarity findings through a lecturer-friendly interface.
                </p>
                <div class="hero-tags">
                    <span class="hero-tag">Curriculum review support</span>
                    <span class="hero-tag">Similarity-based</span>
                    <span class="hero-tag">Lecturer-friendly workflow</span>
                </div>
            </div>
            <div class="hero-side">
                <div class="hero-side-title">Current system state</div>
                <div class="hero-side-value">Ready for review</div>
                <div class="hero-side-text">
                    Dataset loaded, similarity engine available, and report export enabled for academic review sessions.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(
        f"""
        <div class="mini-stat">
            <div class="mini-stat-label">JAMK ICT course set</div>
            <div class="mini-stat-value">{len(embeddings_df)} courses</div>
            <div class="mini-stat-sub">Available in the current similarity review dataset</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        f"""
        <div class="mini-stat">
            <div class="mini-stat-label">Current alert level</div>
            <div class="mini-stat-value">{score_to_percent(FINAL_LOCKED_THRESHOLD):.0f}%</div>
            <div class="mini-stat-sub">Courses at or above this similarity are flagged for overlap review</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f"""
        <div class="mini-stat">
            <div class="mini-stat-label">Analysis engine</div>
            <div class="mini-stat-value">{safe_html_text(SYSTEM_ENGINE_LABEL)}</div>
            <div class="mini-stat-sub">{safe_html_text(FINAL_MODEL_NAME)} | {safe_html_text(FINAL_TEXT_VARIANT)} | {safe_html_text(FINAL_SIMILARITY_METRIC)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")


# ============================================================
# Main workspace
# ============================================================
st.markdown('<div class="section-kicker">Input</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">New course form</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Enter the proposed course details below. Use one statement per line for the clearest comparison text.</div>',
    unsafe_allow_html=True,
)

with st.form("course_form", clear_on_submit=False):
    top_left, top_right = st.columns([0.34, 0.66])
    with top_left:
        course_code = st.text_input("Course code", placeholder="e.g. TT00NEW1")
    with top_right:
        course_name = st.text_input("Course name *", placeholder="e.g. Applied AI Systems")

    objective_textarea = st.text_area(
        "Objective *",
        height=165,
        placeholder="Write one objective statement per line",
    )
    content_textarea = st.text_area(
        "Content *",
        height=185,
        placeholder="Write one content statement per line",
    )

    learning_outcomes_textarea = st.text_area(
        "Learning outcomes",
        height=120,
        placeholder="Optional, one item per line",
    )
    prerequisites_textarea = st.text_area(
        "Prerequisites",
        height=85,
        placeholder="Optional, one prerequisite per line",
    )

    st.markdown(
        '<div class="section-kicker" style="margin-top:0.5rem;">Competences</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-title" style="font-size:1rem; margin-bottom:0.75rem;">EUR-ACE competence fields</div>',
        unsafe_allow_html=True,
    )

    ec1, ec2 = st.columns(2)

    with ec1:
        knowledge_textarea = st.text_area(
            "Knowledge and understanding",
            height=120,
            placeholder="Optional, one item per line",
        )
        applying_textarea = st.text_area(
            "Applying technology to practice",
            height=100,
            placeholder="Optional, one item per line",
        )
        communication_textarea = st.text_area(
            "Communication and teamwork",
            height=100,
            placeholder="Optional, one item per line",
        )

    with ec2:
        practice_textarea = st.text_area(
            "Engineering practice",
            height=120,
            placeholder="Optional, one item per line",
        )
        multidisciplinary_textarea = st.text_area(
            "Multidisciplinary competence",
            height=100,
            placeholder="Optional, one item per line",
        )
        investigations_textarea = st.text_area(
            "Investigations and information retrieval",
            height=100,
            placeholder="Optional, one item per line",
        )


    bottom_left, bottom_right = st.columns([0.67, 0.33], gap="medium")

    with bottom_left:
        st.markdown(
            """
            <div class="shell-card" style="margin-bottom:0;">
                <div class="section-sub" style="margin-bottom:0; font-weight:700;">
                    READY! Start a new curriculum review session...
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with bottom_right:
        submitted = st.form_submit_button("Run similarity review", width="stretch")
    

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# Run similarity check
# ============================================================

if submitted:
    if not clean_text_value(course_name):
        st.error("Course name is required.")
        st.stop()

    if not clean_text_value(objective_textarea):
        st.error("Objective is required.")
        st.stop()

    if not clean_text_value(content_textarea):
        st.error("Content is required.")
        st.stop()

    objective_items = split_multiline_to_list(objective_textarea)
    content_items = split_multiline_to_list(content_textarea)
    knowledge_items = split_multiline_to_list(knowledge_textarea)
    practice_items = split_multiline_to_list(practice_textarea)
    applying_items = split_multiline_to_list(applying_textarea)
    multidisciplinary_items = split_multiline_to_list(multidisciplinary_textarea)
    communication_items = split_multiline_to_list(communication_textarea)
    investigations_items = split_multiline_to_list(investigations_textarea)
    learning_outcomes_items = split_multiline_to_list(learning_outcomes_textarea)
    prerequisites_items = split_multiline_to_list(prerequisites_textarea)

    final_query_text = build_embedding_text_enriched_from_form(
        course_name=course_name,
        objective_items=objective_items,
        knowledge_items=knowledge_items,
        practice_items=practice_items,
        applying_items=applying_items,
        multidisciplinary_items=multidisciplinary_items,
        communication_items=communication_items,
        investigations_items=investigations_items,
        learning_outcomes_items=learning_outcomes_items,
        content_items=content_items,
        prerequisites_items=prerequisites_items,
    )

    with st.spinner("Reviewing course similarity..."):
        query_embedding = embed_query_text(openai_client, final_query_text)

        search_backend_used = "local parquet fallback"

        if USE_PGVECTOR and DATABASE_URL and PGVECTOR_AVAILABLE:
            try:
                matches_df = pgvector_search(
                    query_embedding=query_embedding,
                    courses_clean_df=courses_clean_df,
                    threshold=FINAL_LOCKED_THRESHOLD,
                    limit=top_k,
                )
                search_backend_used = "pgvector"
            except Exception as e:
                st.warning(
                    f"pgvector search was unavailable, so the app used local fallback search instead. Details: {e}"
                )
                matches_df = local_search(
                    query_embedding=query_embedding,
                    embeddings_df=embeddings_df,
                    courses_clean_df=courses_clean_df,
                    threshold=FINAL_LOCKED_THRESHOLD,
                    limit=top_k,
                )
                search_backend_used = "local parquet fallback"
        else:
            matches_df = local_search(
                query_embedding=query_embedding,
                embeddings_df=embeddings_df,
                courses_clean_df=courses_clean_df,
                threshold=FINAL_LOCKED_THRESHOLD,
                limit=top_k,
            )
            search_backend_used = "local parquet fallback"
            
    st.caption(f"Backend used for this review: {search_backend_used}.")

    top_score = float(matches_df.iloc[0]["similarity_score"])
    above_threshold_count = int(matches_df["overlap_flag"].sum())
    top_match_name = matches_df.iloc[0]["course_name"]
    top_match_code = matches_df.iloc[0]["course_unit_code"]
    top_match_row = matches_df.iloc[0]

    decision_title, decision_text = interpret_decision(top_score, FINAL_LOCKED_THRESHOLD)

    if top_score >= FINAL_LOCKED_THRESHOLD:
        summary_class = "bad"
    elif top_score >= FINAL_LOCKED_THRESHOLD - 0.05:
        summary_class = "mid"
    else:
        summary_class = "good"

    input_sections = {
        "Objective": join_list_field(objective_items, separator=" "),
        "EUR-ACE Knowledge and Understanding": join_list_field(knowledge_items, separator=" "),
        "EUR-ACE Engineering Practice": join_list_field(practice_items, separator=" "),
        "Content": join_list_field(content_items, separator=" "),
        "Prerequisites": join_list_field(prerequisites_items, separator=", "),
    }

    report_df = generate_report_dataframe(
        input_course_name=course_name,
        input_course_code=course_code,
        threshold=FINAL_LOCKED_THRESHOLD,
        text_variant=FINAL_TEXT_VARIANT,
        model_name=FINAL_MODEL_NAME,
        matches_df=matches_df,
    )

    pdf_bytes = b""
    pdf_export_error = None
    pdf_download_disabled = False

    if PDF_AVAILABLE:
        try:
            pdf_bytes = create_similarity_pdf_bytes(
                input_course_code=course_code,
                input_course_name=course_name,
                input_sections=input_sections,
                top_score=top_score,
                above_threshold_count=above_threshold_count,
                threshold=FINAL_LOCKED_THRESHOLD,
                matches_df=matches_df,
                query_text=final_query_text,
            )
        except Exception as e:
            pdf_export_error = str(e)
            pdf_download_disabled = True
    else:
        pdf_export_error = "PDF export is not available because reportlab is not installed."
        pdf_download_disabled = True

    st.markdown("<div class='section-heading' style='margin-top:2.5rem;'>Similarity check</div>", unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3, gap="medium")

    with r1:
        st.markdown('<div class="section-kicker">Top score</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Similarity percentage</div>', unsafe_allow_html=True)

        ring_fig = make_ring_figure(
            score_percent=score_to_percent(top_score),
            threshold_percent=score_to_percent(FINAL_LOCKED_THRESHOLD),
        )
        if ring_fig is not None:
            st.plotly_chart(ring_fig, width="stretch", config={"displayModeBar": False})
        else:
            st.markdown(
                f"<div class='result-stat'>{score_to_percent(top_score):.2f}%</div>",
                unsafe_allow_html=True,
            )

    with r2:
        st.markdown('<div class="section-kicker">Review status</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Overlap courses</div>', unsafe_allow_html=True)
        st.markdown(f"<div class='result-stat'>{above_threshold_count}</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="section-sub">
                Existing courses currently above the alert level of
                <strong>{score_to_percent(FINAL_LOCKED_THRESHOLD):.0f}%</strong>.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="decision-banner {summary_class}">
                <strong>{safe_html_text(decision_title)}</strong><br>{safe_html_text(decision_text)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with r3:
        st.markdown('<div class="section-kicker">Report</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Similarity check report</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-sub" style="margin-bottom:0.8rem;">
            Download a single PDF report containing the submitted course summary, the strongest similarity matches,
            highlighted evidence from the comparison, and a clear overview to support expert review and
            curriculum planning decisions.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            label="Download similarity report",
            data=pdf_bytes,
            file_name=f"{make_safe_filename(course_code or course_name)}_similarity_report.pdf",
            mime="application/pdf",
            width="stretch",
            disabled=pdf_download_disabled,
        )

        if pdf_export_error:
            st.caption(pdf_export_error)

    g1, g2 = st.columns([1.2, 0.8], gap="medium")

    with g1:
        st.markdown('<div class="section-kicker" style="margin-top:3rem;">Graph</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Top candidate match distribution</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-sub" style="margin-bottom:2.5rem;">The submitted course is compared against the strongest existing matches in the review set.</div>',
            unsafe_allow_html=True,
        )
        dist_fig = make_distribution_chart(
            matches_df=matches_df,
            threshold_percent=score_to_percent(FINAL_LOCKED_THRESHOLD),
        )
        if dist_fig is not None:
            st.plotly_chart(dist_fig, width="stretch", config={"displayModeBar": False})
        else:
            st.error(f"Plotly could not be loaded: {PLOTLY_IMPORT_ERROR or 'Unknown import error'}")

    with g2:
        st.markdown('<div class="section-kicker" style="margin-top:3rem;">Interpretation</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">How to read the score</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="helper-box" style="margin-bottom:0.8rem;">
                <h4>Above {score_to_percent(FINAL_LOCKED_THRESHOLD):.0f}%</h4>
                <p>Meaningful overlap candidate. This should normally be reviewed carefully by curriculum experts.</p>
            </div>
            <div class="helper-box" style="margin-bottom:0.8rem;">
                <h4>Within 5 percentage points below threshold</h4>
                <p>Related content may exist. Human review is still recommended when course aims are close.</p>
            </div>
            <div class="helper-box" style="margin-bottom:0;">
                <h4>Clearly below threshold</h4>
                <p>Lower overlap likelihood. The new course is less likely to conflict with the current course set.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-heading' style='margin-top:3rem;'>Course comparison workspace</div>", unsafe_allow_html=True)

    c_left, c_right = st.columns(2, gap="medium")

    with c_left:
        st.markdown('<div class="section-kicker">New Course</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="course-name">{safe_html_text(course_name)}</div>
            <div class="course-code">{safe_html_text(course_code or "New course draft")}</div>
            """,
            unsafe_allow_html=True,
        )

        course_a_sections = [
            ("Objective", input_sections.get("Objective", "")),
            ("EUR-ACE Knowledge and Understanding", input_sections.get("EUR-ACE Knowledge and Understanding", "")),
            ("EUR-ACE Engineering Practice", input_sections.get("EUR-ACE Engineering Practice", "")),
            ("Content", input_sections.get("Content", "")),
            ("Prerequisites", input_sections.get("Prerequisites", "")),
        ]
        for label, value in course_a_sections:
            cleaned = clean_text_value(value)
            if cleaned:
                st.markdown(
                    f"""
                    <div style="margin-bottom:0.95rem;">
                        <div style="font-weight:800; color:{DEEP_NAVY}; margin-bottom:0.18rem; font-size:0.95rem;">{safe_html_text(label)}</div>
                        <div style="line-height:1.72; color:{TEXT_DARK}; font-size:0.96rem;">{safe_html_text(cleaned)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with c_right:
        if above_threshold_count > 0:
            st.markdown('<div class="section-kicker">Similar Existing Course</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="course-name">{safe_html_text(top_match_name)}</div>
                <div class="course-code">{safe_html_text(top_match_code)}</div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                build_structured_match_view(top_match_row, query_text=final_query_text),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="surface-card">
                    <div class="section-kicker">Review note</div>
                    <div class="section-title">No overlap course detected above threshold</div>
                    <div class="compare-note">
                        <strong>Good news.</strong><br><br>
                        The submitted course did not produce any overlap candidates above the current alert level of
                        <strong>{score_to_percent(FINAL_LOCKED_THRESHOLD):.0f}%</strong>.
                        <br><br>
                        You can continue curriculum planning with greater confidence, while still using the lower-ranked matches
                        below as optional review support.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if show_input_text:
        with st.expander("Show submitted text used for comparison", expanded=False):
            st.write(final_query_text)

    st.markdown("<div class='section-heading' style='margin-top:3rem;'>Closest existing courses</div>", unsafe_allow_html=True)

    for _, row in matches_df.iterrows():
        status_text = "Flagged for review" if int(row["overlap_flag"]) == 1 else "Not flagged"
        interpretation_class = get_interpretation_pill_class(row["interpretation"])
        status_class = "bad" if int(row["overlap_flag"]) == 1 else "mid" if row["interpretation"] == "Related but below alert level" else "good"
        score_percent = score_to_percent(float(row["similarity_score"]))

        expander_title = (
            f"{row['course_unit_code']} | {row['course_name']} — {score_percent:.2f}% — {status_text}"
        )

        with st.expander(expander_title, expanded=False):
            st.markdown(
                f"""
                <div class="course-card">
                    <div class="course-name">{safe_html_text(row['course_name'])}</div>
                    <div class="course-code">{safe_html_text(row['course_unit_code'])}</div>
                    <div class="pill-row">
                        <span class="pill score">Similarity: {score_percent:.2f}%</span>
                        <span class="pill {status_class}">{safe_html_text(status_text)}</span>
                        <span class="pill {interpretation_class}">{safe_html_text(row['interpretation'])}</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" style="width:{score_percent}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("**Course details**")
            st.markdown(
                build_structured_match_view(row, query_text=final_query_text),
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-heading' style='margin-top:3rem;'>Report preview</div>", unsafe_allow_html=True)
    st.dataframe(
        report_df[
            [
                "matched_course_unit_code",
                "matched_course_name",
                "similarity_score",
                "similarity_percent",
                "overlap_flag",
                "interpretation",
            ]
        ],
        width="stretch",
        hide_index=True,
    )

    st.markdown(
        """
        <div class="review-note">
            Orange highlight indicates overlap candidates above the threshold. Light blue highlight indicates lower-threshold related content.
            Final curriculum decisions should still be made through expert academic review.
        </div>
        """,
        unsafe_allow_html=True,
    )