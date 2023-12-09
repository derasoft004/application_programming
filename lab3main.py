import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import *

from main import return_next, copy_dataset_rand, copy_dataset2, annotation_maker2

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.dataset_path = ''
        self.main_window()

    def main_window(self, dataset_path='<не выбран>'):
        self.setWindowTitle('Dataset Annotation App')
        self.setGeometry(200, 100, 1000, 650)

        self.folder_button = QtWidgets.QPushButton('Select Dataset Folder', self)
        self.folder_button.clicked.connect(self.select_folder)

        if dataset_path == '<не выбран>' or not dataset_path:
            self.text_label1 = QLabel(f'исходный датасет: "dataset"', self)
        else:
            self.text_label1 = QLabel(f'исходный датасет: "{dataset_path}".', self)
        self.text_label1.setAlignment(Qt.AlignCenter)

        self.create_annotation_button = QtWidgets.QPushButton('Create Annotation File', self)
        self.create_annotation_button.clicked.connect(self.create_annotation)

        self.reorganize_dataset_button = QtWidgets.QPushButton('Reorganize Dataset', self)
        self.reorganize_dataset_button.clicked.connect(self.reorganize_dataset)

        self.next_cat_button = QtWidgets.QPushButton('Next Tiger', self)
        self.next_cat_button.clicked.connect(self.display_next_tiger)

        self.next_dog_button = QtWidgets.QPushButton('Next Leopard', self)
        self.next_dog_button.clicked.connect(self.display_next_leopard)

        # self.layout1 = QtWidgets.QVBoxLayout()
        self.layout2 = QtWidgets.QVBoxLayout()
        # self.layout2.setAlignment(Qt.AlignCenter)

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setFixedSize(1000, 400)


        self.layout2.addStretch(1)
        self.layout2.addWidget(self.lbl)
        self.layout2.addWidget(self.text_label1)
        self.layout2.addWidget(self.folder_button)
        self.layout2.addWidget(self.create_annotation_button)
        self.layout2.addWidget(self.reorganize_dataset_button)
        self.layout2.addWidget(self.next_cat_button)
        self.layout2.addWidget(self.next_dog_button)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout2)
        self.setCentralWidget(widget)

    def press_button3(self):
        """
        нажатие на кнопку отправки в общем задании 1
        :return:
        """
        try:
            print(self.dataset_path)
            self.main_window(self.dataset_path)
        except AttributeError:
            self.main_window('not selected')

    def select_folder(self): # 3
        """
        общее задание 1
        :return:
        """
        self.layout3 = QtWidgets.QVBoxLayout()
        self.setGeometry(200, 100, 100, 100)

        self.layout3.addStretch(1)

        self.textLabel = QLabel('enter the path to the source dataset folder\n'
                                'hint: the original folder with images is called "dataset";'
                                , self)
        # 'the folder with images of task 2 is called "new_dataset_task_2";\n'
        #                                 'the folder with images of task 3 is called "new_dataset_task_3";'
        self.textLabel.setAlignment(Qt.AlignCenter)

        self.inputField = QLineEdit(self)
        self.inputField.textChanged.connect(self.text_changed)

        self.changer = QtWidgets.QPushButton('Change folder', self)
        self.changer.clicked.connect(self.press_button3)

        self.backer = QtWidgets.QPushButton('back', self)
        self.backer.clicked.connect(self.main_window)

        self.layout3.addWidget(self.textLabel)
        self.layout3.addWidget(self.inputField)
        self.layout3.addWidget(self.changer)
        self.layout3.addWidget(self.backer)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout3)
        self.setCentralWidget(widget)

        # folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')

    def text_changed(self, text):
        """
        Метод, который будет вызываться при изменении текста в поле ввода
        :param text:
        :return:
        """
        self.dataset_path = text

    def creater4(self): # задание 2
        # try:
        annotation_maker2('dataset', self.annotation_path, 'annotation.csv', 'tiger/', 'leopard/')
        # except :
        #     annotation_maker2('dataset', '', 'annotation.csv', 'tiger/', 'leopard/')
        # elif self.dataset_path == 'new_dataset_task_2':
        #     annotation_maker('new_dataset_task_2', 'annotation.csv', '', '')
        # elif self.dataset_path == 'new_dataset_task_3':
        #     copy_dataset_rand('new_dataset_task_3', '0new_dataset_annotation.csv')
        self.main_window()

    def text_changed2(self, text):
        self.annotation_path = text

    def create_annotation(self): # 4
        """
        общее задание 2
        :return:
        """
        self.layout4 = QtWidgets.QVBoxLayout()
        self.setGeometry(200, 100, 400, 300)
        self.layout4.addStretch(1)

        self.annotation_path = ''
        self.textLabel = QLabel(f'Annotation for elementary dataset. Input path where it\'s will saved\n' 
                                f'(if you input nothing, will created a directory "file_annotation" and '
                                f'annotation there)', self)
        self.textLabel.setAlignment(Qt.AlignCenter)

        self.inputField = QLineEdit(self)
        self.inputField.textChanged.connect(self.text_changed2)

        self.changer = QtWidgets.QPushButton('Create annotation', self)
        self.changer.clicked.connect(self.creater4)

        self.backer = QtWidgets.QPushButton('back', self)
        self.backer.clicked.connect(self.main_window)

        self.layout4.addWidget(self.textLabel)
        self.layout4.addWidget(self.inputField)
        self.layout4.addWidget(self.changer)
        self.layout4.addWidget(self.backer)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout4)
        self.setCentralWidget(widget)

        # annotation_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Annotation File')

    def text_changed3(self, text):
        self.copy_path = text

    def creater5_11(self):
        copy_dataset2(self.copy_path, 'tiger', 'new_dataset_type_11')
        copy_dataset2(self.copy_path, 'leopard', 'new_dataset_type_11')
        self.main_window()

    def creater5_22(self):
        copy_dataset_rand(self.copy_path, '0new_dataset_annotation.csv')
        self.main_window()

    def reorganize_dataset(self): # 5
        self.layout5 = QtWidgets.QVBoxLayout()
        self.setGeometry(200, 100, 400, 300)
        self.layout5.addStretch(1)

        self.textLabel = QLabel(f'Creating a dataset with a different file organization', self)
        self.textLabel.setAlignment(Qt.AlignCenter)

        self.creater5_1 = QtWidgets.QPushButton('Create a new dataset (type 1), where pictures will named as: '
                                                '"<animal>_<number>"\n'
                                                f'(if you input nothing, will created a directory "new_dataset" and '
                                                f'pictures there)', self)
        self.creater5_1.clicked.connect(self.creater5_11)

        self.inputField = QLineEdit(self)
        self.inputField.textChanged.connect(self.text_changed3)

        self.creater5_2 = QtWidgets.QPushButton('Create a new dataset (type 2), where pictures will named as:'
                                                ' "<random-number>"\n'
                                                f'(if you input nothing, will created a directory "new_dataset" and '
                                                f'pictures there)', self)
        self.creater5_2.clicked.connect(self.creater5_22)

        self.backer = QtWidgets.QPushButton('back', self)
        self.backer.clicked.connect(self.main_window)

        self.layout5.addWidget(self.textLabel)
        self.layout5.addWidget(self.inputField)
        self.layout5.addWidget(self.creater5_1)
        self.layout5.addWidget(self.creater5_2)
        self.layout5.addWidget(self.backer)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout5)
        self.setCentralWidget(widget)

        # destination_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Destination Folder')

    def display_next_tiger(self):
        if self.dataset_path == 'dataset':
            lbl_size = self.lbl.size()
            next_image = return_next('tiger')
            if next_image:
                img = QPixmap(next_image).scaled(lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
                self.lbl.setPixmap(img)
                self.lbl.setAlignment(Qt.AlignCenter)
            else:
                self.display_next_tiger()
        else:
            self.select_folder()

    def display_next_leopard(self):
        if self.dataset_path == 'dataset':
            lbl_size = self.lbl.size()
            next_image = return_next('leopard')
            if next_image:
                img = QPixmap(next_image).scaled(lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
                self.lbl.setPixmap(img)
                self.lbl.setAlignment(Qt.AlignCenter)
            else:
                self.display_next_tiger()
        else:
            self.select_folder()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
