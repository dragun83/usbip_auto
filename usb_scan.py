#!/usr/bin/python3
import re
import subprocess
import time
first_cicle = True
old_usb_dev = []

def scan_usb_dev(): # get a list of usbip devices (lsusb - need to be installed
  device_re = re.compile(b"^\s-\sbusid\s\d+-\d+\s\(\d+:\d+\)\n|^(?!$).*", re.I)
  df = subprocess.check_output(["usbip","list", "-l"])
  devices = []
  for i in df.split(b'\n'):
    print( "str", i)
    if i:
      dev_id = device_re.match(i)
      print("dev_id = ",dev_id)
      if dev_id is not None:
        bus_id = re.search(b"\d+-\d+",dev_id.group(0))
        if bus_id is not None: devices.append(bus_id.group(0))
  print("List len = ",len(devices)," - ", devices)
  return devices 

def compare_usb_list(old, new): # Compare two lists and returne difference and grow\shrink
#  print("Compare lists", len(old), " ",len(new) )
  if(len(old) > len(new)):
    diff = []
    print("Old list is bigger than new")
    for i in old:
      print(i)
      if i not in new:
#        print(i.get('tag').decode('utf-8'))
        print("i = ",i)
        diff.append(i)
    grow = False
  elif(len(old) < len(new)):
    diff = []
    print("Old list is smaller than new")
    for i in new:
      if i not in old:
#        print(i.get('tag').decode('utf-8'))
        print("i = ",i)
        diff.append(i)
    grow = True
  else:
#    print("Old list is equal to new")
    return None, None
  print("diff = ",diff,"  grow = ", grow)
  return diff, grow
  
def bind_usb_dev(device):
  cmd = ["usbip","bind", ("--busid="+device.decode('utf-8'))]
  print(cmd)
 # std_out = subprocess.run(cmd) 

def unbind_usb_dev(device):
  cmd = ["usbip","unbind", "-b ", device.decode('utf-8')]
  print(cmd)
#  std_out = subprocess.run(cmd) 

def print_usb_dev(device_list):
  print (" Devices found: ", len(device_list))
  for i in device_list:
    print("****************")
    print( "Device ID :", i.get('id').decode('utf-8'))
    print(" Device tag :", i.get('tag').decode('utf-8'))
    print(" Device bus :", i.get('bus').decode('utf-8'))
    print(" Device number :", i.get('device').decode('utf-8'))
    print(" Device path :", i.get('path'))

try:
  while True:
    current_usb_dev = scan_usb_dev()
    if (first_cicle):
      print("First run!")
      old_usb_dev = current_usb_dev
    bind,grow = compare_usb_list(old_usb_dev, current_usb_dev)
    if (bind):
      print("Get some diffirince! Bind - ", bind, ' grow - ', grow)
      if (grow):
        for dev in bind:
          print("Binding device : ", dev.decode('utf-8'))
          bind_usb_dev(dev)
      else:
        for dev in bind:
          print("UNBinding device : ", dev.decode('utf-8'))
          unbind_usb_dev(dev)
    old_usb_dev = current_usb_dev
    first_cicle = False
    print("sleep 1 sec")
    time.sleep(1)
except KeyboardInterrupt:
  print("Stopping all!")
  """
except Exception as exc:
  print ("Someting went wrong!!!   ",str(exc))
"""
