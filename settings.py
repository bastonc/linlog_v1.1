import telnetlib
import time
import main
import parse
import shutil
import std
from PyQt5.QtWidgets import QApplication, QAction, QWidget, QMainWindow, QTableView, QTableWidget, QTableWidgetItem, \
    QTextEdit, \
    QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QFrame, QSizePolicy
from PyQt5 import QtCore
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QMessageBox, QLineEdit, QPushButton, QLabel, QColorDialog, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QFileDialog
from PyQt5.QtGui import QIcon, QFocusEvent, QPixmap, QTextTableCell, QStandardItemModel, QPalette, QColor
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtCore import QThread
from time import gmtime, strftime, localtime

class Menu (QWidget):
    def __init__(self, settingsDict, telnetCluster, logForm, logSearch,
                 logWindow, internetSearch, tci_class, parent=None):
        super(Menu, self).__init__(parent)
        self.settingsDict = settingsDict
        self.label_style = "font: 12px;"
        self.initUI()
        self.initData()
        self.telnetCluster = telnetCluster
        self.logForm = logForm
        self.logSearch = logSearch
        self.logWindow = logWindow
        self.internetSearch = internetSearch
        self.tci_class = tci_class
        #print ("Menu init tci class:", self.tci_class.currentThreadId())
        #self.initUI()

    def initUI(self):

        self.setGeometry(300,
                         300,
                         300,
                         300)
        self.setWindowTitle('LinLog | Settings')

        self.setWindowIcon(QIcon('logo.png'))
        style = "QWidget{background-color:" + self.settingsDict['background-color'] + "; color:" + self.settingsDict['color'] + ";}"
        self.setStyleSheet(style)
    # declaration tab
        self.tab = QtWidgets.QTabWidget()
        self.general_tab = QWidget()
        self.cluster_tab = QWidget()
        self.tci_tab = QWidget()
        self.io_tab = QWidget()
    #
        self.tab.addTab(self.general_tab, "General")
        self.tab.addTab(self.cluster_tab, "Cluster")
        self.tab.addTab(self.tci_tab, "TCI")
        self.tab.addTab(self.io_tab, "Log file")
    # create General Tab
        formstyle = "background :"+self.settingsDict['form-background']
        self.general_tab.layout = QVBoxLayout(self) # create vertical lay
        self.call_label = QLabel("You Callsign")
        self.call_input = QLineEdit()
        self.call_input.setFixedWidth(100)
        self.call_input.setStyleSheet(formstyle)

        self.dlg = QColorDialog(self)
        self.back_color_label = QLabel("Window color (Ex. #323232):")
        self.back_color_label.setStyleSheet(self.label_style)
        self.back_color_input = QPushButton()
        self.back_color_input.clicked.connect(self.back_color_select)
        self.back_color_input.setFixedWidth(70)
        self.back_color_input.setStyleSheet("background:" + self.settingsDict['background-color'] + ";")

        #self.back_color_input.setStyleSheet(formstyle)
        self.text_color_label = QLabel("Text color (Ex. #aaaaaa):")
        self.text_color_label.setStyleSheet(self.label_style)
        self.text_color_input = QPushButton()
        self.text_color_input.clicked.connect(self.text_color_select)
        self.text_color_input.setFixedWidth(70)
        self.text_color_input.setStyleSheet("background:" + self.settingsDict['color'] + ";")

        #self.text_color_input.setStyleSheet(formstyle)
        self.form_color_label = QLabel("Form color (Ex. #212121):")
        self.form_color_label.setStyleSheet(self.label_style)
        self.form_color_input = QPushButton()
        self.form_color_input.clicked.connect(self.form_color_select)
        self.form_color_input.setFixedWidth(70)
        self.form_color_input.setStyleSheet("background:" + self.settingsDict['form-background'] + ";")

        # setup all elements to vertical lay
        self.general_tab.layout.addWidget(self.call_label)
        self.general_tab.layout.addWidget(self.call_input)
        self.general_tab.layout.addSpacing(20)

        self.general_tab.layout.addWidget(self.back_color_label)
        self.general_tab.layout.addWidget(self.back_color_input)
        self.general_tab.layout.addSpacing(20)
        self.general_tab.layout.addWidget(self.text_color_label)
        self.general_tab.layout.addWidget(self.text_color_input)
        self.general_tab.layout.addSpacing(20)
        self.general_tab.layout.addWidget(self.form_color_label)
        self.general_tab.layout.addWidget(self.form_color_input)
        self.general_tab.setLayout(self.general_tab.layout)

    # create Cluster tab

        self.cluster_tab.layout = QVBoxLayout(self)
        self.cluster_host = QLabel("Cluster host:")
        self.cluster_host_input = QLineEdit()
        self.cluster_host_input.setFixedWidth(150)
        self.cluster_host_input.setStyleSheet(formstyle)
        self.cluster_port = QLabel("Cluster port:")
        self.cluster_port_input = QLineEdit()
        self.cluster_port_input.setFixedWidth(50)
        self.cluster_port_input.setStyleSheet(formstyle)
        self.host_port_lay = QHBoxLayout()
        # create host:port lay
        self.host_lay = QVBoxLayout()
        self.host_lay.addWidget(self.cluster_host)
        self.host_lay.addWidget(self.cluster_host_input)

        self.port_lay = QVBoxLayout()
        self.port_lay.addWidget(self.cluster_port)
        self.port_lay.addWidget(self.cluster_port_input)

        self.host_port_lay.addLayout(self.host_lay)
        self.host_port_lay.addLayout(self.port_lay)


        # Create calibrate cluster
        self.calibrate_lay = QHBoxLayout()
        ## Create text label
        self.text_and_button_Vlay = QVBoxLayout()
        text = "Press \"Start claibrate\" and select Callsign and Freq \n" \
               "from the received line from the telnet cluster"
        self.message_label = QLabel(text)
        self.message_label.setStyleSheet("font: 12px;")
        self. text_and_button_Vlay.addWidget(self.message_label)

        self.button_and_combo = QHBoxLayout()
        ## Create group from button and combobox
        self.cluster_start_calibrate_button = QPushButton("Start \n callibrate")
        self.cluster_start_calibrate_button.setFixedWidth(100)
        self.cluster_start_calibrate_button.setFixedHeight(60)
        self.button_and_combo.addWidget(self.cluster_start_calibrate_button)
        self.combo_lay = QVBoxLayout()
        self.call_H = QHBoxLayout()
        self.call_H.setAlignment(Qt.AlignRight)
        self.cluster_call_label = QLabel("Call:")

        self.cluster_combo_call = QComboBox()

        self.freq_H = QHBoxLayout()
        self.freq_H.setAlignment(Qt.AlignRight)
        self.cluster_freq_label = QLabel("Freq:")
        self.cluster_combo_freq = QComboBox()
        self.call_H.addWidget(self.cluster_call_label)
        self.call_H.addWidget(self.cluster_combo_call)
        self.freq_H.addWidget(self.cluster_freq_label)
        self.freq_H.addWidget(self.cluster_combo_freq)
        self.combo_lay.addLayout(self.call_H)
        self.combo_lay.addLayout(self.freq_H)
        self.button_and_combo.addLayout(self.combo_lay)
        self.text_and_button_Vlay.addLayout(self.button_and_combo)

        self.calibrate_lay.addLayout(self.text_and_button_Vlay)




        ## Create filter band
        self.cluster_filter_band_combo = QCheckBox("Filter BAND")
        self.cluster_filter_band_combo.setStyleSheet("QCheckBox{ color:" + self.settingsDict['color'] + "; font-size: 12px;}")
        self.cluster_filter_band_input = QLineEdit()
        self.cluster_filter_band_input.setFixedWidth(80)
        self.cluster_filter_band_input.setFixedHeight(20)
        self.cluster_filter_band_input.setStyleSheet("background-color:"+self.settingsDict['form-background']+"; font-size: 12px")
        text = "Bands in m."
        self.message_label_band = QLabel(text)
        self.message_label_band.setStyleSheet("font: 12px;")

        self.filter_band_lay = QVBoxLayout()
        self.filter_band_lay.addWidget(self.cluster_filter_band_combo)
        self.filter_band_lay.addWidget(self.message_label_band)
        self.filter_band_lay.addWidget(self.cluster_filter_band_input)



        ## Create filter spot
        self.cluster_filter_spot_combo = QCheckBox("Filter SPOT")
        self.cluster_filter_spot_combo.setStyleSheet(
            "QCheckBox{ color:" + self.settingsDict['color'] + "; font-size: 12px;}")
        self.cluster_filter_spot_input = QLineEdit()
        self.cluster_filter_spot_input.setFixedWidth(80)
        self.cluster_filter_spot_input.setFixedHeight(20)
        self.cluster_filter_spot_input.setStyleSheet(
            "background-color:" + self.settingsDict['form-background'] + "; font-size: 12px")
        text = "Spot prefixes"
        self.message_label_spot = QLabel(text)
        self.message_label_spot.setStyleSheet("font: 12px;")

        self.filter_spot_lay = QVBoxLayout()
        self.filter_spot_lay.addWidget(self.cluster_filter_spot_combo)
        self.filter_spot_lay.addWidget(self.message_label_spot)
        self.filter_spot_lay.addWidget(self.cluster_filter_spot_input)

        ## create filter spotter
        self.cluster_filter_spotter_combo = QCheckBox("Filter SPOTTER")
        self.cluster_filter_spotter_combo.setStyleSheet(
            "QCheckBox{ color:" + self.settingsDict['color'] + "; font-size: 12px;}")
        self.cluster_filter_spotter_input = QLineEdit()
        self.cluster_filter_spotter_input.setFixedWidth(80)
        self.cluster_filter_spotter_input.setFixedHeight(20)
        self.cluster_filter_spotter_input.setStyleSheet(
            "background-color:" + self.settingsDict['form-background'] + "; font-size: 12px")
        text = "Spotter prefixes"
        self.message_label_spotter = QLabel(text)
        self.message_label_spotter.setStyleSheet("font: 12px;")

        self.filter_spotter_lay = QVBoxLayout()
        self.filter_spotter_lay.addWidget(self.cluster_filter_spotter_combo)
        self.filter_spotter_lay.addWidget(self.message_label_spotter)
        self.filter_spotter_lay.addWidget(self.cluster_filter_spotter_input)

        text = "All value separate by comma"
        self.filter_message_label = QLabel(text)
        self.filter_message_label.setStyleSheet("font: 12px;")

        self.filters_Hlay = QHBoxLayout()
        self.filters_Hlay.addLayout(self.filter_band_lay)
        self.filters_Hlay.addLayout(self.filter_spot_lay)
        self.filters_Hlay.addLayout(self.filter_spotter_lay)

        self.filters_lay = QVBoxLayout()
        self.filters_lay.addSpacing(10)
        self.filters_lay.setAlignment(Qt.AlignCenter)
        self.filters_lay.addLayout(self.filters_Hlay)
        self.filters_lay.addWidget(self.filter_message_label)
        self.filters_lay.addSpacing(10)
        Separador = QFrame()
        Separador.setFrameShape(QFrame.HLine)
        Separador.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        Separador.setLineWidth(1)
        self.filters_lay.addWidget(Separador)


        ## Create List view for input string from cluster

        self.line_text = QLabel()

        self.line_text.setFixedHeight(50)
        # Set all layers to window
        self.cluster_tab.layout.addLayout(self.host_port_lay)
        self.cluster_tab.layout.addSpacing(10)
        self.cluster_tab.layout.addLayout(self.filters_lay)
        self.cluster_tab.layout.addLayout(self.calibrate_lay)
        self.cluster_tab.layout.addWidget(self.line_text)

        ## install lay to main tab (Cluster)
        self.cluster_tab.setLayout(self.cluster_tab.layout)


    # create TCI Tab

        self.tci_enable_combo_lay = QHBoxLayout()
        self.tci_enable_combo_lay.setAlignment(Qt.AlignCenter)
        self.tci_enable_combo = QCheckBox("TCI Enable")
        self.tci_enable_combo.setStyleSheet("QCheckBox{"+self.settingsDict['color']+"}")
        self.tci_enable_combo_lay.addWidget(self.tci_enable_combo)
        self.tci_tab.layout = QVBoxLayout(self)
        self.tci_host = QLabel("TCI host:")
        self.tci_host_input = QLineEdit()
        self.tci_host_input.setFixedWidth(150)
        self.tci_host_input.setStyleSheet(formstyle)
        self.tci_port = QLabel("TCI port:")
        self.tci_port_input = QLineEdit()
        self.tci_port_input.setFixedWidth(50)
        self.tci_port_input.setStyleSheet(formstyle)
        self.host_port_lay = QHBoxLayout()
        # create host:port lay
        self.host_lay = QVBoxLayout()
        self.host_lay.addWidget(self.tci_host)
        self.host_lay.addWidget(self.tci_host_input)

        self.port_lay = QVBoxLayout()
        self.port_lay.addWidget(self.tci_port)
        self.port_lay.addWidget(self.tci_port_input)

        self.host_port_lay.addLayout(self.host_lay)
        self.host_port_lay.addLayout(self.port_lay)


        self.tci_tab.layout.addLayout(self.tci_enable_combo_lay)
        self.tci_tab.layout.addLayout(self.host_port_lay)
        self.tci_tab.layout.addSpacing(250)
        self.tci_tab.setLayout(self.tci_tab.layout)

    # Create io_tab
        self.io_tab_lay = QVBoxLayout()
        self.io_tab_lay.setAlignment(Qt.AlignCenter)
        self.import_button = QPushButton("Import")
        self.import_button.setFixedSize(100, 30)
        self.import_button.clicked.connect(self.import_adi)
        self.import_button.setStyleSheet("width: 100px;")
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_adi)
        self.export_button.setFixedSize(100, 30)
        self.io_tab_lay.addWidget(self.import_button)
        self.io_tab_lay.addWidget(self.export_button)
        self.io_tab.setLayout(self.io_tab_lay)


    # button panel
        self.button_panel = QHBoxLayout()
        button_style = "font: 12px;"
        self.button_save = QPushButton("Save and Exit")
        self.button_save.setStyleSheet(button_style)
        self.button_save.clicked.connect(self.save_and_exit_button)
        self.button_apply = QPushButton("Apply")
        self.button_apply.setStyleSheet(button_style)
        self.button_apply.clicked.connect(self.apply_button)
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setStyleSheet(button_style)
        self.button_cancel.clicked.connect(self.cancel_button)
        self.button_cancel.setFixedWidth(60)
        self.button_panel.addWidget(self.button_cancel)
        self.button_panel.addWidget(self.button_apply)
        self.button_panel.addWidget(self.button_save)


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tab)
        self.mainLayout.addLayout(self.button_panel)
        #self.mainLayout.addWidget(self.tab)
        self.setLayout(self.mainLayout)


        

        #self.setLayout(self.mainLayout)
        #self.show()
        print("Menu() initUi")

    def initData (self):
        #init data in general tab
        self.call_input.setText(self.settingsDict["my-call"])
        self.text_color_input.setText(self.settingsDict['color'])
        self.form_color_input.setText(self.settingsDict['form-background'])
        self.back_color_input.setText(self.settingsDict['background-color'])
        #init data in cluster tab
        self.cluster_host_input.setText(self.settingsDict['telnet-host'])
        self.cluster_port_input.setText(self.settingsDict['telnet-port'])
        if self.settingsDict['filter_by_band'] == 'enable':
            self.cluster_filter_band_combo.setChecked(True)
        self.cluster_filter_band_input.setText(self.settingsDict['list-by-band'])
        if self.settingsDict['filter-by-prefix'] == 'enable':
            self.cluster_filter_spot_combo.setChecked(True)
        self.cluster_filter_spot_input.setText(self.settingsDict['filter-prefix'])
        if self.settingsDict['filter-by-prefix-spotter'] == 'enable':
            self.cluster_filter_spotter_combo.setChecked(True)
        self.cluster_filter_spotter_input.setText(self.settingsDict['filter-prefix-spotter'])
        self.cluster_start_calibrate_button.clicked.connect(self.start_calibrate_cluster)
        #init data in tci tab
        if self.settingsDict['tci'] == 'enable':
            self.tci_enable_combo.setChecked(True)
        host = self.settingsDict['tci-server'].replace("ws://", '')
        self.tci_host_input.setText(host)
        self.tci_port_input.setText(self.settingsDict['tci-port'])

    def closeEvent(self, e):
        print("Close menu", e)
        Menu.close(self)

    def import_adi(self):
        fileimport = QFileDialog()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #fileimport.setNameFilter("Adi file(*.adi)")
        #fileimport.setFilter()
        fname = fileimport.getOpenFileName(self, 'Import adi file', '/home', "*.adi", options=options)[0]
        if fname:
            print(fname)
            self.allCollumn = ['records_number', 'QSO_DATE', 'TIME_ON', 'BAND', 'CALL', 'FREQ', 'MODE', 'RST_RCVD', 'RST_SENT',
                               'NAME', 'QTH', 'COMMENTS', 'TIME_OFF', 'eQSL_QSL_RCVD', 'OPERATOR']
            try:
                allRecords = parse.getAllRecord(self.allCollumn, fname)
                main.Adi_file.record_dict_qso(self, allRecords)
                print(allRecords)
                self.logWindow.refresh_data()
                std.std.message(self, "Import complete!", "Ok")
            except Exception:
                print ("Exception to import")
                std.std.message(self, "Can't import\nCheck encoding file", "STOP!")




    def export_adi(self):
        print("export_adi")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Export adi", "",
                                                  "Adi (*.adi)", options=options)
        if file_name:
            print(file_name)
            copy_file = shutil.copyfile('log.adi', file_name+'.adi')

            if copy_file!='':
                print("Export complete")
                std.std.message(self, "Export to\n"+copy_file+"\n completed", "Export complited")
            else:
                std.std.message(self, "Can't export to file", "Sorry")
    def start_calibrate_cluster(self):
        self.telnetCluster.stop_cluster()
        self.cluster = cluster_in_Thread (self.cluster_host_input.text().strip(),
                                     self.cluster_port_input.text().strip(),
                                     self.call_input.text().strip(), self)
        self.cluster.start()

        print("self.start_calibrate_cluster: Hello")

    def refresh_interface(self):

        self.update_color_schemes()

    def text_color_select(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.text_color_input.setText(color.name())
            self.text_color_input.setStyleSheet("background:" + color.name() + ";")
            self.text_color_input.autoFillBackground()

    def form_color_select(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.form_color_input.setText(color.name())
            self.form_color_input.setStyleSheet("background:" + color.name() + ";")
            self.form_color_input.autoFillBackground()

    #self.back_color_input.clicked.connect(self.text_color_select)

    def back_color_select(self):
        #self.dlg.show()
        color = QColorDialog.getColor()

        if color.isValid():
            self.back_color_input.setText(color.name())
            self.back_color_input.setStyleSheet("background:"+color.name()+";")
            self.back_color_input.autoFillBackground()



    def update_color_schemes(self):
        style = "QWidget{background-color:" + self.settingsDict['background-color'] + "; color:" + \
                self.settingsDict['color'] + ";}"



        self.setStyleSheet(style)

    def store_new_settingsDict(self):
        call = main.settingsDict['my-call']
        self.settingsDict['my-call'] = self.call_input.text()
        self.settingsDict['background-color'] = self.back_color_input.text()
        self.settingsDict['color'] = self.text_color_input.text()
        self.settingsDict['form-background'] = self.form_color_input.text()
        self.settingsDict['telnet-host'] = self.cluster_host_input.text()
        self.settingsDict['telnet-port'] = self.cluster_port_input.text()
        self.settingsDict['list-by-band'] = self.cluster_filter_band_input.text()
        self.settingsDict['filter-prefix'] = self.cluster_filter_spot_input.text()
        self.settingsDict['filter-prefix-spotter'] = self.cluster_filter_spotter_input.text()
        if self.cluster_combo_call.currentText() != '':
            self.settingsDict['telnet-call-position'] = self.cluster_combo_call.currentText().split(":")[0]
        if self.cluster_combo_freq.currentText() != '':
            self.settingsDict['telnet-freq-position'] = self.cluster_combo_freq.currentText().split(":")[0]
        self.settingsDict['tci-server'] = "ws://"+self.tci_host_input.text().strip()
        self.settingsDict['tci-port'] = self.tci_port_input.text().strip()

        cluster_change_flag = 0
        if self.cluster_filter_band_combo.isChecked():
            if main.settingsDict['filter_by_band'] != "enable":
                main.settingsDict['filter_by_band'] = "enable"
                cluster_change_flag = 1
        else:
            if main.settingsDict['filter_by_band'] != "disable":
                main.settingsDict['filter_by_band'] = "disable"
                cluster_change_flag = 1

        if self.cluster_filter_spot_combo.isChecked():
            if main.settingsDict['filter-by-prefix'] != "enable":
                main.settingsDict['filter-by-prefix'] = "enable"
                cluster_change_flag = 1
        else:
            if main.settingsDict['filter-by-prefix'] != "disable":
                main.settingsDict['filter-by-prefix'] = "disable"
                cluster_change_flag = 1

        if self.cluster_filter_spotter_combo.isChecked():
            if main.settingsDict['filter-by-prefix-spotter'] != "enable":
                main.settingsDict['filter-by-prefix-spotter'] = "enable"
                cluster_change_flag = 1
        else:
            if main.settingsDict['filter-by-prefix-spotter'] != "disable":
                main.settingsDict['filter-by-prefix-spotter'] = "disable"
                cluster_change_flag = 1


        return cluster_change_flag

    def apply_button(self):

        cluster_change_flag = self.store_new_settingsDict()   # save all lines from menu window \
                                                                # to dictionary settingsDict

        self.tci_class.stop_tci()
        self.tci_class.start_tci(self.settingsDict['tci-server'], self.settingsDict['tci-port'])
        #self.logForm.update_settings(self.settingsDict)
        self.logForm.refresh_interface()
        #self.logSearch.update_settings(self.settingsDict)
        self.logSearch.refresh_interface()
        #self.logWindow.update_settings(self.settingsDict)
        self.logWindow.refresh_interface()
        #self.internetSearch.update_settings(self.settingsDict)
        self.internetSearch.refresh_interface()
        #self.telnetCluster.update_settings(self.settingsDict)
        self.telnetCluster.refresh_interface()
        self.refresh_interface()
        if cluster_change_flag == 1:
            self.telnetCluster.stop_cluster()
            self.telnetCluster.start_cluster()

    def save_and_exit_button(self):

        cluster_change_flag = self.store_new_settingsDict()

        filename = 'settings.cfg'
        with open(filename, 'r') as f:
            old_data = f.readlines()
        for index, line in enumerate(old_data):
            key_from_line = line.split('=')[0]
            #print ("key_from_line:",key_from_line)
            for key in self.settingsDict:

                if key_from_line == key:
                    #print("key",key , "line", line)
                    old_data[index] = key+"="+self.settingsDict[key]+"\n"
        with open(filename, 'w') as f:
            f.writelines(old_data)
        print ("Save_and_Exit_button: ", old_data)
        Menu.close(self)

    def cancel_button(self):
        Menu.close(self)

class cluster_in_Thread(QThread):
    def __init__(self, host, port, call, parent_window, parent=None):
        super().__init__()
        self.host = host
        self.port = port
        self.call =call
        self.parent_window = parent_window
        # self.run()

    def run(self):

        while 1:
            try:
                telnetObj = telnetlib.Telnet(self.host, self.port)
                break
            except:
                time.sleep(3)
                continue

        lastRow = 0
        message = (self.call + "\n").encode('ascii')
        telnetObj.write(message)
        message2 = (self.call + "\n").encode('ascii')
        telnetObj.write(message2)
        splitString = []
        cleanList = []
        output_data = ""
        i = 0
        print('Starting Telnet cluster:', self.host, ':', self.port, '\nCall:', self.call, '\n\n')
        while 1:
            try:
                output_data = telnetObj.read_some()
            except:
                continue

            if output_data != '':

                    if output_data[0:2].decode(main.settingsDict['encodeStandart']) == "DX":
                        splitString = output_data.decode(main.settingsDict['encodeStandart']).split(' ')
                        count_chars = len(splitString)
                        for i in range(count_chars):
                            if splitString[i] != '':
                                cleanList.append(splitString[i])
                        break
            time.sleep(0.3)
        ##########

        i = 0
        for value in cleanList:
            self.parent_window.cluster_combo_call.addItems([str(i) + ":" + value])
            self.parent_window.cluster_combo_freq.addItems([str(i) + ":" + value])
            i += 1

        self.parent_window.cluster_combo_call.setCurrentIndex(int(main.settingsDict['telnet-call-position']))
        self.parent_window.cluster_combo_freq.setCurrentIndex(int(main.settingsDict['telnet-freq-position']))
        self.parent_window.line_text.setText(' '.join(cleanList))
        self.parent_window.telnetCluster.start_cluster()

        self.currentThread().terminate()






