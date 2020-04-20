import sys
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow

WIDTH = 960
HEIGHT = 540

class VidEditor():
    def __init__(self, inputImg):
        self.img = inputImg

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        # Set up the window for the overall app
        self.setGeometry(50, 50, WIDTH, HEIGHT)
        self.setWindowTitle("CrispCut")

        # Set up the label in the middle of the app
        self.label = QtWidgets.QLabel(self)
        self.label.setText("my fist label!")
        self.label.move((WIDTH / 2) - 100, (HEIGHT / 2) - 50)
        self.label.resize(200, 100)

        # Set up the individual actions that will go in the sub-menus
        # of the menu bar
        self.openAction = QtWidgets.QAction("Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open a file")
        self.openAction.triggered.connect(lambda: self.openFile())
        
        self.cutAction = QtWidgets.QAction("Cut", self)
        self.cutAction.setShortcut("Ctrl+R")
        self.cutAction.setStatusTip("Cut video")
        self.cutAction.triggered.connect(lambda: self.cut("Cut was clicked"))

        # Set up the menu bar at the top of the screen
        self.mainMenu = QtWidgets.QMenuBar(self)
        self.mainMenu.setGeometry(0, 0, WIDTH, 25)
        self.menuFile = self.mainMenu.addMenu("File")
        self.menuFile.addAction(self.openAction)
        self.menuEdit = self.mainMenu.addMenu("Edit")
        self.menuEdit.addAction(self.cutAction)

        # Define the image to edit (even though it hasn't been specified yet)
        self.changePixmap = None
        self.vidCap = None
        self.workingImg = None

        self.timer = None
        self.isPlaying = False

        self.home()

    def clicked(self, text):
        self.label.setText(text)
    
    def home(self):
        self.show()

    def openFile(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File yee')[0]
        self.vidCap = cv2.VideoCapture(name)
        _, self.workingImg = self.vidCap.read()
        self.updateImg()
        self.label.setScaledContents(True)
        self.label.setGeometry(0, 26, self.width(), self.height() - 75)

        self.playPauseAction = QtWidgets.QAction("Play/Pause", self)
        self.playPauseAction.setShortcut(" ")
        self.playPauseAction.setStatusTip("Toggle Play/Pause")
        self.playPauseAction.triggered.connect(lambda: self.playPause())
        self.menuEdit.addAction(self.playPauseAction)

    def updateImg(self):
        color_swapped_image = cv2.cvtColor(self.workingImg, cv2.COLOR_BGR2RGB)
        height, width, _ = color_swapped_image.shape
        self.changePixmap = QtGui.QImage(color_swapped_image.data,
                                    width,
                                    height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.changePixmap))
        

    def playPause(self):
        if self.timer is None:
            self.timer = QtCore.QTimer(self)
            self.timer.setInterval(1000 / self.vidCap.get(cv2.CAP_PROP_FPS))
            self.timer.timeout.connect(lambda: self.advanceFrame())
            self.timer.start()
        elif self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    def advanceFrame(self):
        _, self.workingImg = self.vidCap.read()
        if self.workingImg is None:
            print("All done!")
        else:
            self.updateImg()

    
    def resizeEvent(self, event):
        self.label.resize(self.width(), self.height() - 75)
        self.mainMenu.setGeometry(0, 0, self.width(), 25)
        return super().resizeEvent(event)

def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()