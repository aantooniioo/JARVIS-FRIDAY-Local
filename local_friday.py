"""
JARVIS Local - Versión offline basada en Friday pero 100% local
Usa Ollama + speech recognition + pyttsx3
"""

import os
import sys
import time
from pathlib import Path

# Agregar Friday al path
sys.path.insert(0, str(Path(__file__).parent))

import speech_recognition as sr

import requests
from datetime import datetime


class LocalJARVIS:
    def __init__(self):
        print("\n" + "="*70)
        print(" "*15 + "F.R.I.D.A.Y - Local AI Assistant")
        print("="*70 + "\n")
        
        self.listener = sr.Recognizer()

        
        print("[INIT] Componentes cargados")
        print("[INIT] Escuchando en micrófono...")
        print("[INIT] Conectando con Ollama en localhost:11434...\n")
        
        self.speak("Friday inicializado")
    
    def speak(self, text: str):
        """Habla usando edge-tts"""
        if not text:
            return

        print(f"[FRIDAY] {text}\n")

        try:
            import edge_tts
            import asyncio
            import tempfile
            import os
            from playsound import playsound

            async def _speak(text):
                communicate = edge_tts.Communicate(text, voice="es-ES-ElviraNeural")
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    tmpfile = f.name
                try:
                    await communicate.save(tmpfile)
                    playsound(tmpfile)
                finally:
                    os.unlink(tmpfile)

            asyncio.run(_speak(text))
        except Exception as e:
            print(f"[ERROR VOZ] Fallo al hablar: {e}")
    
    def listen(self) -> str:
        """Escucha micrófono"""
        try:
            with sr.Microphone() as source:
                self.listener.adjust_for_ambient_noise(source, duration=0.5)
                print("[LISTENING] Escuchando...")
                audio = self.listener.listen(source, timeout=5, phrase_time_limit=10)
            
            print("[PROCESSING] Procesando audio...")
            text = self.listener.recognize_google(audio, language="es-ES")
            print(f"[YOU] {text}\n")
            return text.lower()
        
        except sr.UnknownValueError:
            print("[ERROR] No se entendió el audio\n")
            return None
        except sr.RequestError:
            print("[ERROR] Problema con Google Speech\n")
            return None
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"[ERROR] {e}\n")
            return None
    
    def query_ollama(self, prompt: str) -> str:
        """Consulta Ollama"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "num_predict": 50
                },
                timeout=15
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            return "Ahora mismo no puedo usar el modelo local, pero sigo disponible para comandos básicos como la hora."
        
        except Exception as e:
            print(f"[ERROR] Ollama: {e}\n")
            return "Ahora mismo no puedo usar el modelo local, pero sigo disponible para comandos básicos como la hora."
    
    def run(self):
        """Loop principal"""
        while True:
            try:
                text = self.listen()
                
                if not text:
                    continue
                
                # Comandos simples
                # 1. Salir / terminar
                if any(cmd in text for cmd in ["salir", "adiós", "terminar"]):
                    self.speak("Hasta luego, señor.")
                    break
                # 2. Hora
                elif "hora" in text:
                    now = datetime.now()
                    response = f"Son las {now.strftime('%H')} y {now.strftime('%M')}"
                    self.speak(response)
                # 3. Saludo
                elif "hola friday" in text:
                    response = "A sus órdenes, señor."
                    self.speak(response)
                # 4. Ayuda de comandos
                elif "qué puedes hacer" in text:
                    response = "Comandos disponibles: 'hora' para la hora, 'hola Friday' para saludar, 'qué puedes hacer' para esta guía, 'salir' / 'adiós' / 'terminar' para cerrar. Otras consultas usarán el modelo local si está disponible."
                    self.speak(response)
                # 5. Ollama (solo si no es comando básico)
                else:
                    response = self.query_ollama(text)
                    self.speak(response)
                
            except KeyboardInterrupt:
                print("\n[FRIDAY] Apagando...")
                self.speak("Apagando")
                break
            except Exception as e:
                print(f"[ERROR] {e}\n")
                time.sleep(0.5)


if __name__ == "__main__":
    jarvis = LocalJARVIS()
    jarvis.run()
