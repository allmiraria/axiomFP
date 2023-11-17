import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QProgressBar, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import pandas as pd

class WorkerThread(QThread):
    progress_updated = pyqtSignal(int)
    finished_loading = pyqtSignal(pd.DataFrame)

    def __init__(self, file_path):
        super(WorkerThread, self).__init__()
        self.file_path = file_path

    def run(self):
        # Simulate loading a huge tab-delimited text file
        # Replace this with your actual file loading logic
        df = pd.read_csv(self.file_path, delimiter='\t')

        # Emit progress signals (update every 10%)
        total_rows = len(df)
        step = total_rows // 1000
        for i in range(0, total_rows, step):
            self.progress_updated.emit(i)

        self.finished_loading.emit(df)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.status_bar = QStatusBar()
        self.progressBar = QProgressBar()
        self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.status_bar.addWidget(self.progressBar)

        self.status_label = QLabel()
        self.status_bar.addWidget(self.status_label)

        self.load_button = QPushButton("Load File", self)
        self.load_button.clicked.connect(self.load_file)

        layout.addWidget(self.load_button)
        layout.addWidget(self.status_bar)

        central_widget.setLayout(layout)

        self.worker_thread = None

    def load_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Tab-Delimited File", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            self.load_data(file_path)

    def load_data(self, file_path):
        if self.worker_thread is not None and self.worker_thread.isRunning():
            print("Data loading already in progress.")
            return

        self.worker_thread = WorkerThread(file_path)
        self.worker_thread.progress_updated.connect(self.update_progress)
        self.worker_thread.finished_loading.connect(self.handle_finished_loading)

        self.progressBar.setValue(0)
        self.status_label.setText("Loading data...")
        self.worker_thread.start()

    def update_progress(self, value):
        self.progressBar.setValue(value)
        self.status_label.setText(f"Loading... {value}%")

    def handle_finished_loading(self, data_frame):
        # Do something with the loaded data, e.g., display it in a table
        print("Data loaded successfully!")
        print(data_frame.head())

        # Update status bar
        self.progressBar.setValue(100)
        self.status_label.setText("Loading complete.")

        # Clean up the worker thread
        self.worker_thread.quit()
        self.worker_thread.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
