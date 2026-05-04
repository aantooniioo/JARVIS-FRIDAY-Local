"""
F.R.I.D.A.Y. - Interfaz gráfica avanzada (PySide6)
Versión 2.0 - Visual estilo IA / JARVIS con animación
"""

import sys
import math
import json
from pathlib import Path

from PySide6.QtCore import Qt, QSize, QTimer, QRectF, QPointF
from PySide6.QtGui import (
    QFont, QPalette, QColor, QPainter, QPen, QBrush,
    QRadialGradient
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFrame, QGridLayout
)


class CoreVisualizer(QWidget):
    """Visualizador animado tipo núcleo IA"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(360, 360)

        self.state = "standby"
        self.angle = 0.0
        self.pulse = 0.0
        self.secondary_angle = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_frame)
        self.timer.start(16)  # ~60 FPS

    def set_state(self, state):
        self.state = state
        self.update()

    def animate_frame(self):
        if self.state == "processing":
            speed_main = 4.0
            speed_secondary = 2.8
        elif self.state == "listening":
            speed_main = 2.6
            speed_secondary = 1.8
        elif self.state == "active":
            speed_main = 1.8
            speed_secondary = 1.2
        else:
            speed_main = 1.0
            speed_secondary = 0.7

        self.angle = (self.angle + speed_main) % 360
        self.secondary_angle = (self.secondary_angle + speed_secondary) % 360
        self.pulse += 0.08
        self.update()

    def state_colors(self):
        if self.state == "processing":
            return QColor("#FFB347"), QColor("#FF7A00"), QColor("#FFE2B8")
        if self.state == "listening":
            return QColor("#00E5FF"), QColor("#00B8D4"), QColor("#B2F5FF")
        if self.state == "active":
            return QColor("#00FFB2"), QColor("#00C98A"), QColor("#B9FFE8")
        return QColor("#00D4FF"), QColor("#009DCC"), QColor("#BDEFFF")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor("#0A0F18"))

        width = self.width()
        height = self.height()
        side = min(width, height)

        cx = width / 2
        cy = height / 2

        primary, secondary, glow = self.state_colors()

        base_radius = side * 0.12
        pulse_factor = 1.0 + 0.06 * math.sin(self.pulse)

        # Fondo radial suave
        bg_grad = QRadialGradient(QPointF(cx, cy), side * 0.45)
        bg_grad.setColorAt(0.0, QColor(secondary.red(), secondary.green(), secondary.blue(), 45))
        bg_grad.setColorAt(0.5, QColor(secondary.red(), secondary.green(), secondary.blue(), 18))
        bg_grad.setColorAt(1.0, QColor(10, 15, 24, 0))
        painter.setBrush(QBrush(bg_grad))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), side * 0.40, side * 0.40)

        # Anillos exteriores
        ring_radii = [side * 0.19, side * 0.25, side * 0.31]
        ring_alphas = [120, 80, 45]

        for radius, alpha in zip(ring_radii, ring_alphas):
            pen = QPen(QColor(primary.red(), primary.green(), primary.blue(), alpha), 2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(cx, cy), radius, radius)

        # Barridos / arcos rotatorios
        arc_rect_1 = QRectF(cx - side * 0.25, cy - side * 0.25, side * 0.50, side * 0.50)
        arc_rect_2 = QRectF(cx - side * 0.31, cy - side * 0.31, side * 0.62, side * 0.62)

        pen_arc_1 = QPen(QColor(glow.red(), glow.green(), glow.blue(), 220), 4)
        painter.setPen(pen_arc_1)
        painter.drawArc(arc_rect_1, int(-self.angle * 16), int(-85 * 16))

        pen_arc_2 = QPen(QColor(primary.red(), primary.green(), primary.blue(), 170), 3)
        painter.setPen(pen_arc_2)
        painter.drawArc(arc_rect_2, int(self.secondary_angle * 16), int(70 * 16))

        # Líneas de mira
        cross_pen = QPen(QColor(255, 255, 255, 28), 1)
        painter.setPen(cross_pen)
        painter.drawLine(int(cx - side * 0.34), int(cy), int(cx + side * 0.34), int(cy))
        painter.drawLine(int(cx), int(cy - side * 0.34), int(cx), int(cy + side * 0.34))

        # Partículas orbitando
        particle_radius = side * 0.28
        for i in range(12):
            a = math.radians(self.angle * 1.5 + i * 30)
            px = cx + math.cos(a) * particle_radius
            py = cy + math.sin(a) * particle_radius
            size = 3 + (i % 3)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(glow.red(), glow.green(), glow.blue(), 160))
            painter.drawEllipse(QPointF(px, py), size, size)

        # Núcleo exterior
        outer_grad = QRadialGradient(QPointF(cx, cy), base_radius * 1.9 * pulse_factor)
        outer_grad.setColorAt(0.0, QColor(primary.red(), primary.green(), primary.blue(), 120))
        outer_grad.setColorAt(0.6, QColor(secondary.red(), secondary.green(), secondary.blue(), 60))
        outer_grad.setColorAt(1.0, QColor(secondary.red(), secondary.green(), secondary.blue(), 0))
        painter.setBrush(QBrush(outer_grad))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), base_radius * 1.9 * pulse_factor, base_radius * 1.9 * pulse_factor)

        # Núcleo central
        core_grad = QRadialGradient(QPointF(cx, cy), base_radius * 1.2 * pulse_factor)
        core_grad.setColorAt(0.0, QColor(255, 255, 255, 255))
        core_grad.setColorAt(0.25, QColor(glow.red(), glow.green(), glow.blue(), 245))
        core_grad.setColorAt(0.65, QColor(primary.red(), primary.green(), primary.blue(), 210))
        core_grad.setColorAt(1.0, QColor(secondary.red(), secondary.green(), secondary.blue(), 80))
        painter.setBrush(QBrush(core_grad))
        painter.setPen(QPen(QColor(255, 255, 255, 50), 1))
        painter.drawEllipse(QPointF(cx, cy), base_radius * pulse_factor, base_radius * pulse_factor)

        # Anillo fino interno
        painter.setBrush(Qt.NoBrush)
        inner_pen = QPen(QColor(255, 255, 255, 100), 2)
        painter.setPen(inner_pen)
        painter.drawEllipse(QPointF(cx, cy), base_radius * 1.35, base_radius * 1.35)

        # Texto inferior del visualizador
        state_texts = {
            "standby": "EN ESPERA",
            "active": "ACTIVO",
            "listening": "ESCUCHANDO",
            "processing": "PROCESANDO"
        }

        painter.setPen(QColor("#CFEFFF"))
        font = painter.font()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            QRectF(0, cy + side * 0.22, width, 30),
            Qt.AlignCenter,
            state_texts.get(self.state, "EN ESPERA")
        )


class FridayGUI(QMainWindow):
    """Ventana principal"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("J.A.R.V.I.S / F.R.I.D.A.Y. - Sistema Local")
        self.setMinimumSize(QSize(1280, 800))

        self.memory_file = Path("friday_memory.json")

        self.setup_ui()
        self.apply_dark_theme()
        self.refresh_memory_count()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(16)

        # Header
        header = QFrame()
        header.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)
        header_layout.setSpacing(4)

        title = QLabel("F.R.I.D.A.Y.")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")

        subtitle = QLabel("Sistema de Asistencia Local · Interfaz Avanzada")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitleLabel")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        root_layout.addWidget(header)

        # Zona principal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)
        root_layout.addLayout(content_layout, 1)

        # Panel izquierdo
        left_panel = QFrame()
        left_panel.setObjectName("panel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(14)

        self.status_title = QLabel("Estado del sistema")
        self.status_title.setObjectName("sectionTitle")
        left_layout.addWidget(self.status_title)

        self.visualizer = CoreVisualizer()
        left_layout.addWidget(self.visualizer, 1)

        cards_layout = QGridLayout()
        cards_layout.setHorizontalSpacing(12)
        cards_layout.setVerticalSpacing(12)

        self.card_state = self.create_info_card("ESTADO", "En espera")
        self.card_mode = self.create_info_card("MODO", "Visual")
        self.card_memory = self.create_info_card("MEMORIA", "0 recuerdos")
        self.card_engine = self.create_info_card("MOTOR", "Local / Ollama")

        cards_layout.addWidget(self.card_state["frame"], 0, 0)
        cards_layout.addWidget(self.card_mode["frame"], 0, 1)
        cards_layout.addWidget(self.card_memory["frame"], 1, 0)
        cards_layout.addWidget(self.card_engine["frame"], 1, 1)

        left_layout.addLayout(cards_layout)

        content_layout.addWidget(left_panel, 1)

        # Panel derecho
        right_panel = QFrame()
        right_panel.setObjectName("panel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(18, 18, 18, 18)
        right_layout.setSpacing(14)

        log_title = QLabel("Consola / Actividad")
        log_title.setObjectName("sectionTitle")
        right_layout.addWidget(log_title)

        self.conversation = QTextEdit()
        self.conversation.setReadOnly(True)
        self.conversation.setObjectName("logBox")
        self.conversation.append("=== F.R.I.D.A.Y. · Sistema Local ===")
        self.conversation.append("[SISTEMA] Interfaz gráfica cargada.")
        self.conversation.append("[ESTADO] En espera de activación.")
        right_layout.addWidget(self.conversation, 1)

        buttons_layout = QGridLayout()
        buttons_layout.setHorizontalSpacing(10)
        buttons_layout.setVerticalSpacing(10)

        self.btn_start = QPushButton("▶ Iniciar")
        self.btn_start.setStyleSheet(self.button_style("#00AAFF", "#0088DD"))
        self.btn_start.clicked.connect(self.start_assistant)

        self.btn_stop = QPushButton("■ Detener")
        self.btn_stop.setStyleSheet(self.button_style("#FF5A5A", "#D94848"))
        self.btn_stop.clicked.connect(self.stop_assistant)
        self.btn_stop.setEnabled(False)

        self.btn_listen = QPushButton("🎤 Escuchando")
        self.btn_listen.setStyleSheet(self.button_style("#00C4B3", "#00A899"))
        self.btn_listen.clicked.connect(self.simulate_listening)
        self.btn_listen.setEnabled(False)

        self.btn_process = QPushButton("⚙ Procesando")
        self.btn_process.setStyleSheet(self.button_style("#FF9F43", "#E88727"))
        self.btn_process.clicked.connect(self.simulate_processing)
        self.btn_process.setEnabled(False)

        self.btn_clear = QPushButton("🗑 Limpiar historial")
        self.btn_clear.setStyleSheet(self.button_style("#5C667A", "#4B5567"))
        self.btn_clear.clicked.connect(self.clear_history)

        self.btn_memory = QPushButton("📝 Ver memoria")
        self.btn_memory.setStyleSheet(self.button_style("#5C667A", "#4B5567"))
        self.btn_memory.clicked.connect(self.show_memory)

        buttons_layout.addWidget(self.btn_start, 0, 0)
        buttons_layout.addWidget(self.btn_stop, 0, 1)
        buttons_layout.addWidget(self.btn_listen, 1, 0)
        buttons_layout.addWidget(self.btn_process, 1, 1)
        buttons_layout.addWidget(self.btn_clear, 2, 0)
        buttons_layout.addWidget(self.btn_memory, 2, 1)

        right_layout.addLayout(buttons_layout)

        content_layout.addWidget(right_panel, 1)

    def create_info_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("infoCard")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        lbl_title = QLabel(title)
        lbl_title.setObjectName("cardTitle")

        lbl_value = QLabel(value)
        lbl_value.setObjectName("cardValue")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)

        return {
            "frame": frame,
            "title": lbl_title,
            "value": lbl_value
        }

    def button_style(self, color, hover):
        return """
            QPushButton {{
                background-color: {color};
                border: none;
                border-radius: 10px;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: 600;
                color: white;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                padding-top: 13px;
                padding-bottom: 11px;
            }}
            QPushButton:disabled {{
                background-color: #2C3445;
                color: #7E8796;
            }}
        """.format(color=color, hover=hover)

    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#0B111B"))
        palette.setColor(QPalette.WindowText, QColor("#D7E3F4"))
        palette.setColor(QPalette.Base, QColor("#101826"))
        palette.setColor(QPalette.AlternateBase, QColor("#1A2434"))
        palette.setColor(QPalette.ToolTipBase, QColor("#101826"))
        palette.setColor(QPalette.ToolTipText, QColor("#D7E3F4"))
        palette.setColor(QPalette.Text, QColor("#D7E3F4"))
        palette.setColor(QPalette.Button, QColor("#182235"))
        palette.setColor(QPalette.ButtonText, QColor("#D7E3F4"))
        palette.setColor(QPalette.Highlight, QColor("#00AAFF"))
        palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
        self.setPalette(palette)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0B111B;
            }

            QFrame#headerFrame {
                background-color: #101826;
                border: 1px solid #1D2A3F;
                border-radius: 16px;
            }

            QFrame#panel {
                background-color: #101826;
                border: 1px solid #1D2A3F;
                border-radius: 16px;
            }

            QLabel#titleLabel {
                font-size: 34px;
                font-weight: 800;
                color: #00D4FF;
                letter-spacing: 2px;
            }

            QLabel#subtitleLabel {
                font-size: 14px;
                color: #93A6BF;
            }

            QLabel#sectionTitle {
                font-size: 18px;
                font-weight: 700;
                color: #EAF4FF;
            }

            QTextEdit#logBox {
                background-color: #0C121D;
                border: 1px solid #24324A;
                border-radius: 14px;
                padding: 12px;
                color: #DDEBFA;
                font-size: 14px;
            }

            QFrame#infoCard {
                background-color: #0C121D;
                border: 1px solid #24324A;
                border-radius: 14px;
            }

            QLabel#cardTitle {
                color: #7F95B1;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#cardValue {
                color: #F2F8FF;
                font-size: 18px;
                font-weight: 700;
            }
        """)

    def append_log(self, text):
        self.conversation.append(text)

    def set_state(self, state, message=None):
        state_names = {
            "standby": "En espera",
            "active": "Activo",
            "listening": "Escuchando",
            "processing": "Procesando"
        }

        self.visualizer.set_state(state)
        self.card_state["value"].setText(state_names.get(state, "En espera"))

        if message:
            self.append_log(message)

    def refresh_memory_count(self):
        count = 0

        if self.memory_file.exists():
            try:
                content = json.loads(self.memory_file.read_text(encoding="utf-8"))
                if isinstance(content, list):
                    count = len(content)
            except Exception:
                count = 0

        label = "1 recuerdo" if count == 1 else f"{count} recuerdos"
        self.card_memory["value"].setText(label)

    def start_assistant(self):
        self.set_state("active", "[SISTEMA] Asistente iniciado.")
        self.append_log("FRIDAY: Sistema Friday iniciado. En espera, señor.")

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_listen.setEnabled(True)
        self.btn_process.setEnabled(True)

    def stop_assistant(self):
        self.set_state("standby", "[SISTEMA] Asistente detenido.")

        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_listen.setEnabled(False)
        self.btn_process.setEnabled(False)

    def simulate_listening(self):
        self.set_state("listening", "[ESCUCHA] Escuchando comando...")
        QTimer.singleShot(2200, lambda: self.set_state("active", "FRIDAY: Esperando instrucción, señor."))

    def simulate_processing(self):
        self.set_state("processing", "[PROCESO] Analizando solicitud...")
        QTimer.singleShot(2600, lambda: self.set_state("active", "FRIDAY: Solicitud procesada, señor."))

    def clear_history(self):
        self.conversation.clear()
        self.conversation.append("=== F.R.I.D.A.Y. · Sistema Local ===")
        self.conversation.append("[SISTEMA] Historial limpiado.")

    def show_memory(self):
        self.refresh_memory_count()
        self.append_log("[MEMORIA] Cargando recuerdos...")

        if not self.memory_file.exists():
            self.append_log("FRIDAY: No existe archivo de memoria todavía, señor.")
            return

        try:
            data = json.loads(self.memory_file.read_text(encoding="utf-8"))
            if not data:
                self.append_log("FRIDAY: No hay recuerdos guardados, señor.")
                return

            self.append_log("FRIDAY: Estos son los recuerdos guardados:")
            for i, item in enumerate(data, start=1):
                self.append_log(f"  {i}. {item}")

        except Exception as e:
            self.append_log(f"[ERROR] No se pudo leer la memoria: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = FridayGUI()
    window.show()

    sys.exit(app.exec())