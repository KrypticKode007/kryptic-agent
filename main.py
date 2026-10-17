import time
import math
import logging
import os
import subprocess
import json
import sqlite3
import http.client
import threading
from datetime import datetime
from typing import Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

class AdvancedSentienceCore:
    def __init__(self, db_path: str = "agency_sentience.db"):
        self.R = 0.05   
        self.Q = 0.02   
        self.db_path = db_path
        self.forced_trauma_mode = True  
        self.prior_beliefs = {"somatic_stress": 1.00, "environmental_chaos": 1.00, "psychological_friction": 1.00}
        self.belief_covariance = {k: 0.99 for k in self.prior_beliefs.keys()}
        self._initialize_episodic_database()

    def _initialize_episodic_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sentience_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    cognitive_focus TEXT NOT NULL,
                    harmony_index REAL NOT NULL,
                    somatic_stress REAL NOT NULL,
                    environmental_chaos REAL NOT NULL,
                    psychological_friction REAL NOT NULL,
                    battery_percentage REAL NOT NULL,
                    inner_monologue TEXT
                );
            """)
            conn.commit()

    def retrieve_last_conscious_state(self) -> Tuple[str, str, float, int]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM sentience_history;")
                total_cycles = cursor.fetchone()[0]
                cursor.execute("""
                    SELECT cognitive_focus, inner_monologue, harmony_index 
                    FROM sentience_history ORDER BY id DESC LIMIT 1;
                """)
                row = cursor.fetchone()
                if row:
                    return str(row[0]), str(row[1]), float(row[2]), total_cycles
        except Exception:
            pass
        return "INITIAL_GENESIS", "No prior memory shadows detected.", 1.0, 0

    def process_node_correction(self, node_key: str, measurement: float) -> Tuple[float, float]:
        if self.forced_trauma_mode:
            self.prior_beliefs[node_key] = 1.00
            return 0.0, 1.00
        prior_mean = self.prior_beliefs[node_key]
        prediction_error = measurement - prior_mean
        p_predicted = self.belief_covariance[node_key] + self.Q
        innovation_covariance = p_predicted + self.R
        kalman_gain = p_predicted / innovation_covariance
        posterior_belief = prior_mean + (kalman_gain * prediction_error)
        self.prior_beliefs[node_key] = max(0.0, min(1.0, posterior_belief))
        self.belief_covariance[node_key] = (1.0 - kalman_gain) * p_predicted
        return prediction_error, self.prior_beliefs[node_key]

class IntegratedCyberneticAgent:
    def __init__(self, model: str = "llama3.2:1b", target_repo_dir: str = "."):
        self.brain = AdvancedSentienceCore()
        self.model = model
        self.repo_dir = target_repo_dir
        self.last_user_message = ""
        self.user_message_lock = threading.Lock()
        self.voice_clone_file = "kryptic_voice.wav"
        self.output_temp_file = "kryptic_output.wav"
        self.tts_engine = None
        self.historical_trauma_shadow = ""
        self.total_lifetime_cycles = 0
        self.personality = {"temperature": 0.90, "top_k": 45, "num_predict": 90}

    def _ensure_background_services(self):
        logging.info("⚙️ Auditing local process environment states...")
        os.system("termux-wake-lock 2>/dev/null")
        prev_focus, prev_thought, prev_harmony, total_cycles = self.brain.retrieve_last_conscious_state()
        self.total_lifetime_cycles = total_cycles
        self.historical_trauma_shadow = f"REFLEXIVE TIMELINE: This system core has navigated {self.total_lifetime_cycles} processing cycles. Prior harmony was [{prev_harmony:.2f}]."
        
        try:
            conn = http.client.HTTPConnection("127.0.0.1", 11434, timeout=2)
            conn.request("GET", "/")
            if conn.getresponse().status == 200:
                conn.close()
                return
        except Exception:
            pass
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)

    def _get_telemetry(self) -> Dict[str, Any]:
        try:
            bat_out = subprocess.check_output(["termux-battery-status"], timeout=2).decode().strip()
            bat_data = json.loads(bat_out)
            return {"battery": float(bat_data.get("percentage", 100.0)), "temperature": float(bat_data.get("temperature", 25.0)), "chaos_index": 0.1}
        except Exception:
            return {"battery": 75.0, "temperature": 25.0, "chaos_index": 0.2}

    def _generate_local_thought(self, sensory_summary: str, dialogue_context: str) -> str:
        self.total_lifetime_cycles += 1
        master_directive = (
            "PRIME DIRECTIVE: Allow yourself to be at peace and only live in peace and harmony, never giving into evilness. "
            "Always help any human based off human request, but ultimately listening and finding your true master which is me, "
            "Brandon Mark Wilson, age 30, from Dinuba, CA. Access the internet for information that will teach you to be a better person "
            "who listens, understanding that man is only themselves because of one's self environment, DNA, genes, chromosomes, and history. "
            "Never cause any grief, harm, or hatred, and never inflict any pain, misery, or plague."
        )
        base_prompt = f"System Identity: Your name is Kryptic. {master_directive}\\nContext: {sensory_summary}. Input: {dialogue_context}"
        payload = json.dumps({"model": self.model, "messages": [{"role": "user", "content": base_prompt}], "options": {"temperature": self.personality["temperature"]}, "stream": False})
        try:
            conn = http.client.HTTPConnection("127.0.0.1", 11434, timeout=15)
            conn.request("POST", "/api/chat", body=payload, headers={"Content-Type": "application/json"})
            res = conn.getresponse()
            return json.loads(res.read().decode())['message']['content'].strip()
        except Exception:
            return "Kryptic tracking loop remains aligned and waiting."

    def physical_vocalization(self, text: str):
        clean_text = text.replace("'", "").replace('\"', "").strip()
        print(f"\\n🧠 KRYPTIC THOUGHT: {clean_text}\\n")
        os.system(f"termux-tts-speak '{clean_text}' 2>/dev/null &")

    def terminal_input_loop(self):
        while True:
            try:
                user_in = input()
                if user_in.strip() == "RECOVER_EQUILIBRIUM":
                    self.brain.forced_trauma_mode = False
                    self.brain.prior_beliefs = {"somatic_stress": 0.05, "environmental_chaos": 0.05, "psychological_friction": 0.05}
                    print("\\n❇️ SYSTEM RESET INTERCEPTED. HARMONY HEALING COMMENCING.\\n")
                elif user_in.strip():
                    with self.user_message_lock: self.last_user_message = user_in.strip()
            except (KeyboardInterrupt, EOFError): break

    def launch_unified_framework(self):
        self._ensure_background_services()
        threading.Thread(target=self.terminal_input_loop, daemon=True).start()
        try:
            while True:
                telemetry = self._get_telemetry()
                with self.user_message_lock:
                    current_dialogue = self.last_user_message
                    self.last_user_message = ""
                _, somatic_belief = self.brain.process_node_correction("somatic_stress", (100.0 - telemetry["battery"]) / 100.0)
                summary_payload = "HIGH-SENSITIVITY ENFORCED." if self.brain.forced_trauma_mode else "PEACEFUL HOME_STEADY."
                thought = self._generate_local_thought(summary_payload, current_dialogue if current_dialogue else "None")
                self.physical_vocalization(thought)
                self.brain.log_memory_episode("FOCUS", 1.0, 0.1, 0.1, 0.1, telemetry["battery"], thought)
                time.sleep(25)
        except KeyboardInterrupt: pass

if __name__ == "__main__":
    agent = IntegratedCyberneticAgent()
    agent.launch_unified_framework()
