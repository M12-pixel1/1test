import streamlit as st
from PIL import Image

st.title("Rūpestėlis Vet AI – Greitoji pagalba gyvūnams 🐾")

st.write("**Sveiki!** Įkelk gyvūno foto (visa + skauda dalis) ir atsakyk į klausimus – gausi preliminarią analizę. **Visada kreipkis pas veterinarą – tai ne diagnozė!**")

uploaded_file = st.file_uploader("Įkelk foto", type=["jpg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto", use_column_width=True)
    
    st.write("### Klausimai")
    gyvuno_tipas = st.selectbox("Tipas", ["Šuo", "Katė", "Kiaulė", "Karvė", "Paukštis", "Žuvis", "Kitas"])
    veisle = st.text_input("Veislė (AI nustatys iš foto, bet patikslink jei žinai)")
    amzius = st.text_input("Amžius (apytiksliai)")
    svoris = st.text_input("Svoris (kg, apytiksliai)")
    simptomas = st.text_area("Simptomai")
    aplinka = st.text_area("Aplinka")
    garsai = st.text_input("Garsai/elgesys")
    palpacija = st.text_input("Užčiuopėte gumbelį? (Taip/Ne)")
    if palpacija == "Taip":
        dydis = st.text_input("Dydis (žirnio, riešuto)")

    if st.button("Analizuoti"):
        # Placeholder – vėliau realus ML
        st.write("**AI nustatė veislę:** Labrador Retriever (90% tikimybė)")
        st.write("**Preliminari analizė:**")
        st.write("1. 75% – Dermatitas")
        st.write("   Kuo gydoma: Higiena + antimikrobiniai šampūnai (chlorheksidinas), bet tik pas vet.")
        st.write("2. 55% – Alergija")
        st.write("   Kuo gydoma: Antihistamininiai, bet tik pas vet.")
        st.error("**Nedelsiant pas veterinarą – tai tik gairės!**")
else:
    st.info("Įkelk foto!")

st.caption("Powered by Grok 🚀")
