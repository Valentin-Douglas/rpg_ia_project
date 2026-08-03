import os

try:
    from google import genai
except Exception as exc:  # pragma: no cover - ambiente sem SDK
    genai = None
    print(f"google-genai não disponível: {exc}")

try:
    from google.colab import userdata
except Exception:  # pragma: no cover - ambiente local
    class _UserData:
        @staticmethod
        def get(key):
            return os.getenv(key)

    userdata = _UserData()


def get_client():
    if genai is None:
        return None

    api_key = userdata.get("GOOGLE_API_KEY") or userdata.get("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception as exc:
        print(f"Não foi possível iniciar o cliente Gemini: {exc}; usando modo local.")
        return None


client = get_client()
if client is None:
    print("Ambiente preparado para execução local sem conexão com a API Gemini.")
else:
    print("Ambiente preparado com o SDK google-genai.")
