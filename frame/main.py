import configurator
import pictureframe
import machine
from machine import Timer
import time
import os

def clean():
  os.remove("main.py")

configurator = configurator.Configurator()
frame = pictureframe.PictureFrame()
rareTimer = Timer(-1)

def initializeFrame(timer):
  if not configurator.wlan.isconnected():
    print("Attempting network configuration")
    configurator.configureNetwork()

  offset = -4 * 3600
  now = time.localtime(now.time() + offset)

  # Possibly off by 1 hour on DST transitions
  if now[1] > 11 or now[1] < 3:
    # No DST
    offset = -4 * 3600
  elif now[1] == 11 and (now[6] == 6 or (now[6] + 1 < now[2])):
    # No DST
    offset = -4 * 3600
  elif now[1] == 3 and ((now[6] == 6 and now[2] > 8) or (now[6] + 9 < now[2])):
    # No DST
    offset = -4 * 3600
  else:
    # DST
    offset = -5 * 3600

  now = time.localtime(now.time() + offset)

  frame.initialize(now)  

def main():
  print("Configuring...")
  frame.status(8)

  configurationAttempts = 8
  
  while not configurator.configureNetwork() and configurationAttempts > 0:
    machine.idle()
    time.sleep(5)
    machine.idle()
    print("Configuring... {}".format(configurationAttempts))
    configurationAttempts = configurationAttempts - 1
    frame.status(configurationAttempts)

  print("Configuration complete: {0} {1}".format(configurator.wlan.isconnected(), configurator.wlan.status()))

  frame.status(2)

  initializeFrame(None)

  rareTimer.init(period=1000*60*60, mode=Timer.PERIODIC, callback=initializeFrame)

if __name__ == "__main__":
  main()  
