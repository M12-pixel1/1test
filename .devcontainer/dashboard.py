"""
Rūpestėlio Vet AI Dashboard v1.8 – Veikia 100% su foto ir analize
"""
import streamlit as st
import requests
import base64
from PIL import Image
import io
from datetime import datetime

st.set_page_config(page_title="Rūpestėlis Vet AI", page_icon="🐾", layout="centered")

st.title("🐾 Rūpestėlis Vet AI")
st.markdown("**Photo-first veterinarinė triage sistema**")

# ==================== MULTIMODALINĖ ANALIZĖ ====================
def grok_analyze(image_bytes: bytes, symptoms: str) -> str:
    try:
        api_key = st.secrets.get("grok_api_key")
        if not api_key:
            return "⚠️ Grok API key nerastas – įkelk į Streamlit Cloud Secrets"
        
        url = "https://api.x.ai/v1/chat/completions"
        img_base64 = base64.b64encode(image_bytes).decode()
        
        prompt = f"""
Analizuok gyvūno sveikatą pagal nuotrauką.
Papildomi simptomai: {symptoms or "neaprašyti"}
Atsakyk lietuviškai, aiškiai, su rekomendacijomis.
        """
        
        payload = {
            "model": "grok-beta",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                ]
            }],
            "temperature": 0.3
        }
        
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(url, json=payload, headers=headers, timeout=40)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API klaida: {response.status_code} – {response.text}"
    except Exception as e:
        return f"Analizės klaida: {str(e)}"

# ==================== UI ====================
uploaded_image = st.file_uploader(
    "**Įkelkite gyvūno foto** (privaloma)", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Įkeltas foto", use_column_width=True)
else:
    st.info("Įkelkite foto, kad pradėtume analizę")
    st.stop()

symptoms = st.text_area(
    "**Aprašykite simptomus** (neprivaloma, bet rekomenduojama)", 
    placeholder="pvz.: niežulys, kosulys, letargija, mastitas...",
    height=120
)

lump = st.radio("Ar matote/užčiuopiate gumbą?", ["Ne", "Taip"])

if st.button("🚀 Analizuoti su Grok AI", type="primary", use_container_width=True):
    with st.spinner("Grok AI analizuoja vaizdą ir simptomus..."):
        image_bytes = uploaded_image.getvalue()
        result = grok_analyze(image_bytes, symptoms)
        
        st.markdown("### 🧠 Grok AI analizė")
        st.write(result)
        
        if lump == "Taip":
            st.error("🚨 **GUMBAS APTIKTAS – SKUBI VETERINARO APŽIŪRA!**")

st.caption("Rūpestėlis Vet AI v1.8 | Realus Grok multimodal | 2025")
