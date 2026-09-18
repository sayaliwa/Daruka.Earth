import json
import html
import requests
import pandas as pd
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Darukaa.Earth | Biodiversity Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# BACKEND CONFIGURATION
# =========================================================

BACKEND_URL = "http://127.0.0.1:8000"


# =========================================================
# SESSION STATE
# =========================================================

if "assessment" not in st.session_state:
    st.session_state["assessment"] = None

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

if "chat_session_id" not in st.session_state:
    st.session_state["chat_session_id"] = None

if "last_payload" not in st.session_state:
    st.session_state["last_payload"] = None


# =========================================================
# HELPERS
# =========================================================

def safe(value):
    """Safely display dynamic text inside custom HTML."""
    return html.escape(str(value))


def pretty_name(value):
    return str(value).replace("_", " ").replace("-", " ").title()


def format_horizon(value):
    return pretty_name(value)


def backend_health():
    try:
        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=3,
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def send_assessment(payload):
    return requests.post(
        f"{BACKEND_URL}/assess/",
        json=payload,
        timeout=180,
    )


def send_chat(message, location_id):
    payload = {
        "message": message,
        "location_id": location_id,
    }

    if st.session_state["chat_session_id"] is not None:
        payload["session_id"] = st.session_state["chat_session_id"]

    return requests.post(
        f"{BACKEND_URL}/chat/",
        json=payload,
        timeout=180,
    )


def render_metric_card(label, value, status=None, icon="•"):
    status_html = ""
    if status:
        status_html = (
            f'<div class="metric-status">'
            f'<span class="status-dot"></span>{safe(pretty_name(status))}'
            f"</div>"
        )

    st.html(
        f"""
<div class="metric-card">
    <div class="metric-icon">{icon}</div>
    <div class="metric-label">{safe(label)}</div>
    <div class="metric-value">{safe(value)}</div>
    {status_html}
</div>
""",
    )


def render_tag(text, class_name="tag"):
    st.html(
        f'<span class="{class_name}">{safe(pretty_name(text))}</span>',
    )


# =========================================================
# CUSTOM CSS
# =========================================================

st.html(
    """
<style>

/* ---------- GLOBAL ---------- */

.main {
    padding-top: 0.8rem;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at 15% 5%,
            rgba(62, 140, 93, 0.10),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 20%,
            rgba(47, 120, 90, 0.08),
            transparent 28%
        );
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.18);
}

/* ---------- HERO ---------- */

.hero {
    padding: 2.4rem 2.6rem;
    border-radius: 24px;
    border: 1px solid rgba(128,128,128,0.22);
    background:
        linear-gradient(
            135deg,
            rgba(55, 120, 80, 0.18),
            rgba(30, 40, 35, 0.12)
        );
    box-shadow: 0 18px 45px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}

.hero-kicker {
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.65;
    margin-bottom: 0.7rem;
}

.hero-title {
    font-size: 3rem;
    line-height: 1.05;
    font-weight: 800;
    margin-bottom: 0.45rem;
}

.hero-subtitle {
    font-size: 1.25rem;
    font-weight: 600;
    opacity: 0.82;
    margin-bottom: 1rem;
}

.hero-description {
    max-width: 900px;
    font-size: 1rem;
    line-height: 1.75;
    opacity: 0.78;
}

.hero-pills {
    margin-top: 1.4rem;
}

/* ---------- PIPELINE ---------- */

.pipeline-card {
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.20);
    text-align: center;
    min-height: 105px;
    background: rgba(128,128,128,0.035);
}

.pipeline-icon {
    font-size: 1.5rem;
    margin-bottom: 0.35rem;
}

.pipeline-title {
    font-weight: 700;
    font-size: 0.9rem;
}

.pipeline-subtitle {
    font-size: 0.72rem;
    opacity: 0.62;
    margin-top: 0.25rem;
}

/* ---------- SECTION TITLES ---------- */

.section-title {
    font-size: 1.55rem;
    font-weight: 750;
    margin-top: 0.5rem;
    margin-bottom: 0.9rem;
}

.section-caption {
    opacity: 0.68;
    margin-top: -0.4rem;
    margin-bottom: 1rem;
}

/* ---------- METRIC CARDS ---------- */

.metric-card {
    padding: 1.15rem;
    border-radius: 17px;
    border: 1px solid rgba(128,128,128,0.20);
    min-height: 135px;
    background: rgba(128,128,128,0.035);
    transition: transform 0.15s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
}

.metric-icon {
    font-size: 1.15rem;
    margin-bottom: 0.35rem;
}

.metric-label {
    font-size: 0.78rem;
    opacity: 0.62;
    margin-bottom: 0.35rem;
}

.metric-value {
    font-size: 1.48rem;
    font-weight: 760;
    word-break: break-word;
}

.metric-status {
    margin-top: 0.5rem;
    font-size: 0.76rem;
    opacity: 0.72;
}

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: currentColor;
    margin-right: 0.4rem;
}

/* ---------- RECOMMENDATIONS ---------- */

.recommendation-card {
    padding: 1.25rem 1.35rem;
    border-radius: 17px;
    border: 1px solid rgba(128,128,128,0.22);
    margin-bottom: 0.9rem;
    background:
        linear-gradient(
            135deg,
            rgba(70, 140, 90, 0.09),
            rgba(128,128,128,0.025)
        );
}

.recommendation-number {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    opacity: 0.58;
    margin-bottom: 0.3rem;
}

.recommendation-title {
    font-size: 1.05rem;
    font-weight: 720;
    line-height: 1.5;
}

/* ---------- DETAIL CARDS ---------- */

.detail-card {
    padding: 1.15rem;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.20);
    margin-bottom: 0.8rem;
}

.detail-label {
    font-size: 0.74rem;
    opacity: 0.58;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

.detail-value {
    font-weight: 650;
    margin-top: 0.2rem;
}

/* ---------- TAGS ---------- */

.tag {
    display: inline-block;
    padding: 0.28rem 0.65rem;
    border-radius: 999px;
    border: 1px solid rgba(128,128,128,0.28);
    font-size: 0.76rem;
    margin-right: 0.35rem;
    margin-bottom: 0.35rem;
}

.tag-accent {
    display: inline-block;
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    background: rgba(70, 150, 100, 0.12);
    border: 1px solid rgba(70, 150, 100, 0.28);
    font-size: 0.76rem;
    margin-right: 0.35rem;
    margin-bottom: 0.35rem;
}

/* ---------- EVIDENCE ---------- */

.evidence-card {
    padding: 1.1rem;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.20);
    margin-bottom: 0.8rem;
}

.evidence-source {
    font-size: 0.9rem;
    font-weight: 700;
}

.evidence-meta {
    font-size: 0.76rem;
    opacity: 0.62;
    margin-top: 0.3rem;
}

/* ---------- INFO BANNER ---------- */

.info-banner {
    padding: 0.95rem 1.1rem;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.18);
    background: rgba(128,128,128,0.035);
    margin-bottom: 1rem;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    opacity: 0.48;
    padding: 2.5rem 0 1rem 0;
    font-size: 0.78rem;
}

/* ---------- MOBILE ---------- */

@media (max-width: 800px) {
    .hero {
        padding: 1.5rem;
    }

    .hero-title {
        font-size: 2.1rem;
    }
}

</style>
""",
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🌿 Darukaa.Earth")
    st.caption("AI Biodiversity Intelligence Engine")

    st.divider()

    # Backend status
    st.markdown("### ⚡ System Status")

    if backend_health():
        st.success("FastAPI backend connected")
    else:
        st.error("FastAPI backend offline")

    st.caption(f"Backend: `{BACKEND_URL}`")

    st.divider()

    st.markdown("### 🧠 Intelligence Pipeline")

    pipeline_items = [
        "Input",
        "Environmental State",
        "Multi-Metric Reasoning",
        "Scientific RAG",
        "AI Explanation",
        "Actionable Recommendation",
    ]

    for index, item in enumerate(pipeline_items, start=1):
        st.markdown(f"**{index}.** {item}")
        if index < len(pipeline_items):
            st.caption("↓")

    st.divider()

    st.markdown("### 📊 Metrics Covered")

    metrics = [
        "Soil pH",
        "Soil organic carbon",
        "Soil moisture",
        "Temperature",
        "Rainfall",
        "Land use",
        "Tree cover",
        "Species richness",
        "Habitat diversity",
        "Pollution",
        "Deforestation",
    ]

    for metric in metrics:
        st.markdown(f"• {metric}")

    st.divider()

    st.markdown("### 📚 Knowledge Sources")
    st.html(
        """
• FAO<br>
• IPCC<br>
• IPBES<br>
• Scientific papers
""",
    )

    st.divider()

    st.caption(
        "⚠️ Demo environmental values are sample observations "
        "and should not be treated as verified field measurements."
    )


# =========================================================
# HERO
# =========================================================

st.html(
    """
<div class="hero">

    <div class="hero-kicker">
        Environmental Intelligence • RAG • Multi-Metric Reasoning
    </div>

    <div class="hero-title">
        🌿 Darukaa.Earth
    </div>

    <div class="hero-subtitle">
        AI Biodiversity Intelligence Engine
    </div>

    <div class="hero-description">
        Understand environmental conditions, connect soil, climate,
        land and human-pressure variables, retrieve scientific evidence,
        and generate actionable biodiversity recommendations.
    </div>

    <div class="hero-pills">
        <span class="tag-accent">🧠 AI Reasoning</span>
        <span class="tag-accent">📚 Scientific RAG</span>
        <span class="tag-accent">🔗 Multi-Metric</span>
        <span class="tag-accent">🌱 Biodiversity</span>
    </div>

</div>
""",
)


# =========================================================
# PIPELINE VISUAL
# =========================================================

st.html(
    '<div class="section-title">🔄 Intelligence Pipeline</div>',
)

pipeline_cols = st.columns(6)

pipeline_visual = [
    ("📥", "Input", "Text / JSON"),
    ("🌍", "State", "Environment"),
    ("🔗", "Reason", "Relationships"),
    ("📚", "Retrieve", "Scientific RAG"),
    ("🧠", "Explain", "AI reasoning"),
    ("🌱", "Act", "Recommendations"),
]

for column, (icon, title, subtitle) in zip(pipeline_cols, pipeline_visual):
    with column:
        st.html(
            f"""
<div class="pipeline-card">
    <div class="pipeline-icon">{icon}</div>
    <div class="pipeline-title">{title}</div>
    <div class="pipeline-subtitle">{subtitle}</div>
</div>
""",
        )


# =========================================================
# ASSESSMENT MODE
# =========================================================

st.divider()

st.html(
    '<div class="section-title">🔍 Environmental Assessment</div>',
)

st.html(
    '<div class="section-caption">'
    'Provide environmental observations and let the engine reason across them.'
    '</div>',
)

assessment_mode = st.radio(
    "Assessment mode",
    [
        "Demo Location",
        "Manual Environmental Input",
        "JSON Structured Input",
    ],
    horizontal=True,
    label_visibility="collapsed",
)


# =========================================================
# DEMO MODE
# =========================================================

payload = None

if assessment_mode == "Demo Location":

    st.info(
        "Demo mode uses a predefined sample scenario. "
        "It is intended for testing the complete AI + RAG pipeline."
    )

    demo_payload = {
        "location_id": "LOC001",
        "latitude": 21.1458,
        "longitude": 79.0882,
        "soil_ph": 6.2,
        "soil_organic_carbon": 0.35,
        "soil_moisture": 12.0,
        "temperature": 32.0,
        "rainfall": 850.0,
        "land_use": "monoculture",
        "tree_cover_percent": 8.0,
        "species_richness": "low",
        "habitat_diversity": "low",
        "pollution_level": "medium",
        "deforestation_level": "low",
    }

    preview_cols = st.columns(4)

    demo_preview = [
        ("📍", "Location", "LOC001"),
        ("🌱", "Organic Carbon", "0.35"),
        ("💧", "Moisture", "12"),
        ("🌳", "Tree Cover", "8%"),
    ]

    for column, (icon, label, value) in zip(preview_cols, demo_preview):
        with column:
            render_metric_card(label, value, icon=icon)

    payload = demo_payload


# =========================================================
# MANUAL MODE
# =========================================================

elif assessment_mode == "Manual Environmental Input":

    st.markdown("### 📍 Location")

    location_col1, location_col2, location_col3 = st.columns(3)

    with location_col1:
        location_id = st.text_input(
            "Location ID",
            value="CUSTOM001",
        )

    with location_col2:
        latitude = st.number_input(
            "Latitude",
            value=21.1458,
            format="%.4f",
        )

    with location_col3:
        longitude = st.number_input(
            "Longitude",
            value=79.0882,
            format="%.4f",
        )

    st.markdown("### 🌱 Soil")

    soil_col1, soil_col2, soil_col3 = st.columns(3)

    with soil_col1:
        soil_ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.1,
            step=0.1,
        )

    with soil_col2:
        soil_organic_carbon = st.number_input(
            "Soil Organic Carbon",
            min_value=0.0,
            value=0.4,
            step=0.05,
        )

    with soil_col3:
        soil_moisture = st.number_input(
            "Soil Moisture",
            min_value=0.0,
            value=11.0,
            step=1.0,
        )

    st.markdown("### 🌡️ Climate")

    climate_col1, climate_col2 = st.columns(2)

    with climate_col1:
        temperature = st.number_input(
            "Temperature (°C)",
            value=35.0,
            step=0.5,
        )

    with climate_col2:
        rainfall = st.number_input(
            "Rainfall",
            min_value=0.0,
            value=700.0,
            step=50.0,
        )

    st.markdown("### 🌳 Land & Biodiversity")

    land_col1, land_col2, land_col3 = st.columns(3)

    with land_col1:
        land_use = st.selectbox(
            "Land Use",
            [
                "monoculture",
                "agriculture",
                "natural_forest",
                "degraded_land",
                "restoration_area",
            ],
        )

    with land_col2:
        tree_cover_percent = st.number_input(
            "Tree Cover (%)",
            min_value=0.0,
            max_value=100.0,
            value=8.0,
            step=1.0,
        )

    with land_col3:
        species_richness = st.selectbox(
            "Species Richness",
            ["low", "medium", "high"],
        )

    habitat_diversity = st.selectbox(
        "Habitat Diversity",
        ["low", "medium", "high"],
    )

    st.markdown("### ⚠️ Human Pressure")

    pressure_col1, pressure_col2 = st.columns(2)

    with pressure_col1:
        pollution_level = st.selectbox(
            "Pollution Level",
            ["low", "medium", "high"],
        )

    with pressure_col2:
        deforestation_level = st.selectbox(
            "Deforestation Level",
            ["low", "medium", "high"],
        )

    payload = {
        "location_id": location_id,
        "latitude": latitude,
        "longitude": longitude,
        "soil_ph": soil_ph,
        "soil_organic_carbon": soil_organic_carbon,
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "rainfall": rainfall,
        "land_use": land_use,
        "tree_cover_percent": tree_cover_percent,
        "species_richness": species_richness,
        "habitat_diversity": habitat_diversity,
        "pollution_level": pollution_level,
        "deforestation_level": deforestation_level,
    }


# =========================================================
# JSON MODE
# =========================================================

else:

    st.info(
        "JSON mode demonstrates the structured-input capability "
        "required by the biodiversity intelligence system."
    )

    default_json = {
        "location_id": "JSON001",
        "latitude": 21.1458,
        "longitude": 79.0882,
        "soil_ph": 6.2,
        "soil_organic_carbon": 0.35,
        "soil_moisture": 12.0,
        "temperature": 32.0,
        "rainfall": 850.0,
        "land_use": "monoculture",
        "tree_cover_percent": 8.0,
        "species_richness": "low",
        "habitat_diversity": "low",
        "pollution_level": "medium",
        "deforestation_level": "low",
    }

    json_text = st.text_area(
        "Environmental JSON",
        value=json.dumps(default_json, indent=4),
        height=380,
    )

    try:
        parsed_json = json.loads(json_text)

        required_fields = [
            "location_id",
            "latitude",
            "longitude",
            "soil_ph",
            "soil_organic_carbon",
            "soil_moisture",
            "temperature",
            "rainfall",
            "land_use",
            "tree_cover_percent",
            "species_richness",
            "habitat_diversity",
            "pollution_level",
            "deforestation_level",
        ]

        missing = [
            field for field in required_fields
            if field not in parsed_json
        ]

        if missing:
            st.warning(
                "Missing required fields: "
                + ", ".join(missing)
            )
        else:
            st.success("JSON structure looks complete.")
            payload = parsed_json

    except json.JSONDecodeError as error:
        st.error(f"Invalid JSON: {error}")


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.divider()

button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:

    assess_button = st.button(
        "🔍 Analyze Biodiversity",
        type="primary",
        use_container_width=True,
    )


# =========================================================
# API REQUEST
# =========================================================

if assess_button:

    if payload is None:
        st.error("Please provide a valid environmental input first.")
    else:

        st.session_state["last_payload"] = payload

        with st.spinner(
            "🧠 Building environmental state → "
            "reasoning across metrics → retrieving scientific evidence → "
            "generating explanation..."
        ):

            try:

                response = send_assessment(payload)

                if response.status_code == 200:

                    result = response.json()

                    st.session_state["assessment"] = result
                    st.session_state["chat_messages"] = []
                    st.session_state["chat_session_id"] = None

                    st.success(
                        "Assessment completed successfully."
                    )

                else:

                    st.error(
                        f"Backend returned HTTP {response.status_code}"
                    )

                    st.code(response.text)

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to FastAPI. "
                    "Start the backend with: "
                    "`uvicorn app.main:app --reload`"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏳ The assessment timed out. "
                    "The RAG + LLM pipeline may need more time. "
                    "Please try again."
                )

            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )


# =========================================================
# DISPLAY RESULTS
# =========================================================

if st.session_state["assessment"] is not None:

    result = st.session_state["assessment"]

    state = result.get(
        "environmental_state",
        {},
    )

    soil = state.get("soil", {})
    climate = state.get("climate", {})
    land = state.get("land", {})
    biodiversity = state.get("biodiversity", {})
    human_pressure = state.get("human_pressure", {})

    relationships = result.get(
        "detected_relationships",
        [],
    )

    recommendations = result.get(
        "recommendations",
        [],
    )

    details = result.get(
        "recommendation_details",
        [],
    )

    impacted_metrics = result.get(
        "impacted_metrics",
        [],
    )

    evidence = result.get(
        "scientific_evidence",
        [],
    )

    # =====================================================
    # RESULT HEADER
    # =====================================================

    st.divider()

    st.html(
        '<div class="section-title">📊 Intelligence Assessment</div>',
    )

    header_col1, header_col2, header_col3, header_col4 = st.columns(4)

    with header_col1:
        render_metric_card(
            "Location",
            result.get("location_id", "N/A"),
            icon="📍",
        )

    with header_col2:
        render_metric_card(
            "Confidence",
            str(result.get("confidence", "N/A")).upper(),
            icon="🎯",
        )

    with header_col3:
        render_metric_card(
            "Time Horizon",
            format_horizon(
                result.get("time_horizon", "N/A")
            ),
            icon="⏳",
        )

    with header_col4:
        render_metric_card(
            "Relationships Detected",
            len(relationships),
            icon="🔗",
        )

    # =====================================================
    # TABBED RESULTS
    # =====================================================

    tab_overview, tab_reasoning, tab_recommendations, tab_evidence, tab_chat = st.tabs(
        [
            "🌍 Overview",
            "🔗 Reasoning",
            "🌱 Recommendations",
            "📚 Scientific Evidence",
            "💬 Conversation",
        ]
    )

    # =====================================================
    # OVERVIEW TAB
    # =====================================================

    with tab_overview:

        st.html(
            '<div class="section-title">🌱 Environmental State</div>',
        )

        # Soil
        st.markdown("### 🌱 Soil")

        soil1, soil2, soil3 = st.columns(3)

        with soil1:
            render_metric_card(
                "Soil pH",
                soil.get("ph", "N/A"),
                icon="🧪",
            )

        with soil2:
            render_metric_card(
                "Organic Carbon",
                soil.get("organic_carbon", "N/A"),
                soil.get("organic_carbon_status"),
                "🌿",
            )

        with soil3:
            render_metric_card(
                "Soil Moisture",
                soil.get("moisture", "N/A"),
                soil.get("moisture_status"),
                "💧",
            )

        # Climate
        st.markdown("### 🌡️ Climate")

        climate1, climate2 = st.columns(2)

        with climate1:
            render_metric_card(
                "Temperature",
                f'{climate.get("temperature", "N/A")} °C',
                climate.get("temperature_status"),
                "🌡️",
            )

        with climate2:
            render_metric_card(
                "Rainfall",
                climate.get("rainfall", "N/A"),
                icon="🌧️",
            )

        # Land
        st.markdown("### 🌳 Land")

        land1, land2 = st.columns(2)

        with land1:
            render_metric_card(
                "Land Use",
                land.get("land_use", "N/A"),
                icon="🗺️",
            )

        with land2:
            render_metric_card(
                "Tree Cover",
                f'{land.get("tree_cover_percent", "N/A")} %',
                land.get("tree_cover_status"),
                "🌳",
            )

        # Biodiversity
        st.markdown("### 🦋 Biodiversity")

        bio1, bio2 = st.columns(2)

        with bio1:
            render_metric_card(
                "Species Richness",
                biodiversity.get(
                    "species_richness",
                    "N/A",
                ),
                icon="🦋",
            )

        with bio2:
            render_metric_card(
                "Habitat Diversity",
                biodiversity.get(
                    "habitat_diversity",
                    "N/A",
                ),
                icon="🏞️",
            )

        # Human pressure
        st.markdown("### ⚠️ Human Pressure")

        pressure1, pressure2 = st.columns(2)

        with pressure1:
            render_metric_card(
                "Pollution",
                human_pressure.get(
                    "pollution",
                    "N/A",
                ),
                icon="🏭",
            )

        with pressure2:
            render_metric_card(
                "Deforestation",
                human_pressure.get(
                    "deforestation",
                    "N/A",
                ),
                icon="🪓",
            )

        # Impacted metrics
        st.markdown("### 📈 Impacted Environmental Metrics")

        if impacted_metrics:

            for metric in impacted_metrics:
                render_tag(
                    metric,
                    "tag-accent",
                )

        else:

            st.info(
                "No impacted metrics were identified."
            )

    # =====================================================
    # REASONING TAB
    # =====================================================

    with tab_reasoning:

        st.html(
            '<div class="section-title">🔗 Multi-Metric Reasoning</div>',
        )

        st.html(
            """
<div class="info-banner">
    The engine evaluates relationships between environmental
    variables rather than treating every metric independently.
</div>
""",
        )

        if relationships:

            for index, relationship in enumerate(
                relationships,
                start=1,
            ):

                relationship_type = relationship.get(
                    "type",
                    relationship.get(
                        "relationship",
                        f"Relationship {index}",
                    ),
                )

                with st.expander(
                    f"🔗 {index}. {pretty_name(relationship_type)}",
                    expanded=index == 1,
                ):

                    description = relationship.get(
                        "description"
                    )

                    if description:
                        st.markdown(
                            f"**Reasoning:** {description}"
                        )

                    metrics = relationship.get(
                        "affected_metrics",
                        relationship.get(
                            "metrics",
                            [],
                        ),
                    )

                    if metrics:
                        st.markdown(
                            "**Connected Metrics**"
                        )

                        for metric in metrics:
                            render_tag(
                                metric,
                                "tag-accent",
                            )

                    actions = relationship.get(
                        "recommended_actions",
                        relationship.get(
                            "actions",
                            [],
                        ),
                    )

                    if actions:
                        st.markdown("**Possible Actions**")

                        for action in actions:
                            st.markdown(
                                f"• {action}"
                            )

                    with st.expander(
                        "View relationship data"
                    ):
                        st.json(relationship)

        else:

            st.info(
                "No predefined multi-metric relationships "
                "were detected for this assessment."
            )

        # Relationship flow
        st.markdown("### 🧩 Reasoning Chain")

        chain_items = [
            ("Observed Conditions", "Environmental measurements"),
            ("Detected Interaction", "Cross-metric relationship"),
            ("Scientific Retrieval", "Relevant evidence"),
            ("Action", "Evidence-informed recommendation"),
        ]

        for index, (title, subtitle) in enumerate(
            chain_items,
            start=1,
        ):

            chain_col1, chain_col2 = st.columns([1, 5])

            with chain_col1:
                st.markdown(
                    f"### {index}"
                )

            with chain_col2:
                st.html(
                    f"**{title}**  \n"
                    f"<span style='opacity:0.65'>{subtitle}</span>",
                )

    # =====================================================
    # RECOMMENDATIONS TAB
    # =====================================================

    with tab_recommendations:

        st.html(
            '<div class="section-title">🌱 Actionable Recommendations</div>',
        )

        st.html(
            """
<div class="info-banner">
    Recommendations are generated from detected environmental
    relationships and supported with retrieved scientific evidence.
</div>
""",
        )

        if recommendations:

            for index, recommendation in enumerate(
                recommendations,
                start=1,
            ):

                st.html(
                    f"""
<div class="recommendation-card">
    <div class="recommendation-number">
        Recommendation {index}
    </div>
    <div class="recommendation-title">
        🌱 {safe(recommendation)}
    </div>
</div>
""",
                )

        else:

            st.info(
                "No specific recommendations were generated."
            )

        if details:

            st.markdown("### 🎯 Recommendation Details")

            for index, detail in enumerate(
                details,
                start=1,
            ):

                priority = detail.get(
                    "priority",
                    "N/A",
                )

                reason = detail.get(
                    "reason",
                    "N/A",
                )

                horizon = detail.get(
                    "time_horizon",
                    "N/A",
                )

                metrics = detail.get(
                    "affected_metrics",
                    [],
                )

                actions = detail.get(
                    "actions",
                    [],
                )

                with st.container(border=True):

                    st.markdown(
                        f"### Recommendation {index}"
                    )

                    info1, info2, info3 = st.columns(3)

                    with info1:
                        st.write(
                            f"**Priority:** {str(priority).upper()}"
                        )

                    with info2:
                        st.write(
                            f"**Time Horizon:** "
                            f"{format_horizon(horizon)}"
                        )

                    with info3:
                        st.write(
                            f"**Metrics:** {len(metrics)}"
                        )

                    st.markdown(
                        f"**Why this matters:** {reason}"
                    )

                    if metrics:
                        st.markdown(
                            "**Affected Metrics**"
                        )

                        for metric in metrics:
                            render_tag(
                                metric,
                                "tag-accent",
                            )

                    if actions:
                        st.markdown(
                            "**Actions**"
                        )

                        for action in actions:
                            st.markdown(
                                f"• {action}"
                            )

        # AI explanation
        st.markdown("### 🧠 AI Scientific Assessment")

        explanation = result.get(
            "scientific_explanation",
            "",
        )

        if explanation:
            st.markdown(explanation)
        else:
            st.warning(
                "Scientific explanation was not returned."
            )

    # =====================================================
    # EVIDENCE TAB
    # =====================================================

    with tab_evidence:

        st.html(
            '<div class="section-title">📚 Scientific Evidence</div>',
        )

        st.caption(
            "Evidence retrieved from the environmental knowledge base "
            "through semantic search."
        )

        if evidence:

            for index, item in enumerate(
                evidence,
                start=1,
            ):

                organization = item.get(
                    "organization",
                    "Unknown organization",
                )

                source = item.get(
                    "source",
                    "Unknown source",
                )

                page = item.get(
                    "page",
                    "N/A",
                )

                evidence_text = item.get(
                    "evidence",
                    "No evidence text available.",
                )

                distance = item.get(
                    "distance",
                    None,
                )

                with st.expander(
                    f"📚 Evidence {index} — {organization}",
                    expanded=index == 1,
                ):

                    st.html(
                        f"""
<div class="evidence-card">
    <div class="evidence-source">
        {safe(organization)}
    </div>
    <div class="evidence-meta">
        Document: {safe(source)}
        &nbsp; • &nbsp;
        Page: {safe(page)}
    </div>
</div>
""",
                    )

                    st.markdown(
                        "**Retrieved Evidence**"
                    )

                    st.write(evidence_text)

                    if distance is not None:
                        st.caption(
                            f"Semantic retrieval distance: {distance:.4f}"
                        )

        else:

            st.info(
                "No scientific evidence was retrieved."
            )

    # =====================================================
    # CONVERSATION TAB
    # =====================================================

    with tab_chat:

        st.html(
            '<div class="section-title">💬 Biodiversity Intelligence Chat</div>',
        )

        st.html(
            """
<div class="info-banner">
    Ask follow-up questions about the current environmental
    assessment. The prototype retains conversation context
    through the backend chat service.
</div>
""",
        )

        current_location = result.get(
            "location_id",
            state.get(
                "location_id",
                "",
            ),
        )

        st.caption(
            f"Current assessment context: **{current_location}**"
        )

        clear_chat_col1, clear_chat_col2 = st.columns([5, 1])

        with clear_chat_col2:
            if st.button(
                "Clear Chat",
                use_container_width=True,
            ):
                st.session_state["chat_messages"] = []
                st.session_state["chat_session_id"] = None
                st.rerun()

        for message in st.session_state["chat_messages"]:

            with st.chat_message(
                message["role"]
            ):
                st.markdown(
                    message["content"]
                )

        user_message = st.chat_input(
            "Ask about the environmental assessment..."
        )

        if user_message:

            st.session_state["chat_messages"].append(
                {
                    "role": "user",
                    "content": user_message,
                }
            )

            with st.chat_message("user"):
                st.markdown(user_message)

            with st.chat_message("assistant"):

                with st.spinner(
                    "Thinking about the environmental context..."
                ):

                    try:

                        chat_response = send_chat(
                            user_message,
                            current_location,
                        )

                        if chat_response.status_code == 200:

                            chat_result = chat_response.json()

                            # Store the backend conversation session
                            session_id = chat_result.get("session_id")

                            if session_id:
                                st.session_state["chat_session_id"] = session_id

                            assistant_message = chat_result.get(
                                "message",
                                "No response returned.",
                            )

                            st.markdown(
                                assistant_message
                            )

                            st.session_state[
                                "chat_messages"
                            ].append(
                                {
                                    "role": "assistant",
                                    "content": assistant_message,
                                }
                            )

                        else:

                            error_message = (
                                f"Chat backend returned HTTP "
                                f"{chat_response.status_code}."
                            )

                            st.error(error_message)

                    except requests.exceptions.RequestException as error:

                        st.error(
                            f"Could not contact chat service: {error}"
                        )

    # =====================================================
    # LOCATION + DATA EXPORT
    # =====================================================

    st.divider()

    st.html(
        '<div class="section-title">📍 Location & Assessment Data</div>',
    )

    coordinates = state.get(
        "coordinates",
        {},
    )

    loc1, loc2, loc3 = st.columns(3)

    with loc1:
        render_metric_card(
            "Location ID",
            state.get("location_id", "N/A"),
            icon="📍",
        )

    with loc2:
        render_metric_card(
            "Latitude",
            coordinates.get("latitude", "N/A"),
            icon="↕️",
        )

    with loc3:
        render_metric_card(
            "Longitude",
            coordinates.get("longitude", "N/A"),
            icon="↔️",
        )

    if (
        coordinates.get("latitude") is not None
        and coordinates.get("longitude") is not None
    ):

        st.markdown("### 🗺️ Assessment Location")

        map_data = pd.DataFrame(
            [
                {
                    "latitude": coordinates.get("latitude"),
                    "longitude": coordinates.get("longitude"),
                }
            ]
        )

        st.map(
            map_data,
            latitude="latitude",
            longitude="longitude",
            size=80,
        )

    st.markdown("### 📦 Export Assessment")

    export_col1, export_col2 = st.columns(2)

    with export_col1:

        st.download_button(
            "⬇️ Download Assessment JSON",
            data=json.dumps(
                result,
                indent=4,
                default=str,
            ),
            file_name="darukaa_assessment.json",
            mime="application/json",
            use_container_width=True,
        )

    with export_col2:

        if st.session_state["last_payload"] is not None:

            st.download_button(
                "⬇️ Download Input JSON",
                data=json.dumps(
                    st.session_state["last_payload"],
                    indent=4,
                    default=str,
                ),
                file_name="darukaa_environmental_input.json",
                mime="application/json",
                use_container_width=True,
            )

    # =====================================================
    # RAW RESPONSE
    # =====================================================

    with st.expander("🔧 Developer View — Raw API Response"):

        st.json(result)


# =========================================================
# LIMITATION
# =========================================================

st.divider()

st.warning(
    """
**Important limitation:** This prototype uses sample environmental
observations and a curated scientific knowledge base. Generated
recommendations are decision-support outputs and should be validated
against verified local measurements, field observations, and relevant
environmental authorities before real-world use.
"""
)


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
<div class="footer">
    🌿 Darukaa.Earth · AI Biodiversity Intelligence Engine
    <br>
    Environmental State + Multi-Metric Reasoning
    + Scientific RAG + AI
    <br><br>
    Prototype for environmental intelligence and biodiversity
    decision-support research.
</div>
""",
)