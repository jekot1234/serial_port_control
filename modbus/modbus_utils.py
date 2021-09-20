import numpy as np


START_BYTE = 0x3A # 0x3A -> : (ASCII)
CR = 0x0D # 0x0D -> Carriage return
LF = 0x0A # 0x0A -> Line feed (ASCII)

class Wrong_parameter_excpetion(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Data_frame_error_exception(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def int_to_ASCII(number):
    ascii = np.base_repr(number, base=16)
    if number < 16:
        ascii = '0' + ascii[0]
    return ascii.encode()
def ASCII_to_int(ascii):
    ascii = ascii.decode()
    return int(ascii, 16)

