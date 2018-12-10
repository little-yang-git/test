# FileName : PyQtDemo.py
# Author   : Adil
# DateTime : 2018/2/1 11:07
# SoftWare : PyCharm


from PyQt5 import QtWidgets, QtGui
import sys

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.show()
sys.exit(app.exec_())
