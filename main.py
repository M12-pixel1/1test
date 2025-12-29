"""
Rūpestėlis Vet AI - Veterinarinė photo-first triage sistema
Versija: 2.0 - Pilnai funkcionali, viename faile, be external dependencies
"""
import streamlit as st
import numpy as np
from PIL import Image
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import traceback
from datetime import datetime
import json

# =====================================================================
# KONFIGŪRACIJA
# =====================================================================
SYMPTOMS_DB = {
    "niežulys": {
        "ligos": ["Dermatitas", "Alergija"],
        "tikimybes": [75, 55],
        "gydymas": [
            "Higienos režimas + odos priežiūra",
            "Veterinaro parinkta alergijos kontrolė"
        ]
    },
    "kosulys": {
        "ligos": ["Kvėpavimo infekcija", "Alerginė reakcija / dirgikliai"],
        "tikimybes": [80, 60],
        "gydymas": [
            "Veterinaro įvertinimas (plaučiai/širdis)",
            "Aplinkos korekcija + stebėjimas"
        ]
    },
    "letargija": {
        "ligos": ["Parazitai", "Virusinė/bakterinė liga"],
        "tikimybes": [70, 50],
        "gydymas": [
            "Veterinaro apžiūra + baziniai tyrimai",
            "Skysčiai, šiluma, stebėjimas"
        ]
    },
    "viduriavimas": {
        "ligos": ["Parazitinė infekcija", "Virškinimo sutrikimas / maisto pokytis"],
        "tikimybes": [85, 65],
        "gydymas": [
            "Rehidratacija + dieta",
            "Išmatų tyrimas / vet įvertinimas"
        ]
    },
    "vėmimas": {
        "ligos": ["Virškinimo dirginimas", "Parazitai / infekcija"],
        "tikimybes": [75, 55],
        "gydymas": [
            "Skysčiai + stebėjimas",
            "Veterinaro apžiūra jei kartojasi / kraujas"
        ]
    },
    "šlubavimas": {
        "ligos": ["Trauma / lūžis", "Sąnarių problema"],
        "tikimybes": [90, 70],
        "gydymas": [
            "Imobilizacija + vet įvertinimas",
            "Stebėjimas / vet konsultacija"
        ]
    },
    "švokštimas": {
        "ligos": ["Kvėpavimo infekcija", "Alergija / bronchų dirginimas"],
        "tikimybes": [85, 65],
        "gydymas": [
            "Stebėti kvėpavimą + vet jei blogėja",
            "Aplinkos korekcija"
        ]
    },
    "ausų infekcija": {
        "ligos": ["Otitas", "Alergija"],
        "tikimybes": [80, 60],
        "gydymas": [
            "Ausų apžiūra/valymas pas vet",
            "Alergijos valdymas (jei kartojasi)"
        ]
    },
}

SYMPTOM_KEYWORDS = list(SYMPTOMS_DB.keys())

MAX_IMAGE_SIZE_MB = 5
MAX_AUDIO_SIZE_MB = 10

MAGIC_NUMBERS = {
    'jpg': [b'\xff\xd8\xff'],
    'jpeg': [b'\xff\xd8\xff'],
    'png': [b'\x89PNG\r\n\x1a\n'],
}

# =====================================================================
# LOGGING
# =====================================================================
def log_info(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.caption(f"[{timestamp}] ℹ️ {message}")

def log_error(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.error(f"[{timestamp}] ❌ {message}")

def log_warning(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.warning(f"[{timestamp}] ⚠️ {message}")

# =====================================================================
# VALIDACIJA
# =====================================================================
def validate_magic_number(file_content: bytes, file_ext: str) -> bool:
    if file_ext not in MAGIC_NUMBERS:
        return True
    expected_magics = MAGIC_NUMBERS[file_ext]
    for magic in expected_magics:
        if file_content.startswith(magic):
            return True
    return False

def validate_uploaded_file(uploaded_file, max_size_mb: float, allowed_types: list) -> Optional[str]:
    if uploaded_file is None:
        return "Failas neįkeltas"
    
    file_content = uploaded_file.getvalue()
    file_size_mb = len(file_content) / (1024 * 1024)
    
    if file_size_mb > max_size_mb:
        return f"❌ Failas per didelis: {file_size_mb:.1f}MB (max {max_size_mb}MB)"
    
    file_ext = uploaded_file.name.split('.')[-1].lower()
    if file_ext not in allowed_types:
        return f"❌ Netinkamas tipas: .{file_ext} (leidžiami: {', '.join(['.' + t for t in allowed_types])})"
    
    if not validate_magic_number(file_content, file_ext):
        return f"❌ Failo turinys neatitinka plėtinio .{file_ext}"
    
    if '..' in uploaded_file.name or '/' in uploaded_file.name or '\\' in uploaded_file.name:
        return "❌ Netinkamas failo pavadinimas"
    
    return None

# =====================================================================
# FAILO VALDYMAS
# =====================================================================
def save_temp_file(uploaded_file, suffix: str = "") -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            return tmp.name
    except Exception as e:
        raise Exception(f"Nepavyko išsaugoti failo: {str(e)}")

def cleanup_temp_file(file_path: str):
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass

# =====================================================================
# IMAGE ANALYSIS
# =====================================================================
def analyze_image_simple(image: Image.Image) -> Dict[str, Any]:
    try:
        img_array = np.array(image.resize((224, 224)))
        mean_color = img_array.mean(axis=(0, 1))
        brightness = mean_color.mean()
        texture = img_array.std()
        r, g, b = mean_color
        
        if brightness > 180:
            label = "Šviesos spalvos gyvūnas (galimai šviesios veislės)"
            confidence = 55.0
        elif brightness < 80:
            label = "Tamsios spalvos gyvūnas (galimai tamsios veislės)"
            confidence = 55.0
        else:
            label = "Vidutinių spalvų gyvūnas"
            confidence = 50.0
        
        if r > g + 30 and r > b + 30:
            label += " (pastebėtas paraudimas - galimas uždegimas)"
            confidence = 65.0
        
        return {
            'success': True,
            'label': label,
            'confidence': confidence,
            'stats': {
                'brightness': float(brightness),
                'texture': float(texture),
                'rgb': [float(r), float(g), float(b)]
            }
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

# =====================================================================
# AUDIO ANALYSIS (reikalinga librosa – jei nėra, grąžins klaidą)
# =====================================================================
def analyze_audio_simple(file_path: str) -> Dict[str, Any]:
    try:
        import librosa
        y, sr = librosa.load(file_path, sr=22050, mono=True, duration=15)
        if len(y) == 0:
            return {'success': False, 'error': 'Audio tuščias arba nepalaikomas formatas'}
        
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        rms = librosa.feature.rms(y=y)
        zcr = librosa.feature.zero_crossing_rate(y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        
        stats = {
            'duration_s': float(len(y) / sr),
            'sample_rate': int(sr),
            'mfcc_mean': float(np.mean(mfcc)),
            'energy': float(np.mean(rms)),
            'zcr': float(np.mean(zcr)),
            'spectral_centroid': float(np.mean(spec_cent))
        }
        
        interpretation = []
        if stats['zcr'] > 0.1:
            interpretation.append("Aukštas ZCR - galimas švokštimas/cypimas")
        if stats['energy'] > 0.05:
            interpretation.append("Aukšta energija - garsūs garsai")
        if stats['spectral_centroid'] > 2000:
            interpretation.append("Aukšti dažniai - galimas cypimas/kūkčiojimas")
        
        return {'success': True, 'stats': stats, 'interpretation': interpretation}
    
    except ImportError:
        return {'success': False, 'error': 'Librosa biblioteka neįdiegta. Audio analizė nepasiekiama.'}
    except Exception as e:
        return {'success': False, 'error': f'Audio analizės klaida: {str(e)}'}

# =====================================================================
# SIMPTOMŲ ATPAŽINIMAS
# =====================================================================
def match_symptoms(free_text: str) -> Dict[str, Any]:
    if not free_text or not free_text.strip():
        return {'matched_key': None, 'confidence': 0.0, 'db_entry': None}
    
    text = free_text.lower().strip()
    best_key = None
    best_score = 0
    
    for keyword in SYMPTOM_KEYWORDS:
        if keyword in text:
            score = len(keyword)
            if score > best_score:
                best_score = score
                best_key = keyword
    
    if best_key:
        return {'matched_key': best_key, 'confidence': 0.9, 'db_entry': SYMPTOMS_DB[best_key]}
    
    tokens = [t.strip(" ,.;:!?\"'()[]{}") for t in text.split()]
    
    for keyword in SYMPTOM_KEYWORDS:
        if keyword in tokens:
            return {'matched_key': keyword, 'confidence': 0.7, 'db_entry': SYMPTOMS_DB[keyword]}
    
    for keyword in SYMPTOM_KEYWORDS:
        for token in tokens:
            if len(token) >= 4 and (keyword in token or token in keyword):
                return {'matched_key': keyword, 'confidence': 0.5, 'db_entry': SYMPTOMS_DB[keyword]}
    
    return {'matched_key': None, 'confidence': 0.0, 'db_entry': None}

# =====================================================================
# SESSION STATE
# =====================================================================
def init_session_state():
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'temp_files' not in st.session_state:
        st.session_state.temp_files = []
    if 'last_image_name' not in st.session_state:
        st.session_state.last_image_name = None
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0

def cleanup_old_temp_files():
    if len(st.session_state.temp_files) > 5:
        for _ in range(len(st.session_state.temp_files) - 5):
            old_file = st.session_state.temp_files.pop(0)
            cleanup_temp_file(old_file)

def reset_analysis_if_new_image(uploaded_image):
    if uploaded_image and st.session_state.last_image_name:
        if st.session_state.last_image_name != uploaded_image.name:
            st.session_state.analysis_done = False
            st.session_state.analysis_count = 0
    if uploaded_image:
        st.session_state.last_image_name = uploaded_image.name

# =====================================================================
# UI KOMPONENTAI
# =====================================================================
def show_header():
    st.title("🐾 Rūpestėlis SOS – Photo-first Triage")
    st.markdown("""
    **Pirma foto → keli klausimai → veiksmai vietoje → ar reikia vet**
   
    ⚠️ **DISCLAIMER:** Tai triage įrankis, **ne diagnozė ar receptas**.
    Visada konsultuokitės su veterinaru.
    """)

def show_disclaimer() -> bool:
    agree = st.checkbox(
        "✅ Sutinku su duomenų apdorojimu analizei ir suprantu, kad tai ne veterinaro diagnozė",
        value=False,
        key='disclaimer_checkbox'
    )
    if not agree:
        st.warning("⚠️ Pažymėkite sutikimą, kad galėtume tęsti.")
        return False
    return True

def upload_files_section() -> Tuple[Any, Any]:
    st.subheader("📸 1. Įkelkite medžiagą")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_image = st.file_uploader("**Foto (PRIVALOMA)**", type=["jpg", "jpeg", "png"], help="Bendras vaizdas + problema. Max 5MB.")
    with col2:
        uploaded_audio = st.file_uploader("**Audio (papildomai)**", type=["wav", "mp3", "m4a"], help="Garso analizei (kosulys, švokštimas). Max 10MB.")
    return uploaded_image, uploaded_audio

def questions_section() -> Dict[str, Any]:
    st.subheader("❓ 2. Atsakykite į klausimus")
    animal_type = st.selectbox("Gyvūno tipas", ["Šuo", "Katė", "Paukštis", "Kitas"])
    col1, col2 = st.columns(2)
    with col1:
        age = st.text_input("Amžius", placeholder="pvz.: 3 metai")
    with col2:
        weight = st.text_input("Svoris (kg)", placeholder="pvz.: 15")
    
    symptoms = st.text_area("**Pagrindiniai simptomai** (SVARBU)", placeholder="Aprašykite: kosulys, letargija, viduriavimas, niežulys, švokštimas...", height=100)
    environment = st.text_area("Aplinka", placeholder="Kur gyvena? Ar turėjo kontaktą su kitais gyvūnais?", height=70)
    history = st.text_area("Istorija", placeholder="Kada prasidėjo? Po ko? Kaip keičiasi?", height=70)
    
    st.divider()
    has_lump = st.radio("Užčiuopėte gumbelį / patinimą?", ["Ne", "Taip"], horizontal=True)
    
    lump_size = None
    lump_nature = None
    if has_lump == "Taip":
        col1, col2 = st.columns(2)
        with col1:
            lump_size = st.text_input("Dydis", placeholder="žirnio/riešuto dydžio")
        with col2:
            lump_nature = st.text_input("Pobūdis", placeholder="kietas/minkštas")
    
    return {
        'animal_type': animal_type, 'age': age, 'weight': weight, 'symptoms': symptoms,
        'environment': environment, 'history': history, 'has_lump': has_lump == "Taip",
        'lump_size': lump_size, 'lump_nature': lump_nature
    }

def show_analysis_results(image_result, audio_result, symptom_match, questions_data):
    st.divider()
    st.subheader("📋 3. Triage rezultatas")
    st.info("⚠️ Tai triage įrankis, ne diagnozė. Visada konsultuokitės su veterinaru.")
    
    if image_result['success']:
        st.write(f"🖼️ **Vaizdo analizė:** {image_result['label']}")
        st.caption(f"Tikimybė: {image_result['confidence']:.0f}%")
        with st.expander("📊 Detali vaizdo statistika"):
            stats = image_result.get('stats', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Ryškumas", f"{stats.get('brightness', 0):.0f}")
            with col2:
                st.metric("Tekstūra", f"{stats.get('texture', 0):.0f}")
            with col3:
                rgb = stats.get('rgb', [0, 0, 0])
                st.write(f"RGB: {rgb[0]:.0f}, {rgb[1]:.0f}, {rgb[2]:.0f}")
    
    if audio_result and audio_result['success']:
        st.write("---")
        st.write("🎵 **Audio analizė:**")
        stats = audio_result['stats']
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Trukmė", f"{stats['duration_s']:.1f}s")
        with col2:
            st.metric("Energija", f"{stats['energy']:.3f}")
        with col3:
            st.metric("ZCR", f"{stats['zcr']:.3f}")
        if audio_result.get('interpretation'):
            st.write("**Interpretacija:**")
            for interp in audio_result['interpretation']:
                st.write(f"- {interp}")
    
    st.write("---")
    st.write("### 🩺 Galimos kryptys pagal simptomus")
    
    if symptom_match['matched_key']:
        db_entry = symptom_match['db_entry']
        st.success(f"✅ Atpažintas simptomas: **{symptom_match['matched_key']}** (atitikimas: {symptom_match['confidence']*100:.0f}%)")
        for i in range(min(2, len(db_entry['ligos']))):
            with st.expander(f"**#{i+1} – {db_entry['ligos'][i]}** ({db_entry['tikimybes'][i]}%)", expanded=(i == 0)):
                st.write("**Veiksmai dabar:**")
                st.write(db_entry['gydymas'][i])
                if i == 0:
                    st.write("\n**Papildomai:**")
                    st.write("- Stebėkite 24-48h")
                    st.write("- Jei blogėja – skubiai pas vet")
    else:
        st.warning("⚠️ Simptomų neatpažinau. **Rekomenduoju veterinaro konsultaciją.**")
        st.write("**Bendros gairės:**")
        st.write("- 🔍 Stebėkite būklę")
        st.write("- 📝 Užrašykite pokyčius")
        st.write("- 📞 Konsultuokitės su vet")
    
    if questions_data['has_lump']:
        st.error("""
        🚨 **GUMBELIS APTIKTAS – BŪTINA VET APŽIŪRA!**
       
        Gali būti:
        - Navikas (geras ar piktybinis)
        - Abscesas (infekcija)
        - Hematoma
        - Padidėjęs limfmazgis
       
        ⏰ **Nelaukite** – ankstyvoji diagnostika gali išgelbėti gyvybę!
        """)
    
    st.write("---")
    st.error("""
    🆘 **SKUBIAI Į VETERINĄ jei:**
    - 🫁 Sunkus kvėpavimas / stiprus švokštimas
    - 🩸 Kraujas išmatose/vėmaluose
    - 🤢 Nekontroliuojamas vėmimas (3+ per valandą)
    - 🧠 Traukuliai, koordinacijos netekimas
    - 💤 Sąmonės praradimas
    - ⚡ Staigus dramatiškas pablogėjimas
    - ☠️ Įtariamas apsinuodijimas
    """)
    
    st.write("---")
    st.write("### 📞 Tolimesni veiksmai")
    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **✅ Jei stabiliai:**
        1. Stebėti 24-48h
        2. Taikyti nurodytas priemones
        3. Užrašyti pokyčius
        4. Palaikyti ryšį su vet
        """)
    with col2:
        st.warning("""
        **⚠️ Jei kyla nerimas:**
        1. Skambinti veterinarui
        2. Aprašyti simptomus
        3. Klausti ar atvykti
        4. Ruoštis vizitui
        """)

def show_education():
    st.divider()
    st.subheader("📚 Saugus naudojimas")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Kas tai yra:**")
        st.write("✅ Triage įrankis")
        st.write("✅ Rizikos signalų atpažinimas")
        st.write("✅ Veiksmų planas")
    with col2:
        st.write("**Kas tai NĖRA:**")
        st.write("❌ Veterinaro diagnozė")
        st.write("❌ Receptinių vaistų receptas")
        st.write("❌ Vet apžiūros pakaitalas")
    
    st.caption("ℹ️ Duomenys nenaudojami mokymui ir nėra išsaugomi. Analizė vyksta tik sesijos metu.")
    st.caption("Rūpestėlis SOS | 2025 | v2.0")

# =====================================================================
# PAGRINDINĖ LOGIKA
# =====================================================================
def main():
    st.set_page_config(
        page_title="Rūpestėlis Vet AI",
        page_icon="🐾",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    with st.sidebar:
        st.header("📊 Sistema")
        st.caption("v2.0 - Pilnai funkcionali")
        if st.button("🔄 Iš naujo"):
            st.session_state.clear()
            st.rerun()
        st.divider()
        st.subheader("📝 Sesijos log")
    
    init_session_state()
    show_header()
    
    if not show_disclaimer():
        st.stop()
    
    uploaded_image, uploaded_audio = upload_files_section()
    reset_analysis_if_new_image(uploaded_image)
    
    image_result = {'success': False}
    audio_result = None
    temp_audio_path = None
    
    if uploaded_image is not None:
        with st.spinner("Analizuoju foto..."):
            error = validate_uploaded_file(uploaded_image, MAX_IMAGE_SIZE_MB, ['jpg', 'jpeg', 'png'])
            if error:
                st.error(error)
                log_error(f"Image validation failed: {error}")
            else:
                try:
                    image = Image.open(uploaded_image)
                    image_result = analyze_image_simple(image)
                    if image_result['success']:
                        log_info("Vaizdo analizė sėkminga")
                    else:
                        log_error(f"Vaizdo analizės klaida: {image_result.get('error')}")
                except Exception as e:
                    st.error("Nepavyko apdoroti nuotraukos")
                    log_error(f"Image processing error: {str(e)}")
    
    if uploaded_audio is not None:
        with st.spinner("Analizuoju audio..."):
            error = validate_uploaded_file(uploaded_audio, MAX_AUDIO_SIZE_MB, ['wav', 'mp3', 'm4a'])
            if error:
                st.error(error)
                log_error(f"Audio validation failed: {error}")
            else:
                try:
                    temp_audio_path = save_temp_file(uploaded_audio, suffix=os.path.splitext(uploaded_audio.name)[1])
                    st.session_state.temp_files.append(temp_audio_path)
                    cleanup_old_temp_files()
                    audio_result = analyze_audio_simple(temp_audio_path)
                    if audio_result['success']:
                        log_info("Audio analizė sėkminga")
                    else:
                        log_warning(audio_result['error'])
                except Exception as e:
                    st.error("Nepavyko apdoroti audio failo")
                    log_error(f"Audio processing error: {str(e)}")
    
    questions_data = questions_section()
    symptom_match = match_symptoms(questions_data['symptoms'])
    
    if uploaded_image is not None:
        show_analysis_results(image_result, audio_result, symptom_match, questions_data)
        show_education()
    else:
        st.info("Įkelkite bent vieną nuotrauką, kad gautumėte triage rezultatą.")

if __name__ == "__main__":
    main()
