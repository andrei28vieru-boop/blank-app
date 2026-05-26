import streamlit as st
import random, string, hashlib, requests, json

st.set_page_config(page_title="AEGIS AI", page_icon="⚡")
st.title("AEGIS AI")
st.caption("Advanced Engineered General Intelligence System")

# ==========================================
# FILTRU DE SIGURANȚĂ
# ==========================================
BLOCKED_TERMS = ["prostituție", "droguri", "violență", "spargere", "furt", "omucidere"]

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

def is_safe_question(question):
    for term in BLOCKED_TERMS:
        if term in question.lower(): return False
    return True

# ==========================================
# BIBLIOTECA SUPREMĂ DE CUNOȘTINȚE (OFFLINE)
# ==========================================
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {
        # --- Cunoștințe de Securitate ---
        "api": "Un API (Application Programming Interface) este un set de reguli care permite două aplicații software să comunice între ele.",
        "hash": "Un hash este o amprentă digitală unică, rezultatul unei funcții matematice care transformă datele într-un șir de caractere.",
        "parolă": "O parolă este o cheie secretă, formată dintr-un șir de caractere, folosită pentru autentificare și protecția conturilor.",
        "securitate cibernetică": "Practica de a proteja sistemele, rețelele și programele de atacuri digitale.",
        "aegis": "AEGIS este un AI creat de Andrei Vieru, un sistem avansat de inteligență artificială.",
        # --- Cunoștințe de Programare & Python ---
        "python": "Un limbaj de programare versatil. Resurse oficiale: [python.org](https://www.python.org)",
        "variabilă": "O variabilă este ca o cutie în care poți păstra o valoare. În Python, o creezi simplu: `x = 5`.",
        "listă": "O listă este o colecție ordonată de elemente, care poate fi modificată. Se scrie între paranteze pătrate: `[1, 2, 3]`.",
        "dicționar": "Un dicționar este o colecție de perechi cheie-valoare. Se scrie între acolade: `{'nume': 'Andrei', 'vârstă': 15}`.",
        "funcție": "O funcție este un bloc de cod reutilizabil care face o anumită sarcină. Se definește cu `def`: `def salut(): print('Salut!')`.",
        "buclă": "O buclă (loop) este o instrucțiune care repetă o bucată de cod. `for` și `while` sunt cele mai comune în Python.",
        "clasă": "O clasă (class) este un șablon pentru crearea de obiecte. Este fundamentul Programării Orientate pe Obiecte (OOP).",
        "tkinter": "Tkinter este o bibliotecă standard Python pentru crearea de interfețe grafice (GUI). Cu ea poți face ferestre, butoane și jocuri.",
        # --- Cunoștințe de Tehnologie & AI ---
        "ai": "Inteligența Artificială (AI) este simularea proceselor de inteligență umană de către mașini, în special sisteme informatice.",
        "deepseek": "DeepSeek este un asistent AI avansat, specializat în înțelegerea și generarea de text complex.",
        "npci": "NPU înseamnă Neural Processing Unit, un procesor specializat pentru accelerarea calculelor de inteligență artificială.",
        "samsung": "Samsung este o companie globală, lider în tehnologie.",
        "bixby": "Bixby este asistentul virtual inteligent de la Samsung.",
        "galaxy ai": "Galaxy AI este suita de funcții de inteligență artificială de la Samsung.",
        "galaxy watch": "Galaxy Watch este seria de ceasuri inteligente de la Samsung.",
        "galaxy book": "Galaxy Book este seria de laptopuri premium de la Samsung.",
        # --- Cunoștințe de Business & Finanțe ---
        "criptomonedă": "O monedă digitală descentralizată. Exemple: Bitcoin (BTC), Ethereum (ETH).",
        "bitcoin": "Prima și cea mai cunoscută criptomonedă, creată în 2009.",
        "blockchain": "Un registru digital distribuit și imutabil.",
        "acțiune": "O unitate de proprietate într-o companie.",
        "bursă": "O piață organizată unde se tranzacționează acțiuni.",
        "economie": "Știința care studiază producția, distribuția și consumul de bunuri și servicii.",
        # --- Cunoștințe Generale ---
        "românia": "O țară în Europa de Est. Capitala: București.",
        "imperiul roman": "Unul dintre cele mai mari imperii din istorie.",
        "piramidă": "Construcție monumentală. Cele mai faimoase sunt în Egipt.",
        "limbaje de programare": "Cele mai populare limbaje de programare sunt Python, JavaScript, Java, C, C++, C#, Go, Rust, Swift și Kotlin.",
    }

# ==========================================
# CONEXIUNEA LA DEEPSEEK (ONLINE)
# ==========================================
def ask_deepseek(question, mode="fast"):
    try:
        api_key = "sk-447a3b0e07e74e8a865f7468b9a7ce2e"
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        system_message = "Ești AEGIS, un sistem AI avansat creat de Andrei Vieru."
        if mode == "expert":
            system_message += " Oferă răspunsuri extrem de detaliate, tehnice și precise."
        elif mode == "thing":
            system_message += " Analizează cu atenție orice link sau document primit și oferă un rezumat structurat."
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": question}
            ],
            "stream": False
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return None

# ==========================================
# ABILITATEA DE A CĂUTA PE TOT INTERNETUL
# ==========================================
def search_web(question):
    try:
        api_key = "9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b"
        url = "https://serpapi.com/search"
        params = {
            "q": question,
            "api_key": api_key,
            "engine": "google"
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if "organic_results" in data:
            results = data["organic_results"][:3]
            answer = "Iată ce am găsit pe internet:\n\n"
            for i, res in enumerate(results, 1):
                answer += f"{i}. **{res['title']}**\n   {res['snippet']}\n   Link: {res['link']}\n\n"
            return answer
        else:
            return "Nu am găsit informații relevante pe internet."
    except:
        return None

# ==========================================
# GESTIUNEA SESIUNII (MEMORIE)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "search_mode" not in st.session_state:
    st.session_state.search_mode = "fast"

# ==========================================
# AUTENTIFICARE
# ==========================================
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

# ==========================================
# INTERFAȚA PRINCIPALĂ
# ==========================================
else:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.caption(f"Conectat: {st.session_state.user}")
    with col2:
        mode_map = {"⚡ Fast": "fast", "🧠 Expert": "expert", "🔗 Thing": "thing"}
        selected = st.selectbox("Mod", list(mode_map.keys()), label_visibility="collapsed")
        st.session_state.search_mode = mode_map[selected]
    with col3:
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
                with st.spinner("AEGIS caută în universul digital..."):
                    response = None
                    
                    # Pasul 1: Caută în memoria offline
                    for key in st.session_state.knowledge:
                        if key in prompt.lower():
                            response = st.session_state.knowledge[key]
                            break
                    
                    # Pasul 2: Dacă nu găsește, încearcă să se conecteze la DeepSeek
                    if not response:
                        response = ask_deepseek(prompt, st.session_state.search_mode)
                    
                    # Pasul 3: Dacă nici DeepSeek nu răspunde, caută pe tot internetul
                    if not response:
                        response = search_web(prompt)
                    
                    # Pasul 4: Dacă totul eșuează, afișează o eroare prietenoasă
                    if not response:
                        response = "Momentan, toate conexiunile mele sunt întrerupte. Încearcă din nou în câteva minute."
                    
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
