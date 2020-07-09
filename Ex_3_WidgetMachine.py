# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'machine_a_sous.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    """
    This code has been adopted from https://github.com/flvoyer/SlotMachine. This code is used in the execution of the slots machine UI.
    """

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(940, 320)
        self.mLabel = QtWidgets.QLabel(Form)
        self.mLabel.setGeometry(QtCore.QRect(10, 10, 300, 300))
        self.mLabel.setAutoFillBackground(False)
        self.mLabel.setStyleSheet("")
        self.mLabel.setText("")
        self.mLabel.setObjectName("mLabel")
        self.mLabel2 = QtWidgets.QLabel(Form)
        self.mLabel2.setGeometry(QtCore.QRect(320, 10, 300, 300))
        self.mLabel2.setAutoFillBackground(False)
        self.mLabel2.setStyleSheet("")
        self.mLabel2.setText("")
        self.mLabel2.setObjectName("mLabel2")
        self.mLabel3 = QtWidgets.QLabel(Form)
        self.mLabel3.setGeometry(QtCore.QRect(630, 10, 300, 300))
        self.mLabel3.setAutoFillBackground(False)
        self.mLabel3.setStyleSheet("")
        self.mLabel3.setText("")
        self.mLabel3.setObjectName("mLabel3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
