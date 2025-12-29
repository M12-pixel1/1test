"""
Rūpestėlis Vet AI - Veterinarinė photo-first triage sistema
Versija: 4.5 Final | 2025
ATNAUJINTA: Patikimesnis simptomų atpažinimas, normalizacija
"""
import streamlit as st
import numpy as np
from PIL import Image
import io
import re

# === LAZY IMPORTAI ===
def load(name):
    try:
        if name == "yolo": return __import__("ultralytics").YOLO("yolov8n.pt")
        if name == "torch":
            torch = __import__("torch")
            transforms = __import__("torchvision.transforms")
            models = __import__("torchvision").models
            model = models.resnet50(weights="IMAGENET1K_V1")
            model.eval()
            return model, transforms
        if name == "ocr": return __import__("easyocr").Reader(['en','lt'], gpu=False)
        if name == "moviepy": return __import__("moviepy.editor").editor.VideoFileClip
    except Exception as e:
        st.caption(f"℗ {name} neįdiegta arba klaida")
        return None

# === NORMALIZUOTAS TEKSTAS ===
def normalize(text):
    clean = re.sub(r'[^a-ząčęėįšųūž0-9 ]+', '', text.lower())
    return re.sub(r'\s+', ' ', clean).strip()

# === VETIS_DB (sutrumpintas demonstracijai) ===
VETIS_DB = {
    "universal": {
        "niežulys": {
            "ligos": ["Blusos/erkės", "Maisto alergija", "Atopinis dermatitas", "Grybelis"],
            "gydymas": ["Frontline/Advantix", "Hipoalerginė dieta 8-12 sav.", "Apoquel/Cytopoint", "Vet odos tyrimas"]
        }
    },
    "dog": {
        "kosulys": {
            "ligos": ["Kennel cough", "Širdies kirmėlės"],
            "gydymas": ["Doxycycline", "Heartgard"],
            "vakcinacija": "Bordetella + Nobivac KC"
        }
    }
    # ... visa kita duomenų bazė
}

# === ANALIZĖ ===
def analyze(file_bytes: bytes) -> dict:
    result = {"animal": "nežinomas", "species": "Nežinoma", "tag": "", "image_info": ""}
    yolo = load("yolo")
    if yolo:
        img = Image.open(io.BytesIO(file_bytes))
        res = yolo(img, verbose=False)[0]
        if res.boxes:
            cls = int(res.boxes[0].cls[0])
            animal_map = {14:"bird",15:"cat",16:"dog",17:"rabbit",18:"sheep",20:"cow",21:"pig"}
            result["animal"] = animal_map.get(cls, "kita")

            box = res.boxes[0].xyxy[0].cpu().numpy()
            crop = img.crop(box)

            ocr = load("ocr")
            if ocr and result["animal"] in ["cow","sheep","goat","pig"]:
                text = ocr.readtext(np.array(crop), detail=0)
                tags = [t.upper() for t in text if t.isalnum() and 4<=len(t)<=12]
                if tags: result["tag"] = max(tags, key=len)
    return result

# === UI ===
st.set_page_config(page_title="Rūpestėlis Vet AI", page_icon="🐾", layout="centered")

st.title("🐾 Rūpestėlis Vet AI v4.5")

if not st.checkbox("✅ Sutinku, kad tai ne veterinaro diagnozė"): 
    st.stop()

uploaded = st.file_uploader("**Įkelkite foto arba video**", type=["jpg","jpeg","png","mp4"])
if not uploaded:
    st.info("Įkelkite bent vieną failą")
    st.stop()

symptoms = st.text_area("**Simptomai**")
lump = st.radio("Ar yra gumbas?", ["Ne", "Taip"])
submit = st.button("⚛️ Gauti rezultatą")

if submit:
    result = analyze(uploaded.getvalue())
    st.write(f"**Atpažintas gyvūnas:** {result['animal']}")

    clean_symptoms = normalize(symptoms)
    matched = None
    for db in [VETIS_DB.get(result["animal"].lower(), {}), VETIS_DB["universal"]]:
        for k in db:
            if k in clean_symptoms:
                matched = db[k]
                st.success(f"Atpažintas simptomas: {k}")
                for i, l in enumerate(matched["ligos"]):
                    st.write(f"{i+1}. {l} → {matched['gydymas'][i]}")
                if matched.get("vakcinacija"):
                    st.info(f"💉 Vakcinacija: {matched['vakcinacija']}")
                break
        if matched:
            break
    if not matched:
        st.warning("⚠️ Simptomas neatpažintas")

    if lump == "Taip":
        st.error("🚨 GUMBAS APTIKTAS – reikalinga skubi apžiūra")
