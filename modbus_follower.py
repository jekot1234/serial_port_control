import struct
from numpy import broadcast
import serial as pyserial
import traceback

from modbus_utils import *

class Follower(): 
    def __init__(self, port, baudrate, address, message_timeout) -> None:
        if address in range(0, 248) :
            self.address = address
        else:
            raise Wrong_parameter_excpetion
        if message_timeout in range(-1, 1001) and message_timeout%10 == 0:
            self.message_timeout = message_timeout
        else:
            raise Wrong_parameter_excpetion

        self.serial = pyserial.Serial(port, baudrate)

        self.serial.timeout = message_timeout
        self.serial.inter_byte_timeout = message_timeout

        self.string_buffer = ''

        self.decalared_functions = {
            1: self.read,
            2: self.write
        }

    def listen_for_request(self):
        try:
            data = self.serial.read(1)
            if not self.check_start(data[0]):
                return #if recieved character is not start sign discard and retry
            print('recieved message')
            try:
                frame = self.serial.read_until(expected=b'\r\n')
                print(frame)
            except:
                print('timeout')
                return #if recieving process timeouts discard and retry 
            try:
                unpacked_frame = self.check_frame(frame)
                if unpacked_frame != None:
                    print('frame good')
                    arguments = unpacked_frame[2]
                    #call execution function save in decalerd function dictionary
                    print('executing')
                    broadcast = False                    
                    if ASCII_to_int(unpacked_frame[0]) == 0:
                        broadcast = True

                    return self.decalared_functions[ASCII_to_int(unpacked_frame[1])](arguments, broadcast, frame)

            except Data_frame_error_exception:
                traceback.print_exc() 
                self.response_error_message() #if error in frame is found return error response
        except:
            traceback.print_exc()
            return #timeout, retry

 #### RECIEVING ####

    def check_start(self, data):
        #check first byte if it is ':' sign
        if data == START_BYTE:
            return True
        else:
            return False

    def check_frame(self, frame):
        print('frame checking')
        #check correction code
        if not self.check_data_corectness(frame):
            raise Data_frame_error_exception
        print('cc good')
        #unpack frame
        unpacked_frame = struct.unpack(f'<2s2s{len(frame) - 8}s2sBB', frame)
        
        #check function
        if ASCII_to_int(unpacked_frame[1]) not in self.decalared_functions.keys():
            raise Data_frame_error_exception
        
        print('function good')

        #check address
        if not ASCII_to_int(unpacked_frame[0]) == self.address and not ASCII_to_int(unpacked_frame[0]) == 0:
            return None
        
        print('address good')

        return unpacked_frame

    def check_data_corectness(self, data):

        # In ASCII mode, messages include an error–checking field that is based on a Longitudinal Redundancy Checking (LRC) calculation
        # that is performed on the message contents, exclusive of the beginning ‘colon’ and terminating CRLF pair characters. It is applied
        # regardless of any parity checking method used for the individual characters of the message.

        expected_lrc = Follower.calculate_LRC(data[:-4])
        lrc = ASCII_to_int(data[-4:-2])
        print(lrc)
        print(expected_lrc)
        if expected_lrc == lrc:
            return True
        else:
            return False

    def calculate_LRC(message):
        lrc = 0
        for b in message:
            lrc ^= b
        return lrc

 #### EXECUTION ####

    def read(self, args, broadcast, command_frame):
        if not broadcast:
            response_frame = self.function_response(b'Ok', 1)
        else:
            response_frame = None
        return (1, args, command_frame, response_frame)

    def write(self, args, broadcast, command_frame):
        if not broadcast:
            response_frame = self.function_response(self.string_buffer.encode(), 2)
        else:
            response_frame = None
        return (2, None, command_frame, response_frame)

 #### RESPONSING ####

    def response_error_message(self, funtion_code):
        pass

    def function_response(self, data, funtion_code):
        pdu = struct.pack(f'<2s2s{len(data)}s', int_to_ASCII(self.address), int_to_ASCII(funtion_code), data)
        lrc = Follower.calculate_LRC(pdu)
        serial_line_pdu = struct.pack(f'<B{len(pdu)}s2sBB', START_BYTE, pdu, int_to_ASCII(lrc), CR, LF)
        self.send_response(serial_line_pdu)
        return serial_line_pdu

    def send_response(self, data): 
        try:
            self.serial.write(data)
        except:
            return


if __name__ == '__main__':
    follower = Follower('COM11', 9600, 15, 500)
    print(follower.listen_for_request())