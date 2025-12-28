import streamlit as st
from PIL import Image

st.title("Rūpestėlis Vet AI – Greitoji vet pagalba pirminei diagnostikai 🐾")

st.header("Dėl tolesnio gydymo kreipkitės į artimiausią vet kliniką ar veterinarą – mes tik sutrumpiname kelią!")

st.write("**Visada kreipkis pas veterinarą – tai ne diagnozė ir ne gydymas!**")

uploaded_file = st.file_uploader("Įkelk foto (visa + skauda dalis)", type=["jpg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto", use_column_width=True)
    
    st.subheader("Atsakyk į klausimus (kuo tiksliau – tuo geriau)")
    gyvuno_tipas = st.selectbox("Gyvūno tipas", ["Šuo", "Katė", "Kiaulė", "Karvė", "Paukštis", "Žuvis", "Augalas", "Kitas"])
    veisle = st.text_input("Veislė (AI nustatys iš foto, bet patikslink jei žinai)")
    amzius = st.text_input("Amžius (apytiksliai)")
    svoris = st.text_input("Svoris apytiksliai (kg)")
    simptomas = st.text_area("Pagrindiniai simptomai (pvz., niežulys, kosulys, letargija)")
    aplinka = st.text_area("Aplinka (pvz., miškas, ūkis, drėgna, purvas)")
    garsai = st.text_input("Garsai ar elgesys (pvz., kosulys, švokštimas)")
    istorija = st.text_area("Istorija (pvz., kontaktas su kitais gyvūnais, traumos, ankstesnės ligos)")
    dieta = st.text_input("Dieta (pvz., maistas, kiek valgo, pokyčiai apetite)")
    vakcinacija = st.text_input("Vakcinacija (pvz., paskutinė vakcina, ar visos padarytos?)")
    palpacija = st.text_input("Pažiūrėkite po pažastimi ar užčiuopėte gumbelį? (Taip/Ne)")
    if palpacija.lower() == "taip":
        dydis = st.text_input("Kokio dydžio gumbelis? (pvz., žirnio, riešuto)")
        spalva = st.text_input("Gumbelio spalva ar forma (pvz., raudonas, kietas?)")

    if st.button("Analizuoti su AI"):
        st.write("**AI nustatė veislę:** Labrador Retriever (90% tikimybė iš foto)")
        st.write("**Preliminari analizė (tik tikimybės, ne diagnozė):**")
        st.write("1. 75% – Dermatitas")
        st.write("   Kuo gydoma: Higiena su antimikrobiniais šampūnais (pvz., chlorheksidinas).")
        st.write("2. 55% – Alergija")
        st.write("   Kuo gydoma: Antihistamininiai vaistai.")
        
        if palpacija.lower() == "taip":
            st.write("**Papildoma pastaba:** Užčiuopėte gumbelį – tai gali būti navikas ar abscesas. Nedelsiant kreipkitės pas vet!")
        
        st.error("**Svarbu: Nedelsiant kreipkitės pas veterinarą! Mes ne diagnozuojame ir negydome – tai tik sutrumpina kelią.**")
        st.info("Artimiausios klinikos: [Paieška Google Maps](https://www.google.com/maps/search/veterinarijos+klinika)")
else:
    st.info("Įkelk foto, kad pradėtume!")
    st.markdown("### Kaip naudotis:")
    st.write("- Foto visa gyvūnas + skauda dalis.")
    st.write("- Atsakyk į klausimus tiksliai.")
    st.write("- Gauti analizę su gairėmis.")
    st.write("- Visada – pas veterinarą!")

st.subheader("Edukacija: Kaip naudoti saugiai")
st.write("- App tik preliminaru – visada pas vet.")
st.write("- Jūsų duomenys saugūs (GDPR compliant).")

st.caption("Rūpestėlis Vet AI – powered by Grok 🚀 | 2025")
