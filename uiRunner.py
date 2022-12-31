import uiFile
import PyQt5.QtWidgets

# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = PyQt5.QtWidgets.QApplication(sys.argv)
ex = uiFile.Ui_MainWindow()
w = PyQt5.QtWidgets.QMainWindow()
ex.setupUi(w)
w.show()
sys.exit(app.exec())