import sys
import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import threading
import time

DB_PATH = "kryptic_agent_persistence.db"

class KrypticTelemetryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kryptic-Agent Edge Node Telemetry Panel")
        self.root.geometry("750x450")
        self.root.configure(bg="#070a12")
        
        # Setup modern dark style themes
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background="#070a12", foreground="#38bdf8", fieldbackground="#1e293b")
        self.style.configure("TLabel", background="#070a12", foreground="#38bdf8", font=("Courier", 11))
        
        # Heading Section
        self.title_label = tk.Label(
            root, text="KRYPTIC CYBERNETIC NODE TELEMETRY", 
            font=("Courier", 16, "bold"), bg="#070a12", fg="#38bdf8"
        )
        self.title_label.pack(pady=15)
        
        # Metadata Frame
        self.meta_frame = tk.Frame(root, bg="#070a12")
        self.meta_frame.pack(pady=5)
        self.operator_label = tk.Label(self.meta_frame, text="Operator: Brandon Mark Wilson | Location: Dinuba, CA", font=("Courier", 10), bg="#070a12", fg="#94a3b8")
        self.operator_label.pack()

        # Telemetry Content Display Cards Frame
        self.card_frame = tk.Frame(root, bg="#070a12")
        self.card_frame.pack(pady=20, fill="x", px=40)
        
        self.distance_card = self.create_metric_card(self.card_frame, "COGNITIVE DISTANCE", "12.5000%")
        self.distance_card.pack(side="left", expand=True, fill="both", mx=10)
        
        self.variance_card = self.create_metric_card(self.card_frame, "C++ MATRIX VARIANCE", "0.0000")
        self.variance_card.pack(side="left", expand=True, fill="both", mx=10)

        # Active Monologue Tracking Monitor Window
        self.log_frame = tk.LabelFrame(root, text=" Live In-Memory State Trace ", bg="#1e293b", fg="#38bdf8", font=("Courier", 10, "bold"), bd=2)
        self.log_frame.pack(pady=20, fill="both", expand=True, px=20, py=10)
        
        self.log_text = tk.Text(self.log_frame, bg="#070a12", fg="#10b981", font=("Courier", 10), state="disabled", wrap="word", bd=0)
        self.log_text.pack(fill="both", expand=True, px=10, py=10)

        # Run automated refresh daemon thread loop
        self.is_running = True
        self.refresh_thread = threading.Thread(target=self.database_refresh_loop, daemon=True)
        self.refresh_thread.start()
        
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_metric_card(self, parent, title, initial_value):
        frame = tk.LabelFrame(parent, text=f" {title} ", bg="#1e293b", fg="#94a3b8", font=("Courier", 9, "bold"), bd=1)
        label = tk.Label(frame, text=initial_value, font=("Courier", 18, "bold"), bg="#1e293b", fg="#f1f5f9")
        label.pack(pady=15, px=10)
        frame.label_ref = label  # Save reference to modify values dynamically
        return frame

    def database_refresh_loop(self):
        """Reads latest database ledger rows every second to refresh active screen variables."""
        while self.is_running:
            if os.path.exists(DB_PATH):
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT thought_vector, metric_variance FROM loop_records ORDER BY id DESC LIMIT 1")
                    row = cursor.fetchone()
                    conn.close()
                    
                    if row:
                        thought, variance = row
                        # Extract percentage safely from string formatting tracks
                        distance_str = "12.5000%"
                        if "Distance:" in thought:
                            distance_str = thought.split("Distance:")[1].split("|")[0].strip()
                        
                        # Dispatch safe updates to main Tkinter graphics context thread
                        self.root.after(0, self.update_display, distance_str, f"{variance:.4f}", thought)
                except Exception:
                    pass
            time.sleep(1.0)

    def update_display(self, distance, variance, thought):
        self.distance_card.label_ref.config(text=distance)
        self.variance_card.label_ref.config(text=variance)
        
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, f"[STATE TRACE] {thought}")
        self.log_text.config(state="disabled")

    def on_close(self):
        self.is_running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KrypticTelemetryGUI(root)
    root.mainloop()
      
