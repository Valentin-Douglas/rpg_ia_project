try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover - fallback simples para ambientes sem pydantic
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        @classmethod
        def model_json_schema(cls):
            return {}

        @classmethod
        def model_validate_json(cls, data):
            import json

            if isinstance(data, (bytes, bytearray)):
                data = data.decode("utf-8")
            payload = json.loads(data)
            return cls(**payload)

    def Field(*args, **kwargs):
        return None


class GMOutput(BaseModel):
    narrativa_ic: str = Field(description="Texto imersivo para o jogador.")
    comando_ooc: str = Field(description="Instruções mecânicas ou análise do sistema.")
    teste_sugerido: str | None = Field(default=None, description="Ex: 'Força + Briga'")


class GameMaster:
    def __init__(self, client=None):
        self.client = client
        self.model_id = "gemini-3.6-flash"
        self.sys_prompt = "Você é o GM do RPG Isekai 'Crônicas de Aethelgard'. Separe IC de OOC."
        self.last_error = None

    def _fallback_response(self, user_input):
        prompt = (user_input or "").strip() or "uma ação vaga"
        return GMOutput(
            narrativa_ic=(
                f"O cenário ecoa a ação '{prompt}' com uma atmosfera de mistério e tensão."
            ),
            comando_ooc=(
                "Ação interpretada em modo local. Conecte a API do Gemini para gerar respostas mais ricas."
            ),
            teste_sugerido="Teste de coragem",
        )

    def interagir(self, user_input, interaction_id=None):
        """Retorna a resposta do GM, usando fallback local quando a API não estiver disponível."""
        if self.client is not None and hasattr(self.client, "interactions"):
            try:
                response = self.client.interactions.create(
                    model=self.model_id,
                    system_instruction=self.sys_prompt,
                    input=user_input,
                    previous_interaction_id=interaction_id,
                    response_format={
                        "type": "text",
                        "mime_type": "application/json",
                        "schema": GMOutput.model_json_schema(),
                    },
                )
                self.last_error = None
                return GMOutput.model_validate_json(response.output_text), response.id
            except Exception as exc:
                self.last_error = str(exc)

        return self._fallback_response(user_input), self._make_interaction_id(interaction_id)

    def _make_interaction_id(self, interaction_id=None):
        if interaction_id:
            return interaction_id
        return "local-interaction-1"