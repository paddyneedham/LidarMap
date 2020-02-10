import smbus
import time

#i2c bus
bus = smbus.SMBus(1)

time.sleep(1)

#i2c device address
address = 0x04

def writeNumber(value):
  bus.write_byte(0x4, value)
  return -1

def readNumber():
  number = bus.read_byte(address)
  return number

def LidarOn():
  writeNumber(0x01)

def SendHeartBeat():
  writeNumber(0xFF)
