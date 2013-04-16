#!/usr/bin/python
"""
Read a MagTek USB HID Swipe Reader in Linux. A description of this
code can be found at: 
The code is based of the work of Micah Carrick check out: http://www.micahcarrick.com/credit-card-reader-pyusb.html

You must be using the new PyUSB 1.0 branch and not the 0.x branch.

Copyright (c) 2013 - Kim Lindhard
"""
import sys
import usb.core
import threading
    
class MagtekUsbCardReader(threading.Thread):
    VENDOR_ID = 0x0801
    PRODUCT_ID = 0x0002
    DATA_SIZE = 337
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        
        # find the MagTek reader
        self.device = usb.core.find(idVendor=MagtekUsbCardReader.VENDOR_ID, idProduct=MagtekUsbCardReader.PRODUCT_ID)
        if self.device is None:
            self.notify("status","Could not find MagTek USB HID Swipe Reader.")
            sys.exit();
        # make sure the hiddev kernel driver is not active
        if self.device.is_kernel_driver_active(0):
            try:
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                self.notify("status","Could not detatch kernel driver: %s" % str(e))
        
        # set configuration
        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            self.notify("status","Could not set configuration: %s" % str(e))
            
        self.endpoint = self.device[0][(0,0)][0]
    
    
    
        # wait for swipe
        self.notify("status","Ready to read card")
        while True:
            swiped = False
            data = []
            while True:
                try:
                    data += self.device.read(self.endpoint.bEndpointAddress, self.endpoint.wMaxPacketSize,  timeout=250)
                    if not swiped: 
                         self.notify("status","Card swiped")
                    swiped = True
            
                except usb.core.USBError as e:
                    if e.args == (110, 'Operation timed out') and swiped:
                        if data[0] == 0 and data[1] == 0 and data[2] == 0:
                            break  # we got it!
                        
                        else:
                            self.notify("status","Bad read")
                            data = []
                            swiped = False
                            continue
                        
            returnList = []
            for item in data:
                if chr(item) != "\x00":
                    returnList.append(item)
            self.notify("swipe",''.join(map(chr, returnList)))
            
    observers = []
    SUBJECT_NAME = "CardReader"
    def registerObserver(self, observer):
        self.observers.append(observer)
    def unRegisterObserver(self, observer): 
        if observer in self.observers:
            self.observers.remove(observer)
    def notify(self, eventType, event):
        for eachObserver in self.observers:
            eachObserver.notify(self.SUBJECT_NAME, eventType, event)