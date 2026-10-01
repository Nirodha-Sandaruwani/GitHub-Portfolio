import json
import requests
import streamlit as st

# =========================================================
# App configuration
# =========================================================
API_BASE = "http://127.0.0.1:8000"
DEFAULTS_PATH = "ui_defaults.json"
MAPE = 0.0686  # ~6.86%

st.set_page_config(
    page_title="Used Car Price Predictor",
    page_icon="💲",
    layout="wide",
)

# =========================================================
# UI Engineer – Website-grade Styling
# =========================================================
st.markdown(
    """
    <style>
    /* ---------- Page container ---------- */
    .block-container {
        max-width: 1320px;
        padding-top: 3.8rem;
        padding-bottom: 2rem;
    }

    /* ---------- Typography ---------- */
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        color: #F8FAFC;
        letter-spacing: 0.02em;
    }

    .price {
        font-size: 3.4rem;
        font-weight: 800;
        color: #3B82F6; /* Premium blue */
        margin: 1rem 0 0.3rem 0;
        letter-spacing: -0.03em;
    }

    .range {
        font-size: 0.95rem;
        color: #CBD5E1;
        margin-bottom: 1rem;
    }

    .hint {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-top: 1.2rem;
    }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        background: linear-gradient(135deg, #7C2D12, #EA580C);
        color: #FFF7ED;
        border-radius: 16px;
        padding: 0.7rem 1.6rem;
        font-weight: 700;
        font-size: 1.05rem;
        border: none;
        margin-top: -0.3rem;
        box-shadow: 0 8px 24px rgba(234,88,12,0.35);
        transition: all 0.25s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #9A3412, #FB923C);
        transform: translateY(-1px);
        box-shadow: 0 12px 30px rgba(251,146,60,0.45);
        color: #FFF7ED;
    }

    /* ---------- Divider ---------- */
    .soft-divider {
        height: 1px;
        background: linear-gradient(
            to right,
            transparent,
            #7C2D12,
            #1E3A8A,
            transparent
        );
        margin: 1rem 0;
    }

    /* ---------- Expanders ---------- */
    details > summary {
        padding: 0.4rem 0;
        color: #F1F5F9;
        font-weight: 600;
    }

    /* ---------- Tabs (Luxury Nav Bar) ---------- */
    div[data-testid="stTabs"] {
        margin-top: 0.5rem;
    }

    button[role="tab"] {
    background: rgba(255,255,255,0.04);          /* neutral glass */
    border: 1px solid rgba(203,213,225,0.22);
    padding: 0.6rem 1.3rem;
    margin-right: 0.4rem;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.95rem;
    color: #FFF7ED;
    transition: all 0.2s ease;
    margin-bottom: 0.5rem !important;
}

button[role="tab"]:hover {
    background: rgba(255,255,255,0.07);          /* slight lift only */
    color: #FFF7ED;
    border-color: rgba(203,213,225,0.35);
}

    div.stButton > button:hover {
    color: #FFF7ED;
}

/*ACTIVE TAB — WARM INNER ORANGE */
button[aria-selected="true"] {
    background:
        linear-gradient(
            180deg,
            rgba(255,237,213,0.38),   /* strong inner orange */
            rgba(255,237,213,0.22)
        ),
        rgba(255,255,255,0.06) !important;
    color: #FFFFFF !important;
    border-color: rgba(234,88,12,0.55);
}
/* ---------- Inputs ---------- */
    input, select, textarea {
        background-color: #020617 !important;
        color: #F8FAFC !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        height: 38px;       
        padding: 0 12px;           
        font-size: 0.95rem;     
        line-height: 38px;      
    }

    label {
        color: #CBD5E1 !important;
        font-weight: 500;
    }

    /* ===== HERO BACKGROUND FOR HEADER + TABS ===== */
.block-container::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 295px; /* controls how far background goes */
    background:
        linear-gradient(
            to bottom,
            rgba(2,6,23,0.75),
            rgba(2,6,23,0.9)
        ),
        url("https://images.unsplash.com/photo-1503376780353-7e6692767b70");
    background-size: cover;
    background-position: center;
    z-index: -1;
}

/* Ensure content stays above background */
.block-container {
    position: relative;
    z-index: 1;
}

/* ===== STREAMLIT SELECTBOX DROPDOWN MENU ===== */

/* Dropdown options */
li[role="option"] {
    background-color: #E5E7EB !important;
    color: #020617 !important;
}

/* Selected option */
li[aria-selected="true"] {
    background-color: #1B2A41 !important;
    color: #F1F5F9 !important;
}  
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# API helpers
# =========================================================
@st.cache_data(show_spinner=False)
def get_codes():
    r = requests.get(f"{API_BASE}/codes", timeout=10)
    r.raise_for_status()
    return r.json()

@st.cache_data(show_spinner=False)
def get_health():
    r = requests.get(f"{API_BASE}/health", timeout=10)
    r.raise_for_status()
    return r.json()

def load_defaults():
    try:
        with open(DEFAULTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "year": 2020,
            "combined_fuel_economy": 25.0,
            "mileage": 4432.0,
            "horsepower": 228.0,
            "torque": 265.21883948671586,
            "legroom": 80.16630453611096,
            "maximum_seating": 5,
            "size_of_vehicle": 457.9,
            "major_options_count": 6.0,
            "has_incidents": 0,
            "fuel_type": "Flex Fuel Vehicle",
            "transmission": "M",
            "body_type": "Wagon",
            "engine_type": "I4 Compressed Natural Gas",
            "wheel_system": "4WD",
        }

defaults = load_defaults()

# =========================================================
# Sidebar — system status
# =========================================================
st.sidebar.markdown("## 🔌 System Status")
try:
    health = get_health()
    st.sidebar.success("API online")
    st.sidebar.caption(f"Features used: {health.get('n_features')}")
    st.sidebar.caption(f"Log target: {health.get('log_target')}")
except Exception as e:
    st.sidebar.error("API not reachable")
    st.sidebar.code(str(e))
    st.stop()

codes = get_codes()

# =========================================================
# Header
# =========================================================
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:0.6rem;">
        <span style="font-size:2.3rem;font-weight:800;color:#F8FAFC;">
            Used Car Price Prediction
        </span>
    </div>
    <div style="font-size:0.95rem;color:#94A3B8;margin-bottom:0.8rem;">
        Luxury ML Deployment · Streamlit → FastAPI → Random Forest
    </div>
    
    """,
    unsafe_allow_html=True,
)


tab1, tab2, tab3 = st.tabs([" Predict", " Payload", " Notes"])

# =========================================================
# Helpers
# =========================================================
def idx(options, value):
    try:
        return options.index(value)
    except Exception:
        return 0

def build_payload():
    return {
        "year": int(st.session_state["year"]),
        "combined_fuel_economy": float(st.session_state["combined_fuel_economy"]),
        "mileage": float(st.session_state["mileage"]),
        "horsepower": float(st.session_state["horsepower"]),
        "torque": float(st.session_state["torque"]),
        "legroom": float(st.session_state["legroom"]),
        "maximum_seating": int(st.session_state["maximum_seating"]),
        "size_of_vehicle": float(st.session_state["size_of_vehicle"]),
        "major_options_count": float(st.session_state["major_options_count"]),
        "has_incidents": int(st.session_state["has_incidents"]),
        "fuel_type": st.session_state["fuel_type"],
        "transmission": st.session_state["transmission"],
        "body_type": st.session_state["body_type"],
        "engine_type": st.session_state["engine_type"],
        "wheel_system": st.session_state["wheel_system"],
    }

def call_predict(payload):
    r = requests.post(f"{API_BASE}/predict", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

# =========================================================
# TAB 1 — Prediction
# =========================================================
with tab1:
    left, spacer, right = st.columns([1.55, 0.08, 1])

    # ---------- Inputs ----------
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Vehicle Information</div>', unsafe_allow_html=True)
        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

        with st.expander("📌 Paste JSON payload to auto-fill"):
            json_text = st.text_area(
                "Paste payload JSON here",
                value=json.dumps(defaults, indent=2),
                height=200,
            )
            if st.button("Load JSON into form"):
                try:
                    for k, v in json.loads(json_text).items():
                        st.session_state[k] = v
                    st.success("Loaded JSON into form")
                    st.rerun()
                except Exception as e:
                    st.error(f"Invalid JSON: {e}")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input("Year", 1980, 2026, int(defaults["year"]), key="year")
        with c2:
            st.number_input("Mileage", 0.0, value=float(defaults["mileage"]), step=500.0, key="mileage")
        with c3:
            st.number_input("Combined fuel economy", 0.0, value=float(defaults["combined_fuel_economy"]), step=0.5, key="combined_fuel_economy")

        c4, c5, c6 = st.columns(3)
        with c4:
            st.selectbox("Fuel type", codes["fuel_type"], index=idx(codes["fuel_type"], defaults["fuel_type"]), key="fuel_type")
        with c5:
            st.selectbox("Transmission", codes["transmission"], index=idx(codes["transmission"], defaults["transmission"]), key="transmission")
        with c6:
            st.selectbox("Wheel system", codes["wheel_system"], index=idx(codes["wheel_system"], defaults["wheel_system"]), key="wheel_system")

        c7, c8, c9 = st.columns(3)
        with c7:
            st.selectbox("Body type", codes["body_type"], index=idx(codes["body_type"], defaults["body_type"]), key="body_type")
        with c8:
            st.selectbox("Engine type", codes["engine_type"], index=idx(codes["engine_type"], defaults["engine_type"]), key="engine_type")
        with c9:
            st.selectbox("Has incidents (0/1)", codes["has_incidents"], index=0, key="has_incidents")

        with st.expander("Advanced numeric features (optional)"):
            a1, a2, a3 = st.columns(3)
            with a1:
                st.number_input("Horsepower", 0.0, value=float(defaults["horsepower"]), step=5.0, key="horsepower")
            with a2:
                st.number_input("Torque", 0.0, value=float(defaults["torque"]), step=5.0, key="torque")
            with a3:
                st.number_input("Legroom", 0.0, value=float(defaults["legroom"]), step=0.5, key="legroom")

            b1, b2, b3 = st.columns(3)
            with b1:
                st.number_input("Maximum seating", 1, 10, int(defaults["maximum_seating"]), key="maximum_seating")
            with b2:
                st.number_input("Size of vehicle", 0.0, value=float(defaults["size_of_vehicle"]), step=1.0, key="size_of_vehicle")
            with b3:
                st.number_input("Major options count", 0.0, value=float(defaults["major_options_count"]), step=1.0, key="major_options_count")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Result ----------
    with right:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("### Estimated Market Value")
      

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        if st.button("🚀 Predict price", use_container_width=True):
            out = call_predict(build_payload())
            pred = float(out["predicted_price"])
            low = pred * (1 - MAPE)
            high = pred * (1 + MAPE)

            st.markdown(f'<div class="price">${pred:,.0f}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="range">Expected range (±{MAPE*100:.2f}%): '
                f'${low:,.0f} – ${high:,.0f}</div>',
                unsafe_allow_html=True,
            )

            with st.expander("API response details"):
                st.json(out)
        else:
            st.markdown('<div class="hint">Enter details and click Predict.</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2 — Payload
# =========================================================
with tab2:
    st.markdown("### Payload sent to the prediction API")
    st.json(build_payload())

# =========================================================
# TAB 3 — Notes
# =========================================================
with tab3:
    st.markdown(
        """
        **Why some inputs look non-intuitive?**  
        The model relies on engineered features.

        **Demo purpose**  
        End-to-end ML deployment demonstration (model → API → UI).
        """
    )
