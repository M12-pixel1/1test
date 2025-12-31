# tools.py
def get_available_tools():
    return ["view_image", "web_search", "code_execution", "static_analysis"]

# Stub tool'ai (vėliau pakeisime į tikrus)
def view_image_tool(**kwargs):
    return "Vaizdas analizuotas – matomas gyvūnas su simptomais"

def web_search_tool(**kwargs):
    return "Rasta VETIS info apie simptomą"

def code_execution_tool(**kwargs):
    return "Kodas paleistas sėkmingai"

def static_analysis_tool(**kwargs):
    return "Kodo analizė: jokių klaidų"
# multimodal_tool.py
import requests
import base64
from io import BytesIO

def analyze_image_with_grok(image_bytes: bytes, prompt: str = "Aprašyk gyvūno simptomus ir galimas ligas") -> str:
    api_key = st.secrets["grok_api_key"]  # arba env
    url = "https://api.x.ai/v1/chat/completions"
    
    # Encode image
    buffered = BytesIO(image_bytes)
    img = Image.open(buffered)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    payload = {
        "model": "grok-beta",  # arba grok-vision jei yra
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
            ]}
        ]
    }
    
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# Naudojimas app'e
if uploaded_image:
    result = analyze_image_with_grok(uploaded_image.getvalue(), f"Gyvūnas: {animal_type}. Simptomai: {symptoms}")
    st.write(result)
