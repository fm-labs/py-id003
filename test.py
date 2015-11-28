#!/usr/bin/env python3

from id003 import BillVal
import serial.tools.list_ports
import serial
import time


def main():
    avail_ports = serial.tools.list_ports.comports()
    if not len(avail_ports):
        raise Exception("No serial port available")
    else:
        com_port = -1
        while -1 < com_port < len(avail_ports):
            for i, p in enumerate(avail_ports):
                print(i + ') ' + p)
            com_port = int(input("Which com port? "))
        port = avail_ports[com_port]
        
    baud = None
    while baud not in (9600, 19200):
        baud = int(input("Baud rate? (Only 9600 and 19200 supported) "))
    
    timeout = 1.0
    
    bv = BillVal(port, baud, serial.EIGHTBITS, serial.PARITY_EVEN, timeout)
    bv.power_on()
    
    if bv.init_status == id003.POW_UP:
        print("BV powered up normally, version:\n\t" + bv.bv_version)
    elif bv.init_status == id003.POW_UP_BIA:
        print("BV powered up with bill in acceptor.")
    elif bv.init_status == id003.POW_UP_BIS:
        print("BV powered up with bill in stacker.")
        
    while True:
        status, data = bv.req_status()
        
        print(hex(status) + ' ' + data)
        
        time.sleep(0.2)


if __name__ == '__main__':
    main()