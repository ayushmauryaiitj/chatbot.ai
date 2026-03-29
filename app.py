import streamlit as st

st.set_page_config(page_title="Government Schemes AI", page_icon="🏛️", layout="wide")

SCHEMES = [
    {"name": "PM Kisan Samman Nidhi", "name_hi": "पीएम किसान सम्मान निधि", "category": "Agriculture", "icon": "🌾", "keywords": ["farmer", "kisan", "agriculture", "किसान", "खेती"], "eligibility": "किसान परिवार", "eligibility_hi": "किसान परिवार", "benefit": "6000 per year", "benefit_hi": "6000 प्रति वर्ष", "link": "https://pmkisan.gov.in/"},
    {"name": "Scholarship Portal", "name_hi": "स्कॉलरशिप पोर्टल", "category": "Education", "icon": "🎓", "keywords": ["student", "education", "scholarship", "छात्र", "शिक्षा"], "eligibility": "विद्यार्थी", "eligibility_hi": "विद्यार्थी", "benefit": "Financial aid", "benefit_hi": "वित्तीय सहायता", "link": "https://scholarships.gov.in/"},
    {"name": "Skill India", "name_hi": "स्किल इंडिया", "category": "Employment", "icon": "🛠️", "keywords": ["job", "skill", "training", "unemployed", "नौकरी"], "eligibility": "काम खोज रहे", "eligibility_hi": "काम खोज रहे", "benefit": "Job training", "benefit_hi": "कौशल प्रशिक्षण", "link": "https://skillindia.gov.in/"},
    {"name": "PM Jan Dhan", "name_hi": "पीएम जन धन", "category": "Banking", "icon": "🏦", "keywords": ["bank", "account", "dhan", "खाता"], "eligibility": "सभी नागरिक", "eligibility_hi": "सभी नागरिक", "benefit": "Bank account", "benefit_hi": "खाता खोलना", "link": "https://pmjdy.gov.in/"},
    {"name": "Ayushman Bharat", "name_hi": "आयुष्मान भारत", "category": "Health", "icon": "🩺", "keywords": ["health", "hospital", "स्वास्थ्य"], "eligibility": "परिवार", "eligibility_hi": "परिवार", "benefit": "5L health coverage", "benefit_hi": "5 लाख स्वास्थ्य कवरेज", "link": "https://pmjay.gov.in/"},
]

def tr(en, hi):
    return hi if st.session_state.lang == "हिंदी" else en

def score_match(query, keywords):
    query_lower = query.lower()
    return sum(1 for kw in keywords if kw.lower() in query_lower) * 20

if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "results" not in st.session_state:
    st.session_state.results = []

st.markdown("<style>.stApp { background: linear-gradient(135deg, #04111d 0%, #0a1f33 100%); }</style>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.session_state.lang = st.selectbox("Language", ["English", "हिंदी"], key="lang_select")
with col2:
    category = st.selectbox("Category", ["All"] + list(set(s["category"] for s in SCHEMES)))

st.title(tr("🇮🇳 Government Schemes", "🇮🇳 सरकारी योजना"))
st.write(tr("Find schemes tailored for you", "आपके लिए योजनाएं खोजें"))

query = st.chat_input(tr("Tell us about yourself...", "अपने आप के बारे में बताये..."))

if query:
    results = []
    for scheme in SCHEMES:
        score = score_match(query, scheme["keywords"])
        if score > 0 or True:
            scheme_copy = scheme.copy()
            scheme_copy["score"] = score if score > 0 else 50
            results.append(scheme_copy)
    
    results.sort(key=lambda x: x["score"], reverse=True)
    
    if category != "All":
        results = [r for r in results if r["category"] == category]
    
    st.session_state.results = results

if st.session_state.results:
    st.write(tr(f"Found {len(st.session_state.results)} schemes for you:", f"{len(st.session_state.results)} योजनाएं मिली:"))
    
    for scheme in st.session_state.results:
        with st.container():
            col1, col2 = st.columns([1, 5])
            with col1:
                st.write(scheme["icon"])
            with col2:
                name = scheme["name_hi"] if st.session_state.lang == "हिंदी" else scheme["name"]
                st.subheader(name)
                st.write(f"{scheme['category']} | {scheme['score']}%")
                
                eligibility = scheme["eligibility_hi"] if st.session_state.lang == "हिंदी" else scheme["eligibility"]
                benefit = scheme["benefit_hi"] if st.session_state.lang == "हिंदी" else scheme["benefit"]
                
                st.write(f"**{tr('Eligibility', 'पात्रता')}**: {eligibility}")
                st.write(f"**{tr('Benefit', 'लाभ')}**: {benefit}")
                st.link_button(tr("Apply Now ↗", "आवेदन करें ↗"), scheme["link"])
            st.divider()
else:
    st.info(tr("Type a query to see recommendations", "सुझाव देखने के लिए लिखें"))

st.divider()
st.caption(tr("💡 Be specific for better results", "💡 सही परिणाम के लिए विशिष्ट रहें")
