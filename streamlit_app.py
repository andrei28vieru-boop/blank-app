import streamlit as st
import random, string, hashlib

st.set_page_config(page_title="AEGIS AI", page_icon="⚡")
st.title("AEGIS AI")
st.caption("Advanced Engineered General Intelligence System")

BLOCKED_TERMS = ["prostituție", "droguri", "violență", "spargere", "furt"]

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

def is_safe_question(question):
    for term in BLOCKED_TERMS:
        if term in question.lower(): return False
    return True

if "knowledge" not in st.session_state:
    st.session_state.knowledge = {
        "api": "Un API (Application Programming Interface) este un set de reguli care permite două aplicații software să comunice între ele.",
        "hash": "Un hash este o amprentă digitală unică, rezultatul unei funcții matematice care transformă datele într-un șir de caractere.",
        "python": "Python este un limbaj de programare versatil, folosit în dezvoltarea web, știința datelor și inteligența artificială.",
        "aegis": "AEGIS este un AI creat de Andrei Vieru, un sistem avansat de inteligență artificială.",
        "românia": "România este o țară situată în Europa de Est. Capitala este București.",
        "univers": "Universul este tot ceea ce există: spațiu, timp, materie și energie. Se estimează că are o vechime de 13,8 miliarde de ani.",
        "soare": "Soarele este steaua din centrul sistemului nostru solar. Este o minge uriașă de plasmă fierbinte.",
        "planetă": "O planetă este un corp ceresc care orbitează o stea. În sistemul nostru solar sunt 8 planete.",
        "medicina": "Medicina este știința și practica de a diagnostica, trata și preveni bolile.",
        "sport": "Sportul este o activitate fizică competitivă sau recreativă.",
        "muzica": "Muzica este arta de a combina sunete într-o manieră plăcută sau expresivă.",
        "tehnologie": "Tehnologia este aplicarea cunoștințelor științifice pentru scopuri practice.",
        # --- ȚĂRI ȘI CAPITALE ---
        "afganistan": "Țară în Asia de Sud. Capitala: Kabul.",
        "albania": "Țară în Europa de Est. Capitala: Tirana.",
        "germania": "Țară în Europa Centrală. Capitala: Berlin.",
        "japonia": "Țară în Asia de Est. Capitala: Tokyo.",
        "brazilia": "Țară în America de Sud. Capitala: Brasília.",
        "canada": "Țară în America de Nord. Capitala: Ottawa.",
        # --- ELEMENTE CHIMICE ---
        "hidrogen": "Element chimic cu simbolul H și numărul atomic 1. Este cel mai abundent element din univers.",
        "oxigen": "Element chimic cu simbolul O și numărul atomic 8. Este esențial pentru respirația majorității ființelor vii.",
        "aur": "Element chimic cu simbolul Au și numărul atomic 79. Este un metal prețios, folosit în bijuterii și investiții.",
        # --- PROFESII ---
        "medic": "Un medic este un profesionist care diagnostichează, tratează și previne bolile.",
        "avocat": "Un avocat este un profesionist în drept care oferă consultanță juridică și reprezintă clienții în instanță.",
        "inginer": "Un inginer este un specialist care aplică cunoștințele științifice pentru a proiecta, construi și întreține structuri și mașini.",
        "profesor": "Un profesor este un cadru didactic care predă și educă elevii sau studenții.",
        "programator": "Un programator este un specialist care scrie cod pentru a crea software și aplicații.",
        # --- CRIPTOMONEDE ---
        "criptomoneda": "O monedă digitală descentralizată. Exemple: Bitcoin (BTC), Ethereum (ETH).",
        "bitcoin": "Prima și cea mai cunoscută criptomonedă, creată în 2009. Este limitată la 21 de milioane de unități.",
        "ethereum": "O platformă blockchain descentralizată, cunoscută pentru moneda sa Ether (ETH) și pentru contractele smart.",
        "blockchain": "Un registru digital distribuit și imutabil, folosit pentru a înregistra tranzacții într-o manieră sigură.",
        "cum sa investesc in crypto": "Înainte de a investi în criptomonede, informează-te temeinic. Începe cu sume mici, diversifică-ți investițiile și nu investi bani pe care nu ți-i permiți să-i pierzi.",
    }

def get_smart_response(question):
    q = question.lower()
    for key in st.session_state.knowledge:
        if key in q:
            return st.session_state.knowledge[key]
    return f"Nu am informații specifice despre '{question}' în baza mea de date. Însă poți căuta pe Google sau Wikipedia pentru mai multe detalii."

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.logged_in:
    st.subheader("Autentificare")
    auth_choice = st.radio("Opțiuni:", ["Autentificare", "Creează Cont Nou"])
    
    if auth_choice == "Autentificare":
        user = st.text_input("👤 Utilizator")
        pin = st.text_input("🔑 Parolă", type="password")
        if st.button("Autentificare"):
            if user in st.session_state.user_db and st.session_state.user_db[user] == hash_data(pin):
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success(f"Bun venit, {user}.")
                st.rerun()
            else:
                st.error("Autentificare eșuată.")
    else:
        new_user = st.text_input("👤 Alege un nume de utilizator")
        new_pin = st.text_input("🔑 Alege o parolă", type="password")
        if st.button("Creează Cont"):
            if new_user in st.session_state.user_db: st.error("Acest nume de utilizator există deja.")
            elif len(new_pin) < 4: st.error("Parola trebuie să aibă minim 4 caractere.")
            else:
                st.session_state.user_db[new_user] = hash_data(new_pin)
                st.success("Cont creat! Acum te poți autentifica.")

else:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.caption(f"Conectat: {st.session_state.user}")
    with col2:
        if st.button("➕ Nou"):
            st.session_state.messages = []
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Scrie un mesaj..."):
        if not is_safe_question(prompt):
            st.warning("AEGIS este un AI pentru educație și securitate.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                response = get_smart_response(prompt)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
