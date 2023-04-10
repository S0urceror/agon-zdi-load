## Agon ZDI Load.py
##
## Connect via serial and use the 
## ZDI interface to load things into memory

import sys
import serial
import time
import os.path

## syntax
## agon-zdi-load.py FILENAME <PORT> <BAUDRATE>
## 

if len(sys.argv) == 1 or len(sys.argv) >4:
  sys.exit('Usage: agon-zdi-load.py FILENAME <PORT> <BAUDRATE>')

if not os.path.isfile(sys.argv[1]):
  sys.exit(f'Error: file \'{sys.argv[1]}\' not found')

if len(sys.argv) == 2:
  serialport = '/dev/tty.usbserial-212220'

if len(sys.argv) >= 3:
  serialport = sys.argv[2]

if len(sys.argv) == 4:
  baudrate = int(sys.argv[3])
else:
  baudrate = 115200

print(f'Sending {sys.argv[1]}')
print(f'Using port {serialport}')
print(f'Baudrate {baudrate}')

f = open(sys.argv[1], "r")

content = f.readlines()

try:
  with serial.Serial(serialport, baudrate) as ser:
    print('Opening serial port...')
    time.sleep(1)
    print('Writing Intel HEX to serial port')
    ser.write (b'\x1a') # send CTRL-Z to enter ZDI mode
    time.sleep(1)

    for line in content:
        ser.write(str(line).encode('ascii'))
        ser.write (b'\r\n')
        time.sleep (0.1)

    f.close()
    time.sleep (1)

    # run the code
    print('Running code')
    ser.write (b'j 0x40000\r\n')
    
    # escape ZDI mode
    ser.write (b'\x1b') # send ESC to exit ZDI
    
    print('Done')
except serial.SerialException:
  print('Error: serial port unavailable')