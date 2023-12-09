import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from main import return_next

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dataset Annotation App')
        self.setGeometry(100, 100, 1000, 600)


        self.folder_button = QtWidgets.QPushButton('Select Dataset Folder', self)
        self.folder_button.clicked.connect(self.select_folder)

        self.create_annotation_button = QtWidgets.QPushButton('Create Annotation File', self)
        self.create_annotation_button.clicked.connect(self.create_annotation)

        self.reorganize_dataset_button = QtWidgets.QPushButton('Reorganize Dataset', self)
        self.reorganize_dataset_button.clicked.connect(self.reorganize_dataset)

        self.next_cat_button = QtWidgets.QPushButton('Next Tiger', self)
        self.next_cat_button.clicked.connect(self.display_next_tiger)

        self.next_dog_button = QtWidgets.QPushButton('Next Leopard', self)
        self.next_dog_button.clicked.connect(self.display_next_leopard)

        self.layout1 = QtWidgets.QVBoxLayout()
        self.layout2 = QtWidgets.QVBoxLayout()

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.resize(1000, 400)

        self.layout1.addStretch(1)
        self.layout1.addWidget(self.lbl)

        self.layout2.addStretch(1)
        self.layout2.addWidget(self.folder_button)
        self.layout2.addWidget(self.create_annotation_button)
        self.layout2.addWidget(self.reorganize_dataset_button)
        self.layout2.addWidget(self.next_cat_button)
        self.layout2.addWidget(self.next_dog_button)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout2)
        self.setCentralWidget(widget)

    def select_folder(self):
        pass

    def create_annotation(self):
        pass

    def reorganize_dataset(self):
        pass

    def display_next_tiger(self):
        lbl_size = self.lbl.size()
        next_image = return_next('tiger')
        if next_image:
            img = QPixmap(next_image).scaled(lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:
            self.display_next_tiger()

    def display_next_leopard(self):
        lbl_size = self.lbl.size()
        next_image = return_next('leopard')
        if next_image:
            img = QPixmap(next_image).scaled(lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:
            self.display_next_leopard()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
