# J.A.R.V.I.S. / F.R.I.D.A.Y. — Asistente de Voz Local

> *"Fully Responsive Intelligent Digital Assistant for You"*

Un asistente de voz local inspirado en Tony Stark que funciona en tu PC con Windows, sin necesidad de modelos de IA pesados para funcionalidades básicas.

---

## Versión Actual: Friday Local (Estable)

Esta es la versión activa y estable del asistente. Funciona sin Ollama ni APIs de pago para los comandos básicos, utilizando:
- **SpeechRecognition** (API de Google Speech) para entrada de voz (requiere internet)
- **edge-tts** (Microsoft Edge TTS) para salida de voz (requiere internet)
- **playsound** para reproducción de audio
- Comandos básicos integrados (no requiere LLM pesado)

*Nota: Esta versión no es 100% offline, ya que tanto el reconocimiento de voz como la síntesis de voz requieren conexión a internet.*

---

## Características (Versión Local)

### Comandos de Voz Disponibles
| Comando | Respuesta |
|---------|-----------|
| `hola Friday` | "A sus órdenes, señor." |
| `hora` | "Son las [H] y [M]" (ej: "Son las 13 y 27") |
| `qué día es` / `fecha` | "Hoy es [día], [día] de [mes] de [año]." (ej: "Hoy es martes, 28 de abril de 2026.") |
| `buenos días` / `buenas tardes` / `buenas noches` | "Buenos días/tardes/noches, señor." |
| `gracias` | "Siempre a sus órdenes, señor." |
| `cómo estás` | "Operativa y lista para asistirle, señor." |
| `quién eres` | "Soy Fraidey, su asistente local." |
| `qué eres` | "Soy una interfaz de asistencia local inspirada en Fraidey." |
| `qué puedes hacer` | Lista todos los comandos disponibles |
| `abre Chrome` | Abre Google Chrome (si está instalado) |
| `abre VS Code` / `abre Visual Studio Code` | Abre VS Code (si está instalado) |
| `abre Spotify` | Abre Spotify (si está instalado) |
| `abre YouTube` / `abre Google` / `abre GitHub` / `abre ChatGPT` | Abre el sitio web correspondiente |
| `salir` / `adiós` / `terminar` | "Hasta luego, señor." y cierra el asistente |

### Opcional: Integración con Ollama
Para consultas avanzadas más allá de los comandos básicos, puedes usar opcionalmente Ollama con el modelo `mistral`. Si Ollama no está disponible, el asistente responderá con un mensaje amable y continuará funcionando con los comandos básicos.
*Nota: Ollama no es necesario para la funcionalidad básica y no se recomienda para PCs con poca memoria.*

---

## Inicio Rápido (Versión Local)

### Requisitos Previos
- Python 3.11+
- Windows 10/11
- Micrófono funcional
- Conexión a internet (para reconocimiento de voz y síntesis de voz)

### Instalación
1. Clona el repositorio (si no lo has hecho):
   ```bash
   git clone https://github.com/tuusuario/J.A.R.V.I.S.git
   cd J.A.R.V.I.S
   ```

2. Instala las dependencias necesarias:
   ```bash
   python -m pip install SpeechRecognition PyAudio requests edge-tts playsound==1.2.2
   ```

### Ejecución del Asistente
1. Verifica la sintaxis:
   ```bash
   python -m py_compile local_friday.py
   ```

2. Inicia el asistente:
   ```bash
   python local_friday.py
   ```

3. Habla naturalmente al micrófono utilizando los comandos listados arriba.

---

## Alternativa: Versión Cloud/API (Fase Futura)

La versión original de F.R.I.D.A.Y. demo utiliza APIs de pago y LiveKit para una experiencia más avanzada:
- **FastMCP** como servidor de herramientas/extensiones
- **LiveKit Agents** para pipeline de voz en tiempo real
- **Google Gemini** (LLM), **Sarvam** (STT), **OpenAI** (TTS)

Esta versión requiere claves API y una cuenta en LiveKit Cloud, y está planificada como una fase futura. No es la versión activa actual.

### Comparativa: Versión Local vs Cloud
| Característica | Versión Local (Activa) | Versión Cloud (Futura) |
|---------|------------------------|------------------------|
| Requiere internet | Sí (STT/TTS) | Sí (todos los componentes) |
| APIs de pago | No | Sí (múltiples) |
| Privacidad | Procesamiento local (excepto STT/TTS) | Procesamiento en la nube |
| Velocidad | Rápida | Depende de la red |
| Calidad IA | Comandos básicos + Ollama opcional | Alta (Gemini LLM) |
| Tiempo de configuración | ~5 minutos | ~30+ minutos |
| Reconocimiento de voz | Google Speech | Sarvam AI |
| Síntesis de voz | edge-tts (Microsoft) | OpenAI TTS |

Consulta la documentación original del proyecto para detalles de configuración (nota: esta no es la versión estable actual).

---

## Estructura del Proyecto
```
J.A.R.V.I.S/
├── local_friday.py       # Script principal del asistente local (versión activa)
├── server.py             # Servidor FastMCP (versión cloud, fase futura)
├── agent_friday.py       # Agente de voz LiveKit (versión cloud, fase futura)
├── pyproject.toml       # Dependencias del proyecto
├── .env.example         # Plantilla de variables de entorno
├── README.md            # Esta documentación
├── LOCAL_GUIDE.md       # Guía rápida de configuración local
├── friday/              # Paquete MCP para versión cloud (fase futura)
│   ├── config.py
│   ├── tools/
│   ├── prompts/
│   └── resources/
└── .gitignore
```

---

## Problemas Comunes
- **No hay salida de voz**: Verifica que `edge-tts` y `playsound==1.2.2` estén instalados correctamente.
- **El reconocimiento de voz falla**: Revisa la conexión a internet y la configuración del micrófono.
- **Errores de Ollama**: Ignóralos si solo usas comandos básicos; Ollama es opcional.
- **Errores de playsound**: Instala la versión compatible: `pip install playsound==1.2.2`

---

## Licencia
MIT
