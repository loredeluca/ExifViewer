import sys
import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap

from mainwindow import Ui_MainWindow
import exifReader


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, listModel):
        super().__init__()
        self.setupUi(self)

        self.model = listModel
        self.count = 0

        self.img = QPixmap(self.model.current_image)

        self.addImgButton.clicked.connect(self.loadImage)
        self.deleteButton.clicked.connect(self.deleteImage)

        self.listWidget.itemDoubleClicked.connect(self.showNow)

        self.leftRotButton.clicked.connect(self.leftRotate)
        self.rightRotButton.clicked.connect(self.rightRotate)

        self.rightButton.clicked.connect(self.nextImg)
        self.leftButton.clicked.connect(self.previousImg)

    def loadImage(self):
        self.fileName = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files(*.JPG *.jpg *.jpeg")
        self.model.update(self.fileName[0])
        self.model.fill_list(self.fileName[0])

        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.fileName[0]), QtGui.QIcon.Normal)
        item.setIcon(icon)

        self.listWidget.addItem(item)

    def showNow(self):
        self.current_item = self.listWidget.currentRow()
        self.showImg()

    def showImg(self):
        self.model.get_element(self.current_item)
        self.img = QPixmap(self.model.current_image)
        self.label.setPixmap(self.img.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio))
        self.updateExif()

    def resizeEvent(self, event):
        self.label.setPixmap(self.img.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio))

    def deleteImage(self):
        try:
            if len(self.model.get_list()) > 0:
                self.model.delete_element(self.listWidget.currentRow())
                self.listWidget.takeItem(self.listWidget.currentRow())
                self.showNow()
            else:
                QMessageBox.about(self, "File Error", "Empty list")
        except IndexError:
            QMessageBox.about(self, "File Error", "All images deleted")

    def updateExif(self):
        self.tableModel = exifReader.Exif(self)
        exif = exifReader.getExif(self.model.current_image)
        if exif == 'NotFound':
            QMessageBox.about(self, "File Error", "Exif Not Found")
            self.tableView.setModel(None)
        else:
            self.tableModel.update(exif)
            self.tableView.setModel(self.tableModel)
            self.tableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            self.mapButton.clicked.connect(self.openMapPosition)

    def leftRotate(self):
        try:
            self.count = self.count - 1
            self.rotate()
        except IndexError:
            self.count = -1
            self.rotate()

    def rightRotate(self):
        try:
            self.count = self.count + 1
            self.rotate()
        except IndexError:
            self.count = 0
            self.rotate()

    def rotate(self):
        rotation = [0, 90, 180, -90]
        transform = QtGui.QTransform().rotate(rotation[self.count])
        self.img = QtGui.QPixmap(self.model.current_image)
        if rotation[self.count] == 0 or rotation[self.count] == 180:
            self.img = self.img.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
        else:
            self.img = self.img.scaled(self.label.height(), self.label.width(), QtCore.Qt.KeepAspectRatio)
        self.img = self.img.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(self.img)

    def nextImg(self):
        try:
            self.current_item += 1
            self.listWidget.setCurrentRow(self.current_item)
            if len(self.model.get_list()) == self.current_item:
                self.current_item = 0
                self.listWidget.setCurrentRow(self.current_item)
            self.showImg()
        except AttributeError:
            QMessageBox.about(self, "File Error", "No file selected")
        except IndexError:
            self.current_item = 0
            self.showImg()

    def previousImg(self):
        try:
            self.current_item -= 1
            self.listWidget.setCurrentRow(self.current_item)
            if self.current_item == -1:
                self.current_item = len(self.model.get_list()) - 1
                self.listWidget.setCurrentRow(self.current_item)
            self.showImg()
        except AttributeError:
            QMessageBox.about(self, "File Error", "No file selected")
        except IndexError:
            self.current_item = len(self.model.get_list()) - 1
            self.showImg()

    def openMapPosition(self):
        position = self.tableModel.get_position()
        if position is not None:
            webbrowser.open_new("https://www.google.com/maps/search/?api=1&query=" + str(position))
        else:
            QMessageBox.about(self, "File Error", "No GPS info")


class ListModel:
    def __init__(self):
        self.current_image = None
        self.image_list = []

    def update(self, new_img):
        self.current_image = new_img

    def fill_list(self, img):
        self.image_list.append(img)

    def get_element(self, pos):
        current_element = self.image_list[pos]
        self.update(current_element)

    def delete_element(self, pos):
        self.image_list = [x for i, x in enumerate(self.image_list) if i != pos]

    def get_list(self):
        return self.image_list


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    list_model = ListModel()

    window = MainWindow(list_model)
    window.show()
    app.exec()
