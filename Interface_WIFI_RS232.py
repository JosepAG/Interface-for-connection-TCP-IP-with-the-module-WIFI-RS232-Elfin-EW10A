from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from socket import *
import datetime
import select
from PyQt5.QtWidgets import *


class MainWindow(QtWidgets.QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.timer = QtCore.QTimer()
        self.setWindowTitle("CEAM")
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        widget = QLineEdit()
        self.button1 = QPushButton(widget)
        self.button1.setText("Run")
        self.button1.move(211, 200)
        self.labl = QLabel()
        self.labl.setText('Label Example')
        self.labl.setAlignment(QtCore.Qt.AlignCenter)
        widget.setMaxLength(15)
        widget.setAlignment(QtCore.Qt.AlignCenter)
        self.labl = QLabel(self)
        self.labl.move(211, 100)
        self.labl.setText('Label Example')
        self.setFocus()


        widget.setPlaceholderText("192.168.0.201")
        self.ip=str("192.168.0.201")

        widget.textEdited.connect(self.text_edited)
        self.setCentralWidget(widget)

        self.button1.clicked.connect(self.on_pushButton_clicked)

    def text_edited(self, s):
        print("Text edited...")
        self.ip=s
        print(s)


    def on_pushButton_clicked(self):
        self.soc = socket(AF_INET, SOCK_STREAM)
        #self.ip = '192.168.0.201'
        print(self.ip)
        self.button1.setEnabled(False)
        self.timer.singleShot(3000, lambda: self.button1.setDisabled(False))
        try:
            self.soc.connect((self.ip, 23))
            works=1
        except ValueError:
            works=0
        if works==1:
            self.f = open('datos_TCP.txt', 'a')
            self.i = 2
            self.graphWidget = pg.PlotWidget()
            self.setCentralWidget(self.graphWidget)
            self.graphWidget.setTitle("", color="r", size="30pt")

            self.x = list(range(5))  # 100 time points
            self.y = [0,0,0,0,0]  # 100 data points
            print(self.y)

            self.graphWidget.setBackground('w')

            pen = pg.mkPen(color=(255, 0, 0))
            self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
            # ... init continued ...

            self.timer.setInterval(50)
            self.timer.timeout.connect(self.update_plot_data)
            self.timer.start()


    def update_plot_data(self):
        self.f = open('datos_TCP.txt', 'a')
        self.soc.setblocking(0)
        ready=select.select([self.soc], [], [], 1)
        if ready[0]:
            s=self.soc.recv(8192) #####Convertir S al int correspodiente para mostrar en grafica
            s=str(s)
            s=s[2:-3]
            s2 = s.rstrip()
            time = datetime.datetime.now()
            time_str = time.strftime("%m/%d/%Y %H:%M:%S")
            out = str(s2) + ", " + str(time_str)
            self.i = self.i + 1
            if self.i > 3:
                self.graphWidget.setTitle(str(s2), color="r", size="30pt")
                try:
                    float(s)
                    it_is=1
                except ValueError:
                    it_is=0
                if it_is==1:
                    self.x = self.x[1:]  # Remove the first y element.
                    self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
                    self.y = self.y[1:]  # Remove the first
                    self.y.append(float(s))  # Add a new random value.
                    self.data_line.setData(self.x, self.y)  # Update the data.
                print(s)
                self.f.write(out + "\n")
            if self.i > 10:
                self.i = 5
            self.f.close()

######################


#########################################

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()