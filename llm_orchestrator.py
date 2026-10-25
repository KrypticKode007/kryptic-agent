import json
import logging
import requests

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [OLLAMA-ORCHESTRATOR] %(message)s')

class CognitiveBridgeEngine:
    """Interfaces with a local Ollama endpoint to process and refine the agent's internal monologue."""
    def __init__(self, model_name: str = "llama3", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.endpoint = f"{host}/api/generate"

    def process_internal_reflection(self, current_telemetry_summary: str) -> str:
        """Routes raw telemetry summaries to the local model to generate structured reflections."""
        prompt = (
            f"Context: You are Kryptic, an autonomous cybernetic agent built by Brandon Mark Wilson. "
            f"Current telemetry: {current_telemetry_summary}. "
            f"Generate a single-sentence internal reflection maintaining your core purpose of structural harmony."
        )
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            logging.info(f"Dispatching reflection query to local model: {self.model_name}")
            response = requests.post(self.endpoint, json=payload, timeout=5)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Nominal state alignment maintained.").strip()
        except Exception as e:
            logging.warning(f"Local Ollama endpoint offline ({e}). Utilizing deterministic fallback string.")
            
        return "Internal monologue processing nominal. Core safety bounds remain completely stable."

if __name__ == "__main__":
    # Independent diagnostic run of the orchestration module
    bridge = CognitiveBridgeEngine()
    mock_telemetry = "BPM: 80.1 | Distance to Target Signature: 12.45% | Core Stability: OPTIMAL"
    reflection = bridge.process_internal_reflection(mock_telemetry)
    print(f"\nGenerated Reflection Output:\n-> {reflection}\n")
        
