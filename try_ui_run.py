# You need one (and only one) QApplication instance per application.
        # Pass in sys.argv to allow command line arguments for your app.
        # If you know you won't use command line arguments QApplication([]) works too.
import PyQt5
import client_start
import sys

app = PyQt5.QtWidgets.QApplication(sys.argv)
ex = client_start.Ui_MainWindow()
w = PyQt5.QtWidgets.QMainWindow()

ex.setupUi(w)
w.show()
app.exec()