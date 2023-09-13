from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

dialog_style = '''
QDialog {
    background-color: rgb(50, 50, 50);
    color: white;
    font-size: 12px;
    width: 50px;
}

QLabel {
    color: white;
    width: 50px;
}
'''


class LayerSettingDialog(QtWidgets.QDialog):
    def __init__(self, window_name, min_val, max_val, val):
        super().__init__()

        self.setWindowTitle(window_name)
        self.setStyleSheet(dialog_style)

        self.val = val

        self.val_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.val_slider.setValue(val)
        self.val_slider.setMinimum(min_val)
        self.val_slider.setMaximum(max_val)
        self.val_slider.setSingleStep(1)
        self.val_slider.sliderMoved.connect(self.val_spinbox_changed)

        self.val_spinbox = QtWidgets.SpinBox()
        self.val_spinbox.setValue(val)
        self.val_spinbox.setMaximum(max_val)
        self.val_spinbox.setMinimum(min_val)
        self.val_spinbox.setSingleStep(1)
        self.val_spinbox.valueChanged.connect(self.value_changed)

        # ok button, used to close window
        ok_btn = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        ok_btn.accepted.connect(self.accept)

        # add widget to layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.val_slider)
        layout.addWidget(self.val_spinbox)
        layout.addSpacing(10)
        layout.addWidget(ok_btn)
        self.setLayout(layout)

    def accept(self) -> None:
        self.close()

    def val_spinbox_changed(self):
        val = self.val_slider.value()
        self.val = val
        self.val_spinbox.setValue(val)

    def value_changed(self):
        val = self.val_spinbox.value()
        self.val = val
        self.val_slider.setValue(val)


class SliceSettingDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Current Slice Settings')
        self.setStyleSheet(dialog_style)

        self.cut = 'Coronal'
        self.width = 0
        self.height = 0
        self.distance = 0

        self.cut_combo = QtWidgets.QComboBox()
        self.cut_combo.addItems(['Coronal', 'Sagittal', 'Horizontal'])
        self.cut_combo.currentIndexChanged.connect(self.cut_changed)

        width_label = QtWidgets.QLabel('Width (mm):')
        height_label = QtWidgets.QLabel('Height (mm):')
        distance_label = QtWidgets.QLabel('Distance w.r.t. Bregma (mm):')

        self.width_val = QtWidgets.QDoubleSpinBox()
        self.width_val.setValue(0)
        self.width_val.setRange(-50, 50)
        self.width_val.valueChanged.connect(self.width_val_changed)
        self.height_val = QtWidgets.QDoubleSpinBox()
        self.height_val.setValue(0)
        self.height_val.setRange(-50, 50)
        self.height_val.valueChanged.connect(self.height_val_changed)
        self.distance_val = QtWidgets.QDoubleSpinBox()
        self.distance_val.setValue(0)
        self.distance_val.setRange(-50, 50)
        self.distance_val.valueChanged.connect(self.distance_val_changed)

        # ok button, used to close window
        ok_btn = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        ok_btn.accepted.connect(self.accept)

        # add widget to layout
        content_frame = QtWidgets.QFrame()
        content_layout = QtWidgets.QGridLayout(content_frame)
        content_layout.addWidget(self.cut_combo, 0, 0, 1, 2)
        content_layout.addWidget(width_label, 1, 0, 1, 1)
        content_layout.addWidget(self.width_val, 1, 1, 1, 1)
        content_layout.addWidget(height_label, 2, 0, 1, 1)
        content_layout.addWidget(self.height_val, 2, 1, 1, 1)
        content_layout.addWidget(distance_label, 3, 0, 1, 1)
        content_layout.addWidget(self.distance_val, 3, 1, 1, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(content_frame)
        layout.addWidget(ok_btn)
        self.setLayout(layout)

    def accept(self) -> None:
        self.close()

    def cut_changed(self):
        self.cut = self.cut_combo.currentText()

    def width_val_changed(self):
        self.width = self.width_val.value()

    def height_val_changed(self):
        self.height = self.height_val.value()

    def distance_val_changed(self):
        self.distance = self.distance_val.value()


class QDoubleButton(QtWidgets.QPushButton):
    right_clicked = QtCore.pyqtSignal()
    left_clicked = QtCore.pyqtSignal()
    double_clicked = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QDoubleButton, self).__init__(*args, **kwargs)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(150)
        self.timer.timeout.connect(self.timeout)

        self.is_double = False
        self.is_left_click = True

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if not self.timer.isActive():
                self.timer.start()

            self.is_left_click = False
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.is_left_click = True

            return True

        elif event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
            self.is_double = True
            return True

        return False

    def timeout(self):
        if self.is_double:
            self.double_clicked.emit()
        else:
            if self.is_left_click:
                self.left_clicked.emit()
            else:
                self.right_clicked.emit()

        self.is_double = False


class QLabelClickable(QtWidgets.QLabel):
    # doubleClicked = QtCore.pyqtSignal(object)
    clicked = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.ultimo = 'Click'

    def mouseReleaseEvent(self, event):
        if self.ultimo == 'Click':
            QtCore.QTimer.singleShot(QtWidgets.QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)
        else:
            self.ultimo = 'doubleClick'
            self.clicked.emit(self.ultimo)

    def mouseDoubleClickEvent(self, event):
        self.ultimo = 'doubleClick'

    def performSingleClickAction(self):
        if self.ultimo == 'Click':
            self.clicked.emit(self.ultimo)
            self.update()


class QFrameClickable(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(QFrameClickable, self).__init__(parent)

    # def mousePressEvent(self, QMouseEvent):
    #     if QMouseEvent.button() == Qt.LeftButton:
    #         self.clicked.emit()
    #     elif QMouseEvent.button() == Qt.RightButton:
    #         self.clicked.emit()
    #     self.update()

    def mousePressEvent(self, event):
        self.ultimo = 'Click'

    def mouseReleaseEvent(self, event):
        if self.ultimo == 'Click':
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)
        else:
            self.ultimo = 'doubleClick'
            self.clicked.emit(self.ultimo)

    def mouseDoubleClickEvent(self, event):
        self.ultimo = 'doubleClick'

    def performSingleClickAction(self):
        if self.ultimo == 'Click':
            self.clicked.emit(self.ultimo)
            self.update()


class LineEditEntered(QtWidgets.QLineEdit):
    sig_return_pressed = QtCore.pyqtSignal()

    def __init__(self):
       QtWidgets.QLineEdit.__init__(self)

    def keyPressEvent(self, event):
        super(LineEditEntered, self).keyPressEvent(event)

        if event.key() == Qt.Key_Return:
            self.sig_return_pressed.emit()
        elif event.key() == Qt.Key_Enter:
            self.sig_return_pressed.emit()
