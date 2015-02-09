#!/usr/bin/env python
#-*- coding: utf-8 -*-

import usb
import sys
import logging
import debugger


########################################################################
class baseUploader(object):

    # Hex format record types
    # --------------------------------------------------------------------------
    # Data_Record = 00
    # End_Of_File_Record = 01
    # Extended_Segment_Address_Record = 02
    # Start_Segment_Address_Record = 03
    # Extended_Linear_Address_Record = 04
    # Start_Linear_Address_Record = 05

    # Python3 compatibility (octals)
    Data_Record = 0o0
    End_Of_File_Record = 0o1
    Extended_Segment_Address_Record = 0o2
    Start_Segment_Address_Record = 0o3
    Extended_Linear_Address_Record = 0o4
    Start_Linear_Address_Record = 0o5


    # Error codes returned by various functions
    # --------------------------------------------------------------------------
    ERR_NONE = 0
    ERR_CMD_ARG = 1
    ERR_CMD_UNKNOWN = 2
    ERR_DEVICE_NOT_FOUND = 3
    ERR_USB_INIT1 = 4
    ERR_USB_INIT2 = 5
    ERR_USB_OPEN = 6
    ERR_USB_WRITE = 7
    ERR_USB_READ = 8
    ERR_HEX_OPEN = 9
    ERR_HEX_STAT = 10
    ERR_HEX_MMAP = 11
    ERR_HEX_SYNTAX = 12
    ERR_HEX_CHECKSUM = 13
    ERR_HEX_RECORD = 14
    ERR_VERIFY = 15
    ERR_EOL = 16
    ERR_USB_ERASE = 17

# ------------------------------------------------------------------------------
    def __init__(self, hex_file, board):
        self.hex_file = hex_file
        self.filename = hex_file
        self.board = board
        self.report = []


# ------------------------------------------------------------------------------
    def add_report(self, message):
        """ display message in the log window """
        self.report.append(message)

        import sys
        reload(sys)
        sys.stdout.write("DEBUG : " + message + "\r\n")

# ------------------------------------------------------------------------------
    def getDevice(self):
        """ get list of USB devices and search for pinguino """
        busses = usb.busses()
        for bus in busses:
            for device in bus.devices:
                if device.idVendor == self.board.vendor and device.idProduct == self.board.product:
                    return device
        return self.ERR_DEVICE_NOT_FOUND

# ------------------------------------------------------------------------------
    def closeDevice(self):
        """ Close currently-open USB device """
        try:
            self.handle.releaseInterface()
        except:
            pass

########################################################################
class Uploader(object):
    """Universal uploader class"""

    #----------------------------------------------------------------------
    def __init__(self, hex_file, board):

        debugger.Debugger(sys)

        if board.bldr == "noboot":

            # TODO : interface here something like PICpgm (http://www.members.aon.at/electronics/pic/picpgm/)
            #self.logwindow("You choose a board without bootloader.\nYou should either change your board type\nor use a programmer to upload your application on your board", 1)
            raise Exception("You choose a board without bootloader.\nYou should either change your board type\nor use a programmer to upload your application on your board")

        elif board.bldr == "boot2":
            from uploaderVSC import uploaderVSC as Uploader

        #elif board.bldr == 'boot3':
        #    self.uploader = self.uploaderDLN(*parameters)

        elif board.bldr == "boot4":
            from uploader8 import uploader8 as Uploader

        elif board.bldr == "microchip":
            from uploader32 import uploader32 as Uploader

        self.uploader = Uploader(hex_file, board)


    #----------------------------------------------------------------------
    def write_hex(self):

        self.uploader.writeHex()
        return self.uploader.report

