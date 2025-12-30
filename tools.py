# tools.py
def get_available_tools():
    return ["view_image", "web_search", "code_execution", "static_analysis"]

# Paprasti tool stub'ai (realiam – integruok tikrus)
def view_image_tool(image_path: str = ""):
    return f"Vaizdas analizuotas: {image_path or 'bendras vaizdas'} – matomas gyvūnas su simptomais"

def web_search_tool(query: str = ""):
    return f"Paieška '{query}' – rasta VETIS info apie simptomus"

def code_execution_tool(code: str = ""):
    return f"Kodas paleistas: {code[:50]}... – sėkmingai"

def static_analysis_tool(code: str = ""):
    return "Static analysis: jokių klaidų"
