# StellarVoice
StellarVoice is a voice-activated assistant with a graphical user interface (GUI) built using Python. It supports voice and text commands to perform tasks such as opening a web browser, checking the time, and searching online. The assistant features a simple visualization system using bar charts to provide visual feedback for certain actions.
# Features

Voice command recognition using Google's speech recognition API.
Text-to-speech functionality with customizable speech rate.
Basic command execution (e.g., open browser, check time, search online).
Visual feedback with matplotlib-based bar charts.
User-friendly GUI with settings for personalization.
Logging for debugging and error tracking.

# Requirements

Python 3.6 or higher
Dependencies listed in requirements.txt:
pyttsx3>=2.90
SpeechRecognition>=3.8.1
matplotlib>=3.5.0
pyaudio>=0.2.11



# Installation

Clone or download the repository to your local machine.
Create a virtual environment (optional but recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install the required dependencies:pip install -r requirements.txt


Ensure you have a working microphone connected to your system.

# Usage

Run the application:python stellar_voice.py


The GUI will open, displaying a conversation area, input field, and control buttons.
Use the "Listen" button (🎤) to activate voice input or type commands in the text field.
Supported commands include:
"Open browser" - Opens Google Chrome.
"Time" - Displays and speaks the current time.
"Search" - Prompts for a search query and opens it in a browser.


Use the "Settings" button (⚙️) to configure user name and speech rate.
Use the "Exit" button (❌) to close the application.

# Notes

The application uses the sapi5 text-to-speech engine, which is Windows-specific. For cross-platform compatibility, consider replacing pyttsx3 with a different TTS library.
Speech recognition requires an internet connection for Google's API.
Logs are saved to stellar_voice.log for troubleshooting.
Visualizations are simple bar charts displayed above the conversation area.

# Troubleshooting

Microphone issues: Ensure your microphone is properly connected and configured in your system settings.
Speech recognition errors: Check your internet connection or try speaking more clearly.
TTS errors: Verify that sapi5 is available on your system (Windows only).
Visualization errors: Ensure matplotlib is correctly installed.

# Contributing
Contributions are welcome! Please submit a pull request or open an issue on the project repository.
License
This project is licensed under the MIT License. See the LICENSE file for details.
