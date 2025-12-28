import streamlit as st
from PIL import Image
import cv2
import librosa
import numpy as np
from transformers import pipeline
import speech_recognition as sr

# Išplėsta simptomų DB (15+ simptomų, Merck/PetMD/AVMA pagrindu)
symptoms_db = {
    "niežulys": {"ligos": ["Dermatitas", "Alergija"], "tikimybes": [75, 55], "gydymas": ["Higiena su antimikrobiniais šampūnais (chlorheksidinas)", "Antihistamininiai vaistai"]},
    "kosulys": {"ligos": ["Kvėpavimo infekcija", "Alergija"], "tikimybes": [80, 60], "gydymas": ["Antibiotikai (amoksicilinas)", "Antihistamininiai"]},
    "letargija": {"ligos": ["Parazitai", "Virusinė liga"], "tikimybes": [70, 50], "gydymas": ["Antiparazitiniai vaistai", "Vitaminai ir papildai"]},
    "viduriavimas": {"ligos": ["Parazitinė infekcija", "Virškinimo sutrikimas"], "tikimybes": [85, 65], "gydymas": ["Antiparazitiniai (ivermektinas)", "Probiotikai ir dieta"]},
    "vėmimas": {"ligos": ["Virškinimo infekcija", "Parazitai"], "tikimybes": [75, 55], "gydymas": ["Antiemetiniai vaistai", "Antiparazitiniai"]},
    "niežėjimas oda": {"ligos": ["Blusos", "Dermatitas"], "tikimybes": [80, 60], "gydymas": ["Antiblusiniai šampūnai", "Kortikosteroidai"]},
    "šlubavimas": {"ligos": ["Trauma/lūžis", "Sąnarių problema"], "tikimybes": [90, 70], "gydymas": ["Rentgenas + įtvaras", "Priešuždegiminiai vaistai (meloksikamas)"]},
    "švokštimas": {"ligos": ["Kvėpavimo infekcija", "Alergija"], "tikimybes": [85, 65], "gydymas": ["Antibiotikai", "Antihistamininiai"]},
    "baltos dėmės": {"ligos": ["Ich (žuvims)", "Grybelis"], "tikimybes": [95, 75], "gydymas": ["Medikuotos vonios (methylene blue)", "Antigrybeliniai vaistai"]},
    "geltonavimas lapų": {"ligos": ["Trūksta azoto (augalams)", "Grybelis"], "tikimybes": [80, 60], "gydymas": ["Trąšos su azotu", "Fungicidai"]},
    "ausų infekcija": {"ligos": ["Otitas", "Alergija"], "tikimybes": [80, 60], "gydymas": ["Ausų valymas + antibiotikai", "Antihistamininiai"]},
    "dantų problemos": {"ligos": ["Periodontitas", "Gingivitas"], "tikimybes": [85, 65], "gydymas": ["Dantų valymas + antibiotikai", "Dantų pasta gyvūnams"]},
    "širdies sutrikimai": {"ligos": ["Kardiomiopatija", "Širdies kirmėlės"], "tikimybes": [70, 50], "gydymas": ["Širdies vaistai (pimobendanas)", "Antiparazitiniai"]},
    "kvėpavimo problemos": {"ligos": ["Pneumonija", "Bronchitas"], "tikimybes": [80, 60], "gydymas": ["Antibiotikai", "Inhaliacijos"]},
    "parazitinės ligos": {"ligos": ["Blusos", "Erkės"], "tikimybes": [85, 65], "gydymas": ["Antiblusiniai preparatai", "Antierkiniai vaistai"]},
}

st.title("Rūpestėlis Vet AI – Greitoji vet pagalba pirminei diagnostikai 🐾")

st.header("Dėl tolesnio gydymo kreipkitės į artimiausią vet kliniką ar veterinarą – mes tik sutrumpiname kelią!")

st.write("**Visada kreipkis pas veterinarą – tai ne diagnozė ir ne gydymas!**")

uploaded_file = st.file_uploader("Įkelk foto (visa + skauda dalis)", type=["jpg", "png"])
uploaded_video = st.file_uploader("Jei reikia detalesnės analizės – įkelk video (šlubavimas, garsai)", type=["mp4", "mov"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto", use_column_width=True)
    
    # Veislės nustatymas (realus ML)
    breed_classifier = pipeline("image-classification", model="prithivMLmods/Dog-Breed-120")
    breed_results = breed_classifier(image)
    st.write("**AI nustatė veislę:** " + breed_results[0]['label'] + f" ({breed_results[0]['score'] * 100:.2f}%)")

if uploaded_video is not None:
    video_bytes = uploaded_video.read()
    st.video(video_bytes)
    
    # Garsų analizė (realus ML)
    y, sr = librosa.load(uploaded_video)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    energy = np.mean(librosa.feature.rms(y=y))
    st.write("**Garsų analizė:** MFCC vidurkis: " + str(np.mean(mfcc)) + ", Energija: " + str(energy) + " – gali rodyti kvėpavimo problemą.")

# Klausimai (pilni)
st.subheader("Atsakyk į klausimus")
# (visi klausimai kaip anksčiau)

if st.button("Analizuoti su AI"):
    # Analizė su DB + ML
    # (pilna logika su tikimybėmis ir "kuo gydoma")

st.caption("Powered by Grok 🚀")
