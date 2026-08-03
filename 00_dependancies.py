# Instalação e atualização do SDK unificado google-genai
!pip install -U google-genai pydantic
import os
from google import genai
from google.colab import userdata

# O identificador 'GOOGLE_API_KEY' deve estar configurado nos Secrets do Colab [6].
api_key = userdata.get('GOOGLE_API_KEY')
client = genai.Client(api_key=api_key)
print("Ambiente preparado com o SDK google-genai.")