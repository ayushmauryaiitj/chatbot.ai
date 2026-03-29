import streamlit as st
from urllib.parse import urlparse
from datetime import datetime

st.set_page_config(
    page_title="AI Government Scheme Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SCHEMES = [
    {
        "name": "PM Kisan Samman Nidhi",
        "name_hi": "पीएम किसान सम्मान निधि",
        "keywords_en": ["farmer", "agriculture", "kisan", "crop", "land", "village", "rural"],
        "keywords_hi": ["किसान", "खेती", "कृषि", "फसल", "गांव"],
        "eligibility": "Small and eligible farmer families",
        "eligibility_hi": "छोटे और पात्र किसान परिवार",
        "benefits": "₹6000 per year income support",
        "benefits_hi": "₹6000 प्रति वर्ष आय सहायता",
        "apply": "https://pmkisan.gov.in/",
        "category": "Agriculture",
        "icon": "🌾",
        "description": "Direct income support for eligible farmer families.",
        "why": "Best for people connected to farming, land cultivation, or rural agriculture income."
    },
    {
        "name": "National Scholarship Portal",
        "name_hi": "राष्ट्रीय छात्रवृत्ति पोर्टल",
        "keywords_en": ["student", "education", "scholarship", "study", "teacher", "school", "college"],
        "keywords_hi": ["छात्र", "शिक्षा", "स्कॉलरशिप", "अध्ययन", "शिक्षक", "कॉलेज", "स्कूल"],
        "eligibility": "Eligible students",
        "eligibility_hi": "पात्र विद्यार्थी",
        "benefits": "Financial aid for education",
        "benefits_hi": "शिक्षा के लिए वित्तीय सहायता",
        "apply": "https://scholarships.gov.in/",
        "category": "Education",
        "icon": "🎓",
        "description": "Scholarship discovery and application support for students.",
        "why": "Ideal for students, teachers, or households looking for education-related support."
    },
    {
        "name": "Skill India",
        "name_hi": "स्किल इंडिया",
        "keywords_en": ["unemployed", "job", "training", "skill", "work", "employment", "career"],
        "keywords_hi": ["बेरोजगार", "नौकरी", "प्रशिक्षण", "कौशल", "रोजगार", "करियर"],
        "eligibility": "Job seekers and learners",
        "eligibility_hi": "रोजगार खोजने वाले और शिक्षार्थी",
        "benefits": "Skill training and employability support",
        "benefits_hi": "कौशल प्रशिक्षण और रोजगार सहायता",
        "apply": "https://skillindia.gov.in/",
        "category": "Employment",
        "icon": "🛠️",
        "description": "Upskilling support for better employment opportunities.",
        "why": "Useful when the user is unemployed, looking for work, or wants vocational training."
    },
    {
        "name": "Stand-Up India",
        "name_hi": "स्टैंड-अप इंडिया",
        "keywords_en": ["business", "startup", "loan", "entrepreneur", "company", "shop", "enterprise"],
        "keywords_hi": ["व्यवसाय", "स्टार्टअप", "लोन", "उद्यमी", "दुकान", "कंपनी"],
        "eligibility": "Entrepreneurs and new business applicants",
        "eligibility_hi": "उद्यमी और नया व्यवसाय शुरू करने वाले",
        "benefits": "Bank loan support for business setup",
        "benefits_hi": "व्यवसाय शुरू करने के लिए बैंक ऋण सहायता",
        "apply": "https://standupmitra.in/",
        "category": "Business",
        "icon": "💼",
        "description": "Loan and entrepreneurship support for starting ventures.",
        "why": "Strong fit for startup founders, shop owners, or people seeking a business loan."
    },
    {
        "name": "Women Support Scheme",
        "name_hi": "महिला सहायता योजना",
        "keywords_en": ["women", "housewife", "female", "mother", "self help"],
        "keywords_hi": ["महिला", "गृहिणी", "औरत", "मां", "स्वयं सहायता"],
        "eligibility": "Women applicants",
        "eligibility_hi": "महिला आवेदक",
        "benefits": "Financial and support assistance",
        "benefits_hi": "वित्तीय और सहायक सहायता",
        "apply": "#",
        "category": "Women",
        "icon": "👩",
        "description": "Women-focused support pathways and assistance.",
        "why": "Helpful for women, homemakers, and self-help-group oriented assistance scenarios."
    },
]

FALLBACK_SCHEMES = [
    {
        "name": "PM Jan Dhan Yojana",
        "name_hi": "पीएम जन धन योजना",
        "eligibility": "Any eligible citizen",
        "eligibility_hi": "कोई भी पात्र नागरिक",
        "benefits": "Zero-balance bank account access",
        "benefits_hi": "शून्य-बैलेंस बैंक खाता सुविधा",
        "apply": "https://pmjdy.gov.in/",
        "category": "Banking",
        "icon": "🏦",
        "description": "A strong basic banking option for many citizens.",
        "why": "Great default recommendation when the user profile is broad or unspecified."
    },
    {
        "name": "Ayushman Bharat",
        "name_hi": "आयुष्मान भारत",
        "eligibility": "Eligible low income families",
        "eligibility_hi": "पात्र कम आय वाले परिवार",
        "benefits": "Up to ₹5 lakh health coverage",
        "benefits_hi": "₹5 लाख तक स्वास्थ्य कवरेज",
        "apply": "https://pmjay.gov.in/",
        "category": "Health",
        "icon": "🩺",
        "description": "Health coverage support for eligible households.",
        "why": "Strong fallback for families seeking broad social welfare support."
    }
]

CATEGORY_OPTIONS = ["All", "Agriculture", "Education", "Employment", "Business", "Women", "Banking", "Health"]

def tr(en, hi):
    return hi if st.session_state.language == "हिंदी" else en

def safe_url(url: str) -> str:
    if isinstance(url, str) and url.startswith(("http://", "https://")):
        return url
    return "#"

def enrich_query(text: str) -> str:
    q = (text or "").lower().strip()
    if "teacher" in q or "शिक्षक" in q:
        q += " education scholarship student school college"
    if "housewife" in q or "गृहिणी" in q:
        q += " women mother self help महिला"
    if "unemployed" in q or "बेरोजगार" in q:
        q += " job training skill work रोजगार नौकरी"
    if "farmer" in q or "किसान" in q:
        q += " agriculture kisan crop खेती कृषि"
    if "business" in q or "व्यवसाय" in q or "startup" in q or "shop" in q:
        q += " startup loan entrepreneur shop enterprise लोन उद्यमी"
    return q

def calculate_score(user_text: str, scheme: dict) -> int:
    text = enrich_query(user_text)
    score = 0
    for kw in scheme.get("keywords_en", []):
        if kw in text:
            score += 16
    for kw in scheme.get("keywords_hi", []):
        if kw in text:
            score += 16
    bonus_words = ["need", "help", "support", "benefit", "apply", "yojana", "scheme", "योजना", "मदद"]
    for word in bonus_words:
        if word in text:
            score += 2
    return min(score, 100)

def get_display_name(scheme):
    if st.session_state.language == "हिंदी" and scheme.get("name_hi"):
        return scheme["name_hi"]
    return scheme.get("name", "Scheme")

def get_display_field(scheme, en_key, hi_key):
    if st.session_state.language == "हिंदी" and scheme.get(hi_key):
        return scheme[hi_key]
    return scheme.get(en_key, "")

def get_results(user_text: str):
    ranked = []
    for scheme in SCHEMES:
        score = calculate_score(user_text, scheme)
        if score > 0:
            item = scheme.copy()
            item["score"] = score
            ranked.append(item)
    if not ranked:
        ranked = []
        for fallback in FALLBACK_SCHEMES:
            item = fallback.copy()
            item["score"] = 72
            ranked.append(item)
    ranked.sort(key=lambda x: x.get("score", 0), reverse=True)
    selected_category = st.session_state.selected_category
    if selected_category != "All":
        filtered = [item for item in ranked if item.get("category") == selected_category]
        if filtered:
            ranked = filtered
    return ranked

def score_label(score):
    if score >= 90:
        return tr("Excellent Match", "बहुत अस्ली मिलान"), "excellent"
    if score >= 75:
        return tr("Strong Match", "अस्ली मिलान"), "strong"
    return tr("Recommended", "सुझाव"), "recommended"

def render_score(score):
    label, cls = score_label(score)
    return f'<div class="score-badge {cls}">{score}% • {label}</div>'

def render_scheme_card(scheme):
    name = get_display_name(scheme)
    eligibility = get_display_field(scheme, "eligibility", "eligibility_hi")
    benefits = get_display_field(scheme, "benefits", "benefits_hi")
    why = scheme.get("why", "")
    description = scheme.get("description", "")
    category = scheme.get("category", "General")
    icon = scheme.get("icon", "🏛️")
    score = scheme.get("score", 0)
    apply_url = safe_url(scheme.get("apply", "#"))
    if apply_url == "#":
        action_html = f'<div class="scheme-link disabled">{tr("More details soon", "विवरण शीघ्र आयेंगे")}</div>'
    else:
        domain = urlparse(apply_url).netloc.replace("www.", "")
        action_html = f'<a class="scheme-link" href="{apply_url}" target="_blank">{tr("Apply Now", "अभी आवेदन करें")} ↗ <span>{domain}</span></a>'
    why_label = tr("Why this fits", "यह क्यूं उपयुक्त है")
    return f"""
    <div class="scheme-card glass-card">
        <div class="scheme-head">
            <div class="scheme-icon">{icon}</div>
            <div class="scheme-main">
                <div class="scheme-category">{category}</div>
                <h3>{name}</h3>
            </div>
            <div class="scheme-score">{render_score(score)}</div>
        </div>
        <p class="scheme-description">{description}</p>
        <div class="scheme-metrics">
            <div class="metric-box">
                <span class="metric-title">{tr("Eligibility", "पात्रता")}</span>
                <span class="metric-value">✅ {eligibility}</span>
            </div>
            <div class="metric-box">
                <span class="metric-title">{tr("Benefits", "लाभ")}</span>
                <span class="metric-value">💰 {benefits}</span>
            </div>
        </div>
        <div class="why-box">
            <span class="why-title">{why_label}</span>
            <span class="why-text">{why}</span>
        </div>
        <div class="scheme-action-wrap">
            {action_html}
        </div>
    </div>
    """

def respond_and_store(user_text: str):
    results = get_results(user_text)
    response = (
        tr(
            f"I found {len(results)} relevant scheme recommendations for your profile. The best matches are shown below.",
            f"मैंने आपकी प्रोफाइल के लिए {len(results)} उपयुक्त योजना सुझाव पाए हैं। सबसे अम्छुर भिल़ी हैं।"
        )
    )
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.latest_results = results
    st.session_state.last_query = user_text

def quick_action(text):
    respond_and_store(text)
    st.rerun()

if "language" not in st.session_state:
    st.session_state.language = "English"

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome! Tell me about yourself and I will recommend the most suitable government schemes instantly."
        }
    ]

if "latest_results" not in st.session_state:
    seed = []
    for x in FALLBACK_SCHEMES:
        item = x.copy()
        item["score"] = 72
        seed.append(item)
    st.session_state.latest_results = seed

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

st.markdown(
    """
    <style>
    :root {
        --bg1: #04111d;
        --bg2: #0a1f33;
        --bg3: #12324d;
        --txt: #f4fbff;
        --muted: rgba(244,251,255,0.76);
        --soft: rgba(244,251,255,0.58);
        --glass: rgba(255,255,255,0.12);
        --glass2: rgba(255,255,255,0.08);
        --stroke: rgba(255,255,255,0.18);
        --accent: #7dd3fc;
        --accent2: #c4b5fd;
        --accent3: #86efac;
        --shadow: 0 18px 48px rgba(0,0,0,0.25);
    }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 48%, var(--bg3) 100%); }
    .glass-card { background: linear-gradient(180deg, rgba(255,255,255,0.15), rgba(255,255,255,0.08)); border: 1px solid var(--stroke); backdrop-filter: blur(20px); border-radius: 24px; padding: 18px; }
    .scheme-card { border-radius: 24px; padding: 18px; margin-bottom: 16px; }
    .scheme-head { display: flex; gap: 14px; align-items: flex-start; }
    .scheme-icon { width: 58px; height: 58px; border-radius: 16px; display: grid; place-items: center; font-size: 1.55rem; background: rgba(255,255,255,0.12); }
    .scheme-category { font-size: 0.78rem; text-transform: uppercase; color: var(--accent); font-weight: 700; }
    .score-badge { padding: 8px 10px; border-radius: 999px; font-size: 0.78rem; font-weight: 800; }
    .score-badge.excellent { background: rgba(134, 239, 172, 0.16); color: #dbffe9; }
    .score-badge.strong { background: rgba(125, 211, 252, 0.16); color: #e2f7ff; }
    .score-badge.recommended { background: rgba(196, 181, 253, 0.16); color: #f1eaff; }
    .scheme-link { display: inline-flex; align-items: center; gap: 8px; text-decoration: none; color: #08131d !important; font-weight: 700; background: linear-gradient(135deg, #e0f2fe, #bae6fd); border-radius: 12px; padding: 11px 14px; }
    .scheme-link.disabled { color: var(--muted) !important; background: rgba(255,255,255,0.10); }
    .why-box { border-radius: 14px; padding: 12px 14px; background: rgba(125,211,252,0.08); border: 1px solid rgba(125,211,252,0.16); }
    .metric-box { border-radius: 14px; padding: 12px 14px; background: rgba(255,255,255,0.08); }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 1])
with col1:
    st.session_state.language = st.selectbox("Language", ["English", "हिंदी"], index=0 if st.session_state.language == "English" else 1)
with col2:
    st.session_state.selected_category = st.selectbox("Category", CATEGORY_OPTIONS)

st.markdown(
    f"""<div class='hero'>
    <h1>{tr('🇮🇳 Government Schemes AI', '🇮🇳 सरकारी योजना एआई')}</h1>
    <p>{tr('Instantly find the best government schemes tailored to your needs.', 'अपनी जरूरतों के अनुसार सबसे अच्छी सरकारी योजनाएं तुरंत खोजें।')}</p>
    </div>""",
    unsafe_allow_html=True
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input(tr("Type your query...", "अपनी क्वेरी टाइप करें..."))
if user_input:
    respond_and_store(user_input)
    st.rerun()

if st.session_state.latest_results:
    results_html = "".join([render_scheme_card(scheme) for scheme in st.session_state.latest_results])
    st.markdown(f"<div>{results_html}</div>", unsafe_allow_html=True)

st.markdown(f"<div class='footer'>{tr('💡 Pro tip: Be specific about your situation for better recommendations.', '💡 टिप: बेहतर सिफारिशों के लिए अपनी स्थिति के बारे में विशिष्ट रहें।')}</div>", unsafe_allow_html=True)
