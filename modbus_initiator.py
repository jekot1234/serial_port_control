import serial as pyserial
import struct
import traceback

from modbus_utils import *


class Initiator():
    def __init__(self, port, baudrate, transaction_timeout, retries, message_timeout) -> None:
        self.serial = pyserial.Serial(port, baudrate)
        if transaction_timeout in range(-1, 10000) and transaction_timeout%100 == 0:
            self.transaction_timeout = transaction_timeout
        else:
            raise Wrong_parameter_excpetion

        if retries in range(-1, 6):
            self.retries = retries
        else:
            raise Wrong_parameter_excpetion

        if message_timeout in range(-1, 1001) and message_timeout%10 == 0:
            self.message_timeout = message_timeout
        else:
            raise Wrong_parameter_excpetion

        self.serial.timeout = transaction_timeout/1000
        self.serial.write_timeout = transaction_timeout/1000
        self.serial.inter_byte_timeout = message_timeout/1000

    def addressed_transaction(self, address, command, arguments):
        pdu = struct.pack(f'<2s2s{len(arguments)}s', int_to_ASCII(address), int_to_ASCII(command), arguments)
        lrc = Initiator.calculate_LRC(pdu)
        serial_line_pdu = struct.pack(f'<B{len(pdu)}s2sBB', START_BYTE, pdu, int_to_ASCII(lrc), CR, LF)
        response = self.send_command(serial_line_pdu, False)
        return (serial_line_pdu, response)
            

    def broadcast_transaction(self, command, arguments):
        pdu = struct.pack(f'<2s2s{len(arguments)}s', int_to_ASCII(0), int_to_ASCII(command), arguments)
        lrc = Initiator.calculate_LRC(pdu)
        serial_line_pdu = struct.pack(f'<B{len(pdu)}s2sBB', START_BYTE, pdu, int_to_ASCII(lrc), CR, LF)
        self.send_command(serial_line_pdu, True)
        return serial_line_pdu

    def send_command(self, serial_line_pdu, broadcast):
        retries = 0
        while retries <= self.retries:
            try:
                self.serial.write(serial_line_pdu)
                if not broadcast:
                    response = self.recieve_response()
                    if response == None:
                        retries += 1
                    else:
                        return response
                else:
                    return None
            except pyserial.SerialTimeoutException:
                retries += 1
        return None

    def recieve_response(self):
        try:
            data = self.serial.read(1)
            if not self.check_start(data[0]):
                return #if recieved character is not start sign discard and retry
            try:
                frame = self.serial.read_until(expected=b'\r\n')
                print(f'recieved frame:\n {frame}')
            except:
                return #if recieving process timeouts discard and retry 
            try:
                arguments = self.check_frame(frame)
                if arguments != None:
                    return (frame, arguments)
            except Data_frame_error_exception:
                traceback.print_exc() 
        except:
            traceback.print_exc()
            return #timeout, retry

    def check_start(self, data):
        #check first byte if it is ':' sign
        if data == START_BYTE:
            return True
        else:
            return False

    def check_frame(self, frame):
        #check correction code
        if not self.check_data_corectness(frame):
            raise Data_frame_error_exception
        #unpack frame
        unpacked_frame = struct.unpack(f'<2s2s{len(frame) - 8}s2sBB', frame)
        return(unpacked_frame[2])

    def check_data_corectness(self, data):

        # In ASCII mode, messages include an error–checking field that is based on a Longitudinal Redundancy Checking (LRC) calculation
        # that is performed on the message contents, exclusive of the beginning ‘colon’ and terminating CRLF pair characters. It is applied
        # regardless of any parity checking method used for the individual characters of the message.

        expected_lrc = Initiator.calculate_LRC(data[:-4])
        lrc = ASCII_to_int(data[-4:-2])
        if expected_lrc == lrc:
            return True
        else:
            return False
    
    def calculate_LRC(message):
        lrc = 0
        for b in message:
            lrc ^= b
        return lrc

if __name__ == '__main__':
    initiator = Initiator('COM8', 9600, 1000, 5, 1000)
    print(initiator.addressed_transaction(15, 1, b'eeee').decode())