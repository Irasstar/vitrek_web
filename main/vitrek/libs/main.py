# pyuic5 gui.ui -o design.py

import sys
import os
from PyQt5 import QtWidgets, QtCore
import design
from Vitrek4700driver import Vitrek4700, UDPRSConnector
from pandas import DataFrame


class GuiApp(QtWidgets.QMainWindow, design.Ui_Form):
    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.voltage_check_timer = QtCore.QTimer()
        self.setupUi(self)
        self.data = []

        self.progressBar_2.setValue(0)  # init progressbar start value

        self.vitrek = Vitrek4700(connector=UDPRSConnector('172.16.3.204', 5070))

        # connections

        self.pushButton_10.clicked.connect(self.push_button_10_clicked)  # init Vitrek. Connect to vitrek
        self.pushButton_9.clicked.connect(self.push_button_9_clicked)  # init Vitrek. Connect to vitrek

        self.pushButton_6.clicked.connect(self.push_button_6_clicked)  # DC Zero
        self.pushButton_8.clicked.connect(self.push_button_8_clicked)  # Get ID

        self.pushButton.clicked.connect(self.push_button_clicked)  # start measure. start timer
        self.pushButton_2.clicked.connect(self.push_button_2_clicked)  # stop timer

        self.timer.timeout.connect(self.timer_on_timer)  # start measures and run progressbar
        self.voltage_check_timer.timeout.connect(self.voltage_check_timer_on_timer)  # cycle voltage check

        self.pushButton_11.clicked.connect(self.show_file_open_dialog)  # show dir choose dialog
        self.pushButton_3.clicked.connect(self.push_button_3_clicked)  # save file button
        self.pushButton_5.clicked.connect(self.push_button_5_clicked)  # clear text box
        self.pushButton_4.clicked.connect(self.push_button_4_clicked)  # open file with notepad

# Events
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Window Close',
                                               'Are you sure you want to close the window?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.vitrek.connector.disconnect()
            self.timer.stop()
            self.voltage_check_timer.stop()
            event.accept()
        else:
            event.ignore()

# buttons action
    def push_button_10_clicked(self):  # init Vitrek. Connect to vitrek
        if not self.vitrek.connector.is_connected:
            self.vitrek.connector.connect()
            self.voltage_check_timer.start(603)

    def push_button_9_clicked(self):  # init Vitrek. Connect to vitrek
        if self.vitrek.connector.is_connected:
            self.vitrek.connector.disconnect()
            self.voltage_check_timer.stop()

    def push_button_6_clicked(self):  # DC Zero
        if self.vitrek.connector.is_connected:
            self.vitrek.dc_zero()

    def push_button_8_clicked(self):  # Get ID
        if self.vitrek.connector.is_connected:
            self.textBrowser.append(self.vitrek.get_idn())
            self.textBrowser.append(self.vitrek.get_hi_probe_id())
            self.textBrowser.append(self.vitrek.get_lo_probe_id())

    def push_button_clicked(self):  # start measure. start timer
        if self.vitrek.connector.is_connected:
            self.textBrowser.clear()
            self.data.clear()
            self.progressBar_2.setValue(0)
            self.progressBar_2.setMaximum(int(self.lineEdit_5.text()))
            self.timer.start((int(float(self.lineEdit_4.text()) * 1000)))  # time delay seconds to m.seconds

    def push_button_2_clicked(self):  # stop timer
        self.timer.stop()

    def timer_on_timer(self):  # timer for measures and progress bar
        raw_data = self.vitrek.get_measures()
        self.textBrowser.append(f"U= {raw_data['DCV']} V; "
                                f"U~ {raw_data['ACV']} V; "
                                f"f {raw_data['FR']} Hz; "
                                f"Upp {raw_data['Pk-Pk']} V;")
        self.data.append(raw_data)

        self.progressBar_2.setValue(self.progressBar_2.value() + 1)

        if self.progressBar_2.value() == self.progressBar_2.maximum():
            self.timer.stop()

    def voltage_check_timer_on_timer(self):
        if self.checkBox_6.isChecked() and self.vitrek.connector.is_connected:
            self.label_6.setText(f'{self.vitrek.get_dcv()} V')
            self.label_7.setText(f'{self.vitrek.get_acv()} V')
            self.label_8.setText(f'{self.vitrek.get_freq()} Hz')
            self.label_9.setText(f'{self.vitrek.get_peak_peak()} V')
            self.label_10.setText(f'{self.vitrek.get_cr_factor()}')

    def show_file_open_dialog(self):
        self.lineEdit_3.setText(QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose directory', 'C:\\'))

    def push_button_3_clicked(self):
        fields_name = ['DCV', 'ACV', 'FR', 'Pk-Pk', 'CR.f']
        if self.lineEdit_3.text() != '' and self.lineEdit_3.text() != '':
            path = os.path.join(self.lineEdit_3.text(), self.lineEdit_8.text())
            path = self.check_csv_ext(path)
            with open(path, 'a') as csv_file:
                csv_file.write(self.lineEdit_6.text() + "\r\n")
                df = DataFrame(self.data)
                csv_file.write(df.to_string())
                csv_file.write("\r\n")
                # df.to_csv(path)

    def push_button_5_clicked(self):
        self.textBrowser.clear()

    def push_button_4_clicked(self):
        if self.lineEdit_3.text() != '' and self.lineEdit_3.text() != '':
            path = os.path.join(self.lineEdit_3.text(), self.lineEdit_8.text())
            path = self.check_csv_ext(path)
            os.system("notepad.exe " + path)

    @staticmethod
    def check_csv_ext(path):
            _, tail = os.path.split(path)
            if tail != '.csv':
                return path + '.csv'
            else:
                return path



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GuiApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

