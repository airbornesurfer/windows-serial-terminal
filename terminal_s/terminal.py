"""
Terminal for serial port

Requirement:

    + pyserial
    + colorama
    + py-getch
    + click
"""

import os
if os.name == 'nt':
    os.system('title Serial Console')

from collections import deque
import sys
import threading

import colorama
import click
import serial
from serial.tools import list_ports


def run(port, baudrate = 115200, parity='N', stopbits=1):
    try:
        device = serial.Serial(port=port,
                                baudrate=baudrate,
                                bytesize=8,
                                parity=parity,
                                stopbits=stopbits,
                                timeout=0.1)
    except:
        print('--- Failed to open {} ---'.format(port))
        return 0

    print('--- {} is connected. Press Ctrl+] to quit ---'.format(port))
    queue = deque()
    def read_input():
        if os.name == 'nt':
            from msvcrt import getch
        else:
            import tty
            import termios
            stdin_fd = sys.stdin.fileno()
            tty_attr = termios.tcgetattr(stdin_fd)
            tty.setraw(stdin_fd)
            getch = lambda: sys.stdin.read(1).encode()

        while device.is_open:
            ch = getch()
            # print(ch)
            if ch == b'\x1d':                   # 'ctrl + ]' to quit
                break
            if ch == b'\x00' or ch == b'\xe0':  # arrow keys' escape sequences
                ch2 = getch()
                esc_dict = { b'H': b'A', b'P': b'B', b'M': b'C', b'K': b'D', b'G': b'H', b'O': b'F' }
                if ch2 in esc_dict:
                    queue.append(b'\x1b[' + esc_dict[ch2])
                else:
                    queue.append(ch + ch2)
            else:  
                queue.append(ch)

        if os.name != 'nt':
            termios.tcsetattr(stdin_fd, termios.TCSADRAIN, tty_attr)

    colorama.init()

    thread = threading.Thread(target=read_input)
    thread.start()
    while thread.is_alive():
        try:
            length = len(queue)
            if length > 0:
                device.write(b''.join(queue.popleft() for _ in range(length)))

            line = device.readline()
            if line:
                print(line.decode(errors='replace'), end='', flush=True)
        except IOError:
            print('--- {} is disconnected ---'.format(port))
            break

    device.close()
    if thread.is_alive():
        print('--- Press R to reconnect the device, or press Enter to exit ---')
        thread.join()
        if queue and queue[0] in (b'r', b'R'):
            return 1
    return 0

@click.command()
@click.option('-p', '--port', default=None, help='serial port name')
@click.option('-l', is_flag=True, help='list serial ports')

def main(port, l):
    port is None
    if port is None:
        ports = list_ports.comports()
        if not ports:
            print('--- No serial port available ---')
            return
        if len(ports) == 1:
            port = ports[0][0]
        else:
            print('--- Available Ports ----')
            for i, v in enumerate(ports):
                print('---  {}: {} {}'.format(i, v[0], v[2]))
            if l:
                return
            raw = input('--- Select port index: ')
            try:
                n = int(raw)
                port = ports[n][0]
            except:
                return
    baudrate = input("Enter baud rate (Default 115200): ")
    if (len(baudrate) == 0):
        baudrate = 115200
    parity = input("Enter parity [N,E,O,S,M] (Default N): ")
    if (len(parity) == 0):
        parity = "N"
    stopbits = input("Enter stop bit (Default 1): ")
    if (len(stopbits) == 0):
        stopbits = 1    
    while run(port, baudrate, parity, stopbits):
        pass

if __name__ == "__main__":
    main()
