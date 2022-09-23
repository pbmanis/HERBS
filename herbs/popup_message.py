from pyqtgraph.Qt import QtWidgets


class PopupMessage(QtWidgets.QMessageBox):

    def __init__(self, parent=None):
        QtWidgets.QMessageBox.__init__(self)

        self.setWindowTitle("Caution!")
        self.setText('Histological image: is oversized.')
        button = self.exec()
        if button == QtWidgets.QMessageBox.StandardButton.Ok:
            print('222')