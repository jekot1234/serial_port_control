from followerUI import Ui_MainWindow
from modbus_follower import Follower
from PyQt5 import QtWidgets


class Follower_controller(Ui_MainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        
    def start_station(self):
        station_address = int(self.address.text())
        station_timeout = int(self.retries.text())
        station_com_port = self.com_port.text()
        station_baudrate = int(self.baudrate.text())

        self.follower = Follower(station_com_port, station_baudrate, station_address, station_timeout)
        self.update_buffer()
        print(f'Started Follower: {station_address}, {station_timeout}, {station_com_port}, {station_baudrate}')

    def listen_for_request(self):
        cc, response, command_hex, response_hex = self.follower.listen_for_request()

        command_hex = command_hex.hex(' ').upper()
        self.command_preview_2.setText(command_hex)
        if response_hex is not None:
            response_hex = response_hex.hex(' ').upper()
            self.respoonse_preview_2.setText(response_hex)
        else:
            self.respoonse_preview_2.setText('Transakcja rozgłoszeniowa')
        if cc != 2:
            self.incoming_text.setText(response.decode())
        else:
            self.incoming_text.setText('')            

    def update_buffer(self):
        if hasattr(self, 'follower'):
            self.follower.string_buffer = self.outcoming_text.toPlainText()    

    def connect_signals(self):
        self.run_station.clicked.connect(self.start_station)
        self.outcoming_text.textChanged.connect(self.update_buffer)
        self.listen.clicked.connect(self.listen_for_request)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Follower_controller()
    ui.setupUi(MainWindow)
    ui.connect_signals()
    MainWindow.show()
    sys.exit(app.exec_())
