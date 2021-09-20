import serial as pyserial
import struct
import numpy as np





class ASCII_Station():
    def __init__(self, port, baudrate) -> None:
        self.serial = pyserial.Serial(port, baudrate, timeout=0)

            







