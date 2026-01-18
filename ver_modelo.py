import google.generativeai as genai

# PEGA AQUÍ LA API KEY DE TU IMAGEN
GOOGLE_API_KEY = 'TU API AQUI'

genai.configure(api_key=GOOGLE_API_KEY)

print("--- BUSCANDO MODELOS DISPONIBLES ---")
try:
    for m in genai.list_models():
        # Filtramos solo los modelos que sirven para generar texto (chat)
        if 'generateContent' in m.supported_generation_methods:
            print(f"- Encontrado: {m.name}")
except Exception as e:
    print(f"Error al conectar: {e}")