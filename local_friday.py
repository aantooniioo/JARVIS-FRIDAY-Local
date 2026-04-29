"""
JARVIS Local - Versión offline basada en Friday pero 100% local
Usa Ollama + speech recognition + pyttsx3
"""

import os
import sys
import time
import json
import unicodedata
import urllib.parse
import webbrowser
import subprocess
from pathlib import Path


def normalize_text(text):
    """Normaliza texto: minúsculas, sin acentos"""
    if not text:
        return ""
    text = text.lower()
    # Descomponer caracteres acentuados y eliminar marcas no espaciadas
    normalized = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return text


import speech_recognition as sr

import requests
from datetime import datetime


class LocalJARVIS:
    def __init__(self):
        print("\n" + "="*70)
        print(" "*15 + "F.R.I.D.A.Y - Local AI Assistant")
        print("="*70 + "\n")
        
        self.listener = sr.Recognizer()
        self.memory_file = "friday_memory.json"

        
        print("[INIT] Componentes cargados")
        print("[INIT] Escuchando en micrófono...")
        print("[INIT] Conectando con Ollama en localhost:11434...\n")
        
        self.speak("Friday inicializado")
    
    def speak(self, text: str, voice_text: str = None):
        """Habla usando edge-tts"""
        if not text:
            return

        print(f"[FRIDAY] {text}\n")  # Consola: texto original

        # Texto para voz: ajustar pronunciaciones
        spoken_text = voice_text if voice_text is not None else text
        spoken_text = spoken_text.replace("JARVIS", "Yarvis")
        spoken_text = spoken_text.replace("F.R.I.D.A.Y.", "Fraidey")
        spoken_text = spoken_text.replace("Friday", "Fraidey")

        try:
            import edge_tts
            import asyncio
            import tempfile
            import os
            from playsound import playsound

            async def _speak(spoken_text):
                communicate = edge_tts.Communicate(spoken_text, voice="es-ES-ElviraNeural")
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    tmpfile = f.name
                try:
                    await communicate.save(tmpfile)
                    playsound(tmpfile)
                finally:
                    os.unlink(tmpfile)

            asyncio.run(_speak(spoken_text))
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
    
    def load_memory(self):
        """Carga recuerdos desde el archivo JSON"""
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"[ERROR MEMORIA] Error cargando memoria: {e}")
            return []

    def save_memory(self, memory_list):
        """Guarda recuerdos en el archivo JSON"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERROR MEMORIA] Error guardando memoria: {e}")

    def add_memory(self, text):
        """Añade un nuevo recuerdo"""
        memory = self.load_memory()
        memory.append(text)
        self.save_memory(memory)

    def clear_memory(self):
        """Limpia todos los recuerdos"""
        self.save_memory([])
    
    def run(self):
        """Loop principal"""
        while True:
            try:
                text = self.listen()
                
                if not text:
                    continue
                
                norm_text = normalize_text(text)
                
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
                    response = ("Comandos disponibles: "
                        "'hora' para la hora, "
                        "'qué día es' / 'fecha' para la fecha, "
                        "'hola Friday' para saludar, "
                        "'buenos días' / 'buenas tardes' / 'buenas noches' / 'gracias' / 'cómo estás' para cortesía, "
                        "'quién eres' / 'qué eres' para identidad, "
                        "'abre Chrome' / 'abre VS Code' / 'abre Spotify' para aplicaciones, "
                        "'abre YouTube' / 'abre Google' / 'abre GitHub' / 'abre ChatGPT' para webs, "
                        "'abre escritorio' / 'abre descargas' / 'abre documentos' para carpetas, "
                        "'abre mi proyecto' / 'abre JARVIS' para abrir el proyecto local, "
                        "'busca música de [canción]' / 'busca [algo] en YouTube' para buscar música en YouTube, "
                        "'recuerda que [texto]' para guardar recuerdos, "
                        "'qué recuerdas' para leer recuerdos, "
                        "'borra recuerdos' / 'limpia memoria' para limpiar memoria, "
                        "'qué puedes hacer' para esta guía, "
                        "'salir' / 'adiós' / 'terminar' para cerrar. "
                        "Otras consultas usarán el modelo local si está disponible.")
                    self.speak(response)
                # 5. Fecha y día
                elif any(cmd in text for cmd in ["qué día es", "fecha"]):
                    today = datetime.now()
                    days_es = {
                        0: "lunes",
                        1: "martes",
                        2: "miércoles",
                        3: "jueves",
                        4: "viernes",
                        5: "sábado",
                        6: "domingo"
                    }
                    months_es = {
                        1: "enero",
                        2: "febrero",
                        3: "marzo",
                        4: "abril",
                        5: "mayo",
                        6: "junio",
                        7: "julio",
                        8: "agosto",
                        9: "septiembre",
                        10: "octubre",
                        11: "noviembre",
                        12: "diciembre"
                    }
                    day_name = days_es[today.weekday()]
                    month_name = months_es[today.month]
                    response = f"Hoy es {day_name}, {today.day} de {month_name} de {today.year}."
                    self.speak(response)
                # 6. Saludos y cortesía
                elif "buenos días" in text:
                    response = "Buenos días, señor."
                    self.speak(response)
                elif "buenas tardes" in text:
                    response = "Buenas tardes, señor."
                    self.speak(response)
                elif "buenas noches" in text:
                    response = "Buenas noches, señor."
                    self.speak(response)
                elif "gracias" in text:
                    response = "Siempre a sus órdenes, señor."
                    self.speak(response)
                elif "cómo estás" in text:
                    response = "Operativa y lista para asistirle, señor."
                    self.speak(response)
                # 7. Identidad
                elif "quién eres" in text:
                    response = "Soy Fraidey, su asistente local."
                    self.speak(response)
                elif "qué eres" in text:
                    response = "Soy una interfaz de asistencia local inspirada en Fraidey."
                    self.speak(response)
                # 8. Abrir aplicaciones
                elif "abre chrome" in text:
                    try:
                        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
                        response = "Abriendo Chrome, señor."
                    except Exception:
                        response = "No pude abrir Chrome, señor."
                    self.speak(response)
                elif any(cmd in text for cmd in ["abre vs code", "abre visual studio code"]):
                    try:
                        subprocess.Popen("code")
                        response = "Abriendo Visual Studio Code, señor."
                    except Exception:
                        response = "No pude abrir Visual Studio Code, señor."
                    self.speak(response)
                elif "abre spotify" in text:
                    try:
                        subprocess.Popen(r"C:\Users\anton\AppData\Roaming\Spotify\Spotify.exe")
                        response = "Abriendo Spotify, señor."
                    except Exception:
                        response = "No pude abrir Spotify, señor."
                    self.speak(response)
                # 9. Abrir webs
                elif "abre youtube" in text:
                    webbrowser.open("https://youtube.com")
                    response = "Abriendo YouTube, señor."
                    self.speak(response)
                elif "abre google" in text:
                    webbrowser.open("https://google.com")
                    response = "Abriendo Google, señor."
                    self.speak(response)
                elif "abre github" in text:
                    webbrowser.open("https://github.com")
                    response = "Abriendo GitHub, señor."
                    self.speak(response)
                elif "abre chatgpt" in text:
                    webbrowser.open("https://chatgpt.com")
                    response = "Abriendo ChatGPT, señor."
                    self.speak(response)
                # 10. Buscar música en YouTube
                elif (
                    any(prefix in norm_text for prefix in ["busca musica de ", "pon musica de ", "buscame musica de ", "musica de ", "busca musica del ", "pon musica del ", "buscame musica del ", "musica del "])
                    or "en youtube" in norm_text
                ):
                    query = ""
                    # Caso 1: Frases con "busca/pon/buscame musica de " o "del "
                    if "busca musica de " in norm_text:
                        query = norm_text.split("busca musica de ", 1)[1].strip()
                    elif "pon musica de " in norm_text:
                        query = norm_text.split("pon musica de ", 1)[1].strip()
                    elif "buscame musica de " in norm_text:
                        query = norm_text.split("buscame musica de ", 1)[1].strip()
                    elif "musica de " in norm_text:
                        query = norm_text.split("musica de ", 1)[1].strip()
                    elif "busca musica del " in norm_text:
                        query = norm_text.split("busca musica del ", 1)[1].strip()
                    elif "pon musica del " in norm_text:
                        query = norm_text.split("pon musica del ", 1)[1].strip()
                    elif "buscame musica del " in norm_text:
                        query = norm_text.split("buscame musica del ", 1)[1].strip()
                    elif "musica del " in norm_text:
                        query = norm_text.split("musica del ", 1)[1].strip()
                    # Caso 2: Contiene "en youtube"
                    elif "en youtube" in norm_text:
                        pre_youtube = norm_text.split("en youtube", 1)[0].strip()
                        # Quitar prefijos
                        prefixes = ["busca ", "busco ", "pon ", "buscame "]
                        for prefix in prefixes:
                            if pre_youtube.startswith(prefix):
                                pre_youtube = pre_youtube[len(prefix):].strip()
                                break
                        query = pre_youtube
                    
                    if not query:
                        response = "No has especificado qué buscar, señor."
                    else:
                        # Corregir nombres mal reconocidos
                        youtube_aliases = {
                            "central": "central cee",
                            "central si": "central cee",
                            "central sí": "central cee",
                            "central c": "central cee",
                            "beny": "beny jr",
                            "beni jr": "beny jr",
                            "beny junior": "beny jr",
                            "grind": "grind",
                            # Nuevos aliases para "del"
                            "ben": "beny jr",
                            "beni": "beny jr",
                            "el ben": "beny jr",
                            "del ben": "beny jr",
                            "green": "grind",
                            "grin": "grind",
                            "el grind": "grind",
                            "del grind": "grind",
                        }
                        if query in youtube_aliases:
                            query = youtube_aliases[query]
                        
                        encoded_query = urllib.parse.quote_plus(query)
                        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
                        webbrowser.open(search_url)
                        console_response = f"Buscando {query} en YouTube, señor."
                        voice_response = "Buscando en YouTube, señor."
                        self.speak(console_response, voice_text=voice_response)
                # 11. Abrir carpetas locales
                elif "abre escritorio" in text:
                    path = r"C:\Users\anton\Desktop"
                    if os.path.exists(path):
                        os.startfile(path)
                        response = "Abriendo escritorio, señor."
                    else:
                        response = "No he encontrado esa carpeta, señor."
                    self.speak(response)
                elif "abre descargas" in text:
                    path = r"C:\Users\anton\Downloads"
                    if os.path.exists(path):
                        os.startfile(path)
                        response = "Abriendo descargas, señor."
                    else:
                        response = "No he encontrado esa carpeta, señor."
                    self.speak(response)
                elif "abre documentos" in text:
                    path = r"C:\Users\anton\Documents"
                    if os.path.exists(path):
                        os.startfile(path)
                        response = "Abriendo documentos, señor."
                    else:
                        response = "No he encontrado esa carpeta, señor."
                    self.speak(response)
                elif any(cmd in text for cmd in ["abre mi proyecto", "abre mi proyecto jarvis", "abre proyecto jarvis", "abre jarvis"]):
                    path = r"C:\Users\anton\Desktop\J.A.R.V.I.S"
                    if os.path.exists(path):
                        os.startfile(path)
                        response = "Abriendo el proyecto JARVIS, señor."
                    else:
                        response = "No he encontrado esa carpeta, señor."
                    self.speak(response)
                # 11. Guardar recuerdo
                elif "recuerda que" in text:
                    memory_text = text.split("recuerda que", 1)[1].strip()
                    if memory_text:
                        self.add_memory(memory_text)
                        response = "Lo recordaré, señor."
                    else:
                        response = "No has especificado qué recordar, señor."
                    self.speak(response)
                # 11. Leer recuerdos
                elif "qué recuerdas" in text:
                    memory = self.load_memory()
                    if memory:
                        response = "Recuerdos: " + ", ".join([f"{i+1}. {item}" for i, item in enumerate(memory)])
                    else:
                        response = "No tengo recuerdos guardados, señor."
                    self.speak(response)
                # 12. Borrar recuerdos
                elif any(cmd in text for cmd in ["borra recuerdos", "limpia memoria"]):
                    self.clear_memory()
                    response = "Memoria local limpiada, señor."
                    self.speak(response)
                # 13. Ollama (solo si no es comando básico)
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
