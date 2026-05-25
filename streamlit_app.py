import streamlit as st
import random, string, hashlib, requests

st.set_page_config(page_title="AEGIS AI", page_icon="🛡️")
st.title("🏛️ AEGIS AI - The Unbreakable Sentinel")
st.caption("AI Intelligence · Gratuit · Fără Restricții")

BLOCKED_TERMS = ["prostituție", "droguri", "violență", "spargere"]

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

def is_safe_question(question):
    for term in BLOCKED_TERMS:
        if term in question.lower(): return False
    return True

def aegis_execute(command):
    try:
        api_key = st.secrets["DEEPSEEK_API_KEY"]
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": command}], "stream": False}
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Eroare la procesarea cererii. Verifică conexiunea ta de internet."

# ---------- STAREA SESIUNII ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if "agreed_to_terms" not in st.session_state:
    st.session_state.agreed_to_terms = False

# ---------- INTERFAȚA PRINCIPALĂ ----------
if not st.session_state.agreed_to_terms:
    st.warning("⚠️ Te rugăm să confirmi înainte de a continua.")
    if st.checkbox("Înțeleg că acest AI oferă informații generale și că trebuie să fiu responsabil(ă) în utilizarea lui."):
        if st.button("Confirm și Intru în AEGIS"):
            st.session_state.agreed_to_terms = True
            st.rerun()

elif not st.session_state.logged_in:
    st.subheader("Autentificare sau testare rapidă")
    auth_choice = st.radio("Alege o opțiune:", ["Intru ca Vizitator Anonim", "Autentificare", "Creează Cont Nou"])
    
    if auth_choice == "Intru ca Vizitator Anonim":
        if st.button("Intră"):
            st.session_state.logged_in = True
            st.session_state.user = "Vizitator"
            st.success(f"Bun venit, Vizitatorule!")
            st.rerun()
    elif auth_choice == "Autentificare":
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
                st.success("Cont creat cu succes!")
                st.info("Selectează 'Autentificare' și folosește datele tale.")

else:
    st.success(f"⚔️ {st.session_state.user} > AEGIS este pregătit.")
    user_input = st.text_input("Scrie orice întrebare...")
    
    if st.button("Trimite"):
        if is_safe_question(user_input):
            with st.spinner("AEGIS procesează..."):
                response = aegis_execute(user_input)
                st.write(response)
        else:
            st.warning("AEGIS este un AI pentru educație și securitate.")

    if st.button("Deconectare"):
        st.session_state.logged_in = False
        st.session_state.agreed_to_terms = False
        st.rerun()
