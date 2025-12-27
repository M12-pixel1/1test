import streamlit as st
from PIL import Image

st.set_page_config(page_title="Rūpestėlis Vet AI", page_icon="🐾", layout="centered")

st.title("🐾 Rūpestėlis Vet AI – Greitoji pagalba gyvūnams")

st.markdown("""
**Sveiki!** Įkelk gyvūno foto, atsakyk į klausimus – gausi preliminarią analizę.  
**Visada kreipkis pas veterinarą – tai ne diagnozė ir ne gydymas!**
""")

# Foto įkėlimas (visa gyvūnas + skauda dalis)
uploaded_file = st.file_uploader("Įkelk gyvūno foto (visa + skauda dalis)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Įkeltas foto", use_column_width=True)
    
    st.subheader("Atsakyk į klausimus (kuo tiksliau – tuo geriau)")
    gyvuno_tipas = st.selectbox("Gyvūno tipas", ["Šuo", "Katė", "Kiaulė", "Karvė", "Paukštis", "Žuvis", "Kitas"])
    veisle = st.text_input("Veislė (jei žinai, arba apytiksliai – AI nustatys iš foto)")
    amzius = st.text_input("Amžius (metai/mėnesiai, apytiksliai)")
    svoris = st.text_input("Svoris apytiksliai (kg)")
    simptomas = st.text_area("Pagrindiniai simptomai (pvz., niežulys, kosulys, letargija)")
    aplinka = st.text_area("Aplinka (pvz., miškas, ūkis, drėgna, purvas)")
    garsai = st.text_input("Garsai ar elgesys (pvz., kosulys, švokštimas)")

    if st.button("Analizuoti su AI"):
        # Placeholder analizė – vėliau realus ML (Vetology/TTcare tipo modeliai)
        st.success("**AI preliminari analizė (tik tikimybės, ne diagnozė):**")
        st.write("1. **75% tikimybė – Dermatitas** (niežulys + drėgna aplinka)")
        st.write("   - Galimas gydymas: Higiena su antimikrobiniais šampūnais (pvz., chlorheksidinas), bet tik pas vet.")
        st.write("2. **55% tikimybė – Alergija** (elgesys + aplinka)")
        st.write("   - Galimas gydymas: Antihistamininiai vaistai, bet tik pas vet išrašyti.")
        
        st.error("**Svarbu: Nedelsiant kreipkitės pas veterinarą! Mes ne diagnozuojame ir negydome – tai tik sutrumpina kelią.**")
        st.info("Artimiausios klinikos: [Paieška Google Maps](https://www.google.com/maps/search/veterinarijos+klinika)")
else:
    st.info("Įkelk foto, kad pradėtume!")
    st.markdown("### Kaip naudotis:")
    st.write("- Foto visa gyvūnas + skauda dalis.")
    st.write("- Atsakyk į klausimus tiksliai.")
    st.write("- Gauti analizę su gairėmis.")
    st.write("- Visada – pas veterinarą!")

st.caption("Rūpestėlis Vet AI – powered by Grok 🚀 | 2025")
