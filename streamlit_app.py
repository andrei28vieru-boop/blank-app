import streamlit as st
import random, string, hashlib, requests

st.set_page_config(page_title="AEGIS AI", page_icon="🛡️")
st.title("🏛️ AEGIS AI - The Unbreakable Sentinel")

# ---------- FILTRU DE SIGURANȚĂ ----------
BLOCKED_TERMS = ["prostituție", "droguri", "violență", "spargere"]

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

def is_safe_question(question):
    for term in BLOCKED_TERMS:
        if term in question.lower(): return False
    return True

def ask_deepseek(question, mode="fast"):
    try:
        # Cheia API este acum direct în cod, nu mai e nevoie de Secrets
        api_key = "sk-447a3b0e07e74e8a865f7468b9a7ce2e"
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        system_message = "Ești AEGIS, un asistent AI creat de Andrei Vieru."
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
        return "🤖 AEGIS: Momentan am o mică problemă de conexiune. Verifică internetul și încearcă din nou."

# ---------- GESTIUNEA SESIUNII ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "search_mode" not in st.session_state:
    st.session_state.search_mode = "fast"

# ---------- AUTENTIFICARE ----------
if not st.session_state.logged_in:
    st.subheader("Autentificare sau Înregistrare")
    auth_choice = st.radio("Alege o opțiune:", ["Autentificare", "Creează Cont Nou"])
    
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
                st.info("Selectează 'Autentificare' și folosește datele tale.")

# ---------- INTERFAȚA PRINCIPALĂ (CA DEEPSEEK) ----------
else:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.caption(f"Conectat ca: {st.session_state.user}")
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
                with st.spinner(f"AEGIS se gândește..."):
                    response = ask_deepseek(prompt, st.session_state.search_mode)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
