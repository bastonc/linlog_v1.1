from PyQt5.QtWidgets import QMessageBox

class std:
    def get_std_band(self, freq):  # get Band in m
        #print(freq)
        band ="GEN"
        if int(freq)>1800000 and int(freq)<2000000:
            band = '160'
        if int(freq)>3500000 and int(freq)<3800000:
            band = '80'
        if int(freq)>7000000 and int(freq)<7200000:
            band = '40'
        if int(freq)>10100000 and int(freq)<10150000:
            band = '30'
        if int(freq)>14000000 and int(freq)<14500000:
            band = '20'
        if int(freq)>18068000 and int(freq)<18168000:
            band = '17'
        if int(freq)>21000000 and int(freq)<21450000:
            band = '15'
        if int(freq)>24890000 and int(freq)<24990000:
            band = '12'
        if int(freq)>28000000 and int(freq)<29700000:
            band = '10'
        if int(freq)>28000000 and int(freq)<29700000:
            band = '10'
        if int(freq)>50000000 and int(freq)<54000000:
            band = '6'
        if int(freq) > 144000000 and int(freq) < 144500000:
            band = '2'
        #print("get_std_band: band", band)
        return band

    def std_freq(self, freq):   # get format freq in Hz (Ex.14000000)
        freq = freq.replace('.', '')
        len_freq = len(freq)
        if len_freq < 8 and len_freq <= 5:
            while len_freq < 7:
                freq += "0"
                len_freq = len(freq)
            freq = "0" + freq
        if len(freq) < 8 and len(freq) > 5 and len(freq) != 7:
            while len_freq < 8:
                freq += "0"
                len_freq = len(freq)
        return freq

    def message(self, detail_text, text_short):
        message = QMessageBox(self)
        message.setGeometry(500, 300, 1000, 500)
        message.setWindowTitle("Information")
        message.setText(text_short)
        message.setInformativeText(detail_text)
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()