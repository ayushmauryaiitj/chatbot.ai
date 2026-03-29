import streamlit as st

st.set_page_config(page_title="Government Schemes Chatbot", page_icon="🤖", layout="wide")

SCHEMES = [
    {"name": "PM Kisan Samman Nidhi", "name_hi": "पीएम किसान", "category": "Farmer", "keywords": ["farmer", "kisan", "किसान"], "eligibility": "All farmer families owning land", "eligibility_hi": "भूमि वाले किसान", "benefit": "₹6000/year in 3 installments", "benefit_hi": "साल में ₹6000", "how_to_apply": "Visit pmkisan.gov.in", "how_to_apply_hi": "pmkisan.gov.in पर जाएं", "link": "https://pmkisan.gov.in/"},
    {"name": "National Scholarship Portal", "name_hi": "छात्रवृत्ति पोर्टल", "category": "Student", "keywords": ["student", "scholarship", "छात्र"], "eligibility": "Class 1 to post-graduation students", "eligibility_hi": "कक्षा 1 से PG तक", "benefit": "Financial help for education", "benefit_hi": "शिक्षा के लिए सहायता", "how_to_apply": "Register on scholarships.gov.in", "how_to_apply_hi": "scholarships.gov.in पर", "link": "https://scholarships.gov.in/"},
    {"name": "Skill India", "name_hi": "स्किल इंडिया", "category": "Job Seeker", "keywords": ["job", "skill", "नौकरी"], "eligibility": "15-45 years job seekers", "eligibility_hi": "15-45 साल के लोग", "benefit": "Free training + job help", "benefit_hi": "मुफ्त प्रशिक्षण", "how_to_apply": "Visit skillindia.gov.in", "how_to_apply_hi": "skillindia.gov.in पर", "link": "https://skillindia.gov.in/"},
    {"name": "PM Jan Dhan Yojana", "name_hi": "जन धन योजना", "category": "General", "keywords": ["bank", "account", "खाता"], "eligibility": "All Indian citizens", "eligibility_hi": "सभी भारतीय", "benefit": "Zero balance bank account", "benefit_hi": "जीरो बैलेंस खाता", "how_to_apply": "Visit any bank with Aadhaar", "how_to_apply_hi": "किसी बैंक में जाएं", "link": "https://pmjdy.gov.in/"},
    {"name": "Ayushman Bharat", "name_hi": "आयुष्मान भारत", "category": "General", "keywords": ["health", "hospital", "स्वास्थ्य"], "eligibility": "Low income families", "eligibility_hi": "कम आय वाले", "benefit": "Free health coverage ₹5L/year", "benefit_hi": "मुफ्त इलाज ₹5L", "how_to_apply": "Check pmjay.gov.in", "how_to_apply_hi": "pmjay.gov.in चेक करें", "link": "https://pmjay.gov.in/"}
]

def tr(en, hi):
    return hi if st.session_state.lang == "हिंदी" else en

def filter_by_category(categories):
    if not categories or "All" in categories:
        return SCHEMES
    filtered = []
    for scheme in SCHEMES:
        if scheme["category"] in categories:
            filtered.append(scheme)
    return filtered if filtered else SCHEMES

def find_schemes(query):
    query_lower = query.lower()
    matches = []
    for scheme in SCHEMES:
        for kw in scheme["keywords"]:
            if kw.lower() in query_lower:
                matches.append(scheme)
                break
    return matches if matches else SCHEMES

def answer_question(query):
    query_lower = query.lower()
    schemes = find_schemes(query)
    if not schemes:
        schemes = SCHEMES
    scheme = schemes[0]
    
    if any(word in query_lower for word in ["eligibility", "पात्रता", "qualify"]):
        elig = scheme["eligibility_hi"] if st.session_state.lang == "हिंदी" else scheme["eligibility"]
        link = scheme["link"]
        name = scheme["name_hi"] if st.session_state.lang == "हिंदी" else scheme["name"]
        answer = f"**{name}**: {elig}\n\n[Visit Website]({link}) 🔗"
        return answer, scheme
    elif any(word in query_lower for word in ["benefit", "लाभ", "मिलेगा"]):
        benefit = scheme["benefit_hi"] if st.session_state.lang == "हिंदी" else scheme["benefit"]
        link = scheme["link"]
        name = scheme["name_hi"] if st.session_state.lang == "हिंदी" else scheme["name"]
        answer = f"**{name}**: {benefit}\n\n[Visit Website]({link}) 🔗"
        return answer, scheme
    elif any(word in query_lower for word in ["apply", "कैसे", "how"]):
        how = scheme["how_to_apply_hi"] if st.session_state.lang == "हिंदी" else scheme["how_to_apply"]
        link = scheme["link"]
        name = scheme["name_hi"] if st.session_state.lang == "हिंदी" else scheme["name"]
        answer = f"**{name}**: {how}\n\n[Apply Now]({link}) 🔗"
        return answer, scheme
    else:
        return None, schemes[:3]

if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("""<style>.stApp { background: linear-gradient(135deg, #04111d 0%, #0a1f33 100%); }</style>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 2])
with col1:
    st.session_state.lang = st.selectbox(tr("Language", "भाषा"), ["English", "हिंदी"])
with col2:
    categories = st.multiselect(tr("I am a:", "मैं हूं:"), ["Student", "Farmer", "Job Seeker", "General", "All"], default=["All"])

st.title(tr("🤖 Government Schemes Chatbot", "🤖 सरकारी योजना चैटबॉट"))
st.caption(tr("Ask about schemes or select your category!", "योजनाओं के बारे में पूछें या category चुनें!"))

filtered_schemes = filter_by_category(categories)
if len(categories) > 0 and "All" not in categories:
    st.subheader(tr(f"Schemes for: {', '.join(categories)}", f"योजनाएं: {', '.join(categories)}"))
    for scheme in filtered_schemes:
        name = scheme["name_hi"] if st.session_state.lang == "हिंदी" else scheme["name"]
        benefit = scheme["benefit_hi"] if st.session_state.lang == "हिंदी" else scheme["benefit"]
        with st.expander(f"{name}"):
            st.write(f"**{tr('Benefit', 'लाभ')}:** {benefit}")
            st.link_button(tr("→ Apply Now", "→ अभी आवेदन करें"), scheme["link"])
    st.divider()

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
            msg = f"Found {len(schemes)} schemes!"
            for s in schemes:
                msg += f"\n- {s['name']}"
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
