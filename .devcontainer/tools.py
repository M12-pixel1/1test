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
