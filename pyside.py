import sys
from Pyside6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Titulek")
window.resize(200,100)


window.show(app.exec())
sys.exit(app.exec())