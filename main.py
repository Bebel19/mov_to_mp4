import os
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal

class ConverterThread(QThread):
    # Signal pour envoyer les messages de statut
    statusSignal = pyqtSignal(str)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        command = [
            "ffmpeg", "-i", self.input_path,
            "-c:v", "libx264", "-preset", "medium",
            "-c:a", "aac", "-strict", "experimental",
            self.output_path
        ]
        try:
            subprocess.run(command, check=True)
            self.statusSignal.emit(f'Conversion successful: {self.output_path}')
        except subprocess.CalledProcessError:
            self.statusSignal.emit('Error during conversion.')

class VideoConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MOV to MP4 Converter')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Select a MOV file and convert it to MP4.')
        layout.addWidget(self.label)

        self.btnSelectFile = QPushButton('Select MOV File', self)
        self.btnSelectFile.clicked.connect(self.openFileNameDialog)
        layout.addWidget(self.btnSelectFile)

        self.btnConvert = QPushButton('Convert to MP4', self)
        self.btnConvert.clicked.connect(self.prepareConversion)
        layout.addWidget(self.btnConvert)

        self.setLayout(layout)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a MOV File", "", "MOV Files (*.mov)", options=options)
        if fileName:
            self.selectedFile = fileName
            self.label.setText(f'Selected File: {fileName}')

    def prepareConversion(self):
        if hasattr(self, 'selectedFile'):
            input_path = self.selectedFile
            output_path = os.path.splitext(input_path)[0] + ".mp4"
            self.convertVideo(input_path, output_path)
        else:
            self.label.setText('No file selected.')

    def convertVideo(self, input_path, output_path):
        self.converterThread = ConverterThread(input_path, output_path)
        self.converterThread.statusSignal.connect(self.updateStatusLabel)
        self.converterThread.start()

    def updateStatusLabel(self, message):
        self.label.setText(message)

def main():
    app = QApplication(sys.argv)
    ex = VideoConverter()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
