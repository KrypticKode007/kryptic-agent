#!/usr/bin/env python3
"""
Module: llm_orchestrator.py
Branch: feature/ascendant-core-integration

Orchestrates local Ollama inference and external OpenAI API hooks, mapping 
cognitive responses directly into the agent's core internal monologue tracking cycles.
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional

# Dynamic orchestration library tracking block
try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install --quiet requests")
    import requests

class CognitiveBridgeEngine:
    """Manages dual LLM API integration workflows for the Kryptic Agent architecture."""
    def __init__(self, use_local_ollama: bool = True):
        self.use_local = use_local_ollama
        self.ollama_endpoint = "http://localhost:11434/api/generate"
        self.openai_endpoint = "https://openai.com"
        self.openai_key = os.environ.get("OPENAI_API_KEY", "")

    def process_cognitive_cycle(self, system_prompt: str, active_thought: str) -> str:
        """Routes execution state prompts to local models or external fallbacks based on environment rules."""
        if self.use_local:
            return self._query_local_ollama(system_prompt, active_thought)
        return self._query_openai_api(system_prompt, active_thought)

    def _query_local_ollama(self, system: str, prompt: str) -> str:
        """Executes a local inference pipeline cycle via Ollama (Default Model: llama3)."""
        payload = {
            "model": "llama3",
            "prompt": f"System: {system}\nContext: {prompt}\nAgent Reflection:",
            "stream": False,
            "options": {"temperature": 0.2}
        }
        try:
            response = requests.post(self.ollama_endpoint, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            return "Local inference loop timed out. Routing internal monologue to fallback rules."
        except Exception:
            return "Local network bridge offline. Transitioning to baseline rules."

    def _query_openai_api(self, system: str, prompt: str) -> str:
        """Executes cloud-based narrative processing cycles via OpenAI API endpoints."""
        if not self.openai_key:
            return "OpenAI authorization credentials missing. Internal monologue clamped."
        
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        try:
            response = requests.post(self.openai_endpoint, headers=headers, json=payload, timeout=12)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            return f"OpenAI interface error: Code {response.status_code} received."
        except Exception as err:
            return f"Cloud completion failure: {str(err)}"

# =====================================================================
# SYSTEM MAIN ENGINE INTEGRATION PREVIEW
# =====================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("⚡ TESTING COGNITIVE BRIDGE ORCHESTRATION PIPELINES")
    print("=" * 70)
    
    bridge = CognitiveBridgeEngine(use_local_ollama=True)
    
    system_rules = "You are the internal monologue engine of a self-healing cybernetic agent. Respond in 1 brief sentence."
    current_state = "IM-FIN node indicates stamina is 42.5. Drone battery level operational at 75%."
    
    print("[*] Testing local Ollama communication node...")
    test_reflection = bridge.process_cognitive_cycle(system_rules, current_state)
    print(f"[+] Output Monologue Reflection:\n    \"{test_reflection}\"")
    print("=" * 70)
      
