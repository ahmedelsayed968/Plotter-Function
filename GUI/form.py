from PySide2.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QDesktopWidget,QHBoxLayout,QVBoxLayout,QGroupBox,QMainWindow
import sys
from PySide2.QtGui import QIcon
sys.path.append('utils')

from Plot import Plotter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# from utils.Parser import Parser
# import utils

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Function Plotter')
        self.setGeometry(100,100,640,480)
        self.center()
        # self.setMinimumHeight(300)
        # self.setMinimumWidth(300)
        # self.setMaximumHeight(1080)
        # self.setMaximumWidth(720)
        
        #set icon for the window
        self.set_icon()
    
        self.set_button()
        #set Icon Mode
        self.set_icon_modes()

        
    def set_icon(self):
        self.setWindowIcon(QIcon('GUI\\img\\plotter.png'))
        
    def set_icon_modes(self):
        icon1 = QIcon('GUI\\img\\bar-graph.png')
        label1 = QLabel('Sample',self)
        pixmap1 = icon1.pixmap(100,100,QIcon.Active,QIcon.On)
        label1.setPixmap(pixmap1)
        
        icon2 = QIcon('GUI\\img\\graph.png')
        label2 = QLabel('Sample',self)
        pixmap2 = icon2.pixmap(100,100,QIcon.Active,QIcon.On)
        label2.setPixmap(pixmap2)
        label2.move(150,0)
        
        icon3 = QIcon('GUI\\img\\line-chart.png')
        label3 = QLabel('Sample',self)
        pixmap3 = icon3.pixmap(100,100,QIcon.Active,QIcon.On)
        label3.setPixmap(pixmap3)
        label3.move(300,0)
        
    
    def set_button(self):
        btn1 = QPushButton('Plot',self)
        btn1.move(50,100)
        btn1.clicked.connect(self.plot)    
        
    def plot(self):
        p = Plotter('5+x',1,10)
        x,y = p.plot_function()
        self.set_figure(x,y)
        
    def center(self):
        qReact = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.move(qReact.topLeft()) 
        
        
        
    def set_figure(self,x,y):
        fig = Figure()
        canvas = FigureCanvas(fig)
        
        ax = fig.add_subplot(111)
        ax.plot(x,y)
        
        layout = QHBoxLayout()
        layout.addWidget(canvas)
        
        # Create a widget and set the layout
        widget = QWidget()
        widget.setLayout(layout)
        
        # Set the central widget of the main window
        # self.setCentralWidget(widget)    
        
def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = Window()
    window.show()
    # app.exec_()
    sys.exit(app.exec_())       
        
if __name__ == '__main__':
    main()    