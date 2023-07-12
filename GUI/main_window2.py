from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QMessageBox
import sys
sys.path.append('utils')
from Plot import Plotter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PySide2.QtGui import QIcon
import math
# from PySide2.QtWidgets.QMessageBox import Icon
class EmptyField(Exception):
        pass

class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                MainWindow.setObjectName("Function Plotter")
                MainWindow.resize(879, 727)
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                # self.setStyleSheet('background-color: yellow;')
                self.centralwidget.setObjectName("centralwidget")
                self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
                MainWindow.setWindowIcon(QIcon('GUI\img\line-chart.png'))
                
                self.configure_layout()
                self.add_validator()
                self.configure_plot()
                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)
                
                
        def add_validator(self):
                validator_x_values = QRegExpValidator(QRegExp(r'^-?\d+$|^-?\d+(\.\d+)?$'))
                validator_function_input = QRegExpValidator(QRegExp(r'^[0-9|x|^\/*+\-|sin|cos|tan|e|()]+$'))
                self.lineEdit_2.setValidator(validator_x_values)
                self.lineEdit_3.setValidator(validator_x_values)
                self.lineEdit.setValidator(validator_function_input)
                
        def plot(self):
                self.figure.clear()
                x_min = self.lineEdit_2.text()
                x_max = self.lineEdit_3.text()
                try:    
                        self.validate_fields(x_min,x_max)
                        p = Plotter(self.lineEdit.text(),float(x_min),float(x_max))
                        x_values , y_values = p.plot_function() 
                        # plt.ylim(min(y_values), max(y_values))        
                        plt.plot(x_values,y_values)
                        plt.xlabel('x-value')
                        plt.ylabel('y-value')
                        plt.title(f'f(x):= {self.lineEdit.text()}')
                        self.convas.draw()
                except Exception as e:
                        msg = QMessageBox()
                        msg.setWindowTitle('Error')
                        msg.setText(f'{e}')
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()        
                        
        def validate_fields(self,x_min,x_max):
                if self.lineEdit.text() == '':
                        raise EmptyField('Please Enter the Function')
                if x_min == '':
                        raise EmptyField('Please Enter value of x-min') 
                
                if x_max == '':
                        raise EmptyField('Please Enter value of x-max') 
                
                                        
                                
        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "Function Plotter"))
                self.label.setText(_translate("MainWindow", "Input Function "))
                self.label_2.setText(_translate("MainWindow", "x-min"))
                self.label_3.setText(_translate("MainWindow", "x-max"))
                self.pushButton.setText(_translate("MainWindow", "Plot"))
                self.label_4.setText(_translate("MainWindow", "Graph"))
                
        def configure_layout(self):
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.frame_2 = QtWidgets.QFrame(self.centralwidget)
                self.frame_2.setEnabled(True)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
                self.frame_2.setSizePolicy(sizePolicy)
                self.frame_2.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.frame_2.setAutoFillBackground(True)
                self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_2.setObjectName("frame_2")
                self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
                self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
                self.verticalLayout_4.setObjectName("verticalLayout_4")
                self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
                self.horizontalLayout_2.setContentsMargins(-1, -1, 9, -1)
                self.horizontalLayout_2.setObjectName("horizontalLayout_2")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout()
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.label = QtWidgets.QLabel(self.frame_2)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
                self.label.setSizePolicy(sizePolicy)
                self.label.setStyleSheet("QFrame{\n"
        "    font: 18pt \"MS Shell Dlg 2\";\n"
        "    color: rgb(40, 180, 99);\n"
        "}")
                self.label.setTextFormat(QtCore.Qt.PlainText)
                self.label.setObjectName("label")
                self.verticalLayout_2.addWidget(self.label)
                self.lineEdit = QtWidgets.QLineEdit(self.frame_2)
                self.lineEdit.setMinimumSize(QtCore.QSize(0, 37))
                self.lineEdit.setObjectName("lineEdit")
                self.verticalLayout_2.addWidget(self.lineEdit)
                self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_3.setObjectName("horizontalLayout_3")
                self.verticalLayout = QtWidgets.QVBoxLayout()
                self.verticalLayout.setObjectName("verticalLayout")
                self.label_2 = QtWidgets.QLabel(self.frame_2)
                self.label_2.setStyleSheet("QFrame{\n"
        "    font: 12pt \"MS Shell Dlg 2\";\n"
        "    color: rgb(40, 180, 99);\n"
        "}")
                self.label_2.setObjectName("label_2")
                self.verticalLayout.addWidget(self.label_2)
                self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_2)
                self.lineEdit_2.setText("")
                self.lineEdit_2.setObjectName("lineEdit_2")
                self.verticalLayout.addWidget(self.lineEdit_2)
                self.horizontalLayout_3.addLayout(self.verticalLayout)
                self.verticalLayout_3 = QtWidgets.QVBoxLayout()
                self.verticalLayout_3.setObjectName("verticalLayout_3")
                self.label_3 = QtWidgets.QLabel(self.frame_2)
                self.label_3.setStyleSheet("QFrame{\n"
        "    font: 12pt \"MS Shell Dlg 2\";\n"
        "    color: rgb(40, 180, 99);\n"
        "}")
                self.label_3.setObjectName("label_3")
                self.verticalLayout_3.addWidget(self.label_3)
                self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_2)
                self.lineEdit_3.setText("")
                self.lineEdit_3.setObjectName("lineEdit_3")
                self.verticalLayout_3.addWidget(self.lineEdit_3)
                self.horizontalLayout_3.addLayout(self.verticalLayout_3)
                self.verticalLayout_2.addLayout(self.horizontalLayout_3)
                self.pushButton = QtWidgets.QPushButton(self.frame_2)
                self.pushButton.clicked.connect(self.plot)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
                self.pushButton.setSizePolicy(sizePolicy)
                self.pushButton.setIconSize(QtCore.QSize(32, 16))
                self.pushButton.setObjectName("pushButton")
                self.verticalLayout_2.addWidget(self.pushButton)
                spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_2.addItem(spacerItem)
                self.horizontalLayout_2.addLayout(self.verticalLayout_2)
                self.verticalLayout_5 = QtWidgets.QVBoxLayout()
                self.verticalLayout_5.setObjectName("verticalLayout_5")
                self.label_4 = QtWidgets.QLabel(self.frame_2)
                self.label_4.setStyleSheet("QFrame{\n"
        "    font: 18pt \"MS Shell Dlg 2\";\n"
        "    color: rgb(40, 180, 99);\n"
        "}")
                self.label_4.setObjectName("label_4")
                self.verticalLayout_5.addWidget(self.label_4)
                self.frame_3 = QtWidgets.QFrame(self.frame_2)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
                self.frame_3.setSizePolicy(sizePolicy)
                self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_3.setObjectName("frame_3")
                self.verticalLayout_5.addWidget(self.frame_3)
                self.horizontalLayout_2.addLayout(self.verticalLayout_5)
                self.verticalLayout_4.addLayout(self.horizontalLayout_2)
                self.horizontalLayout.addWidget(self.frame_2)
                MainWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 879, 21))
                self.menubar.setObjectName("menubar")
                MainWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)        

        def configure_plot(self):
                self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_3)
                self.horizontalLayout_4.setObjectName('horizontalLayout_4')
                self.figure = plt.figure()
                self.convas = FigureCanvas(self.figure)
                self.horizontalLayout_4.addWidget(self.convas)
                
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
