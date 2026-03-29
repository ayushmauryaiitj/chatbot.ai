import streamlit as st

st.set_page_config(page_title="Government Schemes Chatbot", page_icon="🤖", layout="wide")

SCHEMES = [
    {
        "name": "PM Kisan Samman Nidhi",
        "name_hi": "पीएम किसान सम्मान निधि",
        "keywords": ["farmer", "kisan", "agriculture", "किसान"],
        "eligibility": "All farmer families owning cultivable land",
        "eligibility_hi": "खेती योग्य भूमि वाले सभी किसान परिवार",
        "benefit": "₹6000 per year in 3 installments",
        "benefit_hi": "साल में ₹6000 तीन किस्तों में",
        "how_to_apply": "Visit pmkisan.gov.in with Aadhaar and land documents",
        "how_to_apply_hi": "pmkisan.gov.in पर जाएं, आधार और के साथ",
        "link": "https://pmkisan.gov.in/"
    },
    {
        "name": "National Scholarship Portal",
        "name_hi": "राष्ट्रीय छात्रवृत्ति पोर्टल",
        "keywords": ["student", "education", "scholarship", "छात्र"],
        "eligibility": "Students from class 1 to post-graduation based on merit",
        "eligibility_hi": "कक्षा 1 से पोस्ट ग्रेजुएशन तक",
        "benefit": "Financial assistance for education",
        "benefit_hi": "शिक्षा खर्च के लिए सहायता",
        "how_to_apply": "Register on scholarships.gov.in with required documents",
        "how_to_apply_hi": "scholarships.gov.in पर पंजीकरण करें",
        "link": "https://scholarships.gov.in/"
    },
    {
        "name": "Skill India",
        "name_hi": "स्किल इंडिया",
        "keywords": ["job", "skill", "training", "employment", "नौकरी"],
        "eligibility": "Job seekers aged 15-45 years",
        "eligibility_hi": "15-45 साल के नौकरी खोजने वाले",
        "benefit": "Free skill training and job placement",
        "benefit_hi": "मुफ्त कौशल प्रशिक्षण और नौकरी सहायता",
        "how_to_apply": "Visit skillindia.gov.in and enroll in courses",
        "how_to_apply_hi": "skillindia.gov.in पर कोर्स लें",
        "link": "https://skillindia.gov.in/"
    }
]

def tr(en, hi):
    if st.session_state.lang == "हिंदी":
        return hi
    else:
        return en

def find_schemes(query):
    query_lower = query.lower()
    matches = []
    for scheme in SCHEMES:
        for kw in scheme["keywords"]:
            if kw.lower() in query_lower:
                matches.append(scheme)
                break
    if not matches:
        matches = SCHEMES
    return matches

def answer_question(query):
    query_lower = query.lower()
    schemes = find_schemes(query)
    if not schemes:
        schemes = SCHEMES
    scheme = schemes[0]
    
    if any(word in query_lower for word in ["eligibility", "पात्रता", "qualify"]):
        elig = scheme["eligibility_hi"] if st.session_state.lang == "हिंदी" else scheme["eligibility"]
        return f"**{scheme['name']}**: {elig}", scheme
    elif any(word in query_lower for word in ["benefit", "लाभ", "मिलेगा"]):
        benefit = scheme["benefit_hi"] if st.session_state.lang == "हिंदी" else scheme["benefit"]
        return f"**{scheme['name']}**: {benefit}", scheme
    elif any(word in query_lower for word in ["apply", "कैसे", "how"]):
        how = scheme["how_to_apply_hi"] if st.session_state.lang == "हिंदी" else scheme["how_to_apply"]
        return f"**{scheme['name']}**: {how}", scheme
    else:
        return None, schemes[:3]

if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("""<style>.stApp { background: linear-gradient(135deg, #04111d 0%, #0a1f33 100%); }</style>""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    st.session_state.lang = st.selectbox(tr("Language", "भाषा"), ["English", "हिंदी"])

st.title(tr("🤖 Government Schemes Chatbot", "🤖 सरकारी योजनऺ चैटबॉट"))
st.caption(tr("Ask about eligibility, benefits, how to apply!", "पछें: पात्रता, लाभ, कैसे आवेदन"))

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input(tr("Ask me...", "पूछें...")):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        answer, schemes = answer_question(prompt)
        
        if answer:
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            msg = f"Found {len(schemes)} schemes. Pick one!"
            for s in schemes:
                msg += f"\n- {s['name']}"
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
