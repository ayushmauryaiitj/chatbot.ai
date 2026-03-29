import streamlit as st
import re

st.set_page_config(page_title="Government Schemes Chatbot", page_icon="🤖", layout="wide")

SCHEMES = [
 {
 "name": "PM Kisan Samman Nidhi",
 "name_hi": "पीएम किसान सम्मान निधि",
 "category": "Agriculture",
 "icon": "🌾",
 "keywords": ["farmer", "kisan", "agriculture", "किसान", "खेती", "farming"],
 "eligibility": "All farmer families owning cultivable land",
 "eligibility_hi": "खेती योग्य भूमि वाले सभी किसान परिवार",
 "benefit": "₹6000 per year in 3 installments",
 "benefit_hi": "साल में ₹6000 तीन किस्तों में",
 "how_to_apply": "Visit pmkisan.gov.in, register with Aadhaar and land documents",
 "how_to_apply_hi": "pmkisan.gov.in पर जाएं, आधार और जमीन के कागजात से रजिस्टर करें",
 "link": "https://pmkisan.gov.in/"
 },
 {
 "name": "National Scholarship Portal",
 "name_hi": "राष्ट्रीय छात्रवृत्ति पोर्टल",
 "category": "Education",
 "icon": "🎓",
 "keywords": ["student", "education", "scholarship", "छात्र", "शिक्षा", "study", "college"],
 "eligibility": "Students from class 1 to post-graduation based on merit and income",
 "eligibility_hi": "कक्षा 1 से पोस्ट ग्रेजुएशन तक के छात्र योग्यता और आय के आधार पर",
 "benefit": "Financial assistance for education",
 "benefit_hi": "शिक्षा खर्च के लिए वित्तीय सहायता",
 "how_to_apply": "Register on scholarships.gov.in with required documents",
 "how_to_apply_hi": "scholarships.gov.in पर आवश्यक दस्तावेजों के साथ पंजीकरण करें",
 "link": "https://scholarships.gov.in/"
 },
 {
 "name": "Skill India",
 "name_hi": "स्किल इंडिया",
 "category": "Employment",
 "icon": "🛠️",
 "keywords": ["job", "skill", "training", "unemployed", "नौकरी", "work", "employment", "रोजगार"],
 "eligibility": "Job seekers aged 15-45 years",
 "eligibility_hi": "15-45 साल के नौकरी खोजने वाले",
 "benefit": "Free skill training and job placement",
 "benefit_hi": "मुफ्त कौशल प्रशिक्षण और नौकरी सहायता",
 "how_to_apply": "Visit skillindia.gov.in and enroll in courses",
 "how_to_apply_hi": "skillindia.gov.in पर जाकर कोर्स में नामांकन करें",
 "link": "https://skillindia.gov.in/"
 },
 {
 "name": "PM Jan Dhan Yojana",
 "name_hi": "पीएम जन धन योजना",
 "category": "Banking",
 "icon": "🏦",
 "keywords": ["bank", "account", "dhan", "खाता", "banking", "savings"],
 "eligibility": "All Indian citizens without bank account",
 "eligibility_hi": "बिना बैंक खाते वाले सभी भारतीय नागरिक",
 "benefit": "Zero balance account with RuPay debit card and insurance",
 "benefit_hi": "जीरो बैलेंस खाता RuPay डेबिट कार्ड और बीमा के साथ",
 "how_to_apply": "Visit any bank branch with Aadhaar and address proof",
 "how_to_apply_hi": "किसी भी बैंक शाखा में आधार और पते के प्रमाण के साथ जाएं",
 "link": "https://pmjdy.gov.in/"
 },
 {
 "name": "Ayushman Bharat",
 "name_hi": "आयुष्मान भारत",
 "category": "Health",
 "icon": "🏥",
 "keywords": ["health", "hospital", "स्वास्थ्य", "medical", "treatment", "इलाज", "बीमारी"],
 "eligibility": "Families with annual income less than ₹1 lakh",
 "eligibility_hi": "साल में ₹1 लाख से कम कमाने वाले परिवार",
 "benefit": "Free health coverage up to ₹5 lakh per family per year",
 "benefit_hi": "प्रति परिवार प्रति वर्ष ₹5 लाख तक मुफ्त स्वास्थ्य कवरेज",
 "how_to_apply": "Check eligibility at pmjay.gov.in and get card from nearest health center",
 "how_to_apply_hi": "pmjay.gov.in पर पात्रता जांचें और नजदीकी स्वास्थ्य केंद्र से कार्ड प्राप्त करें",
 "link": "https://pmjay.gov.in/"
 }
]

def tr(en, hi):
 return hi if st.session_state.lang == "हिंदी" else en

def find_schemes(query):
 query_lower = query.lower()
 matches = []
 for scheme in SCHEMES:
 score = sum(1 for kw in scheme["keywords"] if kw.lower() in query_lower) * 20
 if score > 0:
 scheme_copy = scheme.copy()
 scheme_copy["score"] = score
 matches.append(scheme_copy)
 if not matches:
 matches = [s.copy() for s in SCHEMES]
 for m in matches:
 m["score"] = 50
 matches.sort(key=lambda x: x["score"], reverse=True)
 return matches

def answer_question(query):
 query_lower = query.lower()
 
 if any(word in query_lower for word in ["eligibility", "पात्रता", "eligible", "qualify", "कौन", "किसके लिए"]):
 scheme = find_schemes(query)[0]
 name = scheme["name_hi"] if st.session_state.lang == "हिंदी" else scheme["name"]
 elig = scheme["eligibility_hi"] if st.session_state.lang == "हिंदी" else scheme["eligibility"]
 ans = tr(
 f"**{name}**: Eligible are - {elig}. Perfect for you if this matches!",
 f"**{name}**: पात्र हैं - {elig}। अगर यह आपके लिए है तो शानदार!"
 )
 return ans, scheme
 
 elif any(word in query_lower for word in ["benefit", "लाभ", "मिलता", "मिलेगा", "get", "फायदा", "पाएंगे"]):
 scheme = find_schemes(query)[0]
 name = scheme["name_hi"] if st.session_state.lang == "हिंदी" else scheme["name"]
 benefit = scheme["benefit_hi"] if st.session_state.lang == "हिंदी" else scheme["benefit"]
 ans = tr(
 f"**{name}**: You get - {benefit}. Great benefits awaiting you!",
 f"**{name}**: आपको मिलेगा - {benefit}। शानदार लाभ आपका इंतज़ार कर रहे हैं!"
 )
 return ans, scheme
 
 elif any(word in query_lower for word in ["apply", "आवेदन", "कैसे", "how", "process", "तरीका"]):
 scheme = find_schemes(query)[0]
 name = scheme["name_hi"] if st.session_state.lang == "हिंदी" else scheme["name"]
 how = scheme["how_to_apply_hi"] if st.session_state.lang == "हिंदी" else scheme["how_to_apply"]
 ans = tr(
 f"**{name}**: Application steps - {how}. Easy process, just follow these steps!",
 f"**{name}**: आवेदन प्रक्रिया - {how}। आसान प्रक्रिया है, बस इन चरणों को फॉलो करें!"
 )
 return ans, scheme
 
 else:
 schemes = find_schemes(query)
 return None, schemes[:3]

if "lang" not in st.session_state:
 st.session_state.lang = "English"
if "messages" not in st.session_state:
 st.session_state.messages = []

st.markdown("""<style>.stApp { background: linear-gradient(135deg, #04111d 0%, #0a1f33 100%); }</style>""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
 st.session_state.lang = st.selectbox(tr("Language", "भाषा"), ["English", "हिंदी"])

st.title(tr("🤖 Government Schemes Chatbot", "🤖 सरकारी योजना चैटबॉट"))
st.caption(tr("Ask me anything about government schemes!", "मुझसे सरकारी योजनाओं के बारे में कुछ भी पूछें!"))

for msg in st.session_state.messages:
 with st.chat_message(msg["role"]):
 st.markdown(msg["content"])
 if "scheme" in msg and msg["scheme"]:
 scheme = msg["scheme"]
 with st.expander(tr("📋 View Full Details", "📋 पूरा विवरण देखें")):
 name = scheme["name_hi"] if st.session_state.lang == "हिंदी" else scheme["name"]
 st.subheader(f"{scheme['icon']} {name}")
 elig = scheme["eligibility_hi"] if st.session_state.lang == "हिंदी" else scheme["eligibility"]
 benefit = scheme["benefit_hi"] if st.session_state.lang == "हिंदी" else scheme["benefit"]
 how = scheme["how_to_apply_hi"] if st.session_state.lang == "हिंदी" else scheme["how_to_apply"]
 st.write(f"**{tr('Eligibility', 'पात्रता')}:** {elig}")
 st.write(f"**{tr('Benefit', 'लाभ')}:** {benefit}")
 st.write(f"**{tr('How to Apply', 'कैसे आवेदन करें')}:** {how}")
 st.link_button(tr("Apply Now ↗", "अभी आवेदन करें ↗"), scheme["link"])

if prompt := st.chat_input(tr("Ask: eligibility, benefits, how to apply...", "पूछें: पात्रता, लाभ, कैसे आवेदन करें...")):
 st.session_state.messages.append({"role": "user", "content": prompt})
 
 with st.chat_message("user"):
 st.markdown(prompt)
 
 with st.chat_message("assistant"):
 with st.spinner(tr("Thinking...", "सोच रहा हूं...")):
 answer, scheme_data = answer_question(prompt)
 
 if answer:
 st.markdown(answer)
 st.session_state.messages.append({
 "role": "assistant",
 "content": answer,
 "scheme": scheme_data
 })
 else:
 msg = tr(
 f"I found **{len(scheme_data)} schemes** that might help:",
 f"मैंने **{len(scheme_data)} योजनाएं** ढूंढी जो मदद कर सकती हैं:"
 )
 schemes_list = ""
 for idx, s in enumerate(scheme_data, 1):
 name = s["name_hi"] if st.session_state.lang == "हिंदी" else s["name"]
 schemes_list += f"\n{idx}. {s['icon']} **{name}** ({s['category']})"
 full_msg = msg + schemes_list
 st.markdown(full_msg)
 st.session_state.messages.append({
 "role": "assistant",
 "content": full_msg,
 "scheme": None
 })
