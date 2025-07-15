import logging
import subprocess
import threading
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext, ttk
import webbrowser
import os
import pyttsx3
import speech_recognition as sr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Configure logging
logging.basicConfig(
    filename="stellar_voice.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class StellarVoiceGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("StellarVoice")
        self.master.geometry("800x600")

        # Initialize text-to-speech engine
        self.engine = self._init_tts_engine()

        # State variables
        self.listening = False
        self.user_preferences = {'name': 'User', 'speech_rate': 150, 'font_size': 12, 'theme': 'light'}
        self.visualization_type = None

        # Create GUI widgets
        self.create_widgets()

        # Initial greeting
        self.assistant_speaks(f"Hello {self.user_preferences['name']}! How can I help you today?")

    def _init_tts_engine(self):
        try:
            engine = pyttsx3.init('sapi5')
            engine.setProperty("rate", self.user_preferences['speech_rate'])
            engine.setProperty("volume", 0.9)
            return engine
        except Exception as e:
            logging.error(f"Failed to initialize TTS engine: {e}")
            return None

    def create_widgets(self):
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TEntry', font=('Arial', 11))

        # Main frame
        main_frame = ttk.Frame(self.master)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Visualization canvas
        self.canvas = tk.Canvas(main_frame, bg='white', height=100)
        self.canvas.pack(fill='x', pady=(0, 10))

        # Conversation area
        self.text_area = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, state='disabled', font=('Arial', self.user_preferences['font_size']),
            bg='white', fg='black', height=20
        )
        self.text_area.pack(expand=True, fill='both')
        self.text_area.tag_config('user', foreground='#2c7be5', font=('Arial', self.user_preferences['font_size'], 'bold'))
        self.text_area.tag_config('assistant', foreground='#00ac69', font=('Arial', self.user_preferences['font_size']))
        self.text_area.tag_config('error', foreground='#e63757', font=('Arial', self.user_preferences['font_size']))

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill='x')

        self.command_entry = ttk.Entry(input_frame)
        self.command_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        self.command_entry.bind("<Return>", self.process_text_command)

        self.listen_btn = ttk.Button(input_frame, text="🎤 Listen", command=self.toggle_listening)
        self.listen_btn.pack(side='left', padx=5)

        ttk.Button(input_frame, text="⚙️ Settings", command=self.show_settings).pack(side='left', padx=5)
        ttk.Button(input_frame, text="❌ Exit", command=self.master.quit).pack(side='left')

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).pack(fill='x')

    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.listen_btn.config(text="🔴 Listening...")
            self.status_var.set("Listening...")
            threading.Thread(target=self.listen_and_process, daemon=True).start()
        else:
            self.listening = False
            self.listen_btn.config(text="🎤 Listen")
            self.status_var.set("Ready")

    def assistant_speaks(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"StellarVoice: {text}\n", 'assistant')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logging.error(f"TTS error: {e}")
                self.text_area.configure(state='normal')
                self.text_area.insert(tk.END, "Error: Could not speak text\n", 'error')
                self.text_area.configure(state='disabled')

    def user_says(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"You: {text}\n", 'user')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

    def process_text_command(self, event=None):
        command = self.command_entry.get().strip()
        self.command_entry.delete(0, tk.END)
        if command:
            self.user_says(command)
            self.execute_command(command)

    def listen_and_process(self):
        command = self.listen()
        if command:
            self.master.after(0, self.user_says, command)
            self.master.after(0, self.execute_command, command)
        self.listening = False
        self.master.after(0, lambda: self.listen_btn.config(text="🎤 Listen"))
        self.master.after(0, lambda: self.status_var.set("Ready"))

    def listen(self):
        recognizer = sr.Recognizer()
       自由

System: ogizer()
        with sr.Microphone() as source:
            self.status_var.set("Listening... Speak now")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language='en').lower()
                self.status_var.set("Processing...")
                return text
            except sr.WaitTimeoutError:
                self.status_var.set("Listening timed out")
                return None
            except sr.UnknownValueError:
                self.assistant_speaks("I didn't catch that. Please repeat.")
                return None
            except sr.RequestError as e:
                self.assistant_speaks("Could not process request; check your internet.")
                logging.error(f"Speech recognition error: {e}")
                return None

    def show_data_visualization(self, data, viz_type="bar"):
        self.canvas.delete("all")
        try:
            fig, ax = plt.subplots(figsize=(4, 1.5), dpi=100)
            fig.patch.set_facecolor('#f0f0f0')

            if viz_type == "bar":
                labels = list(data.keys())
                values = list(data.values())
                ax.bar(labels, values, color=['#2c7be5', '#00ac69'])
                ax.set_title("Results", fontsize=8)

            canvas = FigureCanvasTkAgg(fig, master=self.canvas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        except Exception as e:
            logging.error(f"Visualization error: {e}")
            self.canvas.create_text(400, 50, text="Visualization Error", font=('Arial', 12), fill='#e63757')

    def execute_command(self, command):
        command = command.lower()
        intents = {
            "open browser": lambda: subprocess.run(["start", "chrome"], shell=True),
            "time": lambda:  datetime.now().strftime("%H:%M:%S"),
            "search": lambda: self.handle_search(),
        }

        for intent, action in intents.items():
            if intent in command:
                try:
                    if intent == "time":
                        result = action()
                        self.assistant_speaks(f"The time is {result}")
                        self.canvas.delete("all")
                        self.canvas.create_text(400, 50, text=result, font=('Arial', 16), fill='#2c7be5')
                    elif intent == "search":
                        action()
                    else:
                        action()
                        self.assistant_speaks(f"Executing {intent}...")
                    self.show_data_visualization({"Action": random.randint(10, 50)}, "bar")
                except Exception as e:
                    self.assistant_speaks("Command failed.")
                    logging.error(f"Command error: {e}")
                return
        self.assistant_speaks("I didn't understand that command.")

    def handle_search(self):
        self.assistant_speaks("What do you want to search for?")
        query = self.listen()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            self.assistant_speaks(f"Searching for {query}...")
            self.show_data_visualization({"Search": random.randint(50, 100)}, "bar")

    def show_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("300x200")

        ttk.Label(settings_window, text="User Name:").pack(pady=5)
        name_entry = ttk.Entry(settings_window)
        name_entry.pack(pady=5)
        name_entry.insert(0, self.user_preferences['name'])

        ttk.Label(settings_window, text="Speech Rate:").pack(pady=5)
        rate_slider = ttk.Scale(settings_window, from_=100, to=200, orient='horizontal')
        rate_slider.pack(pady=5)
        rate_slider.set(self.user_preferences['speech_rate'])

        def save_settings():
            self.user_preferences['name'] = name_entry.get()
            self.user_preferences['speech_rate'] = int(rate_slider.get())
            if self.engine:
                self.engine.setProperty("rate", self.user_preferences['speech_rate'])
            self.assistant_speaks("Settings updated.")
            settings_window.destroy()

        ttk.Button(settings_window, text="Save", command=save_settings).pack(side='right', padx=5, pady=10)
        ttk.Button(settings_window, text="Cancel", command=settings_window.destroy).pack(side='right', padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        gui = StellarVoiceGUI(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Application error: {e}")
        raise
