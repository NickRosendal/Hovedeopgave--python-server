from CommandServer import CommandServer
import pygame
from pygame.locals import *
class ObserverbleTest():
    def __init__(self):
        print "start"
        myCommandServer=CommandServer()
        myCommandServer.start()
        myCommandServer.registerObserver(self)
        
      #  myCommandServer.unRegisterObserver(self)
     #   myCommandServer.doSomeWorkAndNotify() # Will never be seen by us
        
    def notify(self, subjectName, message):
            print subjectName + " says " + message

        
#myObserverbleTest = ObserverbleTest() # starts the class 

while True:
    c = sys.stdin.read(1)