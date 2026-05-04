import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";
const WS_URL = "ws://localhost:8000/ws";

function App() {
  const previousRunning = useRef(null);
  const socketRef = useRef(null);

  const [backendStatus, setBackendStatus] = useState(null);
  const [connected, setConnected] = useState(false);
  const [wsConnected, setWsConnected] = useState(false);
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([
    "[SISTEMA] Panel visual F.R.I.D.A.Y. iniciado.",
    "[SISTEMA] Esperando conexión con backend local.",
  ]);

  const addLog = (message) => {
    const time = new Date().toLocaleTimeString("es-ES", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });

    setLogs((prev) => [`[${time}] ${message}`, ...prev].slice(0, 14));
  };

  const fetchStatus = async () => {
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/status`);

      if (!response.ok) {
        throw new Error("Respuesta no válida del backend");
      }

      const data = await response.json();

      setBackendStatus(data);
      setConnected(true);
      addLog("[API] Estado recibido correctamente.");
    } catch (error) {
      setConnected(false);
      setBackendStatus(null);
      addLog("[ERROR] Backend desconectado o no disponible.");
    } finally {
      setLoading(false);
    }
  };

  const startAssistant = async () => {
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/start`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("No se pudo iniciar el asistente");
      }

      const data = await response.json();
      addLog(`[API] ${data.message || "Asistente iniciado."}`);
      await fetchStatus();
    } catch (error) {
      setConnected(false);
      addLog("[ERROR] No se pudo iniciar Friday.");
    } finally {
      setLoading(false);
    }
  };

  const stopAssistant = async () => {
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/stop`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("No se pudo detener el asistente");
      }

      const data = await response.json();
      addLog(`[API] ${data.message || "Asistente detenido."}`);
      await fetchStatus();
    } catch (error) {
      setConnected(false);
      addLog("[ERROR] No se pudo detener Friday.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();

    const socket = new WebSocket(WS_URL);
    socketRef.current = socket;

    socket.onopen = () => {
      setWsConnected(true);
      setConnected(true);
      addLog("[WS] Conexión en tiempo real establecida.");
    };

    socket.onmessage = (event) => {
      try {
        const eventData = JSON.parse(event.data);

        if (eventData.type === "status_update") {
          const data = eventData.data;
          setBackendStatus(data);
          setConnected(true);

          if (previousRunning.current === null) {
            previousRunning.current = data.running;
            return;
          }

          if (previousRunning.current !== data.running) {
            previousRunning.current = data.running;
            addLog(
              data.running
                ? "[WS] Friday ha pasado a estado activo."
                : "[WS] Friday ha vuelto a modo espera."
            );
          }
        }
      } catch (error) {
        addLog("[ERROR] Evento WebSocket no válido.");
      }
    };

    socket.onerror = () => {
      setWsConnected(false);
      addLog("[WS] Error en la conexión en tiempo real.");
    };

    socket.onclose = () => {
      setWsConnected(false);
      addLog("[WS] Conexión en tiempo real perdida.");
    };

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  const assistantName = backendStatus?.assistant || "Friday";
  const running = Boolean(backendStatus?.running);
  const message = backendStatus?.message || "Sin datos del sistema";

  return (
    <main className="jarvis-shell">
      <section className="hero-panel">
        <div className="top-bar">
          <div>
            <p className="eyebrow">Sistema local</p>
            <h1>J.A.R.V.I.S / F.R.I.D.A.Y.</h1>
          </div>

          <div className={`connection-pill ${connected ? "online" : "offline"}`}>
            <span className="dot" />
            {connected ? "Backend conectado" : "Backend desconectado"}
          </div>
        </div>

        <div className="dashboard-grid">
          <section className="core-card">
            <div className={`ai-core ${running ? "running" : "standby"}`}>
              <div className="ring ring-one" />
              <div className="ring ring-two" />
              <div className="ring ring-three" />
              <div className="scanner" />

              <div className="core-center">
                <span>{running ? "ACTIVE" : "STANDBY"}</span>
              </div>
            </div>

            <div className="core-caption">
              <h2>{running ? "Asistente activo" : "En espera"}</h2>
              <p>
                {running
                  ? "Canal local preparado para recibir órdenes."
                  : "Friday permanece en modo visual hasta iniciar el sistema."}
              </p>
            </div>
          </section>

          <section className="status-card">
            <h2>Estado del sistema</h2>

            <div className="status-list">
              <div className="status-row">
                <span>Asistente</span>
                <strong>{assistantName}</strong>
              </div>

              <div className="status-row">
                <span>Backend</span>
                <strong>{connected ? "Operativo" : "Sin conexión"}</strong>
              </div>

              <div className="status-row">
                <span>WebSocket</span>
                <strong>{wsConnected ? "Conectado" : "Desconectado"}</strong>
              </div>

              <div className="status-row">
                <span>Running</span>
                <strong>{running ? "True" : "False"}</strong>
              </div>

              <div className="status-row">
                <span>Mensaje</span>
                <strong>{message}</strong>
              </div>
            </div>

            <div className="button-row">
              <button onClick={fetchStatus} disabled={loading}>
                Consultar estado
              </button>

              <button onClick={startAssistant} disabled={loading}>
                Iniciar asistente
              </button>

              <button onClick={stopAssistant} disabled={loading}>
                Detener
              </button>
            </div>
          </section>

          <section className="log-card">
            <div className="log-header">
              <h2>Actividad</h2>
              <button
                className="ghost-button"
                onClick={() => setLogs(["[SISTEMA] Logs limpiados."])}
              >
                Limpiar logs
              </button>
            </div>

            <div className="log-list">
              {logs.length === 0 ? (
                <p className="empty-log">Sin eventos registrados.</p>
              ) : (
                logs.map((log, index) => (
                  <p key={`${log}-${index}`} className="log-item">
                    {log}
                  </p>
                ))
              )}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

export default App;