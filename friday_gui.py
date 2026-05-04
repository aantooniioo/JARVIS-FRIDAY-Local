"""
F.R.I.D.A.Y. - Interfaz Gráfica Base (PySide6)
Versión 1.0 - Estética moderna, oscura, tipo núcleo/IA
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPalette, QColor


class FridayGUI(QMainWindow):
    """Ventana principal de la interfaz F.R.I.D.A.Y."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("J.A.R.V.I.S / F.R.I.D.A.Y. - Sistema Local")
        self.setMinimumSize(QSize(800, 600))
        self.setup_ui()
        self.apply_dark_theme()

    def setup_ui(self):
        """Configura los elementos visuales"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- Título visual ---
        title_label = QLabel("F.R.I.D.A.Y.")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #00D4FF;
                padding: 10px;
            }
        """)
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("Sistema de Asistencia Local - Versión Base GUI")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #AAAAAA;
                padding-bottom: 20px;
            }
        """)
        main_layout.addWidget(subtitle_label)

        # --- Indicador de estado ---
        self.status_frame = QFrame()
        status_layout = QHBoxLayout(self.status_frame)
        status_layout.setContentsMargins(10, 10, 10, 10)

        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #FF5555;  # Rojo por defecto (inactivo)
            }
        """)
        status_layout.addWidget(self.status_indicator)

        self.status_label = QLabel("En espera")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #CCCCCC;
            }
        """)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        main_layout.addWidget(self.status_frame)

        # --- Panel de conversación (log) ---
        self.conversation = QTextEdit()
        self.conversation.setReadOnly(True)
        self.conversation.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #CCCCCC;
            }
        """)
        self.conversation.append("=== F.R.I.D.A.Y. - Sistema Local ===")
        self.conversation.append("Estado: En espera de activación...")
        main_layout.addWidget(self.conversation)

        # --- Botones de control ---
        button_layout = QHBoxLayout()

        self.btn_start = QPushButton("▶ Iniciar Asistente")
        self.btn_start.setStyleSheet(self.button_style("#00AAFF", "#0088DD"))
        self.btn_start.clicked.connect(self.start_assistant)
        button_layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("■ Detener")
        self.btn_stop.setStyleSheet(self.button_style("#FF5555", "#CC4444"))
        self.btn_stop.clicked.connect(self.stop_assistant)
        self.btn_stop.setEnabled(False)
        button_layout.addWidget(self.btn_stop)

        self.btn_clear = QPushButton("🗑 Limpiar Historia")
        self.btn_clear.setStyleSheet(self.button_style("#555555", "#444444"))
        self.btn_clear.clicked.connect(self.clear_history)
        button_layout.addWidget(self.btn_clear)

        button_layout.addStretch()

        self.btn_memory = QPushButton("📝 Ver Memoria")
        self.btn_memory.setStyleSheet(self.button_style("#555555", "#444444"))
        self.btn_memory.clicked.connect(self.show_memory)
        button_layout.addWidget(self.btn_memory)

        main_layout.addLayout(button_layout)

    def button_style(self, color, hover):
        """Genera estilo para botones"""
        return f"""
            QPushButton {{
                background-color: {color};
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:disabled {{
                background-color: #333333;
                color: #777777;
            }}
        """

    def apply_dark_theme(self):
        """Aplica tema oscuro global"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#121212"))
        palette.setColor(QPalette.WindowText, QColor("#CCCCCC"))
        palette.setColor(QPalette.Base, QColor("#1E1E1E"))
        palette.setColor(QPalette.AlternateBase, QColor("#2A2A2A"))
        palette.setColor(QPalette.ToolTipBase, QColor("#121212"))
        palette.setColor(QPalette.ToolTipText, QColor("#CCCCCC"))
        palette.setColor(QPalette.Text, QColor("#CCCCCC"))
        palette.setColor(QPalette.Button, QColor("#2A2A2A"))
        palette.setColor(QPalette.ButtonText, QColor("#CCCCCC"))
        palette.setColor(QPalette.BrightText, QColor("#FF5555"))
        palette.setColor(QPalette.Highlight, QColor("#00AAFF"))
        palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
        self.setPalette(palette)

    def start_assistant(self):
        """Inicia el asistente (simulación por ahora)"""
        self.status_indicator.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #00FF00;  /* Verde: activo */
            }
        """)
        self.status_label.setText("Asistente activo")
        self.conversation.append("[SISTEMA] Asistente iniciado.")
        self.conversation.append("FRIDAY: Sistema Friday iniciado. En espera, señor.")
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)

    def stop_assistant(self):
        """Detiene el asistente (simulación)"""
        self.status_indicator.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #FF5555;  /* Rojo: inactivo */
            }
        """)
        self.status_label.setText("En espera")
        self.conversation.append("[SISTEMA] Asistente detenido.")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def clear_history(self):
        """Limpia el panel de conversación"""
        self.conversation.clear()
        self.conversation.append("=== F.R.I.D.A.Y. - Sistema Local ===")
        self.conversation.append("Historial limpiado.")

    def show_memory(self):
        """Muestra la memoria local (simulación)"""
        self.conversation.append("[MEMORIA] Cargando recuerdos...")
        # Aquí se conectará con friday_memory.json en el futuro
        self.conversation.append("MEMORIA: No hay recuerdos guardados, señor.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Fuente global
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = FridayGUI()
    window.show()
    sys.exit(app.exec())
