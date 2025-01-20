import sys
import vosk
import pyaudio
import json
import audioop
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget,
    QComboBox, QTextEdit, QMessageBox
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from libretranslatepy import LibreTranslateAPI

class SpeechTranslationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simultaneous Interpretation")
        self.setGeometry(100, 100, 600, 400)

        self.api = LibreTranslateAPI("http://localhost:5000")
        self.model_paths = {
            "Chinese": "model/vosk-model-cn-0.22",
            "English": "model/vosk-model-en-us-0.42-gigaspeech",
            "Russian": "model/vosk-model-ru-0.42"
        }

        self.source_lang = None
        self.target_lang = None
        self.rec = None
        self.stream = None
        self.buffered_text = ""

        self.init_ui()

        # 启动 LibreTranslate 服务
        self.start_libretranslate()

        # 初始化 PyAudio
        self.p = pyaudio.PyAudio()
        self.frames_per_buffer = 16000

        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_audio)

    def init_ui(self):
        layout = QVBoxLayout()

        self.source_label = QLabel("Source language:")
        self.source_combo = QComboBox()
        self.source_combo.addItems(self.model_paths.keys())

        self.target_label = QLabel("Target Language:")
        self.target_combo = QComboBox()
        self.target_combo.addItems(self.model_paths.keys())

        self.start_button = QPushButton("Start interpretation")
        self.start_button.clicked.connect(self.start_translation)

        self.stop_button = QPushButton("Stop interpretation")
        self.stop_button.clicked.connect(self.stop_translation)
        self.stop_button.setEnabled(False)

        self.recognized_text_label = QLabel("Recognized content:")
        self.recognized_text = QTextEdit()
        self.recognized_text.setReadOnly(True)

        self.translated_text_label = QLabel("Interpreted content:")
        self.translated_text = QTextEdit()
        self.translated_text.setReadOnly(True)

        layout.addWidget(self.source_label)
        layout.addWidget(self.source_combo)
        layout.addWidget(self.target_label)
        layout.addWidget(self.target_combo)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.recognized_text_label)
        layout.addWidget(self.recognized_text)
        layout.addWidget(self.translated_text_label)
        layout.addWidget(self.translated_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_libretranslate(self):
        try:
            subprocess.Popen(["libretranslate", "--host", "127.0.0.1", "--port", "5000"], shell=True)
            QMessageBox.information(self, "Message", "LibreTranslate Service has started!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Starting LibreTranslate failed: {e}")
            sys.exit(1)

    def start_translation(self):
        source_lang_name = self.source_combo.currentText()
        target_lang_name = self.target_combo.currentText()

        if source_lang_name == target_lang_name:
            QMessageBox.warning(self, "Warning", "Source Language should be different from target language!")
            return

        self.source_lang = "zh" if source_lang_name == "Chinese" else "en" if source_lang_name == "English" else "ru"
        self.target_lang = "zh" if target_lang_name == "Chinese" else "en" if target_lang_name == "English" else "ru"
        QMessageBox.information(self, "Message", "Loading models...")
        try:
            model_path = self.model_paths[source_lang_name]
            model = vosk.Model(model_path)
            self.rec = vosk.KaldiRecognizer(model, 48000)
            QMessageBox.information(self, "Message", "Models loaded,you can speak now!")
            self.stream = self.p.open(
                format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=self.frames_per_buffer
            )
            self.stream.start_stream()
            self.timer.start(100)  # 每 100ms 处理音频

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Starting interpretation fail: {e}")

    def stop_translation(self):
        self.timer.stop()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def process_audio(self):
        try:
            data = self.stream.read(self.frames_per_buffer, exception_on_overflow=False)
            rms = audioop.rms(data, 2)

            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                text = result.get("text", "").strip()

                if self.source_lang == "zh":
                    text = text.replace(" ", "")

                if text:
                    self.buffered_text += " " + text
                    self.recognized_text.append(text)

                    # 翻译文本
                    translated = self.api.translate(self.buffered_text, source=self.source_lang, target=self.target_lang)
                    self.translated_text.append(translated)
                    self.buffered_text = ""

        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Audio error:{e}")

    def closeEvent(self, event):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Arial", 12)  # 设置字体为 Arial，大小为 12
    app.setFont(font)
    window = SpeechTranslationApp()
    window.show()
    sys.exit(app.exec_())
