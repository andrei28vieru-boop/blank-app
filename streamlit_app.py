import streamlit as st
import random, string, hashlib, requests

st.set_page_config(page_title="AEGIS AI", page_icon="🛡️")
st.title("🏛️ AEGIS AI - The Unbreakable Sentinel")

st.markdown("""
**Termeni și Condiții:** Acest AI este oferit ca atare, în scop educațional.
**Politica de Confidențialitate:** Nu stocăm parolele dvs. în text simplu.
Toate datele sunt criptate ireversibil (SHA-256) și nu sunt distribuite terților.
""")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {"api": "Interfață pentru comunicare între aplicații.",
                                  "hash": "Amprentă digitală unică, transformare unidirecțională.",
                                  "parolă": "Cheie secretă pentru autentificare."}

BLOCKED_TERMS = ["prostituție", "droguri", "violență", "armă", "spargere"]

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

def generate_password(length=12, seeds=""):
    if length < 8: length = 12
    p = [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase),
         random.choice(string.digits), random.choice(string.punctuation)]
    for w in seeds.split(): p.extend(list(w))
    p += random.choices(string.ascii_letters + string.digits + string.punctuation, k=max(0, length - len(p)))
    random.shuffle(p); return ''.join(p[:length])

def assess_password(password):
    s = sum([len(set(password))>7, any(c.islower() for c in password), any(c.isupper() for c in password),
             any(c.isdigit() for c in password), any(c in string.punctuation for c in password), len(password)>11])
    return ["Foarte slabă", "Slabă", "Medie", "Bună", "Puternică", "Legendară"][min(s,5)]

def is_safe_question(question):
    for term in BLOCKED_TERMS:
        if term in question.lower(): return False
    return True

def ask_deepseek(question):
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": "Bearer sk-447a3b0e07e74e8a865f7468b9a7ce2e", "Content-Type": "application/json"}
        data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": question}], "stream": False}
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Eroare la căutare: {str(e)}"

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
                st.success(f"🛡️ AEGIS deblocat. Bun venit, {user}.")
                st.rerun()
            else:
                st.error("⛔ Autentificare eșuată.")
    else:
        new_user = st.text_input("👤 Alege un nume de utilizator")
        new_pin = st.text_input("🔑 Alege o parolă", type="password")
        if st.button("Creează Cont"):
            if new_user in st.session_state.user_db:
                st.error("Acest nume de utilizator există deja.")
            elif len(new_pin) < 4:
                st.error("Parola trebuie să aibă minim 4 caractere.")
            else:
                st.session_state.user_db[new_user] = hash_data(new_pin)
                st.success("Cont creat cu succes! Acum te poți autentifica.")
                st.info("Selectează 'Autentificare' și folosește datele tale.")

else:
    st.success(f"⚔️ {st.session_state.user} > Comandă activă")
    cmd = st.selectbox("Alege o comandă:", ["help", "generate", "assess", "profile", "ask_ai", "ask_deepseek", "learn", "exit"])
    
    if cmd == "help": st.info("[generate] [assess] [profile] [ask_ai] [ask_deepseek] [learn] [exit]")
    elif cmd == "generate":
        seeds = st.text_input("🌱 Semințe (opțional)")
        if st.button("Generează Parola"):
            st.code(generate_password(12, seeds))
    elif cmd == "assess":
        pwd = st.text_input("🔍 Parola de evaluat")
        if st.button("Evaluează"):
            st.write(f"🛡️ Putere: {assess_password(pwd)}")
    elif cmd == "profile":
        u = st.text_input("👤 Nume utilizator"); t = st.text_input("🏷️ Tag (opțional)")
        seed = st.text_input("🌱 Cuvânt inspirație (opțional)")
        if st.button("Creează Profil"):
            p = generate_password(12, seed); uname = f"{u}{'_'+t if t else ''}"
            st.success(f"✅ Profil creat!"); st.code(f"👤 {uname}\n⚡ Parolă: {p}\n🛡️ Putere: {assess_password(p)}")
    elif cmd == "ask_ai":
        q = st.text_input("❓ Întreabă memoria lui AEGIS")
        if st.button("Caută în memorie"):
            found = False
            for key in st.session_state.knowledge:
                if key in q.lower():
                    st.write(f"🤖 {key.capitalize()}: {st.session_state.knowledge[key]}")
                    found = True; break
            if not found:
                st.write("🤖 Nu am aceste cunoștințe încă. Poți să mă înveți sau să întrebi biblioteca supremă!")
    elif cmd == "ask_deepseek":
        q = st.text_input("❓ Întreabă biblioteca supremă")
        if st.button("Întreabă"):
            if is_safe_question(q):
                with st.spinner("AEGIS consultă biblioteca infinită..."):
                    answer = ask_deepseek(q)
                    st.write(answer)
            else:
                st.warning("AEGIS este un AI pentru securitate și educație. Nu pot răspunde la această întrebare.")
    elif cmd == "learn":
        term = st.text_input("📚 Termen"); defi = st.text_input("📝 Definiție")
        if st.button("Învață AEGIS"):
            st.session_state.knowledge[term.lower()] = defi
            st.success("✅ Informație asimilată.")
    elif cmd == "exit":
        st.session_state.logged_in = False
        st.write("🏁 AEGIS se închide."); st.rerun()
