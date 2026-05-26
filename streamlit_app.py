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
        "istorie": "Istoria este studiul trecutului, bazat pe documente, artefacte și alte surse.",
        "geografie": "Geografia este știința care studiază suprafața Pământului, clima, populația și resursele naturale.",
        "stiinta": "Știința este cunoașterea sistematică a lumii fizice sau materiale, obținută prin observație și experimentare.",
        "internet": "Internetul este o rețea globală de calculatoare interconectate, care permite comunicarea și accesul la informații.",
        "economie": "Economia este știința care studiază producția, distribuția și consumul de bunuri și servicii.",
        "politica": "Politica este procesul de luare a deciziilor pentru un grup sau o societate.",
        "psihologie": "Psihologia este știința care studiază comportamentul uman și procesele mentale.",
        "sociologie": "Sociologia este studiul societății umane, al relațiilor sociale și al instituțiilor.",
        "limba": "Limba este un sistem de comunicare bazat pe cuvinte și reguli gramaticale.",
        "arta": "Arta este o gamă variată de activități umane care implică creația de obiecte vizuale, auditive sau interpretative.",
        "filosofie": "Filosofia este studiul problemelor fundamentale legate de existență, cunoaștere, valori, rațiune, minte și limbaj.",
        "galaxie": "O galaxie este un sistem uriaș de stele, planete, gaze și praf cosmic. Galaxia noastră se numește Calea Lactee.",
        "dinozaur": "Dinozaurii au fost reptile care au dominat Pământul timp de peste 160 de milioane de ani, dispărând acum 66 de milioane de ani.",
        "egipt": "Egiptul Antic a fost una dintre cele mai mari civilizații, cunoscută pentru piramide, hieroglife și faraoni. Capitala este Cairo.",
        "piramidă": "Construcție monumentală cu o bază pătrată și patru fețe triunghiulare. Cele mai faimoase sunt în Egipt.",
        "imperiul roman": "Unul dintre cele mai mari imperii din istorie, faimos pentru legiuni, drumuri și dreptul roman.",
        "primul razboi mondial": "Primul Război Mondial a avut loc între 1914 și 1918, implicând marile puteri ale lumii.",
        "al doilea razboi mondial": "Al Doilea Război Mondial a avut loc între 1939 și 1945, fiind cel mai devastator conflict din istorie.",
        "afganistan": "Țară în Asia de Sud. Capitala: Kabul.",
        "Africa de Sud": "Țară în Africa. Capitala: Pretoria (executivă), Cape Town (legislativă), Bloemfontein (judiciară).",
        "albania": "Țară în Europa de Est. Capitala: Tirana.",
        "algeria": "Țară în Africa de Nord. Capitala: Alger.",
        "andorra": "Țară mică în Europa, între Franța și Spania. Capitala: Andorra la Vella.",
        "anglia": "Parte a Regatului Unit. Capitala: Londra.",
        "arabia saudita": "Țară în Orientul Mijlociu. Capitala: Riad.",
        "argentinina": "Țară în America de Sud. Capitala: Buenos Aires.",
        "australia": "Țară și continent. Capitala: Canberra.",
        "austria": "Țară în Europa Centrală. Capitala: Viena.",
        "bangladesh": "Țară în Asia de Sud. Capitala: Dhaka.",
        "belgia": "Țară în Europa de Vest. Capitala: Bruxelles.",
        "brazilia": "Țară în America de Sud. Capitala: Brasília.",
        "bulgaria": "Țară în Europa de Est. Capitala: Sofia.",
        "canada": "Țară în America de Nord. Capitala: Ottawa.",
        "cehia": "Țară în Europa Centrală. Capitala: Praga.",
        "chile": "Țară în America de Sud. Capitala: Santiago.",
        "china": "Țară în Asia de Est. Capitala: Beijing.",
        "columbia": "Țară în America de Sud. Capitala: Bogotá.",
        "Coreea de Sud": "Țară în Asia de Est. Capitala: Seul.",
        "croația": "Țară în Europa de Est. Capitala: Zagreb.",
        "cuba": "Țară insulară în Caraibe. Capitala: Havana.",
        "danemarca": "Țară în Europa de Nord. Capitala: Copenhaga.",
        "elvetia": "Țară în Europa Centrală. Capitala: Berna.",
        "emiratele arabe unite": "Țară în Orientul Mijlociu. Capitala: Abu Dhabi.",
        "estonia": "Țară în Europa de Nord. Capitala: Tallinn.",
        "filipine": "Țară în Asia de Sud-Est. Capitala: Manila.",
        "finlanda": "Țară în Europa de Nord. Capitala: Helsinki.",
        "franta": "Țară în Europa de Vest. Capitala: Paris.",
        "germania": "Țară în Europa Centrală. Capitala: Berlin.",
        "grecia": "Țară în Europa de Sud. Capitala: Atena.",
        "india": "Țară în Asia de Sud. Capitala: New Delhi.",
        "indonezia": "Țară în Asia de Sud-Est. Capitala: Jakarta.",
        "irlanda": "Țară în Europa de Vest. Capitala: Dublin.",
        "islanda": "Țară insulară în Atlanticul de Nord. Capitala: Reykjavik.",
        "israel": "Țară în Orientul Mijlociu. Capitala: Ierusalim.",
        "italia": "Țară în Europa de Sud. Capitala: Roma.",
        "japonia": "Țară în Asia de Est. Capitala: Tokyo.",
        "mexic": "Țară în America de Nord. Capitala: Mexico City.",
        "norvegia": "Țară în Europa de Nord. Capitala: Oslo.",
        "olanda": "Țară în Europa de Vest. Capitala: Amsterdam.",
        "polonia": "Țară în Europa de Est. Capitala: Varșovia.",
        "portugalia": "Țară în Europa de Sud. Capitala: Lisabona.",
        "regatul unit": "Țară în Europa de Vest, format din Anglia, Scoția, Țara Galilor și Irlanda de Nord. Capitala: Londra.",
        "rusia": "Țară în Europa de Est și Asia de Nord. Capitala: Moscova.",
        "spania": "Țară în Europa de Sud. Capitala: Madrid.",
        "statele unite": "Țară în America de Nord. Capitala: Washington D.C.",
        "suedia": "Țară în Europa de Nord. Capitala: Stockholm.",
        "turcia": "Țară transcontinentală (Europa și Asia). Capitala: Ankara.",
        "ucraina": "Țară în Europa de Est. Capitala: Kiev.",
        "ungaria": "Țară în Europa Centrală. Capitala: Budapesta.",
        "hidrogen": "Element chimic cu simbolul H și numărul atomic 1. Este cel mai abundent element din univers.",
        "heliu": "Element chimic cu simbolul He și numărul atomic 2. Este un gaz nobil, ușor și inert.",
        "oxigen": "Element chimic cu simbolul O și numărul atomic 8. Este esențial pentru respirația majorității ființelor vii.",
        "carbon": "Element chimic cu simbolul C și numărul atomic 6. Este fundamentul chimiei organice și al vieții.",
        "fier": "Element chimic cu simbolul Fe și numărul atomic 26. Este un metal folosit pe scară largă în construcții și industrie.",
        "aur": "Element chimic cu simbolul Au și numărul atomic 79. Este un metal prețios, folosit în bijuterii și investiții.",
        "argint": "Element chimic cu simbolul Ag și numărul atomic 47. Este un metal prețios, folosit în bijuterii și industrie.",
        "azot": "Element chimic cu simbolul N și numărul atomic 7. Este principalul component al atmosferei terestre (78%).",
        "clor": "Element chimic cu simbolul Cl și numărul atomic 17. Este folosit ca dezinfectant și în tratarea apei.",
        "sodiu": "Element chimic cu simbolul Na și numărul atomic 11. Este un metal alcalin, esențial pentru organism.",
        "potasiu": "Element chimic cu simbolul K și numărul atomic 19. Este esențial pentru funcționarea celulelor.",
        "calciu": "Element chimic cu simbolul Ca și numărul atomic 20. Este esențial pentru oase și dinți.",
        "medic": "Un medic este un profesionist care diagnostichează, tratează și previne bolile.",
        "avocat": "Un avocat este un profesionist în drept care oferă consultanță juridică și reprezintă clienții în instanță.",
        "inginer": "Un inginer este un specialist care aplică cunoștințele științifice pentru a proiecta, construi și întreține structuri și mașini.",
        "profesor": "Un profesor este un cadru didactic care predă și educă elevii sau studenții.",
        "pilot": "Un pilot este o persoană care pilotează aeronave, cum ar fi avioane sau elicoptere.",
        "programator": "Un programator este un specialist care scrie cod pentru a crea software și aplicații.",
        "polițist": "Un polițist este un funcționar public responsabil cu menținerea ordinii publice și aplicarea legii.",
        "pompier": "Un pompier este un profesionist care stinge incendii și salvează vieți în situații de urgență.",
        "arhitect": "Un arhitect este un specialist care proiectează clădiri și alte structuri.",
        "artist": "Un artist este o persoană care creează opere de artă, cum ar fi picturi, sculpturi sau muzică.",
        "scriitor": "Un scriitor este o persoană care creează opere literare, cum ar fi romane, poezii sau eseuri.",
        "actor": "Un actor este o persoană care interpretează un personaj într-un film, piesă de teatru sau spectacol.",
        "muzician": "Un muzician este o persoană care cântă la un instrument sau compune muzică.",
        "fermier": "Un fermier este o persoană care cultivă pământul și crește animale pentru hrană și alte produse.",
        "pescar": "Un pescar este o persoană care prinde pești pentru consum sau comerț.",
        "sofer": "Un șofer este o persoană care conduce un vehicul, cum ar fi o mașină, camion sau autobuz.",
        "bucatar": "Un bucătar este o persoană care gătește mâncare în mod profesionist.",
        "chelner": "Un chelner este o persoană care servește mâncarea și băutura într-un restaurant.",
        "criptomoneda": "O monedă digitală descentralizată. Exemple: Bitcoin (BTC), Ethereum (ETH).",
        "bitcoin": "Prima și cea mai cunoscută criptomonedă, creată în 2009. Este limitată la 21 de milioane de unități.",
        "ethereum": "O platformă blockchain descentralizată, cunoscută pentru moneda sa Ether (ETH) și pentru contractele smart.",
        "blockchain": "Un registru digital distribuit și imutabil, folosit pentru a înregistra tranzacții într-o manieră sigură.",
        "portofel crypto": "Un portofel crypto este un instrument digital care îți permite să stochezi, trimiți și primești criptomonede.",
        "cheie privata": "O cheie privată este un cod secret care îți oferă acces la fondurile tale crypto. Nu o împărtăși niciodată!",
        "defi": "DeFi (Decentralized Finance) este un sistem financiar care funcționează fără intermediari tradiționali, pe blockchain.",
        "nft": "NFT (Non-Fungible Token) este un certificat digital de proprietate pentru un obiect unic, cum ar fi o operă de artă digitală.",
        "cum sa investesc in crypto": "Înainte de a investi în criptomonede, informează-te temeinic. Începe cu sume mici, diversifică-ți investițiile și nu investi bani pe care nu ți-i permiți să-i pierzi.",
        "risc investitii crypto": "Investițiile în criptomonede sunt extrem de volatile. Prețurile pot fluctua masiv într-un timp scurt. Nu există garanții de profit.",
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
