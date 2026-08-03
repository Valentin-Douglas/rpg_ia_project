from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class GMOutput:
    narrativa_ic: str
    comando_ooc: str
    teste_sugerido: Optional[str] = None


class GameMaster:
    """Orquestrador do Mestre de Jogo para o RPG textual Aethelgard."""

    def __init__(self, client: Any = None, model_id: str = "gemini-2.0-flash"):
        self.client = client
        self.model_id = model_id
        self.sys_prompt = (
            "Você é o GM do RPG Isekai 'Crônicas de Aethelgard'. "
            "Responda sempre em dois blocos claros: IC e OOC. "
            "Mantenha consistência narrativa e não misture narração com instruções mecânicas."
        )
        self.last_error: Optional[str] = None
        self._api_model = None
        self._setup_api_model()

    def _setup_api_model(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self._api_model = genai.GenerativeModel(self.model_id)
        except Exception as exc:
            self.last_error = str(exc)
            self._api_model = None

    def _build_payload(self, user_input: str, character_context: Optional[dict] = None) -> dict:
        context = character_context or {}
        return {
            "prompt": user_input,
            "contexto": {
                "campanha": "Crônicas de Aethelgard",
                "personagem": context,
                "regra": "Separar narrativo IC e instruções OOC.",
            },
        }

    def _fallback_response(self, user_input: str) -> GMOutput:
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

    def _parse_response(self, raw_text: str) -> GMOutput:
        try:
            payload = json.loads(raw_text)
            return GMOutput(
                narrativa_ic=payload.get("narrativa_ic", ""),
                comando_ooc=payload.get("comando_ooc", ""),
                teste_sugerido=payload.get("teste_sugerido"),
            )
        except Exception:
            return self._fallback_response(raw_text)

    def _make_interaction_id(self, interaction_id=None) -> str:
        if interaction_id:
            return interaction_id
        return "local-interaction-1"

    def interagir(self, user_input: str, interaction_id: Optional[str] = None, character_context: Optional[dict] = None) -> tuple[GMOutput, str]:
        payload = self._build_payload(user_input, character_context)
        if self._api_model is None:
            return self._fallback_response(user_input), self._make_interaction_id(interaction_id)

        try:
            response = self._api_model.generate_content(
                f"System: {self.sys_prompt}\n\n{json.dumps(payload, ensure_ascii=False)}",
                generation_config={"response_mime_type": "application/json"},
            )
            text = getattr(response, "text", None) or ""
            return self._parse_response(text), getattr(response, "id", None) or self._make_interaction_id(interaction_id)
        except Exception as exc:
            self.last_error = str(exc)
            return self._fallback_response(user_input), self._make_interaction_id(interaction_id)
