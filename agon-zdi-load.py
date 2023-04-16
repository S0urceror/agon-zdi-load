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
  sys.exit('Usage: agon-zdi-load.py FILENAME START <PORT> <BAUDRATE>')

if not os.path.isfile(sys.argv[1]):
  sys.exit(f'Error: file \'{sys.argv[1]}\' not found')

if len(sys.argv) < 3:
  sys.exit (f'Error: please specify start address')

if len(sys.argv) == 3:
  startaddress = sys.argv[2]
  serialport = '/dev/tty.usbserial-212220'

if len(sys.argv) >= 4:
  serialport = sys.argv[3]

if len(sys.argv) == 5:
  baudrate = int(sys.argv[4])
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
        time.sleep (0.05)

    f.close()
    time.sleep (0.2)
    
    # run the code
    if int(startaddress)>0:
      # escape ZDI mode
      ser.write (b'\x1b') # send ESC to exit ZDI
      time.sleep (1)
      #
      print('Running code')
      ser.write (str('RUN &').encode('ascii'))
      ser.write (str(startaddress).encode('ascii'))
      ser.write (b'\r\n')
    
    print('Done')
except serial.SerialException:
  print('Error: serial port unavailable')